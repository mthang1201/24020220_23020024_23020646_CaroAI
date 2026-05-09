import math
from typing import List, Tuple
from source_code.game.board import Board

class MoveOrderer:
    @staticmethod
    def order_moves(moves: List[Tuple[int, int]], board: Board) -> List[Tuple[int, int]]:
        """
        Sort candidate moves to improve Alpha-Beta pruning efficiency.
        Includes deterministic tie-breaking based on center proximity.
        """
        center = board.size / 2.0
        
        def move_score(move: Tuple[int, int]) -> float:
            # Sort mainly by distance to center. 
            # In a full evaluation-based ordering, we'd apply the heuristic to each move.
            # Here we just use center proximity as a basic deterministic heuristic.
            r, c = move
            # Distance from center
            dist = math.sqrt((r - center)**2 + (c - center)**2)
            # We want smaller distance to be sorted first, so we return dist.
            # To sort descending, we would negate. Ascending is fine here.
            return dist

        return sorted(moves, key=move_score)
