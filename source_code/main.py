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

import sys
import math
from source_code.config import (
    BOARD_SIZE,
    DEFAULT_DEPTH_MINIMAX,
    DEFAULT_DEPTH_ALPHABETA,
    AI,
)
from source_code.game.game_state import GameState
from source_code.ai.minimax import MinimaxAI
from source_code.ai.alphabeta import AlphaBetaAI


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ask_board_size() -> int:
    """Prompt for board size; default 9."""
    raw = input(f"  Board size (default 9, min 9): ").strip()
    if not raw:
        return 9
    try:
        size = int(raw)
        if size < 9:
            print("  ⚠  Board size must be at least 9. Using 9.")
            return 9
        return size
    except ValueError:
        print("  ⚠  Invalid input. Using 9.")
        return 9


def _ask_depth(default: int, label: str = "AI") -> int:
    """Prompt for search depth with a warning for large values."""
    raw = input(f"  Search depth for {label} (default {default}): ").strip()
    if not raw:
        return default
    try:
        depth = int(raw)
        if depth <= 0:
            print(f"  ⚠  Depth must be positive. Using {default}.")
            return default
        if depth >= 5:
            print(f"  ⚠  Depth {depth} may be very slow on a 9x9 board. Continuing…")
        return depth
    except ValueError:
        print(f"  ⚠  Invalid input. Using {default}.")
        return default


def _format_score(score: float) -> str:
    if score == math.inf:
        return "+Inf (AI wins)"
    elif score == -math.inf:
        return "-Inf (Human wins)"
    return f"{score:.2f}"


# ---------------------------------------------------------------------------
# Level 1 – Play vs Minimax
# ---------------------------------------------------------------------------

def run_level1():
    print("\n" + "=" * 55)
    print("  LEVEL 1 – Play against Minimax AI")
    print("=" * 55)

    size  = _ask_board_size()
    depth = _ask_depth(DEFAULT_DEPTH_MINIMAX, label="Minimax")

    ai    = MinimaxAI(depth=depth, time_limit=0)
    state = GameState(board_size=size)

    from source_code.ui.console_ui import ConsoleUI
    ui = ConsoleUI(ai=ai, algo_name="Minimax")
    ui.run(state)


# ---------------------------------------------------------------------------
# Level 2 – Play vs Alpha-Beta (+ optional comparison)
# ---------------------------------------------------------------------------

def run_level2():
    print("\n" + "=" * 55)
    print("  LEVEL 2 – Play against Alpha-Beta AI")
    print("=" * 55)

    size  = _ask_board_size()
    depth = _ask_depth(DEFAULT_DEPTH_ALPHABETA, label="Alpha-Beta")

    print("\n  Choose an option:")
    print("    1  Play with Minimax")
    print("    2  Play with Alpha-Beta")
    print("    3  Compare Minimax vs Alpha-Beta on the current board state")
    choice = input("  Your choice (default 2): ").strip() or "2"

    if choice == "1":
        ai = MinimaxAI(depth=depth, time_limit=0)
        from source_code.ui.console_ui import ConsoleUI
        ConsoleUI(ai=ai, algo_name="Minimax").run(GameState(board_size=size))

    elif choice == "3":
        _run_compare_mode(size=size, depth=depth)

    else:
        # Default: Alpha-Beta
        ai = AlphaBetaAI(depth=depth, time_limit=0)
        from source_code.ui.console_ui import ConsoleUI
        ConsoleUI(ai=ai, algo_name="Alpha-Beta").run(GameState(board_size=size))


def _run_compare_mode(size: int, depth: int):
    """
    Compare mode: run both algorithms on the same board state each turn.

    The human plays a full game. Before every AI move the program runs
    BOTH algorithms on a clone of the current board and prints a comparison
    table, then proceeds with the Alpha-Beta move.
    """
    from source_code.config import SYMBOLS, HUMAN, AI, EMPTY
    from source_code.ui.console_ui import ConsoleUI
    import os

    state = GameState(board_size=size)
    mm_ai = MinimaxAI(depth=depth, time_limit=0)
    ab_ai = AlphaBetaAI(depth=depth, time_limit=0)

    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw(s):
        sz = s.board.size
        print("    " + "  ".join([f"{c:2}" for c in range(sz)]))
        for r in range(sz):
            row = f"{r:3} " + "  ".join(SYMBOLS.get(s.board.grid[r][c], '.') for c in range(sz))
            print(row)
        print()

    def get_human_move(s):
        sz = s.board.size
        while True:
            try:
                raw = input(f"  Your move (row col), 0-{sz-1}: ").strip().split()
                if len(raw) != 2:
                    print("  ✗ Enter row and column separated by space.")
                    continue
                r, c = int(raw[0]), int(raw[1])
                if not s.board.is_valid_pos(r, c):
                    print(f"  ✗ Out of bounds (0–{sz-1}).")
                    continue
                if not s.board.is_empty(r, c):
                    print("  ✗ Cell occupied. Choose another.")
                    continue
                return r, c
            except ValueError:
                print("  ✗ Enter integers only.")
            except (EOFError, KeyboardInterrupt):
                print("\nGame aborted.")
                sys.exit(0)

    clear()
    print("=" * 60)
    print("  LEVEL 2 – COMPARE MODE (Minimax vs Alpha-Beta)")
    print(f"  Board {size}x{size}  |  Depth {depth}")
    print("  You are X, AI is O.  Each AI turn shows both algorithms.")
    print("=" * 60 + "\n")

    while not state.is_terminal:
        draw(state)

        if state.current_player == HUMAN:
            print(">>> Your turn (X):")
            r, c = get_human_move(state)
            state.apply_move(r, c)
            clear()
        else:
            print(">>> AI's turn (O) — running Minimax AND Alpha-Beta…\n")

            # Run both on independent clones
            clone_mm = state.clone()
            clone_ab = state.clone()

            res_mm = mm_ai.choose_move(clone_mm)
            res_ab = ab_ai.choose_move(clone_ab)

            # Comparison table
            same_move = res_mm.best_move == res_ab.best_move
            if res_mm.nodes_explored > 0:
                reduction = (res_mm.nodes_explored - res_ab.nodes_explored) / res_mm.nodes_explored * 100
            else:
                reduction = 0.0

            from tabulate import tabulate
            table = [
                ["Minimax",    str(res_mm.best_move), _format_score(res_mm.evaluation_score),
                 depth, res_mm.nodes_explored, f"{res_mm.execution_time*1000:.2f}"],
                ["Alpha-Beta", str(res_ab.best_move), _format_score(res_ab.evaluation_score),
                 depth, res_ab.nodes_explored, f"{res_ab.execution_time*1000:.2f}"],
            ]
            headers = ["Algorithm", "Best Move", "Score", "Depth", "States", "Runtime(ms)"]
            print(tabulate(table, headers=headers, tablefmt="grid"))
            print(f"\n  Same move?      : {'✓ YES' if same_move else '✗ NO'}")
            print(f"  State reduction : {reduction:.1f}%  "
                  f"({'Alpha-Beta evaluated fewer states' if reduction > 0 else 'no reduction'})")

            # Proceed with Alpha-Beta's move
            if res_ab.best_move:
                r, c = res_ab.best_move
                state.apply_move(r, c)
                print(f"\n  → Proceeding with Alpha-Beta's move: ({r}, {c})\n")
            else:
                print("  AI failed to find a move.")
                break

            input("  [Press Enter to continue] ")
            clear()

    draw(state)
    print("=" * 55)
    if state.winner == HUMAN:
        print("  🎉 Congratulations! You won!")
    elif state.winner == AI:
        print("  🤖 AI wins! Better luck next time.")
    else:
        print("  🤝 It's a draw!")
    print("=" * 55)


# ---------------------------------------------------------------------------
# Level 3 – Experiments
# ---------------------------------------------------------------------------

def run_level3():
    from source_code.experiments import run_experiments
    run_experiments()


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