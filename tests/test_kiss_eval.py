import json
import subprocess
import sys
from pathlib import Path


def _run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def test_generate_validate_evaluate_roundtrip(tmp_path: Path) -> None:
    code = (
        "def add(a, b):\n"
        "    if a > b:\n"
        "        return a - b\n"
        "    return a + b\n"
    )
    src = tmp_path / "sample.py"
    src.write_text(code, encoding="utf-8")

    out = tmp_path / "complexity.json"
    repo = Path(__file__).resolve().parents[1]

    gen = _run(
        [
            sys.executable,
            "scripts/generate.py",
            "--path",
            str(tmp_path),
            "--ext",
            "py",
            "--output",
            str(out),
        ],
        cwd=repo,
    )
    assert gen.returncode == 0, gen.stderr

    validate = _run([sys.executable, "scripts/validate.py", str(out)], cwd=repo)
    assert validate.returncode == 0, validate.stderr

    evaluate = _run(
        [
            sys.executable,
            "scripts/evaluate.py",
            "--input",
            str(out),
            "--ccn",
            "10",
            "--nloc",
            "100",
            "--file-nloc",
            "500",
        ],
        cwd=repo,
    )
    assert evaluate.returncode == 0, evaluate.stderr


def test_evaluate_flags_violation(tmp_path: Path) -> None:
    data = {
        "schema": "complexity",
        "files": {
            "src/a.py": {
                "nloc": 10,
                "functions": [
                    {
                        "name": "f",
                        "ccn": 5,
                        "nloc": 20,
                        "start_line": 1,
                        "end_line": 25,
                    }
                ],
            }
        },
    }
    out = tmp_path / "complexity.json"
    out.write_text(json.dumps(data), encoding="utf-8")

    repo = Path(__file__).resolve().parents[1]
    evaluate = _run(
        [
            sys.executable,
            "scripts/evaluate.py",
            "--input",
            str(out),
            "--ccn",
            "3",
            "--nloc",
            "10",
            "--file-nloc",
            "500",
        ],
        cwd=repo,
    )
    assert evaluate.returncode == 1
    assert "violations" in evaluate.stderr.lower()
