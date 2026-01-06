from pathlib import Path


def test_rule_has_front_matter() -> None:
    text = Path("RULE.md").read_text(encoding="utf-8")
    stripped = text.lstrip()
    assert stripped.startswith("---")
    assert "description:" in text
    assert "alwaysApply:" in text


def test_rule_mentions_kiss() -> None:
    text = Path("RULE.md").read_text(encoding="utf-8")
    assert "KISS Rule" in text


def test_readme_has_install() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "cursorcult link KISS" in text
