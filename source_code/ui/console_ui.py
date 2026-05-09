import os
from source_code.game.game_state import GameState
from source_code.config import SYMBOLS, HUMAN, AI, EMPTY

class ConsoleUI:
    def __init__(self, ai=None):
        self.ai = ai

    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_board(self, state: GameState):
        """Render the board to the console."""
        size = state.board.size
        # Print column headers
        col_headers = "   " + " ".join([f"{c:2}" for c in range(size)])
        print(col_headers)
        
        for r in range(size):
            row_str = f"{r:2} "
            for c in range(size):
                piece = state.board.grid[r][c]
                symbol = SYMBOLS.get(piece, '.')
                row_str += f" {symbol} "
            print(row_str)
        print()

    def get_human_move(self, state: GameState) -> tuple:
        """Prompt human player for a valid move."""
        while True:
            try:
                user_input = input("Enter your move (row col) e.g., '3 4': ")
                parts = user_input.strip().split()
                if len(parts) != 2:
                    print("Invalid format. Please enter row and column separated by space.")
                    continue
                
                r, c = int(parts[0]), int(parts[1])
                
                if not state.board.is_valid_pos(r, c):
                    print(f"Coordinates out of bounds. Please enter values between 0 and {state.board.size - 1}.")
                    continue
                    
                if not state.board.is_empty(r, c):
                    print("That cell is already occupied. Choose an empty cell.")
                    continue
                
                return r, c
            except ValueError:
                print("Invalid input. Please enter numbers.")
            except (EOFError, KeyboardInterrupt):
                print("\nGame aborted by user.")
                exit(0)

    def run(self, state: GameState):
        """Main game loop for Console UI."""
        self.clear_screen()
        print("Welcome to Caro AI Console Mode!")
        print("You are 'X' and AI is 'O'. Get 4 in a row to win!\n")
        
        while not state.is_terminal:
            self.draw_board(state)
            player_symbol = SYMBOLS[state.current_player]
            
            if state.current_player == HUMAN:
                print(f"Human's Turn ({player_symbol})")
                r, c = self.get_human_move(state)
                state.apply_move(r, c)
            else:
                print(f"AI's Turn ({player_symbol})... thinking")
                if self.ai:
                    result = self.ai.choose_move(state)
                    if result and result.best_move:
                        r, c = result.best_move
                        print(f"AI plays: {r} {c}")
                        state.apply_move(r, c)
                    else:
                        print("AI failed to find a move.")
                        break
                else:
                    print("No AI configured!")
                    break
            self.clear_screen()

        self.draw_board(state)
        if state.winner == HUMAN:
            print("Congratulations! You won!")
        elif state.winner == AI:
            print("AI wins! Better luck next time.")
        else:
            print("It's a draw!")
