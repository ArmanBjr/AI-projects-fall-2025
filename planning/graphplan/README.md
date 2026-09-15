# GraphPlan

Builds a layered planning graph, computes mutual-exclusion relations, and extracts a plan
from it.

## How it works

1. **Expand** alternating proposition and action levels. Each action level contains every
   action whose preconditions appear in the previous proposition level, plus *no-op*
   actions that carry propositions forward.
2. **Mark mutexes** between pairs that cannot hold together:
   - *Actions* — inconsistent effects, interference, or competing needs
   - *Propositions* — negation, or every supporting action pair being mutex
3. **Extract** a plan by searching backward from the goal propositions, honouring mutexes.
   If extraction fails, expand another level and retry.
4. **Stop** when the graph levels off and extraction still fails — the problem is unsolvable.

## Layout

| Path | Contents |
|------|----------|
| `Model/` | `Entity`, `Predicate`, `State`, `Action`, `GraphAction` (adds no-op support) |
| `PlanningGraph/` | `PlanningGraph.py` builds levels and mutexes; `GraphPlot.py` renders them |
| `Planners/` | `GraphPlanner` plus the forward and backward planners for comparison |
| `Domains/`, `Problems/` | BlockWorld, Cake, Tire and Satellite |
| `results/` | Extracted plans and rendered planning graphs |

## Running

Each demo builds the planning graph for one domain, renders it, then solves it with
GraphPlan and compares against the forward and backward planners:

```bash
python demo_cake.py         # "have cake and eat it too"
python demo_tire.py         # flat-tyre problem
python demo_blockworld.py   # 3-block stacking
```

Rendering the graph needs `networkx` and `matplotlib`.

## Results

`results/` holds the solved plans (`Answer*Problem.txt`) and the rendered planning graphs
for the block-world, cake and tire domains.
