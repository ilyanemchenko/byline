"""Lint for every skill in ``skills/``: frontmatter, size and the fixed sentences the skills share."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict

import pytest

ROOT = Path(__file__).resolve().parents[1]

ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
EXPECTED = ["angle-brainstorm", "new-post", "person-interview", "post-editor",
            "post-fact-check", "post-writer", "slop-check", "topic-scout"]
READS_PERSON_FILE = ["angle-brainstorm", "new-post", "post-editor", "post-fact-check", "post-writer", "topic-scout"]
NO_INVENTION = ["post-editor", "post-fact-check", "post-writer"]
SKILLS = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))


def body(name: str) -> str:
    return (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def front(name: str) -> Dict[str, str]:
    """The ``key: value`` lines between the first two ``---`` lines of a SKILL.md."""
    lines = body(name).splitlines()
    assert lines and lines[0].strip() == "---", f"{name}: SKILL.md must open with a --- line"
    meta: Dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        key, sep, value = line.partition(":")
        assert sep and key.strip() and not key.startswith((" ", "\t")), f"{name}: not a 'key: value' line: {line!r}"
        assert key.strip() not in meta, f"{name}: key {key.strip()!r} appears twice"
        meta[key.strip()] = value.strip()
    raise AssertionError(f"{name}: the frontmatter has no closing --- line")


def test_only_expected_skills():
    assert set(SKILLS) <= set(EXPECTED)  # Task 13 turns this into SKILLS == EXPECTED


@pytest.mark.parametrize("name", SKILLS)
def test_frontmatter_and_size(name):
    meta = front(name)
    assert set(meta) <= ALLOWED and meta["name"] == name
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and len(name) <= 64
    assert meta["description"].startswith("Use when") and len(meta["description"]) <= 1024
    assert "<" not in meta["description"]
    assert len(body(name).splitlines()) < 400


def test_slop_check_names_the_script_both_ways_and_claims_no_authorship():
    text = body("slop-check")
    assert "${CLAUDE_SKILL_DIR}/scripts/check.py" in text and "relative to this skill's folder" in text
    assert "does not say who wrote the text" in text


@pytest.mark.parametrize("name", [n for n in READS_PERSON_FILE if n in SKILLS])
def test_reader_skills_handle_a_missing_person_file(name):
    assert "byline/person.md" in body(name) and "If `byline/person.md` does not exist" in body(name)


@pytest.mark.parametrize("name", [n for n in NO_INVENTION if n in SKILLS])
def test_no_invention_rule_is_verbatim(name):
    assert "Never invent a number, client, result, event or title." in body(name)


def test_channel_copies_are_identical():
    a, b = ROOT / "skills/post-writer/channels.md", ROOT / "skills/post-editor/channels.md"
    if a.exists() and b.exists():
        assert a.read_bytes() == b.read_bytes()
