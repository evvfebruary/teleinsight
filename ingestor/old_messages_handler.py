from telethon import TelegramClient
from telethon.sessions import StringSession

from ingestor.config import (
    SESSION_STRING,
    API_ID,
    API_HASH,
    LOCAL_PATH_TO_SAVE_IMAGE,
    RETRO_MESSAGE_INGESTOR_TAG,
)
from ingestor.db.handler import insert_events
from ingestor.utils.events import (
    prepare_json_above_event_info,
    handle_photo_attachments,
    get_peer_id,
)
import ujson
from loguru import logger
from telethon.errors import FloodWaitError
import time
import json
import os
import asyncio


import argparse


def save_to_disk(
    batch_messages, peer_id, batch_number, batches_folder_root="./batches"
):
    batch_filepath = os.path.join(
        batches_folder_root, f"{peer_id}/parsed_messages_{batch_number}.json"
    )
    os.makedirs(os.path.join(batches_folder_root, f"{peer_id}"), exist_ok=True)

    with open(batch_filepath, "w") as f:
        json.dump(batch_messages, f, indent=4)
    logger.info(f"# Saved {len(batch_messages)} messages to {batch_filepath}")


async def dump_all_messages_from_chat(
    tg_peer_identificator: str | int, wait_time=2, batch_size=500
):
    parsed_messages = []
    batch_number = 0
    async with TelegramClient(
        StringSession(SESSION_STRING), API_ID, API_HASH
    ) as client:
        async with client.takeout() as takeout:
            logger.info(
                f"# Start crawling all mesages from peer entity with ID: {tg_peer_identificator}"
            )
            async for message in takeout.iter_messages(
                tg_peer_identificator, wait_time=wait_time
            ):
                try:
                    json_message_with_meta = await prepare_json_above_event_info(
                        message, service_tag=RETRO_MESSAGE_INGESTOR_TAG
                    )

                    # Get peer id
                    peer_id = get_peer_id(message.to_dict())

                    if message.photo:
                        s3_object_key = await handle_photo_attachments(
                            tg_client=client,
                            message_media=message.media,
                            local_path_to_save_img=LOCAL_PATH_TO_SAVE_IMAGE,
                            peer_id=peer_id,
                        )

                        # Add s3 prefix as another field
                        json_message_with_meta["photo_attachment_path"] = s3_object_key

                    # Add message to buffer
                    parsed_messages.append([ujson.dumps(json_message_with_meta)])

                    if len(parsed_messages) % batch_size == 0:
                        batch_number += 1
                        save_to_disk(parsed_messages, peer_id, batch_number)
                        insert_events(parsed_messages)
                        parsed_messages.clear()
                        logger.info(
                            f"Successfully received: {batch_number * batch_size} messages"
                        )

                except FloodWaitError as e:
                    logger.info(
                        f"Flood wait error: Need to wait for {e.seconds} seconds."
                    )
                    time.sleep(e.seconds + 10)
                except Exception as err:
                    logger.error(err)
    logger.info(f"# Push last batch: {len(parsed_messages)}")
    insert_events(parsed_messages)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tg_peer_identificator", type=str, help="Peer entity ID")
    args = parser.parse_args()

    await dump_all_messages_from_chat(args.tg_peer_identificator)


if __name__ == "__main__":
    asyncio.run(main())
