import os

PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASS = os.getenv("PROXY_PASS")

HTTP_PROXY = f"http://{PROXY_USERNAME}:{PROXY_PASS}@{PROXY_HOST}"
HTTPS_PROXY = f"http://{PROXY_USERNAME}:{PROXY_PASS}@{PROXY_HOST}"

CH_HOST = os.getenv("CH_HOST")
CH_PORT = os.getenv("CH_PORT")
CH_USERNAME = os.getenv("CH_USERNAME")
CH_PASSWORD = os.getenv("CH_PASSWORD")
CH_DATABASE = os.getenv("CH_TELEINSIGHT_DATABASE")

OPEN_AI_API_KEY = os.getenv("openai_key")


# Prompt to ask model to describe image
VISION_PROMPT = "What’s in this image?"
DETAIL_QUALITY = "low"

# Kafka
KAFKA_USER = os.getenv("KAFKA_USER")
KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
