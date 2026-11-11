"""The reference set and the release bar for a "measured" language (see reference/README.md)."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from slopcheck import rules, scan

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "reference/manifest.json").read_text(encoding="utf-8"))
HUMANS = [r for r in MANIFEST if r["class"] == "human"]


def rows(cls, split):
    return [r for r in MANIFEST if r["class"] == cls and r["split"] == split]


def label(row):
    return scan.scan((ROOT / "reference" / row["file"]).read_text(encoding="utf-8"), language="en").label


def holdout_or_skip():
    if not rows("human", "holdout") and not rows("machine", "holdout"):
        pytest.skip("holdout not added yet")


def test_manifest_is_complete():
    assert all(len(rows(c, "tune")) >= 10 for c in ("human", "machine"))
    assert all(r["split"] in ("tune", "holdout") for r in MANIFEST)
    assert all((ROOT / "reference" / r["file"]).is_file() for r in MANIFEST)
    assert all(r["published"] < "2022-11-01" and r["licence"] and r["licence_url"] and r["url"] for r in HUMANS)
    assert all(120 <= r["words"] <= 450 for r in HUMANS)
    authors = Counter(r["author"] for r in HUMANS)
    assert len(authors) >= 3 and max(authors.values()) <= 0.4 * len(HUMANS)
    assert all(r["model"] and r["prompt"].startswith("Write a LinkedIn post in English about ")
               for r in MANIFEST if r["class"] == "machine")


def test_holdout_is_complete():
    holdout_or_skip()
    assert all(len(rows(c, "holdout")) == 10 for c in ("human", "machine"))
    assert len({r["author"] for r in rows("human", "holdout")}) >= 3


def test_holdout_meets_the_release_bar():
    holdout_or_skip()
    human = Counter(label(r) for r in rows("human", "holdout"))
    machine = Counter(label(r) for r in rows("machine", "holdout"))
    assert human["heavy"] == 0
    assert human["some"] <= 2
    assert machine["some"] + machine["heavy"] >= 7


def test_a_measured_language_has_a_reference_set():
    for code in rules.available():
        if rules.load(code).status == "measured":
            assert (ROOT / "reference" / code / "human").is_dir()
