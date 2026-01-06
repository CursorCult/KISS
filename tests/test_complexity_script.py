import os
import subprocess
import sys
from pathlib import Path


def _write_lizard(tmp_path: Path, stdout: str, exit_code: int) -> Path:
    lizard = tmp_path / "lizard"
    lizard.write_text(
        """
#!/usr/bin/env python3
import sys
sys.stdout.write({stdout!r})
sys.exit({exit_code})
""".format(stdout=stdout, exit_code=exit_code).lstrip()
    )
    lizard.chmod(0o755)
    return lizard


def _run_check(env: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "scripts/check_complexity.py"],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
    )


def test_check_complexity_passes_on_no_thresholds(tmp_path: Path) -> None:
    lizard = _write_lizard(tmp_path, "No thresholds exceeded\n", 0)
    env = os.environ.copy()
    env["LIZARD_CMD"] = str(lizard)
    result = _run_check(env)
    assert result.returncode == 0


def test_check_complexity_fails_on_violation(tmp_path: Path) -> None:
    output = (
        "!!!! Warnings (exceeded limits) !!!!\n"
        "  NLOC    CCN   token   function@file\n"
        "  120     11    300     foo@bad.py\n"
        "====================================\n"
    )
    lizard = _write_lizard(tmp_path, output, 0)
    env = os.environ.copy()
    env["LIZARD_CMD"] = str(lizard)
    result = _run_check(env)
    assert result.returncode == 1
    assert "Warnings" in result.stdout
