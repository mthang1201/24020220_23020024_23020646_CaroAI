from dataclasses import dataclass, field
from typing import Tuple, Optional, Any
from source_code.game.game_state import GameState

class TimeOutException(Exception):
    """Exception raised when the AI search exceeds the allotted time limit."""
    pass

@dataclass
class SearchResult:
    """
    Structured result returned by the AI search algorithms.
    Fields:
        best_move       – (row, col) of the chosen move
        evaluation_score – heuristic score from the AI's perspective (positive = AI favored)
        nodes_explored  – total number of nodes evaluated during the search
        execution_time  – wall-clock time in seconds (use perf_counter)
        depth           – the search depth limit that was used
    """
    best_move: Optional[Tuple[int, int]]
    evaluation_score: float   # Giá trị ước lượng của nước đi
    nodes_explored: int       # Số nút đã khám phá
    execution_time: float = 0.0  # Thời gian thực thi (giây)
    depth: int = 0            # Độ sâu tìm kiếm đã sử dụng

class BaseAI:
    """Shared interface for AI algorithms."""
    def __init__(self, depth: int = 4, time_limit: float = 3.0):
        self.depth = depth
        self.time_limit = time_limit

    def choose_move(self, game_state: GameState) -> SearchResult:
        """
        Determine the best move for the current game state.
        Must return a SearchResult object.
        """
        raise NotImplementedError("choose_move must be implemented by subclasses.")
