---
description: "Keep it simple, stupid (KISS), a rule for minimizing unnecessary complexity"
alwaysApply: true
---

# KISS Rule (Keep It Simple, Stupid)

KISS keeps complexity low by requiring simple, short functions.

Signals:
- 🥖 means KISS is satisfied.
- 🥨 means KISS is not satisfied.

## When it applies

KISS applies to any code source referenced in the `.CCKISS` file, which must exist in a parent directory.

1. When you are writing new code, you should obey KISS.
2. When you find code that does not obey KISS and is referenced in `.CCKISS`, refactor it.

The scripts referenced in `.CCKISS` are used to check the codebase for conformance:
```
cursorcult eval KISS
```

New source directories must be referenced in `.CCKISS` for the rule check to apply.

## Scripts

KISS provides a reference `generate` and `evaluate` script and the canonical `validate` script.

- `scripts/generate.py` - generates `complexity.json` evidence
- `scripts/validate.py complexity.json` - validates proper schema adherence
- `scripts/evaluate.py --input complexity.json` - evaluates rule satisfaction

A standard setup for `.CCKISS` would use this `generate.py` and `evaluate.py`.
The provided `validate.py` is always used.

To call these scripts directly, you will need a supported python version with `lizard` available.

If you use `cursorcult eval KISS` (recommended), then `lizard` is installed with `cursorcult`.

## See Also

See the companion `./README.md` for:

- installing the `.CCKISS` file,
- `complexity.json` schema.
