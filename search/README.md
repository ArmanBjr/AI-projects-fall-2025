# Search

Four projects covering the classical search curriculum, from blind traversal through
game-tree pruning.

## `uninformed/`

Search strategies that expand the frontier without any domain knowledge, applied to a
block-world puzzle read from `tests/*.txt`.

- Breadth-first search
- Depth-first search (frontier-based and explored-set variants)
- Depth-limited search
- Iterative deepening search
- Uniform-cost search

```bash
cd uninformed && python main.py
```

Select a test case by changing `test_case_number` in `main.py`, and the strategy by calling
a different `Search.*` method.

## `informed/`

The same block-world domain, solved with heuristics and local search.

| Method | Notes |
|--------|-------|
| Greedy best-first | Expands on `h(n)` alone |
| A\* | `f(n) = g(n) + h(n)` |
| IDA\* | Iterative-deepening A\*, bounded by an `f`-threshold |
| RBFS | Recursive best-first, linear space |
| Hill climbing | Steepest-ascent |
| Random restart | Escapes local optima by restarting |
| Stochastic hill climbing | Picks randomly among improving neighbours |

```bash
cd informed && python main.py
```

## `adversarial/`

Othello (Reversi) on an 8×8 board, played AI-versus-AI.

- Minimax with alpha–beta pruning, default search depth 5
- Turn passing when a player has no legal move
- Terminal detection on a full board or when neither side can move
- Utility based on disc differential

```bash
cd adversarial && python main.py
```

## `visualizations/`

Standalone, dependency-free reference implementations kept separate from the graded
projects:

- `graph_search_basics.py` — minimal path-returning BFS and DFS
- `graph_search_strategies.py` — one `graph_search()` entry point switchable between
  `bfs`, `dfs`, `ucs` and `astar`
