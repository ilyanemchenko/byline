"""Scan a text for patterns that read as AI-written, score it and label it.

``scan`` reads the text the way a reader notices machine prose: vocabulary markers,
dashes per hundred words, the contrast formula ("it's not X, it's Y") anywhere but the
opening sentence, lists of three, runs of fragments, a closing cliché ("Thoughts?"),
and two channel facts: hashtags over the maximum and the character limit.

One marker is never a verdict. A paragraph is flagged at ``density_markers`` markers,
and the score weighs flagged paragraphs above loose markers. Stacked lists of three
(two in one paragraph, or three in the text) flag the paragraph with the most of them
whatever its marker count. Quoted text is never a vocabulary hit, nor is a marker the
sentence rejects ("stop saying game-changer").
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from . import rules
from .rhythm import dashes, fragment_runs, triads
from .rules import Language, Thresholds
from .text import (HASHTAG, LETTER, URL, blank, clause_starts, inside_any, line_of, negated, normalize,
                   paragraph_of, paragraph_spans, quoted_spans, rhythm_text, sentence_spans, words)

MARKER_CODES = ("vocab", "contrast", "triad", "fragments", "closer", "dash", "hashtags")
# Markers that count towards flagging a paragraph; the dash flag adds one more.
DENSITY_CODES = ("vocab", "contrast", "triad", "fragments")

# score = min(SCORE_MAX, PARAGRAPH_WEIGHT * flagged + round(MARKER_WEIGHT * markers * min(1, WORDS_SCALE / words)))
SCORE_MAX = 100
PARAGRAPH_WEIGHT = 25
MARKER_WEIGHT = 3
WORDS_SCALE = 200
# label: below SOME_FROM is "clean", below HEAVY_FROM is "some", else "heavy".
SOME_FROM = 20
HEAVY_FROM = 50

UNKNOWN_LANGUAGE_NOTE = ("Language not recognised, so only structure was checked: dashes, lists of three, "
                         "fragments, hashtags. Pass --lang with one of: {codes}. "
                         "To add a language, see docs/add-a-language.md.")
BETA_NOTE = "{name} rules are beta: they have not been measured on a reference set yet."

Span = Tuple[int, int]


@dataclass(frozen=True)
class Flag:
    code: str
    start: int
    end: int
    text: str
    paragraph: int
    line: int


@dataclass
class Report:
    language: Optional[str]
    language_status: Optional[str]
    words: int
    paragraphs: int
    dash_count: int
    dash_per_100_words: float
    hashtag_count: int
    over_limit_by: int
    flags: list = field(default_factory=list)
    flagged_paragraphs: list = field(default_factory=list)
    markers: int = 0
    score: int = 0
    label: str = "clean"
    notes: list = field(default_factory=list)


def score_of(flagged: int, markers: int, words: int) -> int:
    """Flagged paragraphs weigh most; loose markers weigh less in a long text."""
    scale = min(1.0, WORDS_SCALE / max(words, 1))
    return min(SCORE_MAX, PARAGRAPH_WEIGHT * flagged + round(MARKER_WEIGHT * markers * scale))


def label_of(score: int) -> str:
    return "clean" if score < SOME_FROM else "some" if score < HEAVY_FROM else "heavy"


# ── helpers ───────────────────────────────────────────────────────────────────


def _channel(channel: Optional[str]) -> Optional[rules.Channel]:
    if channel is None:
        return None
    known = rules.channels()
    if channel not in known:
        raise ValueError(f"unknown channel {channel!r}; valid channels: {', '.join(sorted(known))}")
    return known[channel]


def _language(text: str, language: Optional[str]) -> Optional[Language]:
    code = rules.detect(text) if language is None else language.strip().lower()
    if code is None or code not in rules.available():
        return None
    return rules.load(code)


def _flag(code: str, text: str, start: int, end: int, starts: List[int]) -> Flag:
    return Flag(code, start, end, text[start:end], paragraph_of(starts, start), line_of(text, start))


def _clause_of(clauses: List[int], offset: int) -> int:
    """Start of the clause holding ``offset``."""
    found = 0
    for start in clauses:
        if start > offset:
            break
        found = start
    return found


def _vocab_hits(norm: str, text: str, lang: Language, quotes: List[Span], clauses: List[int],
                starts: List[int]) -> List[Flag]:
    hits: List[Flag] = []
    for match in lang.vocab.finditer(norm):
        if inside_any(match.start(), match.end(), quotes):
            continue
        if negated(norm, match.start(), _clause_of(clauses, match.start()), lang.negation_words,
                   lang.negation_phrases):
            continue
        hits.append(_flag("vocab", text, match.start(), match.end(), starts))
    return hits


def _contrast(norm: str, text: str, lang: Language, sentences: List[Span], starts: List[int]) -> List[Flag]:
    opener_end = sentences[0][1] if sentences else 0
    spans: List[Span] = []
    for regex in lang.contrast:
        for match in regex.finditer(norm):
            start = match.start() + (len(match.group(0)) - len(match.group(0).lstrip()))
            if start < opener_end:
                continue  # the opening sentence may be a contrast
            spans.append((start, match.end()))
    found: List[Flag] = []
    for start, end in sorted(spans):
        if found and start < found[-1].end:
            continue  # one construction matched by two shapes is one flag
        found.append(_flag("contrast", text, start, end, starts))
    return found


def _closer(norm: str, text: str, lang: Language, starts: List[int]) -> Optional[Flag]:
    """A closing cliché on the last line that has letters once hashtags and links are blanked."""
    if lang.closers is None:
        return None
    cursor = len(norm)
    while cursor > 0:
        line_start = norm.rfind("\n", 0, cursor) + 1
        line = blank(blank(norm[line_start:cursor], HASHTAG), URL)
        if LETTER.search(line):
            match = lang.closers.search(line)
            if match is None:
                return None
            return _flag("closer", text, line_start + match.start(), line_start + match.end(), starts)
        cursor = line_start - 1
    return None


def _flagged_paragraphs(flags: List[Flag], dash_offsets: List[int], dash_flagged: bool,
                        paragraph_count: int, starts: List[int], th: Thresholds) -> List[int]:
    counts = [0] * paragraph_count
    for item in flags:
        if item.code in DENSITY_CODES:
            counts[item.paragraph] += 1
    if dash_flagged:  # the dash flag counts once, in the paragraph with the most dashes
        per_paragraph = [0] * paragraph_count
        for offset in dash_offsets:
            per_paragraph[paragraph_of(starts, offset)] += 1
        counts[per_paragraph.index(max(per_paragraph))] += 1
    flagged = {index for index, count in enumerate(counts) if count >= th.density_markers}
    triads_per = [0] * paragraph_count
    for item in flags:
        if item.code == "triad":
            triads_per[item.paragraph] += 1
    if triads_per and (max(triads_per) >= 2 or sum(triads_per) >= 3):
        flagged.add(triads_per.index(max(triads_per)))  # stacked lists of three
    return sorted(flagged)


# ── the scan ──────────────────────────────────────────────────────────────────


def scan(text: str, *, language: Optional[str] = None, channel: Optional[str] = None) -> Report:
    """Measure one text; see the module docstring for what is counted."""
    spec = _channel(channel)
    norm = normalize(text)
    paragraphs = paragraph_spans(norm)
    starts = [start for start, _end in paragraphs]
    word_count = words(norm)
    dash_offsets = dashes(rhythm_text(norm))
    over_limit_by = max(0, len(text) - spec.char_limit) if spec is not None and spec.char_limit is not None else 0
    report = Report(
        language=None,
        language_status=None,
        words=word_count,
        paragraphs=len(paragraphs),
        dash_count=len(dash_offsets),
        dash_per_100_words=round(len(dash_offsets) / word_count * 100, 2) if word_count else 0.0,
        hashtag_count=len(HASHTAG.findall(norm)),
        over_limit_by=over_limit_by,
    )
    if not text.strip():
        return report

    lang = _language(text, language)
    th = lang.thresholds if lang is not None else Thresholds()
    if lang is None:
        report.notes.append(UNKNOWN_LANGUAGE_NOTE.format(codes=", ".join(rules.available())))
    else:
        report.language, report.language_status = lang.code, lang.status
        if lang.status == "beta":
            report.notes.append(BETA_NOTE.format(name=lang.name))

    quotes = quoted_spans(norm)
    sentences = sentence_spans(norm)
    clauses = clause_starts(norm, sentences)
    rhythm = rhythm_text(norm)
    rhythm_sentences = sentence_spans(rhythm)

    flags: List[Flag] = []
    if lang is not None:
        flags += _vocab_hits(norm, text, lang, quotes, clauses, starts)
        flags += _contrast(norm, text, lang, sentences, starts)
        closer = _closer(norm, text, lang, starts)
        if closer is not None:
            flags.append(closer)
    triad_spans, covered = triads(rhythm, rhythm_sentences, paragraphs, lang, th)
    flags += [_flag("triad", text, start, end, starts) for start, end in triad_spans]
    flags += [_flag("fragments", text, start, end, starts)
              for start, end in fragment_runs(rhythm, rhythm_sentences, starts, covered, th)]

    dash_flagged = report.dash_per_100_words > th.dash_per_100_max and len(dash_offsets) >= th.dash_min_count
    if dash_flagged:
        flags.append(_flag("dash", text, dash_offsets[0], dash_offsets[0] + 1, starts))
    hashtag_max = spec.hashtag_max if spec is not None else th.hashtag_max
    first_tag = HASHTAG.search(norm)
    if report.hashtag_count > hashtag_max and first_tag is not None:
        flags.append(_flag("hashtags", text, first_tag.start(), first_tag.end(), starts))
    if over_limit_by:
        flags.append(_flag("over_limit", text, len(text) - over_limit_by, len(text), starts))

    report.flagged_paragraphs = _flagged_paragraphs(flags, dash_offsets, dash_flagged, len(paragraphs), starts, th)
    for index in report.flagged_paragraphs:
        start, end = paragraphs[index]
        flags.append(_flag("density", text, start, end, starts))

    report.flags = sorted(flags, key=lambda item: (item.start, item.code))
    report.markers = sum(1 for item in flags if item.code in MARKER_CODES)
    report.score = score_of(len(report.flagged_paragraphs), report.markers, word_count)
    report.label = label_of(report.score)
    return report
