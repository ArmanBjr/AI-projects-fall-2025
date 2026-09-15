# Fuzzy Logic — Scholarship Eligibility

A Mamdani fuzzy inference system that decides scholarship eligibility from a student's
academic and athletic record.

| | |
|---|---|
| **Input 1** | `GPA`, range 0–20 — *Bad*, *Medium*, *Good*, *Excellent* |
| **Input 2** | `Sport`, range 0–10 — *Ordinary*, *Professional* |
| **Output** | `Scholarship` |
| **Rules** | 8 |
| **Conjunction** | `min` |

Membership functions are a mix of trapezoidal (for the saturating ends of each range) and
triangular (for the interior grades).

## Files

- `scholarship.fis` — starting system
- `scholarship-solution.fis` — completed system with the full rule base

## Running

These are MATLAB/Octave Fuzzy Inference System files, not Python:

```matlab
fis = readfis('scholarship-solution.fis');
evalfis(fis, [17.5 8])     % GPA 17.5, sport score 8
fuzzyLogicDesigner(fis)    % inspect surfaces and rules interactively
```

Requires the MATLAB Fuzzy Logic Toolbox or the Octave `fuzzy-logic-toolkit` package.
