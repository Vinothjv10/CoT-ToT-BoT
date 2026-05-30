#!/usr/bin/env python3
"""
CoT-ToT-BoT — Learn reasoning techniques hands-on.

Usage:
    python main.py <module>

Modules:
    concepts/baseline      Baseline direct prompting
    concepts/cot           Chain of Thought
    concepts/tot           Tree of Thought
    concepts/bot           Beam of Thoughts
    applications/freight   Logistics: freight mode costing (CoT)
    applications/warehouse Logistics: warehouse placement (ToT)
    applications/inventory Logistics: inventory planning (BoT)
    all                    Run everything sequentially
"""

import sys
import importlib

MODULES = {
    "concepts/baseline":      "concepts.baseline",
    "concepts/cot":           "concepts.cot",
    "concepts/tot":           "concepts.tot",
    "concepts/bot":           "concepts.bot",
    "applications/freight":   "applications.freight_costing",
    "applications/warehouse": "applications.warehouse_placement",
    "applications/inventory": "applications.inventory_planning",
}

def run_all():
    for name, mod_path in MODULES.items():
        mod = importlib.import_module(mod_path)
        mod.run()
        print("\n" + "=" * 70 + "\n")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    target = sys.argv[1]

    if target == "all":
        run_all()
        return

    mod_path = MODULES.get(target)
    if not mod_path:
        print(f"Unknown module: {target}")
        print(__doc__)
        sys.exit(1)

    mod = importlib.import_module(mod_path)
    mod.run()

if __name__ == "__main__":
    main()
