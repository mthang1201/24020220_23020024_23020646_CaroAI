import math
from typing import List, Tuple

from source_code.game.board import Board
from source_code.config import AI, HUMAN, EMPTY


class MoveOrderer:

    @staticmethod
    def order_moves(
        moves: List[Tuple[int, int]],
        board: Board
    ) -> List[Tuple[int, int]]:

        center = board.size / 2.0

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        def count_connections(r, c, player):

            total = 0

            for dr, dc in directions:

                count = 0

                # forward
                nr, nc = r + dr, c + dc

                while (
                    board.is_valid_pos(nr, nc)
                    and board.grid[nr][nc] == player
                ):
                    count += 1
                    nr += dr
                    nc += dc

                # backward
                nr, nc = r - dr, c - dc

                while (
                    board.is_valid_pos(nr, nc)
                    and board.grid[nr][nc] == player
                ):
                    count += 1
                    nr -= dr
                    nc -= dc

                total += count

            return total

        def move_heuristic(move):

            r, c = move

            # Existing nearby stones
            neighbor_score = board.neighbor_counts[r][c] * 100

            # Tactical value
            ai_connections = count_connections(r, c, AI)
            human_connections = count_connections(r, c, HUMAN)

            tactical_score = (
                ai_connections * 500
                + human_connections * 700
            )

            # Prefer center slightly
            dist = math.sqrt(
                (r - center) ** 2 +
                (c - center) ** 2
            )

            return (
                neighbor_score +
                tactical_score -
                dist
            )

        return sorted(
            moves,
            key=move_heuristic,
            reverse=True
        )