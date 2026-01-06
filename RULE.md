---
description: "Keep it simple, stupid (KISS), a rule for minimizing unnecessary complexity"
alwaysApply: true
---

# KISS Rule (Keep It Simple, Stupid)

Keep complexity low: functions should be simple and short.

Signals:
- 🥖 means KISS is satisfied.
- 🥨 means KISS is not satisfied.

Run the reference scripts if you want to validate a codebase:

```sh
python .cursor/rules/KISS/scripts/generate.py --glob "src/**/*.py" --output complexity.json
python .cursor/rules/KISS/scripts/validate.py complexity.json
python .cursor/rules/KISS/scripts/evaluate.py --input complexity.json --ccn 10 --nloc 100 --file-nloc 500
```
