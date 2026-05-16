from typing import List, Tuple
from source_code.game.board import Board
from source_code.config import AI, HUMAN, EMPTY

class MoveOrderer:
    # Cache cho bảng điểm tĩnh để tránh tính toán lại nhiều lần
    _static_score_table = None

    @staticmethod
    def _get_static_table(size: int):
        if MoveOrderer._static_score_table is None or len(MoveOrderer._static_score_table) != size:
            center = size // 2
            table = []
            for r in range(size):
                row = []
                for c in range(size):
                    # Điểm cao nhất ở tâm, giảm dần ra xa
                    dist = abs(r - center) + abs(c - center)
                    row.append(max(0, size - dist))
                table.append(row)
            MoveOrderer._static_score_table = table
        return MoveOrderer._static_score_table

    @staticmethod
    def order_moves(moves: List[Tuple[int, int]], board: Board) -> List[Tuple[int, int]]:
        """
        Sort candidate moves to improve Alpha-Beta pruning efficiency.
        Combined Static Proximity and Dynamic Tactical Scoring.
        """
        static_table = MoveOrderer._get_static_table(board.size)
        
        def move_score(move: Tuple[int, int]) -> float:
            r, c = move
            # 1. Điểm tĩnh (vị trí chiến lược)
            score = static_table[r][c]
            
            # 2. Điểm động (mức độ "nóng" của ô cờ)
            # Chúng ta sử dụng neighbor_counts đã có sẵn trong board để tăng tốc
            score += board.neighbor_counts[r][c] * 10
            
            # 3. Tactical Check nhanh (Các hướng)
            # Ưu tiên các nước cờ nối liền hoặc chặn đầu
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                # Kiểm tra 1 ô lân cận theo mỗi hướng
                nr1, nc1 = r + dr, c + dc
                nr2, nc2 = r - dr, c - dc
                
                p1 = board.grid[nr1][nc1] if board.is_valid_pos(nr1, nc1) else None
                p2 = board.grid[nr2][nc2] if board.is_valid_pos(nr2, nc2) else None
                
                if p1 == p2 and p1 is not None and p1 != EMPTY:
                    score += 50  # Nước đi chen giữa 2 quân cờ (cực kỳ quan trọng)
                elif (p1 is not None and p1 != EMPTY) or (p2 is not None and p2 != EMPTY):
                    score += 15  # Nước đi nối tiếp quân cờ có sẵn
            return score

        return sorted(moves, key=move_score, reverse=True)