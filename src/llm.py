import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NVIDIA_API_KEY")
INVOKE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}
DEFAULT_MODEL = "google/gemma-3n-e4b-it"


def ask(messages, temperature=0.7, max_tokens=1024, model=None):
    payload = {
        "model": model or DEFAULT_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 0.95,
        "stream": False
    }
    resp = requests.post(INVOKE_URL, headers=HEADERS, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def ask_simple(system_prompt, user_message, **kwargs):
    return ask([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ], **kwargs)
