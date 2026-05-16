from source_code.game.board import Board
from source_code.config import HUMAN, AI

# ---------------------------------------------------------------------------
# Heuristic weight constants
# ---------------------------------------------------------------------------
# SCORE_WIN    – assigned when 4+ consecutive pieces already exist.
#                Used to ensure that near-terminal states dominate the search.
#                (Terminal wins return ±inf; this catches patterns at depth 0.)
SCORE_WIN = 1_000_000.0

# SCORE_OPEN_3 – three consecutive pieces with BOTH ends open.
#                This is an extremely dangerous threat because the opponent
#                cannot block both sides in one move → high priority.
SCORE_OPEN_3 = 50_000.0

# SCORE_CLOSED_3 – three consecutive pieces with only ONE end open.
#                  Still a strong threat but easier to defend.
SCORE_CLOSED_3 = 10_000.0

# SCORE_OPEN_2 – two consecutive pieces with both ends open.
#                Represents a developing threat; score high enough to
#                encourage building sequences.
SCORE_OPEN_2 = 5_000.0

# SCORE_CLOSED_2 – two consecutive pieces with only one end open.
#                  Minimal threat but still worth a small bonus/penalty.
SCORE_CLOSED_2 = 100.0


class Evaluator:
    @staticmethod
    def evaluate(board: Board) -> float:
        """
        Evaluate the board from the perspective of the AI player.

        Returns a float score:
          - Positive  → board favors AI
          - Negative  → board favors HUMAN
          - 0         → roughly balanced

        Scoring logic per direction per line-start:
          count >= 4  → ±SCORE_WIN   (4-in-a-row found at eval depth)
          count == 3, both ends open → ±SCORE_OPEN_3
          count == 3, one end open   → ±SCORE_CLOSED_3
          count == 2, both ends open → ±SCORE_OPEN_2
          count == 2, one end open   → ±SCORE_CLOSED_2

        Threat asymmetry:
          The weight constants are the same for AI and HUMAN, but the
          MULTIPLIER sign differs (+1 for AI, -1 for HUMAN).
          This means blocking a human OPEN_3 saves 50 000 points,
          which correctly prioritises defence when the human threatens to win.

        Move ordering optimisation:
          Moves are pre-sorted by center proximity (see move_ordering.py)
          before Minimax/Alpha-Beta is called, so the evaluation function
          itself does not need to handle ordering.
        """
        score = 0.0

        # Scan all four directions (each covers its mirror by starting from line origin)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c] == 0:
                    continue

                player = board.grid[r][c]

                # Positive multiplier for AI pieces, negative for HUMAN pieces.
                # This single sign flip makes the evaluation symmetric.
                multiplier = 1.0 if player == AI else -1.0

                for dr, dc in directions:
                    # Skip if this cell is NOT the start of a line in this direction
                    # (avoids double-counting the same line segment).
                    prev_r, prev_c = r - dr, c - dc
                    if board.is_valid_pos(prev_r, prev_c) and board.grid[prev_r][prev_c] == player:
                        continue

                    count = 1
                    open_ends = 0

                    # Check backward open end (cell before the line start)
                    if board.is_empty(prev_r, prev_c):
                        open_ends += 1

                    # Count consecutive pieces forward
                    nr, nc = r + dr, c + dc
                    while board.is_valid_pos(nr, nc) and board.grid[nr][nc] == player:
                        count += 1
                        nr += dr
                        nc += dc

                    # Check forward open end (cell after the line end)
                    if board.is_empty(nr, nc):
                        open_ends += 1

                    # Apply heuristic score based on line length and openness
                    if count >= 4:
                        # 4-in-a-row: effectively a win; dominate all other terms
                        score += SCORE_WIN * multiplier
                    elif count == 3:
                        if open_ends == 2:
                            # Open three – cannot be fully blocked in one move
                            score += SCORE_OPEN_3 * multiplier
                        elif open_ends == 1:
                            # Closed three – dangerous but one move can block it
                            score += SCORE_CLOSED_3 * multiplier
                        # open_ends == 0: completely blocked → no score
                    elif count == 2:
                        if open_ends == 2:
                            # Open two – developing threat worth rewarding
                            score += SCORE_OPEN_2 * multiplier
                        elif open_ends == 1:
                            # Closed two – minimal threat
                            score += SCORE_CLOSED_2 * multiplier
                        # open_ends == 0: completely blocked → no score

        return score
