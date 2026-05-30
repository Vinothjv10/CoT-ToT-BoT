import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}

def ask_llm(messages, temp=0.3, max_tok=1024):
    payload = {
        "model": "google/gemma-3n-e4b-it",
        "messages": messages,
        "max_tokens": max_tok,
        "temperature": temp,
        "top_p": 0.95,
        "stream": False
    }
    resp = requests.post(invoke_url, headers=headers, json=payload)
    return resp.json()["choices"][0]["message"]["content"]

print("=" * 70)
print("LOGISTICS EXAMPLE 1: CoT — Freight Mode Decision")
print("=" * 70)

PROBLEM = """You need to ship 500 kg of electronics from Shenzhen, China to Berlin, Germany.

Option A (Air Freight): $2.50/kg, 3 days transit, $0.50/kg insurance
Option B (Sea Freight): $0.40/kg, 35 days transit, $0.15/kg insurance
Option C (Rail Freight): $0.90/kg, 18 days transit, $0.25/kg insurance

The electronics lose 2% of their value per week in transit due to
depreciation. Total cargo value is $200,000.

Which option has the lowest TOTAL cost including depreciation?"""

print("PROBLEM:")
print(PROBLEM)
print("\n" + "-" * 70)

# Without CoT — direct answer
print("Direct answer (no step-by-step):")
direct = ask_llm([
    {"role": "system", "content": "You are a logistics analyst. Answer concisely."},
    {"role": "user", "content": PROBLEM + "\n\nWhich option is cheapest? Give the total cost for each."}
], temp=0.3)
print(direct + "\n")

print("-" * 70)

# With CoT — systematic breakdown
print("With CoT (step-by-step reasoning):")
cot = ask_llm([
    {"role": "system", "content": "You are a logistics analyst. Always break down costs line by line before concluding."},
    {"role": "user", "content": PROBLEM + "\n\nFor each option, calculate:\n1. Freight cost\n2. Insurance cost\n3. Weeks in transit\n4. Depreciation cost (2% per week of $200,000)\n5. TOTAL = freight + insurance + depreciation\n\nShow each step, then state the cheapest option."}
], temp=0.2)
print(cot)
print("\nCoT forces systematic cost breakdown, preventing overlooked depreciation costs.")
