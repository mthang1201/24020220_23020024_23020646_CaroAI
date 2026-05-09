from source_code.game.board import Board
from source_code.config import WIN_LENGTH, EMPTY

class Rules:
    @staticmethod
    def check_win(board: Board, player: int) -> bool:
        """
        Check if the given player has achieved the win condition.
        Win condition: WIN_LENGTH (default 4) or more consecutive pieces.
        """
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Main diagonal
            (1, -1)   # Anti-diagonal
        ]
        
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c] != player:
                    continue
                
                for dr, dc in directions:
                    count = 1
                    # Forward check
                    nr, nc = r + dr, c + dc
                    while board.is_valid_pos(nr, nc) and board.grid[nr][nc] == player:
                        count += 1
                        nr += dr
                        nc += dc
                        
                    # We don't necessarily need a backward check if we scan all cells
                    # and the check goes in the positive direction of the axes.
                    # Because any line of N will be found starting from its earliest point.
                    
                    if count >= WIN_LENGTH:
                        return True
        return False

    @staticmethod
    def is_draw(board: Board) -> bool:
        """
        Check if the game is a draw (board is full and no one has won).
        (Note: checking win condition separately is recommended).
        """
        return board.is_full()
