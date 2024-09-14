from loguru import logger
from confluent_kafka import Producer
from .config import KAFKA_PASSWORD, KAFKA_USER, KAFKA_PORT, KAFKA_HOST

params = {
    'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
    'security.protocol': 'SASL_SSL',
    'ssl.ca.location': './tools/certificates/YandexInternalRootCA.crt',
    'sasl.mechanism': 'SCRAM-SHA-512',
    'sasl.username': KAFKA_USER,
    'sasl.password': KAFKA_PASSWORD,
    'error_cb': lambda err: logger.error(err)
}

def push_message_to_topic(topic, message, flush_timeout=30):
    p = Producer(params)
    p.produce(topic, message)
    p.flush(flush_timeout)