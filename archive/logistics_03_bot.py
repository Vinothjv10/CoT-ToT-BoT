import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}

BEAM_WIDTH = 3

def ask_llm(messages, temp=0.5, max_tok=1024):
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
print("LOGISTICS EXAMPLE 3: BoT — Inventory Replenishment Strategy")
print("=" * 70)

PROBLEM = """You manage 3 warehouses (North, Central, South) stocking the same SKU.
Current inventory and daily demand:

Warehouse  | Current Stock | Daily Demand | Reorder Cost | Holding Cost/unit/day
North      | 240 units     | 30/day       | $150         | $0.40
Central    | 90 units      | 25/day       | $150         | $0.35
South      | 450 units     | 20/day       | $150         | $0.50

Lead time from supplier: 7 days for all. A stockout costs $12/unit.
You have a budget of $3,000 for this replenishment cycle.
How much should you send to EACH warehouse to minimize total costs?"""

print("PROBLEM:")
print(PROBLEM)
print("Beam width K = " + str(BEAM_WIDTH))
print("\n" + "-" * 70)

# STEP 1: Generate initial allocation strategies (beam seeds)
print("STEP 1 — Generate " + str(BEAM_WIDTH) + " allocation strategies...")
strategies = ask_llm([
    {"role": "system", "content": "You generate diverse inventory allocation strategies."},
    {"role": "user", "content": PROBLEM + "\n\nPropose " + str(BEAM_WIDTH) + " different allocation strategies (how many units to each warehouse). Each should be a specific 3-number split summing to a reasonable total within the $3000 budget at ~$10/unit. Label them Strategy 1, 2, 3."}
], temp=0.8)
print(strategies + "\n")

print("-" * 70)

# STEP 2: Score each strategy
print("STEP 2 — Score each strategy...")
scored = ask_llm([
    {"role": "system", "content": "You score inventory strategies by total cost."},
    {"role": "user", "content": PROBLEM + "\n\nCandidate strategies:\n" + strategies + "\n\nFor EACH strategy, calculate estimated total cost = reorder costs + holding costs for 30 days + expected stockout costs. Score 0-10 (10 = best).\n\nOutput format:\nStrategy 1: Score X/10 — reason\nStrategy 2: Score X/10 — reason\nStrategy 3: Score X/10 — reason\n\nThen write KEEP: <strategy number> for the top " + str(BEAM_WIDTH) + "."}
], temp=0.3)
print(scored + "\n")

kept = re.findall(r"Keep:|KEEP:\s*(\d)", scored)
if not kept:
    kept = ["1", "2", "3"]
print("Keeping strategies: " + str(kept) + "\n")

print("-" * 70)

# STEP 3: Refine kept strategies
print("STEP 3 — Refine top strategies...")
for s in kept:
    refined = ask_llm([
        {"role": "system", "content": "You refine inventory allocation plans."},
        {"role": "user", "content": PROBLEM + "\n\nTake Strategy " + s + " and refine it:\n- Safety stock buffer?\n- Phased delivery schedule?\n- Final exact unit counts?\n\nGive the optimized version."}
    ], temp=0.3)
    print("--- Refined Strategy " + s + " ---\n" + refined + "\n")

print("-" * 70)

# STEP 4: Final recommendation
print("STEP 4 — Final recommendation...")
final = ask_llm([
    {"role": "system", "content": "You synthesize the best answer from multiple analyses."},
    {"role": "user", "content": PROBLEM + "\n\nBased on the refinement above, what is the single best allocation? Give exact numbers for North, Central, South and the expected total cost."}
], temp=0.2)
print("FINAL RECOMMENDATION:\n" + final)
print("\nBoT keeps top-K strategies, scores, prunes, and refines — like beam search for supply chain decisions.")
