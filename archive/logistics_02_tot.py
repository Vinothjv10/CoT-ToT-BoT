import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}

def ask_llm(messages, temp=0.4, max_tok=1024):
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
print("LOGISTICS EXAMPLE 2: ToT — Warehouse Location Strategy")
print("=" * 70)

PROBLEM = """You are expanding your logistics network in Southeast Asia.
You need one new warehouse to serve: Bangkok, Ho Chi Minh City,
Manila, and Jakarta.

Constraints:
- Each warehouse costs $12,000/month to operate
- Shipping cost per pallet: $0.50 per km
- You ship ~150 pallets/month TOTAL to these 4 cities
- The % of volume per city: Bangkok 30%, HCMC 25%, Manila 20%, Jakarta 25%

Candidate warehouse locations and distances (km) to each city:
Location A (Singapore): BKK=1420, HCMC=1090, MNL=2400, JKT=890
Location B (Kuala Lumpur): BKK=1180, HCMC=1050, MNL=2500, JKT=1170
Location C (Bangkok): BKK=50, HCMC=1050, MNL=2200, JKT=2300

Where should you place the warehouse to minimize total monthly cost?"""

print("PROBLEM:")
print(PROBLEM)
print("\n" + "-" * 70)

# STEP 1: Generate branches — cost analysis for each location
print("STEP 1 — Generate cost analysis for each candidate location...")
branches = ask_llm([
    {"role": "system", "content": "You are a logistics analyst generating branch analyses."},
    {"role": "user", "content": PROBLEM + "\n\nFor EACH candidate location (A, B, C), calculate:\n- Monthly shipping cost (sum of city_volume_pallets × distance_km × $0.50)\n- Monthly operating cost ($12,000)\n- TOTAL monthly cost\n\nPresent each as a separate analysis branch, numbered."}
], temp=0.5)
print(branches + "\n")

print("-" * 70)

# STEP 2: Evaluate branches
print("STEP 2 — Evaluate and compare all branches...")
evaluation = ask_llm([
    {"role": "system", "content": "You critically evaluate logistics trade-offs."},
    {"role": "user", "content": PROBLEM + "\n\nHere are the cost analyses:\n" + branches + "\n\nFor EACH location, identify:\n- Is there a hidden risk (longer lead times, customs delays)?\n- Scalability — can it handle 2x volume later?\n- Is the cost difference significant enough to matter?\n\nRank them best → worst and explain why."}
], temp=0.3)
print(evaluation + "\n")

print("-" * 70)

# STEP 3: Expand best branch
print("STEP 3 — Deep-dive into the best location...")
deep_dive = ask_llm([
    {"role": "system", "content": "You are a logistics strategist."},
    {"role": "user", "content": "For the best warehouse location identified above, create an implementation plan:\n1. Which city gets served first?\n2. What fleet size is needed?\n3. What is the payback period vs the worst option?\n\nBe specific with numbers."}
], temp=0.3)
print(deep_dive)
print("\nToT lets you explore multiple locations in parallel, evaluate trade-offs, then deep-dive on the winner.")
