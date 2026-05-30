import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}

PROBLEM = """A bat and a ball cost $1.10 in total.
The bat costs $1.00 more than the ball.
How much does the ball cost?"""

BEAM_WIDTH = 3

def ask_llm(messages, temp=0.7, max_tok=512):
    payload = {
        "model": "google/gemma-3n-e4b-it",
        "messages": messages,
        "max_tokens": max_tok,
        "temperature": temp,
        "top_p": 0.95,
        "stream": False
    }
    try:
        resp = requests.post(invoke_url, headers=headers, json=payload)
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR: {e}]"

print("=" * 60)
print("04 - BEAM OF THOUGHTS (BoT)")
print("=" * 60)
print("BoT = maintain top-K reasoning chains (a 'beam'),")
print("   expand each, score them, prune back to K, repeat.\n")
print("Problem: " + PROBLEM)
print("Beam width K = " + str(BEAM_WIDTH) + "\n")
print("-" * 60)

# STEP 1: Initial reasoning seeds
print("STEP 1: Generate initial reasoning approaches...")
initial = ask_llm([
    {"role": "system", "content": "You generate diverse initial reasoning approaches to math problems."},
    {"role": "user", "content": "Problem: " + PROBLEM + "\n\nGenerate " + str(BEAM_WIDTH) + " different ways someone might start reasoning about this problem. Number them 1, 2, 3. Each should be 2-3 sentences of initial thinking."}
], temp=0.9)
print(initial + "\n")

# STEP 2: Score each reasoning chain
print("STEP 2: Score each chain for correctness potential...")
scored = ask_llm([
    {"role": "system", "content": "You evaluate mathematical reasoning quality."},
    {"role": "user", "content": "Problem: " + PROBLEM + "\n\nReasoning approaches:\n" + initial + "\n\nFor EACH approach (1, 2, 3), assign a score 0-10 based on:\n- Is the math logic sound?\n- Does it avoid common traps (like saying $0.10 for the ball)?\n- Is it on track to find the right answer?\n\nOutput format:\n1. Score: X/10 - short reason\n2. Score: X/10 - short reason\n3. Score: X/10 - short reason\n\nThen write KEEP: <number> for the top " + str(BEAM_WIDTH) + "."}
], temp=0.3)
print(scored + "\n")

kept_nums = re.findall(r"KEEP:\s*(\d)", scored)
if not kept_nums:
    kept_nums = ["1", "2", "3"]
print("Keeping chains: " + str(kept_nums) + "\n")

# STEP 3: Expand kept chains into full solutions
print("STEP 3: Expand kept chains into full solutions...")
for num in kept_nums:
    print("   Expanding chain #" + num + "...")
    expansion = ask_llm([
        {"role": "system", "content": "You complete partial reasoning into a full correct solution."},
        {"role": "user", "content": "Problem: " + PROBLEM + "\n\nStarting from this reasoning chain (approach #" + num + "):\n" + initial + "\n\nComplete it to a full step-by-step solution. End with Final answer: $X.XX."}
    ], temp=0.4)
    print("\n--- Chain #" + num + " expanded ---\n" + expansion + "\n")

# STEP 4: Final selection
print("STEP 4: Pick the best final answer across all chains...")
final = ask_llm([
    {"role": "system", "content": "You select the best final answer after reviewing multiple solution attempts."},
    {"role": "user", "content": "Problem: " + PROBLEM + "\n\nMultiple reasoning chains produced answers. Select the correct one. State the final answer concisely and explain why it's right.\n\nCommon trap: The ball is NOT $0.10! Think about it."}
], temp=0.2)
print("Final answer:\n" + final)
print("\nBoT uses beam search across reasoning chains, scoring & pruning at each step.")
