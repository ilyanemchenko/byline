from __future__ import annotations

import pytest

from slopcheck import scan


@pytest.mark.parametrize("flagged,markers,words,templates,score,label", [
    (0, 0, 150, 0, 0, "clean"), (1, 3, 120, 0, 34, "some"), (2, 6, 150, 0, 68, "heavy"),
    (0, 7, 180, 0, 21, "some"), (0, 4, 400, 0, 6, "clean"), (3, 20, 200, 0, 100, "heavy"),
    (0, 0, 150, 1, 15, "clean"), (0, 0, 150, 2, 30, "some"), (0, 2, 150, 3, 51, "heavy"),
    (0, 0, 150, 4, 60, "heavy"),
])
def test_score_and_label(flagged, markers, words, templates, score, label):
    assert scan.score_of(flagged, markers, words, templates) == score and scan.label_of(score) == label


def test_templates_default_to_none():
    assert scan.score_of(1, 3, 120) == 34


def test_one_template_alone_stays_clean():
    assert scan.label_of(scan.score_of(0, 0, 150, 1)) == "clean"
