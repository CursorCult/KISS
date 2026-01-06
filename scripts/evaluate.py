#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _failures(
    data: Dict[str, Any],
    max_ccn: int,
    max_nloc: int,
    max_file_nloc: int,
) -> List[str]:
    failures: List[str] = []
    for file_path, payload in data.get("files", {}).items():
        file_nloc = payload.get("nloc")
        if isinstance(file_nloc, int) and file_nloc > max_file_nloc:
            failures.append(
                f"{file_path}: file NLOC {file_nloc} exceeds {max_file_nloc}"
            )
        for fn in payload.get("functions", []):
            name = fn.get("name", "<unknown>")
            ccn = fn.get("ccn")
            nloc = fn.get("nloc")
            if isinstance(ccn, int) and ccn > max_ccn:
                failures.append(
                    f"{file_path}:{name}: CCN {ccn} exceeds {max_ccn}"
                )
            if isinstance(nloc, int) and nloc > max_nloc:
                failures.append(
                    f"{file_path}:{name}: NLOC {nloc} exceeds {max_nloc}"
                )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate KISS complexity evidence")
    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--ccn", type=int, default=10, help="Max CCN per function")
    parser.add_argument("--nloc", type=int, default=100, help="Max NLOC per function")
    parser.add_argument(
        "--file-nloc", type=int, default=500, help="Max NLOC per file"
    )
    args = parser.parse_args()

    data = _load(Path(args.input))
    if data.get("schema") != "complexity":
        sys.stderr.write("INVALID: schema must be 'complexity'\n")
        return 1

    failures = _failures(data, args.ccn, args.nloc, args.file_nloc)
    if failures:
        sys.stderr.write("KISS violations found:\n")
        for failure in failures:
            sys.stderr.write(f"- {failure}\n")
        return 1

    sys.stdout.write("KISS OK: complexity thresholds satisfied\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
