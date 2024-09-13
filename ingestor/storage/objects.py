import os
from loguru import logger

import boto3


def upload_to_s3(file_path, bucket_name, prefix):
    logger.info("# Upload image to storage")
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )

    # Get the file name from the file path
    file_name = os.path.basename(file_path)

    # Create the object key with the prefix
    object_key = f"{prefix}/{file_name}"

    # Upload the file
    s3.upload_file(file_path, bucket_name, object_key)
    logger.info(f"File {file_path} uploaded to {bucket_name}/{object_key}")
    return object_key
