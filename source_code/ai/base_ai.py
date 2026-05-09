from dataclasses import dataclass
from typing import Tuple, Optional, Any
from source_code.game.game_state import GameState

@dataclass
class SearchResult:
    """Structured result returned by the AI search algorithms."""
    best_move: Optional[Tuple[int, int]]
    evaluation_score: float
    nodes_explored: int
    execution_time: float = 0.0

class BaseAI:
    """Shared interface for AI algorithms."""
    def choose_move(self, game_state: GameState) -> SearchResult:
        """
        Determine the best move for the current game state.
        Must return a SearchResult object.
        """
        raise NotImplementedError("choose_move must be implemented by subclasses.")
