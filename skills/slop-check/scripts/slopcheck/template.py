"""Patterns of a whole post: the template a reader recognises across the text, not in one paragraph.

A machine-written post often follows one shape from top to bottom: a setup line that announces
what follows ("Here is what I learned:"), a list of short slogans, a negation reframed in the next
sentence more than once, a question to the reader on the last line, a row of hashtags. Each finder
here returns ``(start, end)`` spans on the normalised text; ``scan`` turns them into flags.
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from .rules import Language
from .text import HASHTAG, LETTER, URL, WORD, blank, words

TEMPLATE_CODES = ("setup", "maxim_list", "contrast_run", "closer", "hashtag_row")

SETUP_MIN_WORDS = 2
SETUP_MAX_WORDS = 12
QUESTION_MAX_WORDS = 5  # "The result? Chaos." asks at most this many words
MAXIM_MAX_WORDS = 8     # first sentence of a list item
MAXIM_MIN_ITEMS = 3
HASHTAG_ROW_MIN = 3

Span = Tuple[int, int]

_LINE = re.compile(r"[^\n]*")
_ITEM = re.compile(r"[ \t]*(?:\d+[.)]|[-*•])[ \t]+(?=\S)")
_FIRST_SENTENCE = re.compile(r"(?<=[.!?…])[\"')\]]*\s")
# A short question answered by the next sentence on the same line: "The result? Chaos."
_QUESTION = re.compile(r"(?:^|(?<=[.!…][ \t])|(?<=[.!…][ \t]{2}))([^.!?…\n]+\?)[ \t]+(?=[^\W\d_])([^.!?…\n]*)([.!?…]?)",
                       re.MULTILINE)
_HASHTAG_ROW = re.compile(r"[ \t]*(?:#[^\W\d_]\w*[ \t]*)+")


def _lines(text: str) -> List[Span]:
    return [m.span() for m in _LINE.finditer(text) if m.start() == 0 or text[m.start() - 1] == "\n"]


def _trim(text: str, start: int, end: int) -> Span:
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return start, end


def setups(rhythm: str) -> List[Span]:
    """Colon lines of 2–12 words followed by more text, and short questions answered at once.

    ``rhythm`` is the prose-only text (``text.rhythm_text``): list items, headings and hashtags are
    already blank, so a list item ending in a colon is never a setup.
    """
    found: List[Span] = []
    for start, end in _lines(rhythm):
        start, end = _trim(rhythm, start, end)
        if end <= start or rhythm[end - 1] != ":":
            continue
        if SETUP_MIN_WORDS <= words(rhythm[start:end]) <= SETUP_MAX_WORDS and LETTER.search(rhythm, end):
            found.append((start, end))
    for match in _QUESTION.finditer(rhythm):
        question, answer, stop = match.group(1), match.group(2), match.group(3)
        if stop == "?" or not answer.strip() or not 1 <= words(question) <= QUESTION_MAX_WORDS:
            continue
        found.append(_trim(rhythm, match.start(1), match.end(1)))
    return sorted(found)


def _first_sentence_words(item: str) -> int:
    return words(_FIRST_SENTENCE.split(item, 1)[0])


def maxim_lists(norm: str) -> List[Span]:
    """Runs of three or more list items in a row whose first sentence has at most eight words.

    Items may be separated by blank lines; a line right under an item (no blank line between)
    continues that item. A paragraph of prose, or an item with a long first sentence, ends the run.
    """
    found: List[Span] = []
    run: List[Span] = []
    in_item = blank_before = False

    def close() -> None:
        if len(run) >= MAXIM_MIN_ITEMS:
            found.append((run[0][0], run[-1][1]))
        run.clear()

    for start, end in _lines(norm):
        line = norm[start:end]
        item = _ITEM.match(line)
        if item:
            if _first_sentence_words(line[item.end():]) <= MAXIM_MAX_WORDS:
                run.append(_trim(norm, start, end))
            else:
                close()
            in_item, blank_before = True, False
        elif not line.strip():
            blank_before = True
        elif not (in_item and not blank_before):
            close()
            in_item = False
    close()
    return found


def contrast_run(contrasts: List[Span]) -> Optional[Span]:
    """The second contrast, when the text has two or more (the exempt opener is never among them)."""
    return contrasts[1] if len(contrasts) >= 2 else None


def _reader_word(line: str, lang: Language) -> bool:
    for token in WORD.findall(line):
        if token in lang.reader_words or any(token.startswith(stem) for stem in lang.reader_stems):
            return True
    return False


def closer(norm: str, lang: Optional[Language]) -> Optional[Span]:
    """A closing cliché, or a question to the reader, on the last line that has letters.

    Hashtags and links are blanked first; a last line that is a list item is not prose and never a closer. With a language, the question needs one of its
    ``reader_words``; without one, any final question counts.
    """
    cursor = len(norm)
    while cursor > 0:
        line_start = norm.rfind("\n", 0, cursor) + 1
        line = blank(blank(norm[line_start:cursor], HASHTAG), URL)
        cursor = line_start - 1
        if not LETTER.search(line):
            continue
        if _ITEM.match(line):
            return None  # the post ends on a list item, not on a line of prose
        if lang is not None and lang.closers is not None:
            match = lang.closers.search(line)
            if match is not None:
                return line_start + match.start(), line_start + match.end()
        question = line.rstrip().rstrip("\"')»").rstrip()
        if not question.endswith("?"):
            return None
        if lang is None or _reader_word(question, lang):
            return _trim(norm, line_start, line_start + len(question))
        return None
    return None


def hashtag_row(norm: str) -> Optional[Span]:
    """The last non-empty line, when it holds only hashtags, three or more."""
    for start, end in reversed(_lines(norm)):
        start, end = _trim(norm, start, end)
        if end <= start:
            continue
        line = norm[start:end]
        if _HASHTAG_ROW.fullmatch(line) and len(HASHTAG.findall(line)) >= HASHTAG_ROW_MIN:
            return start, end
        return None
    return None
