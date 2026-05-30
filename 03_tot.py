import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}

PROBLEM = """A farmer has a fox, a chicken, and a bag of grain.
He needs to get all three across a river using a boat that can only
carry him plus ONE item at a time.
If left alone: fox eats chicken, chicken eats grain.
How does he get everything across safely?"""

def ask_llm(messages, temp=0.8):
    payload = {
        "model": "google/gemma-3n-e4b-it",
        "messages": messages,
        "max_tokens": 1024,
        "temperature": temp,
        "top_p": 0.95,
        "stream": False
    }
    resp = requests.post(invoke_url, headers=headers, json=payload)
    return resp.json()["choices"][0]["message"]["content"]

print("=" * 60)
print("03 — TREE OF THOUGHT (ToT)")
print("=" * 60)
print("💡 ToT = explore MULTIPLE reasoning branches in parallel,")
print("   evaluate each, prune weak ones, expand promising ones.\n")
print(f"📥 Problem: {PROBLEM}\n")
print("-" * 60)

# ─── STEP 1: Generate multiple candidate first moves (branching) ───
print("🌱 STEP 1: Generate candidate first moves...")
branches_prompt = ask_llm([
    {"role": "system", "content": "You generate possible first steps for solving river-crossing puzzles."},
    {"role": "user", "content": f"""For the river crossing puzzle: {PROBLEM}

List exactly 3 different possible first moves (what the farmer takes across first).
Number them 1, 2, 3. Be brief — one sentence each."""}
], temp=0.9)
print(f"\n{branches_prompt}\n")

# ─── STEP 2: Evaluate each branch ───
print("🔍 STEP 2: Evaluate each branch's viability...")
evaluation = ask_llm([
    {"role": "system", "content": "You evaluate reasoning paths critically."},
    {"role": "user", "content": f"""Puzzle: {PROBLEM}

Possible first moves suggested:
{branches_prompt}

For EACH move (1, 2, 3), answer:
- Will this lead to a dead end? Why?
- Can the puzzle be solved from this state?
Pick the SINGLE best first move and explain why."""}
], temp=0.3)
print(f"\n{evaluation}\n")

# ─── STEP 3: Expand on the best branch ───
print("🌳 STEP 3: Expand the best branch into full solution...")
solution = ask_llm([
    {"role": "system", "content": "You complete step-by-step puzzle solutions."},
    {"role": "user", "content": f"""Puzzle: {PROBLEM}

Based on this evaluation of first moves:
{evaluation}

Now complete the FULL solution step by step from the best first move
until everything is across safely. Show each trip."""}
], temp=0.4)
print(f"\n💬 Full solution:\n{solution}")
print("\n✅ ToT explores multiple paths, evaluates them, and focuses on the most promising.")
