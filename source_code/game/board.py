from typing import List, Tuple
from source_code.config import BOARD_SIZE, EMPTY

class Board:
    def __init__(self, size: int = BOARD_SIZE):
        self.size = size

        # Tạo bàn cờ với kích thước size x size, ban đầu tất cả các ô đều là EMPTY (0)
        self.grid: List[List[int]] = [[EMPTY for _ in range(size)] for _ in range(size)]
        
        # Số lượng quân cờ trên bàn cờ
        self.piece_count = 0

        # Tối ưu hóa: Theo dõi các ô ứng viên để tránh quét toàn bộ bảng
        # neighbor_counts[r][c] lưu số lượng quân cờ trong bán kính 2 ô xung quanh (r, c)
        self.neighbor_counts: List[List[int]] = [[0 for _ in range(size)] for _ in range(size)]
        self.candidate_moves: set = set()

    def is_valid_pos(self, r: int, c: int) -> bool:
        """Check if the given coordinates are within the board boundaries."""
        return 0 <= r < self.size and 0 <= c < self.size

    def is_empty(self, r: int, c: int) -> bool:
        """Check if a specific cell is empty."""
        return self.is_valid_pos(r, c) and self.grid[r][c] == EMPTY

    def apply_move(self, r: int, c: int, player: int) -> bool:
        """
        Place a piece on the board and update candidate moves.
        """
        if self.is_empty(r, c):
            self.grid[r][c] = player
            self.piece_count += 1
            
            # Cập nhật các ô ứng viên xung quanh nước vừa đi
            if (r, c) in self.candidate_moves:
                self.candidate_moves.remove((r, c))
            
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    if dr == 0 and dc == 0: continue
                    nr, nc = r + dr, c + dc
                    if self.is_valid_pos(nr, nc):
                        self.neighbor_counts[nr][nc] += 1
                        if self.grid[nr][nc] == EMPTY:
                            if self.neighbor_counts[nr][nc] > 0:
                                self.candidate_moves.add((nr, nc))
                            else:
                                self.candidate_moves.discard((nr, nc))
            return True
        return False

    def undo_move(self, r: int, c: int):
        if self.is_valid_pos(r, c) and self.grid[r][c] != EMPTY:

            self.grid[r][c] = EMPTY
            self.piece_count -= 1

            # Giảm neighbor counts trước
            for dr in range(-2, 3):
                for dc in range(-2, 3):

                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = r + dr, c + dc

                    if self.is_valid_pos(nr, nc):

                        self.neighbor_counts[nr][nc] -= 1

                        if (
                            self.neighbor_counts[nr][nc] == 0
                            and (nr, nc) in self.candidate_moves
                        ):
                            self.candidate_moves.remove((nr, nc))

            # Sau khi update xong mới xét ô hiện tại
            if self.neighbor_counts[r][c] > 0:
                self.candidate_moves.add((r, c))

    def is_full(self) -> bool:
        """Check if the board is completely filled."""
        return self.piece_count == self.size * self.size

    def clone(self) -> 'Board':
        """
        Return a deep copy of the board state.
        """
        new_board = Board(self.size)
        new_board.grid = [row[:] for row in self.grid]
        new_board.piece_count = self.piece_count
        new_board.neighbor_counts = [row[:] for row in self.neighbor_counts]
        new_board.candidate_moves = self.candidate_moves.copy()
        return new_board

    def recalculate_candidates(self):
        """
        Manually recalculate neighbor counts and candidate moves from the current grid.
        Useful when the board is initialized from a pre-defined grid.
        """
        self.neighbor_counts = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.candidate_moves = set()
        self.piece_count = 0
        
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != EMPTY:
                    self.piece_count += 1
                    # Cập nhật các ô xung quanh quân cờ
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            if self.is_valid_pos(nr, nc):
                                self.neighbor_counts[nr][nc] += 1
                                if self.grid[nr][nc] == EMPTY:
                                    self.candidate_moves.add((nr, nc))
        
        # Loại bỏ các ô đã có quân khỏi candidate_moves
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != EMPTY and (r, c) in self.candidate_moves:
                    self.candidate_moves.remove((r, c))