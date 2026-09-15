# AI Projects — Fall 2025

Worked implementations of classical Artificial Intelligence algorithms, built for the
**Artificial Intelligence** course at Ferdowsi University of Mashhad (Fall 2025).

Every algorithm here is implemented from scratch — no `scikit-learn` estimators standing in
for the search, planning, or learning logic. The neural network is plain NumPy, the planners
are hand-rolled STRIPS, and the RL agents implement their own update rules.

## Contents

| Area | What's inside |
|------|---------------|
| [`search/`](search) | Uninformed, informed, adversarial and visualised search |
| [`csp/`](csp) | Constraint-satisfaction solver + course scheduler and map colouring |
| [`genetic-algorithms/`](genetic-algorithms) | Sudoku solver using a genetic algorithm |
| [`fuzzy-logic/`](fuzzy-logic) | Fuzzy inference system for scholarship eligibility |
| [`planning/`](planning) | Forward/backward STRIPS planners and GraphPlan |
| [`supervised-learning/`](supervised-learning) | Decision trees, linear regression, NumPy MLP |
| [`reinforcement-learning/`](reinforcement-learning) | Value iteration (MDP) and Q-learning |
| [`prolog/`](prolog) | Logic programming: unification, resolution, graph search |

## Highlights

- **A\*, IDA\* and RBFS** on a block-world puzzle, plus hill-climbing variants with random
  restarts and stochastic selection — [`search/informed/`](search/informed)
- **Othello with minimax + alpha–beta pruning** at depth 5 on an 8×8 board —
  [`search/adversarial/`](search/adversarial)
- **GraphPlan** with mutex computation and rendered planning graphs across four STRIPS
  domains — [`planning/graphplan/`](planning/graphplan)
- **Multi-layer perceptron written in NumPy** (manual forward/backward passes) trained on
  Fashion-MNIST — [`supervised-learning/neural-networks/`](supervised-learning/neural-networks)
- **Q-learning on MiniGrid DoorKey** with ε-greedy exploration and a saved policy —
  [`reinforcement-learning/q-learning/`](reinforcement-learning/q-learning)

## Getting started

Python 3.10 or newer.

```bash
git clone https://github.com/ArmanBjr/AI-projects-fall-2025.git
cd AI-projects-fall-2025

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Each project is self-contained and run from its own directory:

```bash
# Informed search on the block-world puzzle
cd search/informed && python main.py

# Othello with alpha-beta pruning
cd search/adversarial && python main.py

# Course-scheduling CSP
cd csp && python main.py

# Q-learning on MiniGrid
cd reinforcement-learning/q-learning && python main.py
```

Notebooks under `supervised-learning/` open directly in Jupyter or VS Code.

The fuzzy-logic system (`fuzzy-logic/*.fis`) is a MATLAB/Octave Fuzzy Inference System and
needs the MATLAB Fuzzy Logic Toolbox rather than Python.

## Repository layout

```
search/
  uninformed/      BFS, DFS, depth-limited, IDS, uniform-cost
  informed/        Greedy best-first, A*, IDA*, RBFS, hill-climbing
  adversarial/     Othello — minimax with alpha-beta pruning
  visualizations/  Standalone reference implementations of graph search
csp/               Constraint framework, course scheduler, map colouring
genetic-algorithms/  Sudoku via genetic algorithm (+ LaTeX report)
fuzzy-logic/       Scholarship eligibility inference system
planning/
  classical/       Forward and backward STRIPS planners
  graphplan/       Planning graph, mutex reasoning, rendered graphs
supervised-learning/
  decision-trees/     Adult census income classification
  linear-regression/  Fuel-efficiency regression on the mpg dataset
  neural-networks/    NumPy MLP on Fashion-MNIST
reinforcement-learning/
  mdp/             Value iteration on a mini-Tetris environment
  q-learning/      Q-learning agent on MiniGrid DoorKey
prolog/            Logic programming exercises
```

## Authors

- **Arman Bijari** — [@ArmanBjr](https://github.com/ArmanBjr)
- **Reza Farasati** — [@Rfarasati](https://github.com/Rfarasati)

## License

Source code is released under the [MIT License](LICENSE).

Course handouts, problem statements and reference PDFs included for context remain the
property of Ferdowsi University of Mashhad and are provided for educational reference only.
