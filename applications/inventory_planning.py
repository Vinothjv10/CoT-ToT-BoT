"""Logistics Application: BoT — Inventory Replenishment Planning"""

import re
from src.llm import ask
from applications.problems import INVENTORY_PROBLEM

TITLE = "BoT: Inventory Allocation Planning"
BEAM_WIDTH = 3

def generate_strategies():
    return ask([
        {"role": "system", "content": "You generate diverse inventory allocation strategies."},
        {"role": "user", "content": f"{INVENTORY_PROBLEM}\n\nPropose {BEAM_WIDTH} different allocation strategies (units to North, Central, South). Each must fit within the $3,000 budget at ~$10/unit. Label them Strategy 1, 2, 3."}
    ], temperature=0.8)

def score_strategies(strategies):
    return ask([
        {"role": "system", "content": "You score inventory strategies by total cost."},
        {"role": "user", "content": f"{INVENTORY_PROBLEM}\n\nStrategies:\n{strategies}\n\nFor EACH strategy, estimate total cost = reorder + holding (30 days) + stockout. Score 0-10 (10 = best).\n\nOutput:\nStrategy 1: Score X/10 — reason\nStrategy 2: Score X/10 — reason\nStrategy 3: Score X/10 — reason\n\nThen write KEEP: <number> for top-{BEAM_WIDTH}."}
    ], temperature=0.3)

def refine_strategy(num, strategies):
    return ask([
        {"role": "system", "content": "You refine inventory allocation plans."},
        {"role": "user", "content": f"{INVENTORY_PROBLEM}\n\nTake Strategy {num} and refine it:\n- Safety stock buffer?\n- Phased delivery schedule?\n- Final exact unit counts?"}
    ], temperature=0.3)

def final_recommendation():
    return ask([
        {"role": "system", "content": "You synthesize the best answer from multiple analyses."},
        {"role": "user", "content": f"{INVENTORY_PROBLEM}\n\nBased on refined strategies, what is the single best allocation? Give exact numbers for North, Central, South and the expected total cost."}
    ], temperature=0.2)

def run():
    print("=" * 70)
    print(f"APPLICATION: {TITLE}")
    print("=" * 70)
    print(INVENTORY_PROBLEM)
    print(f"Beam width K = {BEAM_WIDTH}")
    print("-" * 70)

    print("🌱 STEP 1/4: Generate candidate strategies...")
    strategies = generate_strategies()
    print(strategies + "\n")
    print("-" * 70)

    print("🏆 STEP 2/4: Score all strategies...")
    scored = score_strategies(strategies)
    print(scored + "\n")

    kept = re.findall(r"KEEP:\s*(\d)", scored)
    if not kept:
        kept = ["1", "2", "3"]
    print(f"🔀 Keeping: {kept}\n")
    print("-" * 70)

    print("🔁 STEP 3/4: Refine top strategies...")
    for num in kept:
        refined = refine_strategy(num, strategies)
        print(f"\n--- Strategy {num} refined ---\n{refined}")

    print("-" * 70)
    print("🎯 STEP 4/4: Final recommendation...")
    final = final_recommendation()
    print(f"Final:\n{final}")
    print("\n✅ Lesson: BoT maintains top-K allocation plans, scores & prunes like beam search.")

if __name__ == "__main__":
    run()
