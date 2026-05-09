from dataclasses import dataclass
from typing import List
from tabulate import tabulate
from source_code.ai.base_ai import SearchResult

@dataclass
class BenchmarkResult:
    scenario_name: str
    algo_name: str
    best_move: str
    score: float
    nodes: int
    time_sec: float

class MetricsReporter:
    def __init__(self):
        self.results: List[BenchmarkResult] = []
        
    def add_result(self, scenario: str, algo: str, search_result: SearchResult):
        self.results.append(BenchmarkResult(
            scenario_name=scenario,
            algo_name=algo,
            best_move=str(search_result.best_move),
            score=search_result.evaluation_score,
            nodes=search_result.nodes_explored,
            time_sec=search_result.execution_time
        ))
        
    def report(self):
        headers = ["Scenario", "Algorithm", "Best Move", "Score", "Nodes Explored", "Time (s)"]
        table_data = []
        
        for r in self.results:
            table_data.append([
                r.scenario_name,
                r.algo_name,
                r.best_move,
                f"{r.score:.2f}",
                r.nodes,
                f"{r.time_sec:.4f}"
            ])
            
        print("\n--- Benchmark Results ---")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
