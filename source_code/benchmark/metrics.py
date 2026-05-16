import csv
import os
from dataclasses import dataclass
from typing import List, Optional
from tabulate import tabulate
from source_code.ai.base_ai import SearchResult


@dataclass
class BenchmarkResult:
    """One row of experiment output for a single algorithm run on a single board state."""
    scenario_name: str
    board_size: int
    depth: int
    algo_name: str
    best_move: str
    score: float
    nodes: int
    time_ms: float
    same_move_as_minimax: Optional[bool] = None   # None when comparing against itself
    reduction_pct: Optional[float] = None          # State reduction vs Minimax (%)


class MetricsReporter:
    """Collects benchmark results and produces a formatted report + CSV export."""

    def __init__(self):
        self.results: List[BenchmarkResult] = []

    def add_result(
        self,
        scenario: str,
        board_size: int,
        depth: int,
        algo: str,
        search_result: SearchResult,
        reference_minimax: Optional[SearchResult] = None,
    ):
        """
        Record one run.

        Args:
            reference_minimax: If provided (and algo != 'Minimax'), compute
                               same_move and reduction_pct relative to this run.
        """
        same_move = None
        reduction = None

        if reference_minimax is not None and algo != "Minimax":
            same_move = (search_result.best_move == reference_minimax.best_move)
            if reference_minimax.nodes_explored > 0:
                reduction = (
                    (reference_minimax.nodes_explored - search_result.nodes_explored)
                    / reference_minimax.nodes_explored
                    * 100.0
                )

        self.results.append(BenchmarkResult(
            scenario_name=scenario,
            board_size=board_size,
            depth=depth,
            algo_name=algo,
            best_move=str(search_result.best_move),
            score=search_result.evaluation_score,
            nodes=search_result.nodes_explored,
            time_ms=search_result.execution_time * 1000.0,
            same_move_as_minimax=same_move,
            reduction_pct=reduction,
        ))

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def report(self):
        """Print the full results table to stdout."""
        headers = [
            "Test Case", "Size", "Depth", "Algorithm",
            "Best Move", "Score", "States", "Runtime(ms)",
            "Same as MM?", "Reduction(%)",
        ]
        table_data = []
        for r in self.results:
            table_data.append([
                r.scenario_name,
                f"{r.board_size}x{r.board_size}",
                r.depth,
                r.algo_name,
                r.best_move,
                f"{r.score:.2f}",
                r.nodes,
                f"{r.time_ms:.2f}",
                ("—" if r.same_move_as_minimax is None
                 else ("Yes" if r.same_move_as_minimax else "No")),
                ("—" if r.reduction_pct is None else f"{r.reduction_pct:.1f}%"),
            ])

        print("\n" + "=" * 80)
        print("EXPERIMENT RESULTS")
        print("=" * 80)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    # ------------------------------------------------------------------
    # CSV Export
    # ------------------------------------------------------------------

    def save_csv(self, path: str):
        """Save results to a CSV file at the given path."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Test Case", "Board Size", "Depth", "Algorithm",
                "Best Move", "Score", "States Evaluated", "Runtime(ms)",
                "Same Move as Minimax?", "State Reduction (%)",
            ])
            for r in self.results:
                writer.writerow([
                    r.scenario_name,
                    f"{r.board_size}x{r.board_size}",
                    r.depth,
                    r.algo_name,
                    r.best_move,
                    f"{r.score:.2f}",
                    r.nodes,
                    f"{r.time_ms:.2f}",
                    ("" if r.same_move_as_minimax is None
                     else ("Yes" if r.same_move_as_minimax else "No")),
                    ("" if r.reduction_pct is None else f"{r.reduction_pct:.1f}"),
                ])
        print(f"\n[Saved] Results written to: {path}")
