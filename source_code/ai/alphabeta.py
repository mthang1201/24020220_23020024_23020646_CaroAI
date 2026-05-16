import math
import time
from typing import Tuple
from source_code.ai.base_ai import BaseAI, SearchResult, TimeOutException
from source_code.ai.evaluation import Evaluator
from source_code.ai.move_ordering import MoveOrderer
from source_code.game.game_state import GameState
from source_code.game.move_generator import MoveGenerator
from source_code.config import DEFAULT_DEPTH_ALPHABETA, AI, HUMAN, DEFAULT_TIME_LIMIT

class AlphaBetaAI(BaseAI):
    def __init__(self, depth: int = DEFAULT_DEPTH_ALPHABETA, time_limit: float = DEFAULT_TIME_LIMIT):
        self.depth = depth
        self.time_limit = time_limit
        self.nodes_explored = 0
        self.start_time = 0.0

    def choose_move(self, game_state: GameState) -> SearchResult:
        self.nodes_explored = 0
        self.start_time = time.perf_counter()
        
        # Sử dụng clone để không làm hỏng state gốc khi bị văng Exception (TimeOut)
        working_state = game_state.clone()
        
        candidates = MoveGenerator.get_candidate_moves(working_state.board)
        candidates = MoveOrderer.order_moves(candidates, working_state.board)
        
        if not candidates:
            return SearchResult(
                best_move=None,
                evaluation_score=0.0,
                nodes_explored=self.nodes_explored,
                execution_time=time.perf_counter() - self.start_time
            )

        best_overall_move = candidates[0]
        best_overall_score = -math.inf
        
        try:
            for current_depth in range(1, self.depth + 1):
                best_score = -math.inf
                best_move = None
                alpha = -math.inf
                beta = math.inf
                
                for r, c in candidates:
                    working_state.apply_move(r, c)
                    score = self._alphabeta(working_state, current_depth - 1, alpha, beta, False)
                    working_state.undo_last_move()
                    
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
                        
                    alpha = max(alpha, best_score)
                
                best_overall_score = best_score
                if best_move:
                    best_overall_move = best_move
                    
                if best_overall_score == math.inf:
                    break
                    
        except TimeOutException:
            pass # Timeout reached, use best move from last completed depth
            
        execution_time = time.perf_counter() - self.start_time
        return SearchResult(
            best_move=best_overall_move,
            evaluation_score=best_overall_score,
            nodes_explored=self.nodes_explored,
            execution_time=execution_time
        )

    def _alphabeta(self, game_state: GameState, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
        if self.time_limit > 0 and time.perf_counter() - self.start_time > self.time_limit:
            raise TimeOutException()
            
        self.nodes_explored += 1
        
        if game_state.is_terminal:
            if game_state.winner == AI:
                return math.inf
            elif game_state.winner == HUMAN:
                return -math.inf
            else:
                return 0.0 # Draw
                
        if depth == 0:
            return Evaluator.evaluate(game_state.board)
            
        candidates = MoveGenerator.get_candidate_moves(game_state.board)
        candidates = MoveOrderer.order_moves(candidates, game_state.board)
        
        if is_maximizing:
            best_score = -math.inf
            for r, c in candidates:
                game_state.apply_move(r, c)
                score = self._alphabeta(game_state, depth - 1, alpha, beta, False)
                game_state.undo_last_move()
                
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break # Beta cut-off
            return best_score
        else:
            best_score = math.inf
            for r, c in candidates:
                game_state.apply_move(r, c)
                score = self._alphabeta(game_state, depth - 1, alpha, beta, True)
                game_state.undo_last_move()
                
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break # Alpha cut-off
            return best_score
