import os
import boto3
import base64
import requests
from loguru import logger
from db import insert_image_description
import ujson


def get_image_description(base64_image):
    api_key = os.environ["openai_key"]

    proxies = {
        "http": f"http://brd-customer-hl_f87a7fc0-zone-datacenter_proxy1:{os.environ['PROXY_PASS']}@brd.superproxy.io:22225",
        "https": f"http://brd-customer-hl_f87a7fc0-zone-datacenter_proxy1:{os.environ['PROXY_PASS']}@brd.superproxy.io:22225",
    }
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        proxies=proxies,
    )

    return response.json()


def read_image_from_s3(event):
    bucket_name = event["messages"][0]["details"]["bucket_id"]
    object_key = event["messages"][0]["details"]["object_id"]

    session = boto3.session.Session()

    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )

    obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    image_data = obj["Body"].read()
    return bucket_name, object_key, image_data


def encode_image(image_data):
    base64_image = base64.b64encode(image_data).decode("utf-8")
    return base64_image


def handler(event, context):
    bucket_name, object_key, image_data = read_image_from_s3(event)
    base64_image = encode_image(image_data)
    logger.info(f"# Call for description to OpenAI itself")
    description = get_image_description(base64_image)

    logger.info(f"# Insert data about {bucket_name}/{object_key} to Clickhouse")
    insert_image_description(bucket_name, object_key, ujson.dumps(description))

    return True
