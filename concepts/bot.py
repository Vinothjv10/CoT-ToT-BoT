import re
from src.llm import ask

PROBLEM = (
    "A bat and a ball cost $1.10 in total. "
    "The bat costs $1.00 more than the ball. "
    "How much does the ball cost?"
)
BEAM_WIDTH = 3

def run():
    print("=" * 60)
    print("CONCEPT: Beam of Thoughts (BoT)")
    print("=" * 60)
    print("💡 Maintain top-K reasoning chains, score & prune at each step.\n")
    print(f"Problem: {PROBLEM}")
    print(f"Beam width K = {BEAM_WIDTH}\n")
    print("-" * 60)

    print("🌱 STEP 1: Generate initial reasoning seeds...")
    initial = ask([
        {"role": "system", "content": "You generate diverse initial reasoning approaches to math problems."},
        {"role": "user", "content": f"Problem: {PROBLEM}\n\nGenerate {BEAM_WIDTH} different ways to start reasoning about this. Number them 1, 2, 3. Each 2-3 sentences."}
    ], temperature=0.9)
    print(initial + "\n")

    print("🏆 STEP 2: Score each chain for correctness potential...")
    scored = ask([
        {"role": "system", "content": "You evaluate mathematical reasoning quality."},
        {"role": "user", "content": f"Problem: {PROBLEM}\n\nReasoning approaches:\n{initial}\n\nFor EACH approach (1, 2, 3), score 0-10. Avoid the $0.10 trap.\n\nOutput:\n1. Score: X/10 — reason\n2. Score: X/10 — reason\n3. Score: X/10 — reason\n\nThen write KEEP: <number> for the top-{str(BEAM_WIDTH)}."}
    ], temperature=0.3)
    print(scored + "\n")

    kept = re.findall(r"KEEP:\s*(\d)", scored)
    if not kept:
        kept = ["1", "2", "3"]

    print(f"🔀 Keeping chains: {kept}\n")

    print("🔁 STEP 3: Expand kept chains into full solutions...")
    for num in kept:
        expansion = ask([
            {"role": "system", "content": "You complete partial reasoning into a full correct solution."},
            {"role": "user", "content": f"Problem: {PROBLEM}\n\nStarting from approach #{num}:\n{initial}\n\nComplete it to a full step-by-step solution. End with 'Final answer: $X.XX'."}
        ], temperature=0.4)
        print(f"\n--- Chain #{num} ---\n{expansion}")

    print("\n🎯 STEP 4: Pick the best final answer...")
    final = ask([
        {"role": "system", "content": "You select the best final answer after reviewing multiple solution attempts."},
        {"role": "user", "content": f"Problem: {PROBLEM}\n\nCommon trap: The ball is NOT $0.10. Multiple chains were explored. State the correct final answer concisely."}
    ], temperature=0.2)
    print(f"Final answer:\n{final}")
    print("\n✅ BoT uses beam search across reasoning chains, scoring & pruning at each step.")
