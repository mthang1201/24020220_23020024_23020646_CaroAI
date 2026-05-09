from source_code.game.board import Board
from source_code.config import HUMAN, AI

# Heuristic weights
SCORE_WIN = 1000000.0
SCORE_OPEN_3 = 50000.0
SCORE_CLOSED_3 = 10000.0
SCORE_OPEN_2 = 5000.0
SCORE_CLOSED_2 = 100.0

class Evaluator:
    @staticmethod
    def evaluate(board: Board) -> float:
        """
        Evaluate the board from the perspective of the AI.
        Positive scores favor the AI, negative scores favor the HUMAN.
        """
        score = 0.0
        
        # Determine score by analyzing all directions
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c] == 0:
                    continue
                
                player = board.grid[r][c]
                multiplier = 1.0 if player == AI else -1.0
                
                for dr, dc in directions:
                    # To avoid double counting, only evaluate lines originating from the 'start'
                    prev_r, prev_c = r - dr, c - dc
                    if board.is_valid_pos(prev_r, prev_c) and board.grid[prev_r][prev_c] == player:
                        continue
                        
                    count = 1
                    open_ends = 0
                    
                    # Check backward open end
                    if board.is_empty(prev_r, prev_c):
                        open_ends += 1
                        
                    # Count forward
                    nr, nc = r + dr, c + dc
                    while board.is_valid_pos(nr, nc) and board.grid[nr][nc] == player:
                        count += 1
                        nr += dr
                        nc += dc
                        
                    # Check forward open end
                    if board.is_empty(nr, nc):
                        open_ends += 1
                        
                    # Scoring logic
                    if count >= 4:
                        score += SCORE_WIN * multiplier
                    elif count == 3:
                        if open_ends == 2:
                            score += SCORE_OPEN_3 * multiplier
                        elif open_ends == 1:
                            score += SCORE_CLOSED_3 * multiplier
                    elif count == 2:
                        if open_ends == 2:
                            score += SCORE_OPEN_2 * multiplier
                        elif open_ends == 1:
                            score += SCORE_CLOSED_2 * multiplier

        return score
