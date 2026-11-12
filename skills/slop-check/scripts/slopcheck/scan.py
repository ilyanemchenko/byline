"""Scan a text for patterns that read as AI-written, score it and label it.

``scan`` reads the text the way a reader notices machine prose: vocabulary markers,
dashes per hundred words, the contrast formula ("it's not X, it's Y") anywhere but the
opening sentence, lists of three, runs of fragments, and two channel facts: hashtags over the
maximum and the character limit. On top of these local markers it looks for the template of a
whole post (``template.py``): a setup line, a list of slogans, a run of contrasts, a closing
question to the reader, a row of hashtags. Each template code counts once.

One marker is never a verdict. A paragraph is flagged at ``density_markers`` markers,
and the score weighs flagged paragraphs above loose markers. Stacked lists of three
(two in one paragraph, or three in the text) flag the paragraph with the most of them
whatever its marker count. Quoted text is never a vocabulary hit, nor is a marker the
sentence rejects ("stop saying game-changer").
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from . import rules, template
from .rhythm import dashes, fragment_runs, triads
from .rules import Language, Thresholds
from .text import (HASHTAG, clause_starts, inside_any, line_of, negated, normalize,
                   paragraph_of, paragraph_spans, quoted_spans, rhythm_text, sentence_spans, words)

MARKER_CODES = ("vocab", "contrast", "triad", "fragments", "dash", "hashtags")
TEMPLATE_CODES = template.TEMPLATE_CODES
# Markers that count towards flagging a paragraph; the dash flag adds one more.
DENSITY_CODES = ("vocab", "contrast", "triad", "fragments")

# score = min(SCORE_MAX, PARAGRAPH_WEIGHT * flagged + round(MARKER_WEIGHT * markers * min(1, WORDS_SCALE / words))
#             + TEMPLATE_WEIGHT * templates), where templates is the number of distinct template codes.
SCORE_MAX = 100
PARAGRAPH_WEIGHT = 25
MARKER_WEIGHT = 3
WORDS_SCALE = 200
TEMPLATE_WEIGHT = 15  # below SOME_FROM: one template pattern alone never leaves "clean"
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


def score_of(flagged: int, markers: int, words: int, templates: int = 0) -> int:
    """Flagged paragraphs and template patterns weigh most; loose markers weigh less in a long text."""
    scale = min(1.0, WORDS_SCALE / max(words, 1))
    return min(SCORE_MAX, PARAGRAPH_WEIGHT * flagged + round(MARKER_WEIGHT * markers * scale)
               + TEMPLATE_WEIGHT * templates)


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
    code = (language or "").strip().lower() or rules.detect(text)
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


def _templates(norm: str, text: str, rhythm: str, lang: Optional[Language], flags: List[Flag],
               starts: List[int]) -> List[Flag]:
    spans = [("setup", span) for span in template.setups(rhythm)]
    spans += [("maxim_list", span) for span in template.maxim_lists(norm)]
    run = template.contrast_run([(item.start, item.end) for item in flags if item.code == "contrast"])
    closer = template.closer(norm, lang)
    row = template.hashtag_row(norm)
    spans += [(code, span) for code, span in (("contrast_run", run), ("closer", closer), ("hashtag_row", row))
              if span is not None]
    return [_flag(code, text, start, end, starts) for code, (start, end) in spans]


# ── the scan ──────────────────────────────────────────────────────────────────


def scan(text: str, *, language: Optional[str] = None, channel: Optional[str] = None) -> Report:
    """Measure one text; see the module docstring for what is counted.

    An explicit ``language`` overrides the text's own script; empty or blank means detect.
    """
    spec = _channel(channel)
    norm = normalize(text)
    paragraphs = paragraph_spans(norm)
    starts = [start for start, _end in paragraphs]
    word_count = words(norm)
    dash_offsets = dashes(norm)
    length = len(text.rstrip())  # a final line break from a file or a heredoc is not part of the post
    over_limit_by = max(0, length - spec.char_limit) if spec is not None and spec.char_limit is not None else 0
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
        flags.append(_flag("over_limit", text, length - over_limit_by, length, starts))
    flags += _templates(norm, text, rhythm, lang, flags, starts)

    report.flagged_paragraphs = _flagged_paragraphs(flags, dash_offsets, dash_flagged, len(paragraphs), starts, th)
    for index in report.flagged_paragraphs:
        start, end = paragraphs[index]
        flags.append(_flag("density", text, start, end, starts))

    report.flags = sorted(flags, key=lambda item: (item.start, item.code))
    local = sum(1 for item in flags if item.code in MARKER_CODES)
    templates = len({item.code for item in flags if item.code in TEMPLATE_CODES})
    report.markers = local + templates
    report.score = score_of(len(report.flagged_paragraphs), local, word_count, templates)
    report.label = label_of(report.score)
    return report
