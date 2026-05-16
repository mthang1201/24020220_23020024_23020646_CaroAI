from typing import List, Tuple

from source_code.game.board import Board
from source_code.config import EMPTY


class MoveGenerator:

    @staticmethod
    def get_candidate_moves(
        board: Board
    ) -> List[Tuple[int, int]]:

        # =====================================
        # FIRST MOVE
        # =====================================

        if board.piece_count == 0:

            center = board.size // 2

            return [(center, center)]

        candidates = []

        # =====================================
        # FILTER CANDIDATES
        # =====================================

        for r, c in board.candidate_moves:

            score = 0

            # ---------------------------------
            # Count nearby stones
            # ---------------------------------

            for dr in range(-2, 3):

                for dc in range(-2, 3):

                    if dr == 0 and dc == 0:
                        continue

                    nr = r + dr
                    nc = c + dc

                    if not board.is_valid_pos(nr, nc):
                        continue

                    if board.grid[nr][nc] != EMPTY:

                        # closer stones = higher score
                        dist = abs(dr) + abs(dc)

                        score += max(0, 5 - dist)

            # ---------------------------------
            # KEEP ONLY GOOD MOVES
            # ---------------------------------

            if score >= 4:

                candidates.append(
                    (
                        score,
                        (r, c)
                    )
                )

        # =====================================
        # SORT STRONGEST FIRST
        # =====================================

        candidates.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        # =====================================
        # LIMIT BRANCHING FACTOR
        # =====================================

        MAX_MOVES = 12

        return [
            move
            for _, move in candidates[:MAX_MOVES]
        ]