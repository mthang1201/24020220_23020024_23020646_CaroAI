from typing import List, Dict
from source_code.config import EMPTY, HUMAN, AI, BOARD_SIZE

# Helper to create an empty board grid
def create_empty_grid(size: int = BOARD_SIZE) -> List[List[int]]:
    return [[EMPTY for _ in range(size)] for _ in range(size)]


# ---------------------------------------------------------------------------
# Scenario 1 – Opening state
# A single human piece near the center, representing a very early game.
# Expected AI behavior: play close to the existing piece to build a sequence.
# ---------------------------------------------------------------------------
state_opening = create_empty_grid()
state_opening[4][4] = HUMAN

# ---------------------------------------------------------------------------
# Scenario 2 – Mid-game state
# A few pieces scattered; both sides have developing threats.
# Expected AI behavior: balance offence and defence.
# ---------------------------------------------------------------------------
state_mid = create_empty_grid()
state_mid[4][4] = HUMAN
state_mid[4][5] = AI
state_mid[3][4] = HUMAN
state_mid[3][5] = AI

# ---------------------------------------------------------------------------
# Scenario 3 – Immediate AI winning opportunity
# AI has 3 consecutive pieces in a row with an open end.
# Expected AI behavior: complete the 4-in-a-row immediately.
# ---------------------------------------------------------------------------
state_ai_win = create_empty_grid()
state_ai_win[2][2] = AI
state_ai_win[2][3] = AI
state_ai_win[2][4] = AI   # AI needs (2,5) or (2,1) to win
state_ai_win[3][3] = HUMAN
state_ai_win[4][3] = HUMAN

# ---------------------------------------------------------------------------
# Scenario 4 – Human near-win requiring block
# Human has 3 consecutive open pieces; AI must block at (5,1) or (5,5).
# Expected AI behavior: block the human threat rather than build its own.
# ---------------------------------------------------------------------------
state_human_threat = create_empty_grid()
state_human_threat[5][2] = HUMAN
state_human_threat[5][3] = HUMAN
state_human_threat[5][4] = HUMAN
state_human_threat[6][2] = AI
state_human_threat[6][3] = AI

# ---------------------------------------------------------------------------
# Scenario 5 – Dense tactical board
# Checkerboard pattern in center; many short sequences in every direction.
# Tests whether the evaluator handles multiple simultaneous threats correctly.
# ---------------------------------------------------------------------------
state_dense = create_empty_grid()
for r in range(3, 6):
    for c in range(3, 6):
        state_dense[r][c] = HUMAN if (r + c) % 2 == 0 else AI

# ---------------------------------------------------------------------------
# Scenario 6 – Many legal moves (sparse early-mid game)
# A handful of pieces spread far apart so the candidate move list is very
# large.  This stresses the search with a high branching factor and allows
# comparison of how many nodes each algorithm visits.
# ---------------------------------------------------------------------------
state_many_moves = create_empty_grid()
state_many_moves[1][1] = HUMAN
state_many_moves[1][7] = AI
state_many_moves[7][1] = AI
state_many_moves[7][7] = HUMAN
state_many_moves[4][4] = HUMAN   # center anchor
state_many_moves[4][5] = AI
state_many_moves[2][5] = HUMAN
state_many_moves[6][3] = AI

TEST_SCENARIOS: Dict[str, List[List[int]]] = {
    "Opening State":            state_opening,
    "Mid-game State":           state_mid,
    "Immediate AI Win":         state_ai_win,
    "Human Near-Win (Threat)":  state_human_threat,
    "Dense Tactical Board":     state_dense,
    "Many Legal Moves":         state_many_moves,
}
