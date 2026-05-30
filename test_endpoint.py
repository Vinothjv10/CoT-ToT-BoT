import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")
if not api_key:
    raise ValueError("NVIDIA_API_KEY not found in .env file")

invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = False

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "text/event-stream" if stream else "application/json"
}

payload = {
    "model": "google/gemma-3n-e4b-it",
    "messages": [{"role": "user", "content": "Say 'Hello, endpoint is working!' and nothing else."}],
    "max_tokens": 512,
    "temperature": 0.20,
    "top_p": 0.70,
    "frequency_penalty": 0.00,
    "presence_penalty": 0.00,
    "stream": stream
}

print(f"Testing endpoint: {invoke_url}")
print(f"Model: {payload['model']}")
print("Sending request...\n")

response = requests.post(invoke_url, headers=headers, json=payload)

if response.status_code == 200:
    print("✅ Endpoint is working!")
    if stream:
        for line in response.iter_lines():
            if line:
                print(line.decode("utf-8"))
    else:
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        print(f"Response: {content}")
else:
    print(f"❌ Request failed with status {response.status_code}")
    print(f"Error: {response.text}")
