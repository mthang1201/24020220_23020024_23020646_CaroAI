from typing import List, Tuple, Optional
from source_code.game.board import Board
from source_code.game.rules import Rules
from source_code.config import EMPTY, HUMAN, AI

class GameState:
    def __init__(self, board_size: int = None):
        # Tạo bàn cờ với kích thước board_size, nếu không truyền thì lấy mặc định trong Board
        self.board = Board(board_size) if board_size else Board()
        self.current_player = AI
        self.move_history: List[Tuple[int, int, int]] = [] # (row, col, player)
        self.is_terminal = False # Chưa kết thúc
        self.winner: Optional[int] = None
        
    def get_opponent(self, player: int) -> int:
        return AI if player == HUMAN else HUMAN

    def apply_move(self, r: int, c: int) -> bool:
        """
        Attempts to apply a move for the current player.
        Updates state, checks for win/draw, and switches turn.
        Returns True if successful, False otherwise.
        """
        if self.is_terminal:
            return False

        if self.board.apply_move(r, c, self.current_player):
            self.move_history.append((r, c, self.current_player))
            
            if Rules.check_win(self.board, self.current_player):
                self.is_terminal = True
                self.winner = self.current_player
            elif Rules.is_draw(self.board):
                self.is_terminal = True
                self.winner = EMPTY
            else:
                self.current_player = self.get_opponent(self.current_player)
            return True
            
        return False

    def undo_last_move(self):
        """
        Undo the last move from the history.
        Crucial for Minimax traversal.
        """
        if not self.move_history:
            return

        r, c, player = self.move_history.pop()
        self.board.undo_move(r, c)
        
        # Revert terminal status
        self.is_terminal = False
        self.winner = None
        self.current_player = player

    def clone(self) -> 'GameState':
        """
        Creates a deep copy of the game state.
        Useful for branching independent simulations or benchmarking.
        """
        new_state = GameState(self.board.size)
        new_state.board = self.board.clone()
        new_state.current_player = self.current_player
        new_state.move_history = list(self.move_history)
        new_state.is_terminal = self.is_terminal
        new_state.winner = self.winner
        return new_state
