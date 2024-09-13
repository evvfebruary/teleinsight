import clickhouse_connect
from .config import CH_HOST, CH_PORT, CH_USERNAME, CH_PASSWORD, CH_DATABASE


def get_ch_client():
    client = clickhouse_connect.get_client(
        host=CH_HOST,
        port=CH_PORT,
        username=CH_USERNAME,
        password=CH_PASSWORD,
        database=CH_DATABASE,
        secure=True,
        verify=False,
    )

    return client


def insert_image_description(client, bucket_name, object_key, image_description):
    client.insert(
        "image_description_dt",
        [[bucket_name, object_key, image_description]],
        column_names=["bucket_name", "object_key", "description"],
        settings={"async_insert": 1, "wait_for_async_insert": 1},
    )
