"""Logistics Application: CoT — Freight Mode Selection"""

from src.llm import ask
from applications.problems import FREIGHT_PROBLEM

TITLE = "CoT: Freight Mode Cost Comparison"

def run():
    print("=" * 70)
    print(f"APPLICATION: {TITLE}")
    print("=" * 70)
    print(FREIGHT_PROBLEM)
    print("-" * 70)

    print("Systematic breakdown (CoT):")
    result = ask([
        {"role": "system", "content": (
            "You are a logistics analyst. Break down costs line by line "
            "before concluding."
        )},
        {"role": "user", "content": (
            f"{FREIGHT_PROBLEM}\n\n"
            "For each option, calculate:\n"
            "1. Freight cost\n"
            "2. Insurance cost\n"
            "3. Weeks in transit\n"
            "4. Depreciation cost (2% per week of $200,000)\n"
            "5. TOTAL = freight + insurance + depreciation\n\n"
            "Show each step, then state the cheapest option."
        )}
    ], temperature=0.2)
    print(result)
    print("\n✅ Lesson: CoT prevents missed costs (depreciation from transit time).")

if __name__ == "__main__":
    run()
