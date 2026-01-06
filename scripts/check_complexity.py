#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path


def _resolve_lizard_cmd() -> str:
    override = os.environ.get("LIZARD_CMD")
    if override:
        return override

    bin_dir = Path(sys.executable).parent
    candidate = bin_dir / "lizard"
    if candidate.exists():
        return str(candidate)
    return "lizard"


def _find_violations(stdout: str) -> bool:
    if "No thresholds exceeded" in stdout:
        return False

    in_section = False
    for line in stdout.splitlines():
        if "!!!! Warnings" in line:
            in_section = True
            continue
        if in_section and "====" in line:
            break
        if in_section and line.strip():
            stripped = line.strip()
            if stripped.startswith("NLOC"):
                continue
            parts = stripped.split()
            if len(parts) >= 4:
                try:
                    int(parts[0])
                    int(parts[1])
                    return True
                except ValueError:
                    pass
    return False


def main() -> int:
    args = sys.argv[1:]
    cmd = [_resolve_lizard_cmd(), "-C", "10", "-L", "100"]
    cmd.extend(args or ["."])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if _find_violations(result.stdout):
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        return 1

    if result.returncode != 0:
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        return result.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
