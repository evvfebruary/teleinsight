import os

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from loguru import logger

from config import SESSION_STRING, API_ID, API_HASH, NEW_MESSAGE_INGESTOR_TAG
from dotenv import load_dotenv

import ujson
from ingestor.db.handler import insert_event
from ingestor.storage.objects import upload_to_s3

load_dotenv()

client = TelegramClient(
    StringSession(SESSION_STRING),
    int(API_ID),
    API_HASH,
)


def create_meta_tags():
    meta_tags = {"__service_tag": NEW_MESSAGE_INGESTOR_TAG}
    return meta_tags


@client.on(events.NewMessage)
async def handler(event):
    logger.info("# Receive new event")
    sender_info = await event.get_sender()

    # Enrich with meta tags
    json_message_with_meta = {
        "event": event.to_json(),
        "sender": sender_info.to_json(),
        "x_meta": create_meta_tags(),
    }

    logger.info(f"# Get attributes of new message: {json_message_with_meta}")

    if event.message.photo:
        logger.info("# Message have attachment")
        file_path = await client.download_media(
            event.message.media, "./attachments/images/"
        )
        logger.info(f"File path {file_path}")
        upload_to_s3(file_path, bucket_name="teleinsight", prefix="attachments/images")
        json_message_with_meta["photo_attachment_path"] = file_path
        os.remove(file_path)

    insert_event(ujson.dumps(json_message_with_meta))


def entrypoint(tg_client):
    logger.info("# New messages handler has started")
    with tg_client:
        tg_client.run_until_disconnected()


if __name__ == "__main__":
    entrypoint(client)
