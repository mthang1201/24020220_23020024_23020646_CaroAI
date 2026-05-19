# ---------------------------------------------------------------------------
# Level 2 – Play vs Alpha-Beta (+ optional comparison)
# ---------------------------------------------------------------------------

from source_code.levels import ask_level
from source_code.ai.minimax import MinimaxAI
from source_code.game.game_state import GameState
from source_code.config import DEFAULT_DEPTH_ALPHABETA
from source_code.ai.alphabeta import AlphaBetaAI
import math
import sys
import os


def _format_score(score: float) -> str:
    if score == math.inf:
        return "+Inf (AI wins)"
    elif score == -math.inf:
        return "-Inf (Human wins)"
    return f"{score:.2f}"


def _run_compare_mode(size: int, depth: int):
    """
    Compare mode: run both algorithms on the same board state each turn.

    The human plays a full game. Before every AI move the program runs
    BOTH algorithms on a clone of the current board and prints a comparison
    table, then proceeds with the Alpha-Beta move.
    """
    from source_code.config import SYMBOLS, HUMAN, AI, EMPTY
    from source_code.ui.console_ui import ConsoleUI

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


def run_level2():
    print("\n" + "=" * 55)
    print("  LEVEL 2 – Play against Alpha-Beta AI")
    print("=" * 55)

    size  = ask_level.ask_board_size()
    depth = ask_level.ask_depth(DEFAULT_DEPTH_ALPHABETA, label="Alpha-Beta")

    print("\n  Choose an option:")
    print("    1  Play with Minimax")
    print("    2  Play with Alpha-Beta")
    print("    3  Compare Minimax vs Alpha-Beta on the current board state")
    choice = input("  Your choice (default 2): ").strip() or "2"

    if choice == "3":
        _run_compare_mode(size=size, depth=depth)
    else:
        # Ask for UI type for standard playing options
        ui_type = ask_level.ask_ui()

        if choice == "1":
            ai = MinimaxAI(depth=depth, time_limit=0)
            algo_name = "Minimax"
        else:
            # Default: Alpha-Beta
            ai = AlphaBetaAI(depth=depth, time_limit=0)
            algo_name = "Alpha-Beta"

        if ui_type == "pygame":
            from source_code.ui.pygame_ui import PyGameUI
            ui = PyGameUI(ai=ai)
        else:
            from source_code.ui.console_ui import ConsoleUI
            ui = ConsoleUI(ai=ai, algo_name=algo_name)

        ui.run(GameState(board_size=size))