"""
main.py – Caro AI entry point
==============================

Menu:
  1. Level 1 – Play vs Minimax
  2. Level 2 – Play vs Alpha-Beta (with optional Minimax vs Alpha-Beta comparison)
  3. Level 3 – Run automated experiments and generate report

Run from the project root:
    python -m source_code.main
"""

from source_code.levels.level_1 import run_level1
from source_code.levels.level_2 import run_level2
from source_code.levels.level_3 import run_level3
import sys

# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

def main():
    print("\n" + "=" * 55)
    print("  CARO AI  –  Main Menu")
    print("=" * 55)
    print("  1  Level 1 – Play vs Minimax")
    print("  2  Level 2 – Play vs Alpha-Beta (+ compare option)")
    print("  3  Level 3 – Run experiments & generate report")
    print("=" * 55)

    choice = input("  Your choice (1 / 2 / 3): ").strip()
    if choice == "1":
        run_level1()
    elif choice == "2":
        run_level2()
    elif choice == "3":
        run_level3()
    else:
        print("  ⚠  Invalid choice. Please run again and enter 1, 2, or 3.")
        sys.exit(1)


if __name__ == "__main__":
    main()