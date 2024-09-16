from enum import Enum
import os

import ujson
from loguru import logger

from ingestor.config import S3_BUCKET, NEW_MESSAGE_INGESTOR_TAG
from ingestor.storage.objects import upload_to_s3
from ingestor.utils.meta import create_meta_tags


class PeerTypeIdKey(Enum):
    PeerChat = "chat_id"
    PeerUser = "user_id"
    PeerChannel = "channel_id"


TYPE_ID_KEY_MAPPING = {element.name: element.value for element in PeerTypeIdKey}


def get_peer_id(event: dict) -> int:
    peer_id_with_type = event.get("peer_id")
    peer_type = peer_id_with_type.get("_")
    id_key = TYPE_ID_KEY_MAPPING.get(peer_type)

    return peer_id_with_type.get(id_key)


async def handle_photo_attachments(
    tg_client, message_media, local_path_to_save_img: str, peer_id: int
) -> str:
    prefix = os.path.join("attachments", str(peer_id), "photo")

    file_path = await tg_client.download_media(message_media, local_path_to_save_img)

    object_key = upload_to_s3(file_path, bucket_name=S3_BUCKET, prefix=prefix)

    os.remove(file_path)

    return object_key


async def prepare_json_above_event_info(event, service_tag):
    sender_info = await event.get_sender()

    # Enrich with meta tags
    json_message_with_meta = {
        "event": ujson.loads(event.to_json()),
        "sender": ujson.loads(sender_info.to_json()),
        "x_meta": create_meta_tags(service_tag),
    }

    return json_message_with_meta
