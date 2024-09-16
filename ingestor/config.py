import os
import dotenv

dotenv.load_dotenv()

# Telegram environments
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# Yandex storage
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")

# Proxie to avoid open ai region restrictions
PROXIE_PASS = os.getenv("PROXIE_PASS")

# Clickhouse
CH_HOST = os.getenv("CH_HOST")
CH_PORT = os.getenv("CH_PORT")
CH_USERNAME = os.getenv("CH_USERNAME")
CH_PASSWORD = os.getenv("CH_PASSWORD")
CH_TELEINSIGHT_DATABASE = os.getenv("CH_TELEINSIGHT_DATABASE")

# Local path to save images
LOCAL_PATH_TO_SAVE_IMAGE = os.getenv("LOCAL_PATH_TO_SAVE_IMAGE")


# App related tags
NEW_MESSAGE_INGESTOR_TAG = "online-ingestor"
RETRO_MESSAGE_INGESTOR_TAG = "retro-ingestor"
