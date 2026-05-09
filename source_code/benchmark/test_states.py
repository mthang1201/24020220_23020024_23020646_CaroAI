from typing import List, Dict
from source_code.config import EMPTY, HUMAN, AI, BOARD_SIZE

# Helper to create an empty board grid
def create_empty_grid() -> List[List[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# 1. Opening state: Empty board
state_opening = create_empty_grid()
state_opening[4][4] = HUMAN

# 2. Mid-game state: A few pieces scattered
state_mid = create_empty_grid()
state_mid[4][4] = HUMAN
state_mid[4][5] = AI
state_mid[3][4] = HUMAN
state_mid[3][5] = AI

# 3. Immediate AI winning opportunity: AI has 3 in a row
state_ai_win = create_empty_grid()
state_ai_win[2][2] = AI
state_ai_win[2][3] = AI
state_ai_win[2][4] = AI
state_ai_win[3][3] = HUMAN
state_ai_win[4][3] = HUMAN

# 4. Human near-win requiring block: Human has 3 in a row, open ends
state_human_threat = create_empty_grid()
state_human_threat[5][2] = HUMAN
state_human_threat[5][3] = HUMAN
state_human_threat[5][4] = HUMAN
state_human_threat[6][2] = AI
state_human_threat[6][3] = AI

# 5. Dense tactical board: Clustered pieces in the center
state_dense = create_empty_grid()
for r in range(3, 6):
    for c in range(3, 6):
        # Checkerboard pattern
        state_dense[r][c] = HUMAN if (r + c) % 2 == 0 else AI

TEST_SCENARIOS: Dict[str, List[List[int]]] = {
    "Opening State": state_opening,
    "Mid-game State": state_mid,
    "Immediate AI Win": state_ai_win,
    "Human Near-Win (Threat)": state_human_threat,
    "Dense Tactical Board": state_dense
}
