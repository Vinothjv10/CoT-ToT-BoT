from src.llm import ask_simple

PROBLEM = (
    "Roger has 5 tennis balls. He buys 2 more cans of tennis balls. "
    "Each can has 3 tennis balls. How many tennis balls does he have now?"
)

def run():
    print("=" * 60)
    print("CONCEPT: Chain of Thought (CoT)")
    print("=" * 60)
    print("💡 Force step-by-step reasoning before the final answer.\n")
    print(f"Problem: {PROBLEM}\n")

    result = ask_simple(
        "Always reason step-by-step before giving the final answer.",
        f"Let's think step by step, then answer:\n\n{PROBLEM}",
        temperature=0.7
    )
    print(f"Model output:\n{result}")
    print("\n✅ CoT reveals intermediate logic, catching arithmetic errors early.")
