"""Logistics Application: ToT — Warehouse Location Strategy"""

from src.llm import ask
from applications.problems import WAREHOUSE_PROBLEM

TITLE = "ToT: Warehouse Location Selection"

def branch_generation():
    return ask([
        {"role": "system", "content": "You are a logistics analyst generating branch analyses."},
        {"role": "user", "content": f"{WAREHOUSE_PROBLEM}\n\nFor EACH candidate location (A, B, C), calculate:\n- Monthly shipping cost (city_pallets × distance × $0.50)\n- Monthly operating cost ($12,000)\n- TOTAL monthly cost\n\nPresent each as a numbered analysis branch."}
    ], temperature=0.5)

def branch_evaluation(branches):
    return ask([
        {"role": "system", "content": "You critically evaluate logistics trade-offs."},
        {"role": "user", "content": f"{WAREHOUSE_PROBLEM}\n\nCost analyses:\n{branches}\n\nFor EACH location, assess:\n- Hidden risks (lead times, customs)?\n- Scalability for 2x volume?\n- Is the cost difference significant?\n\nRank best → worst. Explain why."}
    ], temperature=0.3)

def deep_dive():
    return ask([
        {"role": "system", "content": "You are a logistics strategist."},
        {"role": "user", "content": "For the best warehouse location, create an implementation plan:\n1. Which city gets served first?\n2. What fleet size is needed?\n3. Payback period vs the worst option?\n\nBe specific with numbers."}
    ], temperature=0.3)

def run():
    print("=" * 70)
    print(f"APPLICATION: {TITLE}")
    print("=" * 70)
    print(WAREHOUSE_PROBLEM)
    print("-" * 70)

    print("🌱 Branch 1/3 — Generate cost for each location...")
    branches = branch_generation()
    print(branches + "\n")
    print("-" * 70)

    print("🔍 Branch 2/3 — Evaluate and compare...")
    evaluation = branch_evaluation(branches)
    print(evaluation + "\n")
    print("-" * 70)

    print("🌳 Branch 3/3 — Deep-dive on best location...")
    plan = deep_dive()
    print(plan)
    print("\n✅ Lesson: ToT lets you compare multiple locations side-by-side before committing.")

if __name__ == "__main__":
    run()
