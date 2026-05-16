from source_code.game.board import Board
from source_code.config import AI, HUMAN, EMPTY


class Evaluator:

    # =========================================
    # SCORE TABLE
    # =========================================

    FIVE = 10000000

    OPEN_FOUR = 1000000
    CLOSED_FOUR = 100000

    OPEN_THREE = 10000
    CLOSED_THREE = 1000

    OPEN_TWO = 100
    CLOSED_TWO = 10

    DIRECTIONS = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal \
        (1, -1)   # diagonal /
    ]

    @staticmethod
    def evaluate(board: Board) -> int:

        ai_score = 0
        human_score = 0

        visited_ai = set()
        visited_human = set()

        for r in range(board.size):
            for c in range(board.size):

                piece = board.grid[r][c]

                if piece == EMPTY:
                    continue

                # =========================================
                # AI
                # =========================================

                if piece == AI:

                    for dr, dc in Evaluator.DIRECTIONS:

                        key = (r, c, dr, dc)

                        if key in visited_ai:
                            continue

                        score, cells = Evaluator.evaluate_direction(
                            board,
                            r,
                            c,
                            dr,
                            dc,
                            AI
                        )

                        ai_score += score

                        for cell in cells:
                            visited_ai.add(
                                (cell[0], cell[1], dr, dc)
                            )

                # =========================================
                # HUMAN
                # =========================================

                elif piece == HUMAN:

                    for dr, dc in Evaluator.DIRECTIONS:

                        key = (r, c, dr, dc)

                        if key in visited_human:
                            continue

                        score, cells = Evaluator.evaluate_direction(
                            board,
                            r,
                            c,
                            dr,
                            dc,
                            HUMAN
                        )

                        human_score += score

                        for cell in cells:
                            visited_human.add(
                                (cell[0], cell[1], dr, dc)
                            )

        return ai_score - human_score

    @staticmethod
    def evaluate_direction(
        board: Board,
        r: int,
        c: int,
        dr: int,
        dc: int,
        player: int
    ):

        size = board.size
        grid = board.grid

        cells = [(r, c)]

        count = 1

        # =========================================
        # FORWARD
        # =========================================

        nr = r + dr
        nc = c + dc

        while (
            0 <= nr < size and
            0 <= nc < size and
            grid[nr][nc] == player
        ):
            count += 1
            cells.append((nr, nc))

            nr += dr
            nc += dc

        forward_open = (
            0 <= nr < size and
            0 <= nc < size and
            grid[nr][nc] == EMPTY
        )

        # =========================================
        # BACKWARD
        # =========================================

        nr = r - dr
        nc = c - dc

        while (
            0 <= nr < size and
            0 <= nc < size and
            grid[nr][nc] == player
        ):
            count += 1
            cells.append((nr, nc))

            nr -= dr
            nc -= dc

        backward_open = (
            0 <= nr < size and
            0 <= nc < size and
            grid[nr][nc] == EMPTY
        )

        # =========================================
        # OPEN ENDS
        # =========================================

        open_ends = 0

        if forward_open:
            open_ends += 1

        if backward_open:
            open_ends += 1

        # =========================================
        # SCORE
        # =========================================

        score = Evaluator.pattern_score(
            count,
            open_ends
        )

        return score, cells

    @staticmethod
    def pattern_score(
        count: int,
        open_ends: int
    ) -> int:

        # FIVE
        if count >= 5:
            return Evaluator.FIVE

        # FOUR
        if count == 4:

            if open_ends == 2:
                return Evaluator.OPEN_FOUR

            if open_ends == 1:
                return Evaluator.CLOSED_FOUR

        # THREE
        if count == 3:

            if open_ends == 2:
                return Evaluator.OPEN_THREE

            if open_ends == 1:
                return Evaluator.CLOSED_THREE

        # TWO
        if count == 2:

            if open_ends == 2:
                return Evaluator.OPEN_TWO

            if open_ends == 1:
                return Evaluator.CLOSED_TWO

        return 0