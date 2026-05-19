from typing import List, Tuple

from source_code.game.board import Board
from source_code.config import EMPTY, AI, HUMAN


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
            # KEEP ONLY GOOD MOVES WITH TACTICAL BONUS
            # ---------------------------------
            # Tăng điểm cực lớn cho các nước đi hoàn thành chuỗi thắng hoặc chặn đối thủ
            tactical_bonus = 0
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                # Đếm quân AI liên tiếp qua (r, c)
                count_ai = 0
                nr, nc = r + dr, c + dc
                while board.is_valid_pos(nr, nc) and board.grid[nr][nc] == AI:
                    count_ai += 1
                    nr += dr
                    nc += dc
                nr, nc = r - dr, c - dc
                while board.is_valid_pos(nr, nc) and board.grid[nr][nc] == AI:
                    count_ai += 1
                    nr -= dr
                    nc -= dc

                # Đếm quân HUMAN liên tiếp qua (r, c)
                count_human = 0
                nr, nc = r + dr, c + dc
                while board.is_valid_pos(nr, nc) and board.grid[nr][nc] == HUMAN:
                    count_human += 1
                    nr += dr
                    nc += dc
                nr, nc = r - dr, c - dc
                while board.is_valid_pos(nr, nc) and board.grid[nr][nc] == HUMAN:
                    count_human += 1
                    nr -= dr
                    nc -= dc

                # Nếu giúp AI tạo chuỗi 4 (thắng ngay lập tức)
                if count_ai >= 3:
                    tactical_bonus += 10000
                # Nếu giúp chặn đối thủ tạo chuỗi 4 (ngăn đối thủ thắng ngay lập tức)
                if count_human >= 3:
                    tactical_bonus += 5000
                # Nếu tạo chuỗi 3 mở
                if count_ai == 2:
                    tactical_bonus += 200
                if count_human == 2:
                    tactical_bonus += 150

            score += tactical_bonus

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

        MAX_MOVES = 24

        return [
            move
            for _, move in candidates[:MAX_MOVES]
        ]