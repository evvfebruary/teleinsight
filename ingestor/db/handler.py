import clickhouse_connect
from ..config import CH_HOST, CH_PORT, CH_USERNAME, CH_PASSWORD, CH_TELEINSIGHT_DATABASE

# Create the ClickHouse client
client = clickhouse_connect.get_client(
    host=CH_HOST,
    port=CH_PORT,
    username=CH_USERNAME,
    password=CH_PASSWORD,
    database=CH_TELEINSIGHT_DATABASE,
    secure=True,
    verify=False,
)


def insert_event(event_with_meta_json):
    client.insert(
        "tg_events_dt",
        [[event_with_meta_json]],
        column_names=["event_json"],
        settings={"async_insert": 1, "wait_for_async_insert": 1},
    )


def insert_events(parsed_messages):
    client.insert(
        "tg_events_dt",
        parsed_messages,
        column_names=["event_json"],
        settings={"async_insert": 1, "wait_for_async_insert": 1},
    )
