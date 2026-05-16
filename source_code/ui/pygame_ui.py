import sys
try:
    import pygame
except ImportError:
    pygame = None

from source_code.game.game_state import GameState
from source_code.config import EMPTY, HUMAN, AI

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

CELL_SIZE = 50
MARGIN = 20

class PyGameUI:
    def __init__(self, ai=None):
        if pygame is None:
            print("Error: pygame is not installed. Please install it using 'pip install pygame' or run with '--ui console'.")
            sys.exit(1)
        self.ai = ai
        self.window = None
        self.font = None

    def _init_pygame(self, board_size: int):
        pygame.init()
        window_size = board_size * CELL_SIZE + 2 * MARGIN # Kích thước bằng số ô * kích thước ô + 2 bên của lề
        self.window = pygame.display.set_mode((window_size, window_size)) # Tạo cửa sổ vuông
        pygame.display.set_caption("Caro AI")
        self.font = pygame.font.SysFont("arial", 24)

    def draw_board(self, state: GameState, ai_result=None):
        self.window.fill(WHITE)
        size = state.board.size
        
        # Draw grid
        for i in range(size + 1):
            x = MARGIN + i * CELL_SIZE
            y = MARGIN + i * CELL_SIZE
            pygame.draw.line(self.window, BLACK, (MARGIN, y), (MARGIN + size * CELL_SIZE, y))
            pygame.draw.line(self.window, BLACK, (x, MARGIN), (x, MARGIN + size * CELL_SIZE))

        # Draw pieces
        for r in range(size):
            for c in range(size):
                if state.board.grid[r][c] == HUMAN:
                    self._draw_x(r, c)
                elif state.board.grid[r][c] == AI:
                    self._draw_o(r, c)

        # Thông tin của AI
        if ai_result is not None:
            score_text = self.font.render(
                f"Score: {ai_result.evaluation_score:.2f}",
                True,
                BLACK
            )

            nodes_text = self.font.render(
                f"Nodes: {ai_result.nodes_explored}",
                True,
                BLACK
            )

            self.window.blit(score_text, (10, 10))
            self.window.blit(nodes_text, (10, 40))

        pygame.display.flip()

    def _draw_x(self, r: int, c: int):
        center_x = MARGIN + c * CELL_SIZE + CELL_SIZE // 2
        center_y = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
        offset = CELL_SIZE // 3
        pygame.draw.line(self.window, BLUE, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), 3)
        pygame.draw.line(self.window, BLUE, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), 3)

    def _draw_o(self, r: int, c: int):
        center_x = MARGIN + c * CELL_SIZE + CELL_SIZE // 2
        center_y = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 3
        pygame.draw.circle(self.window, RED, (center_x, center_y), radius, 3)

    def run(self, state: GameState, ai_result=None):
        self._init_pygame(state.board.size)
        self.draw_board(state, ai_result)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if not state.is_terminal and state.current_player == HUMAN:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = event.pos
                        c = (x - MARGIN) // CELL_SIZE
                        r = (y - MARGIN) // CELL_SIZE
                        
                        if state.board.is_valid_pos(r, c) and state.board.is_empty(r, c):
                            state.apply_move(r, c)
                            self.draw_board(state)
            
            # AI Turn
            if not state.is_terminal and state.current_player == AI:
                pygame.time.delay(10) # Small delay for better UX
                if self.ai:
                    ai_result = self.ai.choose_move(state)
                    if ai_result.best_move:
                        r, c = ai_result.best_move
                        state.apply_move(r, c)
                self.draw_board(state, ai_result)
                
            if state.is_terminal:
                self.draw_board(state)
                if state.winner == HUMAN:
                    msg = "Human Wins!"
                elif state.winner == AI:
                    msg = "AI Wins!"
                else:
                    msg = "Draw!"
                
                # Render message over board
                text = self.font.render(msg, True, BLACK, GRAY)
                text_rect = text.get_rect(center=(self.window.get_width()//2, self.window.get_height()//2))
                self.window.blit(text, text_rect)
                pygame.display.flip()

        pygame.quit()
