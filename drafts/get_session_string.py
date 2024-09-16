from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os
from loguru import logger

with TelegramClient(StringSession(), os.getenv('API_ID'), os.getenv("API_HASH")) as client:
    logger.info(client.session.save())