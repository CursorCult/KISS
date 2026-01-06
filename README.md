# Part of the [CursorCult](https://github.com/CursorCult)

# KISS

KISS: **Keep It Simple, Stupid**.

**Install**

```sh
pipx install cursorcult
cursorcult link KISS
```

Rule file format reference: https://cursor.com/docs/context/rules#rulemd-file-format

**Programmatic evaluation (.CCKISS)**

Create a `.CCKISS` at repo root with full command lines. Generators must include
`--output`, and the evaluator must include `--input`. All generators must write
to the same output file (typically `complexity.json`).

Example:

```text
python .cursor/rules/KISS/scripts/generate.py --glob "src/**/*.py" --output complexity.json
python .cursor/rules/KISS/scripts/evaluate.py --input complexity.json --ccn 10 --nloc 100 --file-nloc 500
```

The output schema is `complexity`:

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

**When to use**

- You are tempted to add a framework, pattern, or layer to solve a small problem.
- The simplest solution already works but feels too plain.
- The team is spending more time explaining the system than using it.

**What it enforces**

- Prefer the simplest solution that solves the problem well.
- Avoid abstraction until it earns its keep.
- Reduce moving parts, not just lines of code.
- Optimize for clarity and maintenance over cleverness.
- Keep cyclomatic complexity per function at or below 10 (CCN <= 10).
- Keep function length at or below 100 lines of code (NLOC <= 100).

**Signals**

- 🥖 means KISS is satisfied.
- 🥨 means KISS is not satisfied.

**Reference scripts**

```sh
python .cursor/rules/KISS/scripts/generate.py --glob "src/**/*.py" --output complexity.json
python .cursor/rules/KISS/scripts/validate.py complexity.json
python .cursor/rules/KISS/scripts/evaluate.py --input complexity.json --ccn 10 --nloc 100 --file-nloc 500
```

**Credits**

- Developed by Will Wieselquist. Anyone can use it.

**Origins**

- The KISS principle has roots in engineering practice and is commonly attributed to Kelly Johnson at Lockheed Skunk Works.
