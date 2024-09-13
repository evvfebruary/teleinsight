from .config import (
    OPEN_AI_API_KEY,
    VISION_PROMPT,
    DETAIL_QUALITY,
    HTTP_PROXY,
    HTTPS_PROXY,
)
import requests


def create_headers():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_AI_API_KEY}",
    }
    return headers


def create_payload(
    base64_image,
    max_tokens=300,
    detail_quality=DETAIL_QUALITY,
    model_request=VISION_PROMPT,
):
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": model_request},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": detail_quality,
                        },
                    },
                ],
            }
        ],
        "max_tokens": max_tokens,
    }

    return payload


def get_proxies():
    proxies = {"http": HTTP_PROXY, "https": HTTPS_PROXY}

    return proxies


def get_image_description(base64_image):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=create_headers(),
        json=create_payload(base64_image),
        proxies=get_proxies(),
    )
    return response.json()
