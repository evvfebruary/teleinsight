import os
import clickhouse_connect

client = clickhouse_connect.get_client(
    host=os.getenv('CH_SHARD1_HOST'),
    port=os.getenv('CH_SHARD1_PORT'),
    username=os.getenv('CH_USERNAME'),
    password=os.getenv('CH_PASSWORD'),
    database=os.getenv('CH_TELEINSIGHT_DATABASE'),
    secure=True,
    verify=False
)

def insert_image_description(bucket_name, object_key, image_description):
    client.insert(
        'image_description_dt',
        [[bucket_name, object_key, image_description]],
        column_names=['bucket_name', 'object_key', 'description'],
        settings={
            'async_insert': 1,
            'wait_for_async_insert': 1
        }
    )