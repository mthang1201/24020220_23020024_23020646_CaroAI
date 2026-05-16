from dataclasses import dataclass
from typing import Tuple, Optional, Any
from source_code.game.game_state import GameState

class TimeOutException(Exception):
    """Exception raised when the AI search exceeds the allotted time limit."""
    pass

@dataclass
class SearchResult:
    """Structured result returned by the AI search algorithms."""
    best_move: Optional[Tuple[int, int]]
    evaluation_score: float # Giá trị ước lượng của nước đi
    nodes_explored: int # Số nút đã khám phá
    execution_time: float = 0.0 # Thời gian thực thi

class BaseAI:
    """Shared interface for AI algorithms."""
    def __init__(self, depth: int = 4, time_limit: float = 3.0):
        from source_code.config import DEFAULT_DEPTH, DEFAULT_TIME_LIMIT
        self.depth = DEFAULT_DEPTH
        self.time_limit = DEFAULT_TIME_LIMIT

    def choose_move(self, game_state: GameState) -> SearchResult:
        """
        Determine the best move for the current game state.
        Must return a SearchResult object.
        """
        raise NotImplementedError("choose_move must be implemented by subclasses.")
