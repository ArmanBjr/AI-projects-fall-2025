# Artificial Intelligence — Course Code

Archive of coursework and projects from the **Artificial Intelligence** course at Ferdowsi University of Mashhad (5th semester). Organized by session/topic.

## Topics covered

| Session | Topic | Highlights |
|---------|-------|------------|
| `AI-graphicSearch/` | Uninformed & informed search | BFS, DFS, A*, block-world problem |
| `view/` | Search visualizations | Interactive search demos |
| `Session3/` | Search project variant | Graph search implementation |
| `session4/` | Genetic algorithms | Sudoku solver + write-up |
| `session5/` | Constraint satisfaction (CSP) | Course scheduling, map coloring |
| `session6/` | Adversarial search | Minimax board game |
| `SESSION7/` | Adversarial search (variant) | Extended minimax project |
| `Session8/` | Fuzzy logic | Scholarship eligibility (`.fis`) |
| `session9/` | Classical planning | Forward / backward planners |
| `session10/` | GraphPlan | Planning graph, STRIPS-style domains |
| `session11/` | Supervised learning I | Decision trees, linear regression |
| `session12/` | Supervised learning II | MLP on Fashion MNIST |
| `session13/` | MDPs | Value iteration, Tetris environment |
| `session14/` | Reinforcement learning | Q-learning on MiniGrid |
| `Prolog/` | Logic programming | Prolog exercises |

## Requirements

Python 3.10+ recommended. Dependencies vary by session — common packages:

```bash
pip install numpy pandas matplotlib jupyter ta gymnasium minigrid
```

Individual sessions may include their own `requirements.txt` (e.g. session14 Q-learning project).

## Running examples

**Search (block world):**

```bash
cd AI-graphicSearch
python main.py
```

**CSP course scheduler:**

```bash
cd session5/csp
python main.py
```

**Q-learning:**

```bash
cd session14/Q-learning Project
pip install -r requirements.txt
python main.py
```

**Jupyter notebooks** (session11–12): open `.ipynb` files in Jupyter Lab or VS Code.

## Repository layout

```
AI-graphicSearch/     # Session 2 — search algorithms
view/                 # Search demo scripts
Session3/ … session14/
Prolog/               # Prolog exercises
```

Local reference materials (`Expect/`, `expected/`, `strawberry/`) are kept on disk but not published in this repo.

## Author

**Arman Bijari** — [GitHub](https://github.com/ArmanBjr)

**Reza Farasati** _ [GitHub](https://github.com/Rfarasati)
## License

Educational archive — provided for portfolio reference. Course materials © Ferdowsi University of Mashhad.
