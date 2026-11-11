"""Render a scan ``Report`` as plain text for a person or as JSON for a program."""

from __future__ import annotations

import json
import re
from typing import List

from . import rules
from .scan import Report

DISCLAIMER = "This names patterns. It does not say who wrote the text."
LABEL_TEXT = {"clean": "clean", "some": "some AI tells", "heavy": "heavy AI tells"}

QUOTE_MAX = 60  # longer flag texts (a whole flagged paragraph) are cut to this many characters
_SPACE = re.compile(r"\s+")


def _quote(text: str) -> str:
    flat = _SPACE.sub(" ", text).strip()
    if len(flat) > QUOTE_MAX:
        flat = flat[:QUOTE_MAX - 1].rstrip() + "…"
    return f'"{flat}"'


def _count(number: int, noun: str) -> str:
    return f"{number} {noun}" if number == 1 else f"{number} {noun}s"


def _language_line(report: Report) -> str:
    if report.language is None:
        language = "Language: unknown"  # the scan's note explains what was checked
    else:
        language = f"Language: {rules.load(report.language).name} ({report.language_status})"
    return (f"{language}, {_count(report.words, 'word')}, {_count(report.paragraphs, 'paragraph')}, "
            f"{_count(report.markers, 'marker')}")


def render_text(report: Report) -> str:
    lines: List[str] = [f"byline slop-check: {LABEL_TEXT[report.label]} (score {report.score}/100)",
                        _language_line(report)]
    flagged = set(report.flagged_paragraphs)
    for paragraph in sorted({item.paragraph for item in report.flags}):
        heading = f"Paragraph {paragraph + 1}"
        if paragraph in flagged:
            heading += " (flagged)"
        lines += ["", heading]
        lines += [f"  line {item.line:<4} {item.code:<10} {_quote(item.text)}"
                  for item in report.flags if item.paragraph == paragraph]
    if report.notes:
        lines.append("")
        lines += [f"Note: {note}" for note in report.notes]
    lines += ["", DISCLAIMER]
    return "\n".join(lines) + "\n"


def render_json(report: Report) -> str:
    data = {
        "label": report.label,
        "score": report.score,
        "language": report.language,
        "language_status": report.language_status,
        "words": report.words,
        "paragraphs": report.paragraphs,
        "markers": report.markers,
        "flagged_paragraphs": list(report.flagged_paragraphs),
        "flags": [{"code": item.code, "line": item.line, "paragraph": item.paragraph,
                   "start": item.start, "end": item.end, "text": item.text} for item in report.flags],
        "notes": list(report.notes),
        "disclaimer": DISCLAIMER,
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
