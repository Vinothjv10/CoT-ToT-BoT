# CoT-ToT-BoT

Learn **Chain of Thought**, **Tree of Thought**, and **Beam of Thoughts** reasoning techniques hands-on, with logistics domain applications.

## Project Structure

```
├── main.py                  CLI entry point
├── src/
│   └── llm.py               Shared LLM client (NVIDIA API)
├── concepts/                Core reasoning techniques
│   ├── baseline.py          Direct prompting (no reasoning structure)
│   ├── cot.py               Chain of Thought (step-by-step reasoning)
│   ├── tot.py               Tree of Thought (branch, evaluate, prune)
│   └── bot.py               Beam of Thoughts (beam search over chains)
└── applications/            Logistics domain examples
    ├── problems.py          Shared problem definitions
    ├── freight_costing.py   CoT: Freight mode cost comparison
    ├── warehouse_placement.py  ToT: Warehouse location strategy
    └── inventory_planning.py   BoT: Inventory allocation planning
```

## Usage

```bash
# Concepts
python main.py concepts/baseline      # Direct answer (baseline)
python main.py concepts/cot           # Chain of Thought
python main.py concepts/tot           # Tree of Thought
python main.py concepts/bot           # Beam of Thoughts

# Logistics Applications
python main.py applications/freight   # CoT: freight mode selection
python main.py applications/warehouse # ToT: warehouse placement
python main.py applications/inventory # BoT: inventory planning

# Run everything
python main.py all
```

## What Each Technique Does

| Technique | Approach | Best For |
|-----------|----------|----------|
| **CoT** | Single chain, step-by-step | Cost breakdowns, multi-step calculations |
| **ToT** | Multiple branches, evaluate & prune | Decisions with discrete choices (location selection) |
| **BoT** | Top-K chains, score & expand | Resource allocation under constraints |
