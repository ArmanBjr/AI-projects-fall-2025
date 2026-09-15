# Automated Planning

STRIPS-style planning in two stages: first state-space search, then planning-graph search.

- [`classical/`](classical) — forward (progression) and backward (regression) planners
- [`graphplan/`](graphplan) — planning graph construction, mutex reasoning, GraphPlan

Both share the same modelling vocabulary:

| Concept | Meaning |
|---------|---------|
| `Entity` | An object in the world (a block, a tool, a satellite) |
| `Predicate` | A relation over entities, e.g. `on(a, b)` |
| `State` | A set of predicates held true |
| `Action` | Preconditions plus add/delete effects |
| `Domain` | The action schemas available |
| `Problem` | A domain together with an initial state and a goal |

Adding a new domain means subclassing `Domain` with your action schemas and `Problem` with
an initial state and goal — the planners themselves stay untouched.
