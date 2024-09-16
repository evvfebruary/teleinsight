from quixstreams import Application
from loguru import logger

from embedder.clip import get_model_and_processor, preprocess_images, get_embeddings
from embedder.config import (
    KAFKA_HOST,
    KAFKA_PORT,
    CONSUMER_GROUP,
    INPUT_TOPIC,
    OUTPUT_TOPIC,
    BUCKET_NAME,
)
from embedder.storage import read_image_from_s3
from functools import partial

from quixstreams.kafka.configuration import ConnectionConfig

connection = ConnectionConfig(
    bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}",
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-512",
    sasl_username="admin",
    sasl_password="evvbmstu",
    ssl_ca_location="./certificates/YandexInternalRootCA.crt",
)


def create_embeddings(row, model, processor):
    object_key = row["object_key"]
    try:
        # Read image data
        _, _, image_data = read_image_from_s3(
            bucket_name=BUCKET_NAME, object_key=object_key
        )
        inputs = preprocess_images(image_data, processor)
        embeddings = get_embeddings(inputs, model).tolist()[0]
    except Exception as e:
        logger.error(e)
        embeddings = []
    return embeddings


def listen_and_push_embeddings():
    app = Application(
        broker_address=connection,
        consumer_group=CONSUMER_GROUP,
        auto_create_topics=False,
    )

    model, processor = get_model_and_processor()

    # Describe topics
    input_new_images_topic = app.topic(INPUT_TOPIC, value_deserializer="json")
    output_new_images_x_embedding_topic = app.topic(
        OUTPUT_TOPIC, value_serializer="json"
    )

    sdf = app.dataframe(topic=input_new_images_topic)
    sdf = sdf.update(lambda val: logger.info(f"Received update: {val}"))

    sdf["embeddings"] = sdf.apply(
        partial(create_embeddings, model=model, processor=processor)
    )

    sdf = sdf.to_topic(output_new_images_x_embedding_topic)

    app.run(sdf)


if __name__ == "__main__":
    listen_and_push_embeddings()
