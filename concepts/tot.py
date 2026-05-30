from src.llm import ask

PROBLEM = (
    "A farmer has a fox, a chicken, and a bag of grain. "
    "He needs to get all three across a river using a boat that can only "
    "carry him plus ONE item at a time. "
    "If left alone: fox eats chicken, chicken eats grain. "
    "How does he get everything across safely?"
)

def run():
    print("=" * 60)
    print("CONCEPT: Tree of Thought (ToT)")
    print("=" * 60)
    print("💡 Branch → Evaluate → Prune → Expand on the best path.\n")
    print(f"Problem: {PROBLEM}\n")
    print("-" * 60)

    print("🌱 STEP 1: Generate candidate first moves...")
    branches = ask([
        {"role": "system", "content": "You generate possible first steps for solving river-crossing puzzles."},
        {"role": "user", "content": f"For the river crossing puzzle: {PROBLEM}\n\nList exactly 3 different possible first moves. Number them 1, 2, 3. Be brief."}
    ], temperature=0.9)
    print(branches + "\n")

    print("🔍 STEP 2: Evaluate each branch's viability...")
    evaluation = ask([
        {"role": "system", "content": "You evaluate reasoning paths critically."},
        {"role": "user", "content": f"Puzzle: {PROBLEM}\n\nPossible first moves:\n{branches}\n\nFor EACH move, answer: will this lead to a dead end? Pick the single best first move."}
    ], temperature=0.3)
    print(evaluation + "\n")

    print("🌳 STEP 3: Expand the best branch into full solution...")
    solution = ask([
        {"role": "system", "content": "You complete step-by-step puzzle solutions."},
        {"role": "user", "content": f"Puzzle: {PROBLEM}\n\nBest first move per evaluation:\n{evaluation}\n\nComplete the full step-by-step solution. Show each trip."}
    ], temperature=0.4)
    print(f"Full solution:\n{solution}")
    print("\n✅ ToT explores multiple paths, evaluates them, and deepens the most promising.")
