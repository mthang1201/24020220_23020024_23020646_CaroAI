from typing import List, Tuple
from source_code.config import BOARD_SIZE, EMPTY

class Board:
    def __init__(self, size: int = BOARD_SIZE):
        self.size = size
        self.grid: List[List[int]] = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.piece_count = 0

    def is_valid_pos(self, r: int, c: int) -> bool:
        """Check if the given coordinates are within the board boundaries."""
        return 0 <= r < self.size and 0 <= c < self.size

    def is_empty(self, r: int, c: int) -> bool:
        """Check if a specific cell is empty."""
        return self.is_valid_pos(r, c) and self.grid[r][c] == EMPTY

    def apply_move(self, r: int, c: int, player: int) -> bool:
        """
        Place a piece on the board.
        Returns True if successful, False if invalid or already occupied.
        """
        if self.is_empty(r, c):
            self.grid[r][c] = player
            self.piece_count += 1
            return True
        return False

    def undo_move(self, r: int, c: int):
        """
        Remove a piece from the board. Used for Minimax search tree traversal.
        """
        if self.is_valid_pos(r, c) and self.grid[r][c] != EMPTY:
            self.grid[r][c] = EMPTY
            self.piece_count -= 1

    def is_full(self) -> bool:
        """Check if the board is completely filled."""
        return self.piece_count == self.size * self.size

    def clone(self) -> 'Board':
        """
        Return a deep copy of the board state.
        Mainly used for setting up test states or copying state to avoid mutations
        during concurrent/independent processes.
        """
        new_board = Board(self.size)
        new_board.grid = [row[:] for row in self.grid]
        new_board.piece_count = self.piece_count
        return new_board
