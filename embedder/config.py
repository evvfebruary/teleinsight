import os
import dotenv

dotenv.load_dotenv()


KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
CONSUMER_GROUP = "teleinsight-new-images-getters"
CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"
TOPIC_WITH_NEW_ATTACHMENTS = "freshly_created_attachments"


INPUT_TOPIC = "freshly_created_attachments"
OUTPUT_TOPIC = "embeddings_out"
BUCKET_NAME = "teleinsight"


sasl_username = os.getenv("SASL_USERNAME")
sasl_password= os.getenv("SASL_PASSWORD")
