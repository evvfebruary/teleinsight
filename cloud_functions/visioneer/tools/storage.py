import boto3
from loguru import logger

def read_image_from_s3(event):
    bucket_name = event["messages"][0]["details"]["bucket_id"]
    object_key = event["messages"][0]["details"]["object_id"]

    logger.info(f"# Read image from {bucket_name}/{object_key}")

    session = boto3.session.Session()

    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )

    obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    image_data = obj["Body"].read()
    return bucket_name, object_key, image_data
