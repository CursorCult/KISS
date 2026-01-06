import json
import os
import subprocess
import sys


def rule_dir() -> str:
    env_dir = os.environ.get("KISS_RULE_DIR")
    if env_dir:
        return env_dir
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_generate(tmpdir: str) -> dict:
    out_path = "complexity.json"
    pattern = os.path.join("src", "**", "*.py")
    script = os.path.join(rule_dir(), "scripts", "generate.py")
    subprocess.run(
        [
            sys.executable,
            script,
            "--glob",
            pattern,
            "--output",
            out_path,
        ],
        check=True,
        cwd=tmpdir,
    )
    with open(os.path.join(tmpdir, out_path), "r", encoding="utf-8") as handle:
        return json.load(handle)


def test_generate_validate_evaluate(repo_fixture) -> None:
    tmpdir = repo_fixture("python", "repo01")
    data = run_generate(str(tmpdir))
    assert data.get("schema") == "complexity"

    files = data.get("files", {})
    assert set(files.keys()) == {os.path.join("src", "simple.py")}
    functions = files[os.path.join("src", "simple.py")].get("functions", [])
    names = {item.get("name") for item in functions}
    assert names == {"simple", "complex"}

    validate = subprocess.run(
        [sys.executable, os.path.join(rule_dir(), "scripts", "validate.py"), "complexity.json"],
        cwd=str(tmpdir),
        capture_output=True,
        text=True,
    )
    assert validate.returncode == 0, validate.stderr

    evaluate = subprocess.run(
        [
            sys.executable,
            os.path.join(rule_dir(), "scripts", "evaluate.py"),
            "--input",
            "complexity.json",
            "--ccn",
            "100",
            "--nloc",
            "1000",
            "--file-nloc",
            "5000",
        ],
        cwd=str(tmpdir),
        capture_output=True,
        text=True,
    )
    assert evaluate.returncode == 0, evaluate.stderr


def test_evaluate_flags_violation(repo_fixture) -> None:
    tmpdir = repo_fixture("python", "repo01")
    run_generate(str(tmpdir))
    evaluate = subprocess.run(
        [
            sys.executable,
            os.path.join(rule_dir(), "scripts", "evaluate.py"),
            "--input",
            "complexity.json",
            "--ccn",
            "0",
            "--nloc",
            "0",
            "--file-nloc",
            "0",
        ],
        cwd=str(tmpdir),
        capture_output=True,
        text=True,
    )
    assert evaluate.returncode == 1
    assert "violations" in evaluate.stderr.lower()
