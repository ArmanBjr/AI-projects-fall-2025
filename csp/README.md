# Constraint Satisfaction Problems

A reusable CSP framework plus two problems built on top of it.

## Framework — `CSP/`

| File | Role |
|------|------|
| `Variable.py` | A variable, its domain, and its current assignment |
| `Constraint.py` | Base class; subclasses implement the satisfaction test |
| `Problem.py` | Holds variables and constraints, defines the goal test |
| `Solver.py` | Backtracking search with heuristics |

The solver combines:

- **MRV** (minimum remaining values) for variable selection
- **LCV** (least constraining value) for value ordering
- **Forward checking** to prune neighbour domains after each assignment,
  with domain save/restore on backtrack

## Problems

**`CourseScheduler/`** — assigns courses to time slots subject to an all-different
constraint over slots plus per-course constraints.

**`States/`** — map colouring: adjacent regions must not share a colour.

## Running

```bash
python main.py
```

`main.py` runs the course scheduler by default. Swap in `StatesProblem` to solve the map
colouring instance instead.

Problem statement and worked solution are in `problem-statement.pdf` and `solution.pdf`.
