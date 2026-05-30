import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}

PROBLEM = """Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
Each can has 3 tennis balls. How many tennis balls does he have now?"""

def ask_llm(system_prompt, user_message):
    payload = {
        "model": "google/gemma-3n-e4b-it",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.95,
        "stream": False
    }
    resp = requests.post(invoke_url, headers=headers, json=payload)
    return resp.json()["choices"][0]["message"]["content"]

print("=" * 60)
print("01 — BASELINE: Direct Answer (No CoT)")
print("=" * 60)

# Direct prompt — just ask for the answer right away
direct_answer = ask_llm(
    "You are a helpful assistant. Answer concisely.",
    f"Answer: {PROBLEM}"
)
print(f"\n📥 Problem: {PROBLEM}")
print(f"\n💬 Direct answer:\n{direct_answer}")
print("\n⚠️  Notice: Without step-by-step reasoning, the model may get the wrong answer!")
