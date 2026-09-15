# Classical Planning

State-space planners searching forward from the initial state or backward from the goal.

## Planners

| Planner | Direction | Idea |
|---------|-----------|------|
| `ForwardPlanner` | Progression | From the initial state, apply any action whose preconditions hold, until the goal is satisfied |
| `BackwardPlanner` | Regression | From the goal, pick actions that achieve an open subgoal and regress it into new subgoals |
| `GraphPlanPlanner` | — | Planning-graph variant; see [`../graphplan/`](../graphplan) for the fuller treatment |

## Domains

- `BlockWorld` — stacking and unstacking blocks
- `TireDomain` — the classic flat-tyre problem
- `LabRobotsDomain` — robots moving between rooms and carrying items

## Running

```bash
python demo.py
```

`demo.py` runs the tyre problem. Swap the domain/problem pair and the planner class at the
bottom of the file to plan elsewhere — the commented blocks show the block-world and
lab-robots variants.
