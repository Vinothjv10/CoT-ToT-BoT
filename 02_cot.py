import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}

PROBLEM = """Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
Each can has 3 tennis balls. How many tennis balls does he have now?"""

def ask_llm(messages):
    payload = {
        "model": "google/gemma-3n-e4b-it",
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.95,
        "stream": False
    }
    resp = requests.post(invoke_url, headers=headers, json=payload)
    return resp.json()["choices"][0]["message"]["content"]

print("=" * 60)
print("02 — CHAIN OF THOUGHT (CoT)")
print("=" * 60)
print("💡 CoT = prompt the model to reason step-by-step before answering.\n")

# CoT prompt — ask for step-by-step reasoning
cot_answer = ask_llm([
    {"role": "system", "content": "You are a helpful assistant. Always reason step-by-step, then give the final answer."},
    {"role": "user", "content": f"Let's think step by step, then answer:\n\n{PROBLEM}"}
])
print(f"📥 Problem: {PROBLEM}")
print(f"\n💬 CoT output:\n{cot_answer}")
print("\n✅ CoT makes intermediate reasoning explicit, reducing errors on multi-step problems.")
