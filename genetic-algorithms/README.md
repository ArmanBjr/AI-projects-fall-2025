# Genetic Algorithms — Sudoku Solver

Solves Sudoku puzzles with a genetic algorithm built on [PyGAD](https://pygad.readthedocs.io),
using custom operators rather than the library defaults.

## Approach

Only the **empty cells** are encoded as genes, so the fixed clues are never disturbed and
the search space shrinks to the unknowns.

| Component | Implementation |
|-----------|----------------|
| Initial population | Random fills that respect each row's missing-digit multiset |
| Crossover | Custom uniform crossover — each gene taken from either parent at random |
| Mutation | Custom operator that swaps or resamples genes within a unit |
| Fitness | Counts constraint violations across rows, columns and 3×3 boxes |

Fitness peaks when no row, column or box repeats a digit.

## Running

```bash
pip install pygad numpy
python Sudoku.py
```

Population size, generation count and mating pool are arguments to `solve()`.

## Files

- `Sudoku.py` — solver
- `sample-output.txt` — example run
- `report.tex` / `report.pdf` — write-up of the approach and results
- `sudoku1.pdf`, `sudoku2.pdf` — problem statements
