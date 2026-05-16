from typing import List, Tuple
from source_code.game.board import Board

class MoveGenerator:
    @staticmethod
    def get_candidate_moves(board: Board) -> List[Tuple[int, int]]:
        """
        Generate candidate moves.
        Optimized by returning pre-calculated candidate moves from the board.
        """
        if board.piece_count == 0:
            center = board.size // 2
            return [(center, center)]
        else:
            # Chuyển set sang list để thuật toán AI sử dụng
            return list(board.candidate_moves)