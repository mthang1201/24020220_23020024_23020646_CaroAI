import argparse
import sys
from source_code.config import BOARD_SIZE, DEFAULT_UI, DEFAULT_DEPTH, DEFAULT_DEPTH_MINIMAX, DEFAULT_DEPTH_ALPHABETA, DEFAULT_TIME_LIMIT
from source_code.game.game_state import GameState
from source_code.ai.minimax import MinimaxAI
from source_code.ai.alphabeta import AlphaBetaAI
from source_code.benchmark.benchmark_runner import run_benchmarks

def main():
    # Chọn giao diện chơi
    print("Welcome to Caro AI!")
    ui_choice = input("Choose UI:\n\t1 Console\n\t2 PyGame\n\t(default: Console):\nYour choice (1 or 2):")
    if ui_choice == "2":
        global DEFAULT_UI
        DEFAULT_UI = "pygame"
    
    # Chọn thuật toán AI
    algo_choice = input("Choose AI Algorithm:\n\t1 Minimax\n\t2 Alpha-Beta\n\t(default: Alpha-Beta):\nYour choice (1 or 2):")
    if algo_choice == "1":
        algo = "minimax"
    else:        
        algo = "alphabeta"

    # Chọn độ khó (độ sâu và thời gian suy nghĩ)
    depth_choice = input("Choose AI Difficulty:\n\t1 Easy\n\t2 Medium\n\t3 Hard\n\t(default: Medium):\nYour choice (1, 2, or 3):")
    global depth_limit, time_limit, DEFAULT_DEPTH_MINIMAX, DEFAULT_DEPTH_ALPHABETA, DEFAULT_TIME_LIMIT
    if depth_choice == "1":
        depth_limit = 3
        depth_limit = 4
        time_limit = DEFAULT_TIME_LIMIT - 1
    elif depth_choice == "3":
        depth_limit = 5
        depth_limit = 8
        time_limit = DEFAULT_TIME_LIMIT + 2
    else:
        depth_limit = DEFAULT_DEPTH_MINIMAX
        depth_limit = DEFAULT_DEPTH_ALPHABETA
        time_limit = DEFAULT_TIME_LIMIT

    # Thiết lập tham số
    parser = argparse.ArgumentParser(description="Caro AI Project")
    parser.add_argument("--ui", type=str, default=DEFAULT_UI, choices=["console", "pygame"], help="User interface to use")
    parser.add_argument("--algo", type=str, default=algo, choices=["minimax", "alphabeta"], help="AI Algorithm")
    parser.add_argument("--depth", type=int, default=None, help="Search depth for the AI")
    parser.add_argument("--time_limit", type=float, default=time_limit, help="Time limit for AI thinking (seconds)")
    parser.add_argument("--board_size", type=int, default=BOARD_SIZE, help="Size of the board")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark instead of the game")
    
    args = parser.parse_args()

    if args.benchmark:
        run_benchmarks()
        sys.exit(0)

    # Determine depth based on algorithm if not provided
    if args.depth is None:
        depth = DEFAULT_DEPTH_ALPHABETA if args.algo == "alphabeta" else depth_limit
    else:
        depth = args.depth

    print(f"Initializing Caro AI with {args.algo} (Depth {depth}, Time Limit {args.time_limit}s) on {args.board_size}x{args.board_size} board...")

    # Initialize AI
    if args.algo == "minimax":
        ai = MinimaxAI(depth=depth, time_limit=args.time_limit)
    else:
        ai = AlphaBetaAI(depth=depth, time_limit=args.time_limit)

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