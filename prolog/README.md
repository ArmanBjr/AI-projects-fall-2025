# Prolog

Logic programming exercises — knowledge representation, recursion over lists, and search
expressed declaratively.

A recurring theme is reimplementing the standard library: most files define their own
`member/2`, `append/3` and `reverse/2` rather than leaning on the built-ins, so the
recursion stays explicit.

| File | Topic |
|------|-------|
| `list-predicates.pl` | A small standard library from scratch — `append`, `member`, `reverse`, `flatten`, `length`, `sum_list`, `max_list`, `list_to_set`, `all_diff`, `factorial` (comments in Persian) |
| `graph-path.pl` | Weighted path finding with cycle avoidance, using built-in `member/2` and `reverse/2` |
| `graph-path-no-builtins.pl` | The same task with every list utility hand-rolled |
| `logic-puzzle.pl` | Five-person constraint puzzle — generate-and-test over names, distances and colours |
| `course-recommender.pl` | Recommends courses from recorded selections, grades and teaching assistants |
| `course-recommender-v2.pl` | Revised version of the above |
| `task-dependency-graph.py` | Renders a 15-task dependency (PERT/CPM) graph with NetworkX |

## `graph-algorithms/`

Dijkstra's shortest path in pure Prolog — hand-rolled list utilities, manual neighbour
enumeration without `findall/3`, and iterative relaxation of the frontier. Problem statement
in `problem-statement.pdf`.

## `resolution/`

Resolution and unification exercises. `list-operations.pl` implements `union/3` over lists
via a hand-written `member/2`; `resolution-exercises.pdf` holds the accompanying problems.

## Running

Any standard Prolog system works — [SWI-Prolog](https://www.swi-prolog.org/) is recommended:

```bash
swipl
?- ['graph-path.pl'].
?- findPath([edge(a,b,3), edge(b,c,4)], a, c, Path, Length).
Path = [a, b, c],
Length = 7.
```

Or load a file directly:

```bash
swipl -s logic-puzzle.pl
```
