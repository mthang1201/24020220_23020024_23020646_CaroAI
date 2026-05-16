# Centralized configuration and constants for the Caro AI project

# Board and Game Settings
BOARD_SIZE = 9
WIN_LENGTH = 4

# Player definitions
EMPTY = 0
HUMAN = 1
AI = 2

# Player Symbols for Console UI
SYMBOLS = {
    EMPTY: '.',
    HUMAN: 'X',
    AI: 'O'
}

# UI Settings
DEFAULT_UI = "console"

# Search Settings
DEFAULT_DEPTH_MINIMAX = 3
DEFAULT_DEPTH_ALPHABETA = 5
DEFAULT_TIME_LIMIT = 5

# Move Generation Constraints
# Generate only cells within distance <= MAX_CANDIDATE_DISTANCE from existing pieces
MAX_CANDIDATE_DISTANCE = 2

DEFAULT_ALGORITHM = "alphabeta"