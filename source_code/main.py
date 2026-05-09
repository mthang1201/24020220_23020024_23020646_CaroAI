import argparse
import sys
from source_code.config import BOARD_SIZE, DEFAULT_UI, DEFAULT_DEPTH_MINIMAX, DEFAULT_DEPTH_ALPHABETA
from source_code.game.game_state import GameState
from source_code.ai.minimax import MinimaxAI
from source_code.ai.alphabeta import AlphaBetaAI

def main():
    parser = argparse.ArgumentParser(description="Caro AI Project")
    parser.add_argument("--ui", type=str, default=DEFAULT_UI, choices=["console", "pygame"], help="User interface to use")
    parser.add_argument("--algo", type=str, default="alphabeta", choices=["minimax", "alphabeta"], help="AI Algorithm")
    parser.add_argument("--depth", type=int, default=None, help="Search depth for the AI")
    parser.add_argument("--board_size", type=int, default=BOARD_SIZE, help="Size of the board")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark instead of the game")
    
    args = parser.parse_args()

    if args.benchmark:
        from source_code.benchmark.benchmark_runner import run_benchmarks
        run_benchmarks()
        sys.exit(0)

    # Determine depth based on algorithm if not provided
    if args.depth is None:
        depth = DEFAULT_DEPTH_ALPHABETA if args.algo == "alphabeta" else DEFAULT_DEPTH_MINIMAX
    else:
        depth = args.depth

    print(f"Initializing Caro AI with {args.algo} (Depth {depth}) on {args.board_size}x{args.board_size} board...")

    # Initialize AI
    if args.algo == "minimax":
        ai = MinimaxAI(depth=depth)
    else:
        ai = AlphaBetaAI(depth=depth)

    # Initialize Game State
    state = GameState(board_size=args.board_size)

    # Start UI
    if args.ui == "console":
        from source_code.ui.console_ui import ConsoleUI
        ui = ConsoleUI(ai=ai)
        ui.run(state)
    elif args.ui == "pygame":
        from source_code.ui.pygame_ui import PyGameUI
        ui = PyGameUI(ai=ai)
        ui.run(state)

if __name__ == "__main__":
    main()
