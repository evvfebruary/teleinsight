from loguru import logger
from confluent_kafka import Producer
from cloud_functions.visioneer.tools.config import KAFKA_PASSWORD
from embedder.config import KAFKA_HOST

params = {
    'bootstrap.servers': 'rc1a-vgl0p6gcddnhop6e.mdb.yandexcloud.net:9091',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'SCRAM-SHA-512',
    'sasl.username': KAFKA_HOST,
    'sasl.password': KAFKA_PASSWORD,
    'error_cb': lambda err: logger.error(err)
}

def push_message_to_topic(topic, message, flush_timeout=2):
    p = Producer(params)
    p.produce(topic, message)
    p.flush(flush_timeout)