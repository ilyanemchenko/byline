"""Rhythm detectors: dashes, lists of three and runs of fragments.

The list and fragment detectors read the prose-only text of ``text.rhythm_text``,
where a heading is not a sentence and a bullet list is not three fragments.
``dashes`` reads the whole normalised text, so a dash inside a bullet line counts;
it skips a dash that opens its line. All return offsets and spans that are also
offsets into the original text; the scan builds the flags.

Word sets come from a ``Language`` and limits from ``Thresholds``. With no
language the word sets are empty and the detectors still run on structure alone.
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Dict, List, Optional, Pattern, Sequence, Set, Tuple

from .rules import Language, Thresholds
from .text import WORD, paragraph_of, words

Span = Tuple[int, int]

_DASH = re.compile(r"[—–]|(?<=\s)-(?=\s)")
# A comma between digits is a decimal or thousands separator, never a list item boundary.
_COMMA_SPLIT = re.compile(r"(?<!\d),(?!\d)")
_EMPTY: frozenset = frozenset()


def dashes(text: str) -> List[int]:
    """Offsets of dashes that count: not the first mark on its line (dialogue, bullets),
    not an attribution after direct speech, not a numeric range."""
    found: List[int] = []
    for match in _DASH.finditer(text):
        line_start = text.rfind("\n", 0, match.start()) + 1
        before = text[line_start:match.start()].rstrip()
        if not before:
            continue  # the first mark on its line: dialogue, a bullet
        if before[-1] in ".!?…,":
            continue  # attribution after direct speech: «— Ты уверен? — спросил он», «— Да, — сказал он»
        if match.start() > 0 and text[match.start() - 1].isdigit() and text[match.end():match.end() + 1].isdigit():
            continue  # a range: 2019–2021
        found.append(match.start())
    return found


@lru_cache(maxsize=None)
def _list_lead(leads: frozenset) -> Optional[Pattern]:
    if not leads:
        return None
    return re.compile(r"^(?:" + "|".join(re.escape(lead) for lead in sorted(leads)) + r")\s+")


def _same_opener(items: List[str], th: Thresholds) -> bool:
    """"No fluff, no jargon, no filler": three short items opening on one word are the
    canonical list of three, whatever that word is."""
    heads = [WORD.search(item) for item in items]
    return (all(head is not None and 1 <= words(item) <= th.triad_item_max_words for head, item in zip(heads, items))
            and len({head.group(0) for head in heads if head is not None}) == 1)


def _list_item(item: str, lang: Optional[Language], th: Thresholds, *, middle: bool = False) -> bool:
    """A short list item: one to ``triad_item_max_words`` words that neither open on a
    conjunction or an interjection nor are a parenthetical (a noun-like one counts only
    in the ``middle``). ``item`` is a slice of the normalised rhythm text."""
    first = WORD.search(item)
    if first is None or not 1 <= words(item) <= th.triad_item_max_words:
        return False
    not_item_start = lang.not_item_start if lang else _EMPTY
    parentheticals = lang.parentheticals if lang else _EMPTY
    middle_only = lang.middle_only_parentheticals if lang else _EMPTY
    key = " ".join(WORD.findall(item))
    parenthetical = key in parentheticals and (middle or key not in middle_only)
    return first.group(0) not in not_item_start and not parenthetical


def triads(rhythm: str, sentences: Sequence[Span], paragraphs: Sequence[Span],
           lang: Optional[Language], th: Thresholds) -> Tuple[List[Span], Set[int]]:
    """Lists of three: comma triads, one line of three short sentences, and three
    one-sentence paragraphs in a row with the same first word or a shared ``?``/``!``
    ending. Returns the spans and the sentence indexes a list covers (no fragment run there)."""
    found: List[Span] = []
    covered: Set[int] = set()
    lead = _list_lead(lang.list_leads if lang else _EMPTY)

    for index, (start, end) in enumerate(sentences):
        body = rhythm[start:end].rstrip(" .!?…")
        items = [item.strip() for item in _COMMA_SPLIT.split(body)]
        if lead is not None:
            items = [lead.sub("", item) for item in items]
        if len(items) == 3 and (_same_opener(items, th)
                                or all(_list_item(item, lang, th, middle=(i == 1)) for i, item in enumerate(items))):
            found.append((start, end))
            covered.add(index)

    # "Simple. Fast. Done.": one line holding exactly three short sentences and nothing else.
    by_line: Dict[int, List[int]] = {}
    for index, (start, _end) in enumerate(sentences):
        by_line.setdefault(rhythm.rfind("\n", 0, start) + 1, []).append(index)
    for line_start, indexes in by_line.items():
        line_end = rhythm.find("\n", line_start)
        line_end = len(rhythm) if line_end < 0 else line_end
        short = all(1 <= words(rhythm[sentences[i][0]:sentences[i][1]]) <= th.triad_item_max_words
                    for i in indexes)
        if len(indexes) == 3 and short and not any(i in covered for i in indexes):
            found.append((line_start, line_end))
            covered.update(indexes)

    # Three one-sentence paragraphs in a row that open on the same word or all end on ? or !.
    starts = [p_start for p_start, _p_end in paragraphs]
    per_paragraph = [0] * len(paragraphs)
    if paragraphs:
        for s, _e in sentences:
            per_paragraph[paragraph_of(starts, s)] += 1
    single: List[Optional[Tuple[int, int, str, str]]] = []
    for index, (p_start, p_end) in enumerate(paragraphs):
        piece = rhythm[p_start:p_end].strip()
        if per_paragraph[index] == 1 and 1 <= words(piece) <= th.triad_line_max_words:
            first = WORD.search(piece)
            single.append((p_start, p_end, first.group(0) if first else "", piece[-1:]))
        else:
            single.append(None)
    i = 0
    while i <= len(single) - 3:
        trio = single[i:i + 3]
        if any(item is None for item in trio):
            i += 1
            continue
        heads = {item[2] for item in trio if item is not None}
        marks = {item[3] for item in trio if item is not None}
        same_word = len(heads) == 1 and bool(next(iter(heads)))
        same_mark = len(marks) == 1 and next(iter(marks)) in "?!"
        if same_word or same_mark:
            found.append((trio[0][0], trio[2][1]))  # type: ignore[index]
            i += 3  # a run of one-liners is one list, however long
            continue
        i += 1
    return found, covered


def fragment_runs(rhythm: str, sentences: Sequence[Span], paragraph_starts: List[int],
                  covered: Set[int], th: Thresholds) -> List[Span]:
    """Runs of at least ``fragment_run`` short sentences (up to ``fragment_max_words``
    words) in one paragraph, outside any list of three."""
    found: List[Span] = []
    run: List[int] = []

    def close() -> None:
        if len(run) >= th.fragment_run:
            found.append((sentences[run[0]][0], sentences[run[-1]][1]))
        run.clear()

    for index, (start, end) in enumerate(sentences):
        short = 1 <= words(rhythm[start:end]) <= th.fragment_max_words and index not in covered
        same_paragraph = (not run or paragraph_of(paragraph_starts, sentences[run[-1]][0])
                          == paragraph_of(paragraph_starts, start))
        if short and same_paragraph:
            run.append(index)
        else:
            close()
            if short:
                run.append(index)
    close()
    return found
