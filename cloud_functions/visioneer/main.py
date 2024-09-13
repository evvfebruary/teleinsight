import ujson
import base64
from loguru import logger

from tools.db import get_ch_client
from tools.db import insert_image_description
from tools.openai import get_image_description
from tools.storage import read_image_from_s3


def encode_image(image_data):
    base64_image = base64.b64encode(image_data).decode("utf-8")
    return base64_image


def handler(event, context):
    logger.info(f"# Encode image to base64")
    bucket_name, object_key, image_data = read_image_from_s3(event)
    base64_image = encode_image(image_data)

    logger.info(f"# Call for description to OpenAI itself")
    description = get_image_description(base64_image)

    logger.info(f"# Insert data about {bucket_name}/{object_key} to Clickhouse")
    ch_client = get_ch_client()
    insert_image_description(
        ch_client, bucket_name, object_key, ujson.dumps(description)
    )

    return True
