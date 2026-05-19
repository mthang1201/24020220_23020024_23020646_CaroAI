import os
import math
from source_code.game.game_state import GameState
from source_code.config import SYMBOLS, HUMAN, AI, EMPTY


class ConsoleUI:
    """
    Console-based game loop for human vs AI.

    Parameters
    ----------
    ai        : AI instance (MinimaxAI or AlphaBetaAI)
    algo_name : Human-readable label shown in the AI move info block,
                e.g. "Minimax" or "Alpha-Beta".
    """

    def __init__(self, ai=None, algo_name: str = "AI"):
        self.ai = ai
        self.algo_name = algo_name

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_board(self, state: GameState):
        """Render the current board to the console."""
        size = state.board.size
        # Column header row
        col_headers = "    " + "  ".join([f"{c:2}" for c in range(size)])
        print(col_headers)

        for r in range(size):
            row_str = f"{r:3} "
            for c in range(size):
                piece = state.board.grid[r][c]
                symbol = SYMBOLS.get(piece, '.')
                row_str += f" {symbol} "
            print(row_str)
        print()

    def print_ai_info(self, result, move: tuple):
        """
        Print a clearly formatted block of AI statistics after its move.

        Format (as required by the assignment):
            [AI: <algorithm>]
            Move      : (row, col)
            Score     : ...
            Depth     : ...
            States    : ...
            Runtime   : ... ms
        """
        r, c = move
        runtime_ms = result.execution_time * 1000.0

        # Format score: handle ±inf or large win scores gracefully
        if result.evaluation_score == math.inf or result.evaluation_score >= 100000000:
            score_str = "+Infinity (AI wins)"
        elif result.evaluation_score == -math.inf or result.evaluation_score <= -100000000:
            score_str = "-Infinity (Human wins)"
        else:
            score_str = f"{result.evaluation_score:.2f}"

        print("\n" + "-" * 40)
        print(f"[AI: {self.algo_name}]")
        print(f"  Move            : ({r}, {c})")
        print(f"  Score           : {score_str}")
        print(f"  Depth           : {result.depth}")
        print(f"  States evaluated: {result.nodes_explored}")
        print(f"  Runtime         : {runtime_ms:.2f} ms")
        print("-" * 40 + "\n")

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def get_human_move(self, state: GameState) -> tuple:
        """Prompt human player for a valid move with full error handling."""
        size = state.board.size
        while True:
            try:
                user_input = input(f"Enter your move (row col), values 0-{size - 1}: ")
                parts = user_input.strip().split()
                if len(parts) != 2:
                    print("  ✗ Invalid format. Please enter row and column separated by a space.")
                    continue

                r, c = int(parts[0]), int(parts[1])

                if not state.board.is_valid_pos(r, c):
                    print(f"  ✗ Out of bounds. Please enter values between 0 and {size - 1}.")
                    continue

                if not state.board.is_empty(r, c):
                    print("  ✗ That cell is already occupied. Choose an empty cell.")
                    continue

                return r, c

            except ValueError:
                print("  ✗ Invalid input. Please enter integers only.")
            except (EOFError, KeyboardInterrupt):
                print("\nGame aborted by user.")
                exit(0)

    # ------------------------------------------------------------------
    # Game loop
    # ------------------------------------------------------------------

    def run(self, state: GameState):
        """Main game loop."""
        self.clear_screen()
        print("=" * 50)
        print("   Welcome to Caro AI — Console Mode")
        print("=" * 50)
        print(f"  Algorithm : {self.algo_name}")
        print(f"  Board     : {state.board.size}x{state.board.size}")
        print(f"  You are X, AI is O. First to 4 in a row wins!\n")

        while not state.is_terminal:
            self.draw_board(state)
            player_symbol = SYMBOLS[state.current_player]

            if state.current_player == HUMAN:
                print(f">>> Your turn ({player_symbol})")
                r, c = self.get_human_move(state)
                state.apply_move(r, c)
                self.clear_screen()
            else:
                print(f">>> AI's turn ({player_symbol}) — thinking…")
                if self.ai:
                    result = self.ai.choose_move(state)
                    if result and result.best_move:
                        r, c = result.best_move
                        state.apply_move(r, c)
                        self.clear_screen()
                        self.draw_board(state)
                        self.print_ai_info(result, (r, c))
                    else:
                        print("AI failed to find a move.")
                        break
                else:
                    print("No AI configured!")
                    break

        # Final state
        self.draw_board(state)
        print("=" * 50)
        if state.winner == HUMAN:
            print("  🎉 Congratulations! You won!")
        elif state.winner == AI:
            print("  🤖 AI wins! Better luck next time.")
        else:
            print("  🤝 It's a draw!")
        print("=" * 50)
