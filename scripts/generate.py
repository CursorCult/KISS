#!/usr/bin/env python3
import argparse
import glob
import json
import sys
from pathlib import Path
from typing import Iterable, List


def _expand_paths(globs: Iterable[str], paths: Iterable[str]) -> List[Path]:
    files: List[Path] = []
    for pattern in globs:
        matches = glob.glob(pattern, recursive=True)
        files.extend(Path(m) for m in matches)
    for path in paths:
        p = Path(path)
        if p.is_dir():
            files.extend(f for f in p.rglob("*") if f.is_file())
        elif p.exists():
            files.append(p)
    return files


def _relpath(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except Exception:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate KISS complexity evidence using lizard")
    parser.add_argument("--glob", action="append", default=[], help="Glob pattern to include")
    parser.add_argument("--path", action="append", default=[], help="Path to file or directory")
    parser.add_argument("--ext", action="append", default=[], help="Limit to file extensions")
    parser.add_argument("--output", required=True, help="Output JSON file")
    args = parser.parse_args()

    if not args.glob and not args.path:
        parser.error("Provide at least one --glob or --path")

    try:
        import lizard
    except Exception as exc:
        sys.stderr.write(f"ERROR: lizard is required: {exc}\n")
        return 1

    files = _expand_paths(args.glob, args.path)
    if args.ext:
        allowed = {e.lstrip(".") for e in args.ext}
        files = [f for f in files if f.suffix.lstrip(".") in allowed]

    if not files:
        sys.stderr.write("ERROR: no files matched input patterns\n")
        return 1

    infos = lizard.analyze_files([str(f) for f in files], exts=args.ext or None)

    data = {"schema": "complexity", "files": {}}
    for info in infos:
        rel = _relpath(Path(info.filename))
        data["files"][rel] = {
            "nloc": int(info.nloc),
            "functions": [
                {
                    "name": fn.name,
                    "ccn": int(fn.cyclomatic_complexity),
                    "nloc": int(fn.nloc),
                    "start_line": int(fn.start_line),
                    "end_line": int(fn.end_line),
                }
                for fn in info.function_list
            ],
        }

    out_path = Path(args.output)
    out_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
