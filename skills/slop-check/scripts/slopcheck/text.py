"""Text primitives for the slop check.

Everything here keeps character offsets stable. ``normalize`` maps every input
character to exactly one output character, and ``blank`` replaces markup with
spaces of the same length instead of removing it, so a span found on the
normalised or prose-only text indexes the original text.
"""

from __future__ import annotations

import re
import unicodedata
from bisect import bisect_right
from typing import Dict, Iterable, List, Pattern, Tuple

WORD = re.compile(r"[^\W_]+(?:['’-][^\W_]+)*")
URL = re.compile(r"(?:https?://|www\.)[^\s<>\"'«»]+", re.IGNORECASE)
HASHTAG = re.compile(r"(?<![\w#&/])#[^\W\d_]\w*")
LETTER = re.compile(r"[^\W\d_]")

_CHAR_MAP: Dict[str, str] = {
    # typographic double quotes and guillemets -> "
    "“": '"', "”": '"', "„": '"', "‟": '"', "«": '"', "»": '"',
    "″": '"',
    # typographic single quotes, backtick, acute accent -> '
    "‘": "'", "’": "'", "‚": "'", "‛": "'", "´": "'", "`": "'",
    # no-break and thin spaces -> space; non-breaking hyphen -> -
    " ": " ", " ": " ", " ": " ", " ": " ", "‑": "-",
    "ё": "е",  # yo -> ye
}

_BLANK_LINE = re.compile(r"\n[ \t]*\n(?:[ \t]*\n)*")
_SENTENCE_BREAK = re.compile(r"\n+|[.!?…]+[\"')\]]*[ \t]+")
_CLAUSE_BREAK = re.compile(r"[,;:(—–]|\s-\s")
_DOUBLE_QUOTED = re.compile(r"\"[^\"\n]{1,300}\"")
# An apostrophe between two letters ("let's") is part of a word, not a quote end.
_SINGLE_QUOTED = re.compile(r"(?<!\w)'(?:[^'\n]|(?<=\w)'(?=\w)){1,200}'(?!\w)")
_BLOCKQUOTE = re.compile(r"^[ \t]*>[^\n]*", re.MULTILINE)
_NEGATION_TOKEN = re.compile(r"[\w']+")
# Lines that are structure, not prose: headings, quotes, numbered items, and any line that opens on a
# symbol or emoji (markdown bullets, check-mark lists, dash bullets and dialogue). A line that opens on a
# letter, a digit, a quote, a bracket or an inverted Spanish mark is prose.
_STRUCTURE_LINE = re.compile(r"^[ \t]*(?:#+[ \t]|>|\d+[.)][ \t]|[^\w\s\"'«“‘(¿¡$€£%&@+=~.…]).*$", re.MULTILINE)
_INLINE_MARKUP = re.compile(r"\*\*|__|[`*]")


def _fold(ch: str) -> str:
    mapped = _CHAR_MAP.get(ch)
    if mapped is not None:
        return mapped
    low = ch.lower()
    if len(low) != 1:
        low = ch
    mapped = _CHAR_MAP.get(low)
    if mapped is not None:
        return mapped
    if not low.isascii() and low.isalpha():
        base = unicodedata.normalize("NFD", low)[0]
        # Only Latin letters lose their diacritics (día -> dia); Cyrillic й
        # decomposes to и + breve and must stay й.
        if base.isascii():
            return base
    return low


def normalize(text: str) -> str:
    """Lower-case, fold typographic quotes and spaces, ``ё`` and Latin diacritics.

    The result has the same length as ``text``.
    """
    return "".join(_fold(ch) for ch in text)


def words(text: str) -> int:
    """Number of words; a contraction or a hyphenated word counts once."""
    return len(WORD.findall(text))


def paragraph_spans(text: str) -> List[Tuple[int, int]]:
    """``(start, end)`` of each non-empty paragraph; paragraphs split on blank lines only."""
    spans: List[Tuple[int, int]] = []
    cursor = 0
    for gap in _BLANK_LINE.finditer(text):
        if text[cursor:gap.start()].strip():
            spans.append((cursor, gap.start()))
        cursor = gap.end()
    if text[cursor:].strip():
        spans.append((cursor, len(text)))
    return spans


def paragraph_of(starts: List[int], offset: int) -> int:
    """Index of the paragraph holding ``offset``, given the paragraphs' start offsets."""
    return max(0, bisect_right(starts, offset) - 1)


def line_of(text: str, offset: int) -> int:
    """1-based number of the line holding ``offset``."""
    return text.count("\n", 0, offset) + 1


def _skip_to_letter(text: str, pos: int, end: int) -> int:
    while pos < end and not text[pos].isalpha():
        pos += 1
    return pos


def _append_span(spans: List[Tuple[int, int]], text: str, start: int, end: int) -> None:
    start = _skip_to_letter(text, start, end)
    if start < end:
        spans.append((start, end))


def sentence_spans(text: str) -> List[Tuple[int, int]]:
    """``(start, end)`` of each sentence or line; ``start`` is its first letter."""
    spans: List[Tuple[int, int]] = []
    cursor = 0
    for brk in _SENTENCE_BREAK.finditer(text):
        _append_span(spans, text, cursor, brk.start())
        cursor = brk.end()
    _append_span(spans, text, cursor, len(text))
    return spans


def clause_starts(text: str, sentences: Iterable[Tuple[int, int]]) -> List[int]:
    """First letter of every clause: sentence starts plus after ``, ; : ( — –``."""
    starts = set()
    for start, end in sentences:
        starts.add(start)
        for brk in _CLAUSE_BREAK.finditer(text, start, end):
            pos = _skip_to_letter(text, brk.end(), end)
            if pos < end:
                starts.add(pos)
    return sorted(starts)


def quoted_spans(norm: str) -> List[Tuple[int, int]]:
    """Spans inside quotation marks or on a ``>`` quote line (normalised text)."""
    spans = [m.span() for m in _DOUBLE_QUOTED.finditer(norm)]
    spans += [m.span() for m in _SINGLE_QUOTED.finditer(norm)]
    spans += [m.span() for m in _BLOCKQUOTE.finditer(norm)]
    return spans


def inside_any(start: int, end: int, spans: Iterable[Tuple[int, int]]) -> bool:
    """True when ``[start, end)`` lies wholly inside one of ``spans``."""
    return any(s <= start and end <= e for s, e in spans)


def negated(
    norm: str,
    start: int,
    clause_start: int,
    words: frozenset,
    phrases: Iterable[Pattern[str]],
    *,
    window: int = 6,
) -> bool:
    """True when the last ``window`` words before ``start`` in its clause
    reject, quote or criticise what follows ("don't", "stop", "posts that")."""
    before = norm[clause_start:start]
    tokens = _NEGATION_TOKEN.findall(before)[-window:]
    if any(token in words for token in tokens):
        return True
    tail = before[-60:]
    return any(pattern.search(tail) for pattern in phrases)


def blank(text: str, pattern: Pattern[str]) -> str:
    """Replace every match with spaces of the same length, so offsets stay those of ``text``."""
    return pattern.sub(lambda m: " " * (m.end() - m.start()), text)


def rhythm_text(norm: str) -> str:
    """Prose only, same length: headings, quote lines, list items, URLs, hashtags and inline markup blanked."""
    out = blank(norm, _STRUCTURE_LINE)
    out = blank(out, URL)
    out = blank(out, HASHTAG)
    return blank(out, _INLINE_MARKUP)
