import torch
from transformers import CLIPProcessor, CLIPModel
from config import CLIP_MODEL_NAME
from PIL import Image
import dotenv
import io

dotenv.load_dotenv("../ingestor/.env")


def get_model_and_processor():
    model = CLIPModel.from_pretrained(CLIP_MODEL_NAME, local_files_only=True)
    processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME, local_files_only=True)
    return model, processor


def preprocess_images(image_bytes, processor):
    pil_image = Image.open(io.BytesIO(image_bytes))
    inputs = processor(images=pil_image, return_tensors="pt", padding=True)
    return inputs


def get_embeddings(inputs, model):
    with torch.no_grad():
        image_embeddings = model.get_image_features(**inputs)
    return image_embeddings
