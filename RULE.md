---
description: "Keep it simple, stupid (KISS), a rule for minimizing unnecessary complexity"
alwaysApply: true
---

# KISS Rule (Keep It Simple, Stupid)

KISS means choosing the simplest design that solves the real problem. Complexity is a tax: it slows understanding, increases defects, and raises the cost of change.

## Signals

- 🥖 means KISS is satisfied.
- 🥨 means KISS is not satisfied.

## What it enforces

- Keep cyclomatic complexity per function at or below 10 (CCN <= 10).
- Keep function length at or below 100 lines of code (NLOC <= 100).
- Use `lizard` to measure complexity and function length.

## Reference scripts

```sh
python .cursor/rules/KISS/scripts/generate.py --glob "src/**/*.py" --output complexity.json
python .cursor/rules/KISS/scripts/validate.py complexity.json
python .cursor/rules/KISS/scripts/evaluate.py --input complexity.json --ccn 10 --nloc 100 --file-nloc 500
python .cursor/rules/KISS/scripts/check_complexity.py
```

KISS uses the `complexity` schema for its evidence:

```json
{
  "schema": "complexity",
  "files": {
    "src/app.py": {
      "nloc": 120,
      "functions": [
        {
          "name": "run",
          "ccn": 3,
          "nloc": 40,
          "start_line": 10,
          "end_line": 60
        }
      ]
    }
  }
}
```

## Guidelines

- Start with the smallest viable solution. Add complexity only when the simpler version fails.
- Prefer direct, readable code over cleverness or premature optimization.
- Avoid layers, indirection, or abstractions that do not clearly reduce total complexity.
- Keep interfaces minimal. Fewer concepts are easier to test and explain.
- If you cannot explain a design in a short paragraph, it is probably too complex.
