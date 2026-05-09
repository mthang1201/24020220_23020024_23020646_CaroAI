# Caro AI Project

A playable Caro (Gomoku-style) AI game where a human player competes against the computer. The project implements and compares Minimax and Alpha-Beta Pruning algorithms with a heuristic evaluation function.

## Features
- **Algorithms:** Minimax (Depth-limited) and Alpha-Beta Pruning
- **Board Size:** Configurable (default 9x9)
- **Win Condition:** 4 or more consecutive pieces
- **User Interfaces:** Console (Text-based) and PyGame (Graphical GUI)
- **Benchmarking:** Automated side-by-side performance comparison of algorithms

## Installation

1. Ensure you have Python 3.8+ installed.
2. Clone this repository.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Dependencies include `pygame`, `pytest`, and `tabulate`)*

## Running the Game

To start the game with the default settings (Console UI, Alpha-Beta AI on 9x9 board):
```bash
python3 -m source_code.main
```

### Configuration Options
You can configure the game using command-line arguments:

- `--ui`: Choose between `console` (default) and `pygame`
- `--algo`: Choose the AI algorithm, `minimax` or `alphabeta` (default)
- `--depth`: Specify the search depth for the AI (default: 3 for minimax, 4 for alphabeta)
- `--board_size`: Specify the grid size (default: 9)

**Examples:**
Play with PyGame UI using Minimax depth 3:
```bash
python source_code/main.py --ui pygame --algo minimax --depth 3
```

Play on a larger 15x15 board with AlphaBeta depth 4:
```bash
python source_code/main.py --board_size 15 --algo alphabeta --depth 4
```

## Running Benchmarks

The benchmarking system automatically compares Minimax and Alpha-Beta pruning on 5 predefined test scenarios. Both algorithms run on identically cloned board states to ensure fair metrics collection.

Run the benchmark with:
```bash
python source_code/main.py --benchmark
```

## Repository Structure

```
project_root/
├── source_code/
│   ├── ai/
│   │   ├── base_ai.py          # Abstract base AI class
│   │   ├── minimax.py          # Minimax implementation
│   │   ├── alphabeta.py        # Alpha-Beta pruning implementation
│   │   ├── evaluation.py       # Heuristic evaluation function
│   │   └── move_ordering.py    # Heuristic move sorting for Alpha-Beta
│   ├── game/
│   │   ├── board.py            # Board state and mutation logic
│   │   ├── rules.py            # Win/draw checking logic
│   │   ├── game_state.py       # Manages full state, turns, history
│   │   └── move_generator.py   # Valid move generation with pruning
│   ├── ui/
│   │   ├── console_ui.py       # Text-based interface
│   │   └── pygame_ui.py        # Graphical interface
│   ├── benchmark/
│   │   ├── benchmark_runner.py # Benchmark script
│   │   ├── test_states.py      # Predefined test boards
│   │   └── metrics.py          # Result recording and table output
│   ├── utils/
│   │   └── timer.py            # Execution timer helper
│   ├── config.py               # Centralized configuration and constants
│   └── main.py                 # Core entry point
├── requirements.txt            # Dependencies
└── README.md                   # This file
```