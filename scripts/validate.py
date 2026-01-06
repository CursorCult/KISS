#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any, Dict


def _fail(msg: str) -> int:
    sys.stderr.write(f"INVALID: {msg}\n")
    return 1


def _require_int(value: Any, field: str) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate(data: Dict[str, Any]) -> int:
    if data.get("schema") != "complexity":
        return _fail("schema must be 'complexity'")
    files = data.get("files")
    if not isinstance(files, dict):
        return _fail("files must be an object")

    for path, payload in files.items():
        if not isinstance(path, str):
            return _fail("file keys must be strings")
        if not isinstance(payload, dict):
            return _fail(f"file entry for {path} must be an object")
        if not _require_int(payload.get("nloc"), "nloc"):
            return _fail(f"file nloc for {path} must be an int")
        funcs = payload.get("functions")
        if not isinstance(funcs, list):
            return _fail(f"functions for {path} must be a list")
        for fn in funcs:
            if not isinstance(fn, dict):
                return _fail(f"function entry for {path} must be an object")
            if not isinstance(fn.get("name"), str):
                return _fail(f"function name for {path} must be a string")
            for key in ("ccn", "nloc", "start_line", "end_line"):
                if not _require_int(fn.get(key), key):
                    return _fail(f"{key} for {path}:{fn.get('name')} must be an int")

    return 0


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: validate.py <input.json>\n")
        return 1
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return _fail(f"failed to parse JSON: {exc}")
    return validate(data)


if __name__ == "__main__":
    raise SystemExit(main())
