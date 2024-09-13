from telethon import TelegramClient, events
from telethon.sessions import StringSession
from loguru import logger

from config import SESSION_STRING, API_ID, API_HASH, LOCAL_PATH_TO_SAVE_IMAGE

import ujson
from ingestor.db.handler import insert_event
from config import NEW_MESSAGE_INGESTOR_TAG
from ingestor.utils.events import get_peer_id, handle_photo_attachments
from utils.meta import create_meta_tags

client = TelegramClient(
    StringSession(SESSION_STRING),
    int(API_ID),
    API_HASH,
)


@client.on(events.NewMessage)
async def handler(event):
    try:
        logger.info("# Receive new event")
        sender_info = await event.get_sender()

        # Enrich with meta tags
        json_message_with_meta = {
            "event": event.to_json(),
            "sender": sender_info.to_json(),
            "x_meta": create_meta_tags(NEW_MESSAGE_INGESTOR_TAG),
        }

        # Get peer id
        peer_id = get_peer_id(event.message.to_dict())

        if event.message.photo:
            s3_object_key = await handle_photo_attachments(
                tg_client=client,
                tg_event=event,
                local_path_to_save_img=LOCAL_PATH_TO_SAVE_IMAGE,
                peer_id=peer_id,
            )

            # Add s3 prefix as another field
            json_message_with_meta["photo_attachment_path"] = s3_object_key

        # Save json to clickhouse
        insert_event(ujson.dumps(json_message_with_meta))
    except Exception as e:
        logger.error(e)


def entrypoint(tg_client):
    logger.info("# New messages handler has started")
    with tg_client:
        tg_client.run_until_disconnected()


if __name__ == "__main__":
    entrypoint(client)
