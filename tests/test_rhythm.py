from __future__ import annotations

import re
from typing import List, Optional, Tuple

import pytest

from slopcheck import rhythm, rules
from slopcheck import text as t


def _prepare(text: str, code: Optional[str]):
    norm = t.normalize(text)
    prose = t.rhythm_text(norm)
    sentences = t.sentence_spans(prose)
    paragraphs = t.paragraph_spans(norm)
    lang = rules.load(code) if code else None
    th = lang.thresholds if lang else rules.Thresholds()
    found, covered = rhythm.triads(prose, sentences, paragraphs, lang, th)
    return prose, sentences, paragraphs, th, found, covered


def spans(text: str, code: Optional[str] = None) -> List[Tuple[int, int]]:
    return _prepare(text, code)[4]


def runs(text: str, code: Optional[str] = "en") -> List[Tuple[int, int]]:
    prose, sentences, paragraphs, th, _found, covered = _prepare(text, code)
    return rhythm.fragment_runs(prose, sentences, [p[0] for p in paragraphs], covered, th)


@pytest.mark.parametrize("text,count", [
    ("Fast — and cheap — now", 2), ("word - word", 1),
    ("— Привет, — сказал он.\n— Да.", 0), ("2019–2021 was fine", 0),
    ("- item one\n- item two", 0), ("self-made, well-known", 0),
])
def test_dashes(text, count):
    assert len(rhythm.dashes(text)) == count


@pytest.mark.parametrize("text,count", [
    ("We made it faster, cheaper, calmer.", 1), ("No fluff, no jargon, no filler.", 1),
    ("Simple. Fast. Done.", 1), ("Yes, I know, thanks.", 0), ("I was, honestly, done.", 0),
    ("It costs 1,200 or 1,500, sometimes 2,000 dollars.", 0),
    ("We met in Paris, talked for an hour about the contract terms, and signed.", 0),
    ("You plan.\n\nYou ship.\n\nYou learn.", 1),
    ("Быстрее, дешевле, спокойнее.", 1), ("Мы, конечно, попробовали.", 0),
])
def test_triads(text, count):
    code = "ru" if re.search("[а-я]", text) else "en"
    assert len(spans(text, code)) == count


def test_triad_without_a_language_still_fires():
    assert len(spans("Simple. Rápido. Hecho.", None)) == 1


def test_fragment_run_needs_three_short_sentences_in_one_paragraph():
    assert len(runs("It broke. Twice. In prod. Badly. Then we fixed the deploy script.")) == 1
    assert runs("It broke. Twice.\n\nIn prod.") == []


def test_bullets_and_a_triad_are_not_a_fragment_run():
    assert runs("- one thing\n- two things\n- three things") == []
    assert runs("Simple. Fast. Done.") == []
