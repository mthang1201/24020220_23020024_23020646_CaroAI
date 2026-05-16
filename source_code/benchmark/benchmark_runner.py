import copy
from source_code.game.game_state import GameState
from source_code.game.board import Board
from source_code.ai.minimax import MinimaxAI
from source_code.ai.alphabeta import AlphaBetaAI
from source_code.benchmark.metrics import MetricsReporter
from source_code.benchmark.test_states import TEST_SCENARIOS
from source_code.config import BOARD_SIZE, AI

def build_game_state_from_grid(grid) -> GameState:
    state = GameState(board_size=BOARD_SIZE)
    # Reconstruct board state
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if grid[r][c] != 0:
                state.board.grid[r][c] = grid[r][c]
    
    # Quan trọng: Cập nhật các ô ứng viên sau khi nạp grid trực tiếp
    state.board.recalculate_candidates()
    
    # For testing, we just set the AI to move next
    state.current_player = AI
    return state

def run_benchmarks():
    print("Initializing Benchmark Runner...")
    reporter = MetricsReporter()
    
    # We use a smaller depth for benchmark to ensure it finishes quickly on identical states
    depth = 3
    
    minimax_ai = MinimaxAI(depth=depth)
    alphabeta_ai = AlphaBetaAI(depth=depth)
    
    for name, grid in TEST_SCENARIOS.items():
        print(f"Running scenario: {name}")
        
        # Ensure identically cloned states
        base_state = build_game_state_from_grid(grid)
        
        state_for_minimax = base_state.clone()
        res_minimax = minimax_ai.choose_move(state_for_minimax)
        reporter.add_result(name, "Minimax", res_minimax)
        
        state_for_ab = base_state.clone()
        res_ab = alphabeta_ai.choose_move(state_for_ab)
        reporter.add_result(name, "Alpha-Beta", res_ab)
        
        # Verify both algorithms return identical best moves
        if res_minimax.best_move != res_ab.best_move:
            print(f"WARNING: Move mismatch in {name}! Minimax: {res_minimax.best_move}, AlphaBeta: {res_ab.best_move}")
            
    reporter.report()

if __name__ == "__main__":
    run_benchmarks()
