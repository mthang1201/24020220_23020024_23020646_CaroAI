import sys
from source_code.config import (
    BOARD_SIZE,
    DEFAULT_UI,
    DEFAULT_DEPTH_MINIMAX,
    DEFAULT_DEPTH_ALPHABETA,
    DEFAULT_TIME_LIMIT,
    DEFAULT_ALGORITHM
)
from source_code.game.game_state import GameState
from source_code.ai.minimax import MinimaxAI
from source_code.ai.alphabeta import AlphaBetaAI
from source_code.benchmark.benchmark_runner import run_benchmarks

def main():
    # Chọn chế độ chơi: (Play or Benchmark)
    mode = input("Choose mode:\n\t1 Play\n\t2 Benchmark\n\t(default: Play):\nYour choice (1 or 2):")
    if mode == "2":
        run_benchmarks()
        sys.exit(0)
    else:
        # Chọn giao diện chơi
        print("Welcome to Caro AI!")
        ui = DEFAULT_UI
        ui_choice = input(f"Choose UI:\n\t1 Console\n\t2 PyGame\n\t(default: {DEFAULT_UI}):\nYour choice (1 or 2):")
        if ui_choice == "2":
            ui = "pygame"
        
        # Chọn thuật toán AI
        algorithm_choice = input(f"Choose AI Algorithm:\n\t1 Minimax\n\t2 Alpha-Beta\n\t(default: {DEFAULT_ALGORITHM}):\nYour choice (1 or 2):")
        algorithm = DEFAULT_ALGORITHM
        if algorithm_choice == "1":
            algorithm = "minimax"

        # Chọn độ khó (độ sâu và thời gian suy nghĩ)
        difficulty_settings = {
            "minimax": {
                "1": (3, DEFAULT_TIME_LIMIT - 1), # Easy
                "2": (DEFAULT_DEPTH_MINIMAX, DEFAULT_TIME_LIMIT), # Medium
                "3": (5, DEFAULT_TIME_LIMIT + 2) # Hard
            },

            "alphabeta": {
                "1": (4, DEFAULT_TIME_LIMIT - 1),
                "2": (DEFAULT_DEPTH_ALPHABETA, DEFAULT_TIME_LIMIT),
                "3": (6, DEFAULT_TIME_LIMIT + 2)
            }
        }
        difficulty_choice = input("Choose AI Difficulty:\n\t1 Easy\n\t2 Medium\n\t3 Hard\n\t(default: Medium):\nYour choice (1, 2, or 3):")
        depth_limit, time_limit = difficulty_settings[algorithm].get(difficulty_choice, difficulty_settings[algorithm]["2"])

        print(f"Initializing Caro AI with {algorithm} (Depth {depth_limit}, Time Limit {time_limit}s) on {BOARD_SIZE}x{BOARD_SIZE} board...")

        # Initialize AI
        if algorithm == "minimax":
            ai = MinimaxAI(depth=depth_limit, time_limit=time_limit)
        else:
            ai = AlphaBetaAI(depth=depth_limit, time_limit=time_limit)

        # Initialize Game State
        state = GameState(board_size=BOARD_SIZE)

        # Start UI
        if ui == "console":
            from source_code.ui.console_ui import ConsoleUI
            ui = ConsoleUI(ai=ai)
            ui.run(state)
        elif ui == "pygame":
            from source_code.ui.pygame_ui import PyGameUI
            ui = PyGameUI(ai=ai)
            ui.run(state)

if __name__ == "__main__":
    main()