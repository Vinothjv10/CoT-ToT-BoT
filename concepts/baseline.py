from src.llm import ask_simple

PROBLEM = (
    "Roger has 5 tennis balls. He buys 2 more cans of tennis balls. "
    "Each can has 3 tennis balls. How many tennis balls does he have now?"
)

def run():
    print("=" * 60)
    print("CONCEPT: Baseline — Direct Answer (No Reasoning Structure)")
    print("=" * 60)
    print(f"Problem: {PROBLEM}\n")

    result = ask_simple(
        "You are a helpful assistant. Answer concisely.",
        f"Answer: {PROBLEM}",
        temperature=0.7
    )
    print(f"Model output:\n{result}")
    print("\n⚠️  Without explicit reasoning instructions, the model may guess incorrectly.")
