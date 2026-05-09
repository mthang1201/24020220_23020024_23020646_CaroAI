from typing import List, Tuple
from source_code.game.board import Board
from source_code.config import MAX_CANDIDATE_DISTANCE, EMPTY

class MoveGenerator:
    @staticmethod
    def get_candidate_moves(board: Board) -> List[Tuple[int, int]]:
        """
        Generate candidate moves.
        To optimize, we only consider empty cells that are within a distance
        of MAX_CANDIDATE_DISTANCE from any existing piece.
        If the board is empty, returns the center of the board.
        """
        if board.piece_count == 0:
            center = board.size // 2
            return [(center, center)]

        candidates = set()
        
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c] != EMPTY:
                    # Found a piece, now check its neighbors within distance
                    for dr in range(-MAX_CANDIDATE_DISTANCE, MAX_CANDIDATE_DISTANCE + 1):
                        for dc in range(-MAX_CANDIDATE_DISTANCE, MAX_CANDIDATE_DISTANCE + 1):
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if board.is_valid_pos(nr, nc) and board.grid[nr][nc] == EMPTY:
                                candidates.add((nr, nc))
                                
        return list(candidates)
