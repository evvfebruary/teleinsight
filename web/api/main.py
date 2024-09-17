import os
import clickhouse_connect
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import dotenv
import base64
import boto3
from loguru import logger
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv('../../ingestor/.env')


import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import dotenv
import io

CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"

def get_model_and_processor():
    model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
    processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)
    return model, processor


def preprocess_images(image_bytes, processor):
    pil_image = Image.open(io.BytesIO(image_bytes))
    inputs = processor(images=pil_image, return_tensors="pt", padding=True)
    return inputs


def get_embeddings(inputs, model):
    with torch.no_grad():
        image_embeddings = model.get_image_features(**inputs)
    return image_embeddings



def read_image_from_s3(bucket_name, object_key):
    logger.info(f"# Read image from {bucket_name}/{object_key}")

    session = boto3.session.Session()

    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )

    obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    image_data = obj["Body"].read()
    return image_data

app = FastAPI()

# Mocked image data (a small red dot as an example)
mock_image_data = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcA"
    "AABBAA/+BlbPAAAAAElFTkSuQmCC"
)

origins = [
    "http://localhost",
    "http://localhost:63342",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model, processor = get_model_and_processor()

def get_text_embedding(description):
    embeddings_model = OpenAIEmbeddings(
        model='text-embedding-3-small',
    )
    description_embedding = embeddings_model.embed_query(description)
    return description_embedding

def get_ch_client():
    client = clickhouse_connect.get_client(
        host=os.getenv('CH_HOST'),
        port=os.getenv('CH_PORT'),
        username=os.getenv('CH_USERNAME'),
        password=os.getenv('CH_PASSWORD'),
        database=os.getenv('CH_DATABASE'),
        secure=True,
        verify=False,
    )

    return client

def encode_image(image_data):
    base64_image = base64.b64encode(image_data).decode("utf-8")
    return base64_image

@app.post("/api")
async def receive_data(text: str = Form(None), file: UploadFile = File(None)):
    logger.info(f"# Received text: {text}")
    most_closest_count = 1
    ch_client = get_ch_client()
    response_data = []
    if text is not None:
        text_embedding = get_text_embedding(text)
        logger.info(text_embedding)
        most_closest_df = ch_client.query_df(f"""SELECT DISTINCT object_key,extracted_description,L2Distance({text_embedding}, embeddings) as score FROM teleinsight.image_description_dt ORDER BY score ASC LIMIT {most_closest_count};""")

        for each in most_closest_df[['object_key', 'extracted_description', 'score']].to_dict("records"):
            response_data.append(
                {'image_data': encode_image(read_image_from_s3('teleinsight',each['object_key'])), "text_description": [f"{each['extracted_description']}\nScore: {each['score']}"]}
            )
    elif file is not None:
        logger.info("# Work with image")
        image_bytes = await file.read()
        inputs = preprocess_images(image_bytes, processor)
        image_embedding = get_embeddings(inputs, model).numpy().flatten().tolist()
        logger.info(image_embedding)
        most_closest_df = ch_client.query_df(f""" SELECT object_key, score, L2Distance({image_embedding}, embeddings) as score FROM teleinsight.image_description_dt ORDER BY score ASC LIMIT {most_closest_count};""")
        for each in most_closest_df[['object_key', 'score']].to_dict("records"):
            response_data.append(
                {'image_data': encode_image(read_image_from_s3('teleinsight',each['object_key'])), "text_description": [f"Score: {each['score']}"]}
            )


    return JSONResponse(content=response_data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
