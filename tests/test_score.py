from __future__ import annotations

import pytest

from slopcheck import scan


@pytest.mark.parametrize("flagged,markers,words,score,label", [
    (0, 0, 150, 0, "clean"), (1, 3, 120, 34, "some"), (2, 6, 150, 68, "heavy"),
    (0, 7, 180, 21, "some"), (0, 4, 400, 6, "clean"), (3, 20, 200, 100, "heavy"),
])
def test_score_and_label(flagged, markers, words, score, label):
    assert scan.score_of(flagged, markers, words) == score and scan.label_of(score) == label
