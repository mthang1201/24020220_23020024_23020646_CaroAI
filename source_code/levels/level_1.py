# ---------------------------------------------------------------------------
# Level 1 – Play vs Minimax
# ---------------------------------------------------------------------------
from source_code.levels import ask_level
from source_code.ai.minimax import MinimaxAI
from source_code.game.game_state import GameState
from source_code.config import DEFAULT_DEPTH_MINIMAX


def run_level1():
    print("\n" + "=" * 55)
    print("  LEVEL 1 – Play against Minimax AI")
    print("=" * 55)

    size  = ask_level.ask_board_size()
    depth = ask_level.ask_depth(DEFAULT_DEPTH_MINIMAX, label="Minimax")
    ui_type = ask_level.ask_ui()

    ai    = MinimaxAI(depth=depth, time_limit=0)
    state = GameState(board_size=size)

    if ui_type == "pygame":
        from source_code.ui.pygame_ui import PyGameUI
        ui = PyGameUI(ai=ai)
    else:
        from source_code.ui.console_ui import ConsoleUI
        ui = ConsoleUI(ai=ai, algo_name="Minimax")
    ui.run(state)