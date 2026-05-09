import math
import time
from typing import Tuple
from source_code.ai.base_ai import BaseAI, SearchResult
from source_code.ai.evaluation import Evaluator
from source_code.ai.move_ordering import MoveOrderer
from source_code.game.game_state import GameState
from source_code.game.move_generator import MoveGenerator
from source_code.config import DEFAULT_DEPTH_ALPHABETA, AI, HUMAN

class AlphaBetaAI(BaseAI):
    def __init__(self, depth: int = DEFAULT_DEPTH_ALPHABETA):
        self.depth = depth
        self.nodes_explored = 0

    def choose_move(self, game_state: GameState) -> SearchResult:
        self.nodes_explored = 0
        start_time = time.perf_counter()
        
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf
        
        candidates = MoveGenerator.get_candidate_moves(game_state.board)
        candidates = MoveOrderer.order_moves(candidates, game_state.board)
        
        for r, c in candidates:
            game_state.apply_move(r, c)
            score = self._alphabeta(game_state, self.depth - 1, alpha, beta, False)
            game_state.undo_last_move()
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
                
            alpha = max(alpha, best_score)
                
        if not best_move and candidates:
            best_move = candidates[0]
            
        execution_time = time.perf_counter() - start_time
        return SearchResult(
            best_move=best_move,
            evaluation_score=best_score,
            nodes_explored=self.nodes_explored,
            execution_time=execution_time
        )

    def _alphabeta(self, game_state: GameState, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
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
