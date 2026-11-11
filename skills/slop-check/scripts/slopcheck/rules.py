"""Language rules as data: load, validate and detect the languages in ``rules/``.

Each ``rules/<code>.json`` holds one language's word lists and patterns, all in the
normalised form of ``text.normalize``. ``load`` compiles a file into a ``Language``;
``channels`` reads ``rules/channels.json``.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, fields
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Pattern

from .text import WORD, normalize

STATUSES = ("measured", "beta")
REQUIRED_KEYS = ("code", "name", "status", "detect_markers", "vocab")
# Lists of plain entries: each must already be in normalised form.
_PLAIN_LISTS = ("detect_markers", "endings", "final_e_endings", "closers", "negation_words",
                "list_leads", "not_item_start", "parentheticals", "middle_only_parentheticals")
# Lists of raw regular expressions.
_REGEX_LISTS = ("contrast", "negation_phrases")

# detect: a language needs this many distinct markers, and this lead over the runner-up.
DETECT_MIN_MARKERS = 3
DETECT_MIN_LEAD = 2


class UnknownLanguage(ValueError):
    """No ``rules/<code>.json`` for the requested language."""


@dataclass(frozen=True)
class Thresholds:
    density_markers: int = 3
    dash_per_100_max: float = 1.0
    dash_min_count: int = 2
    fragment_run: int = 3
    fragment_max_words: int = 3
    triad_item_max_words: int = 4
    triad_line_max_words: int = 12
    hashtag_max: int = 5  # used when no channel is given


_THRESHOLD_NAMES = frozenset(f.name for f in fields(Thresholds))


@dataclass(frozen=True)
class Language:
    code: str
    name: str
    status: str
    vocab: Pattern
    closers: Optional[Pattern]
    contrast: tuple
    negation_words: frozenset
    negation_phrases: tuple
    list_leads: frozenset
    not_item_start: frozenset
    parentheticals: frozenset
    middle_only_parentheticals: frozenset
    detect_markers: frozenset
    thresholds: Thresholds


@dataclass(frozen=True)
class Channel:
    char_limit: Optional[int]
    hashtag_max: int


def rules_dir() -> Path:
    """The ``rules/`` folder of the slop-check skill."""
    return Path(__file__).resolve().parent.parent.parent / "rules"


def available() -> List[str]:
    """Sorted codes of the language files in ``rules/``."""
    return sorted(path.stem for path in rules_dir().glob("[a-z][a-z].json"))


def _compile_problem(pattern: str) -> Optional[str]:
    try:
        re.compile(pattern)
    except re.error as exc:
        return str(exc)
    return None


def validate(data: dict) -> List[str]:
    """Problems in one language file's data; ``[]`` when it is fine."""
    problems: List[str] = []
    for key in REQUIRED_KEYS:
        if key not in data:
            problems.append(f"missing key {key!r}")
    status = data.get("status")
    if "status" in data and status not in STATUSES:
        problems.append(f"status {status!r} is not one of {', '.join(STATUSES)}")

    for key in ("vocab",) + _PLAIN_LISTS + _REGEX_LISTS:
        value = data.get(key, [])
        if not isinstance(value, list) or not all(isinstance(entry, str) for entry in value):
            problems.append(f"{key!r} must be a list of strings")
            continue
        for entry in value:
            if key in _REGEX_LISTS or (key == "vocab" and entry.startswith("re:")):
                pattern = entry[3:] if key == "vocab" else entry
                error = _compile_problem(pattern)
                if error is not None:
                    problems.append(f"{key} entry {entry!r} is not a valid regular expression: {error}")
            elif entry != normalize(entry):
                problems.append(f"{key} entry {entry!r} is not in normalised form ({normalize(entry)!r})")

    thresholds = data.get("thresholds", {})
    if not isinstance(thresholds, dict):
        problems.append("'thresholds' must be an object")
    else:
        for name in sorted(set(thresholds) - _THRESHOLD_NAMES):
            problems.append(f"unknown thresholds key {name!r}")
    return problems


def _entry_pattern(entry: str, endings: List[str], final_e_endings: List[str]) -> str:
    if entry.startswith("re:"):
        return entry[3:]
    if entry.endswith("*"):
        return re.escape(entry[:-1]) + r"\w*"
    parts = entry.split()
    if len(parts) == 1:
        word = parts[0]
        if word.endswith("e") and final_e_endings:
            return re.escape(word[:-1]) + "(?:" + "|".join(map(re.escape, final_e_endings)) + ")"
        if endings:
            return re.escape(word) + "(?:" + "|".join(map(re.escape, endings)) + ")?"
        return re.escape(word)
    return r"\s+".join(re.escape(part) for part in parts)


def _phrase(entry: str) -> str:
    return r"\s+".join(re.escape(part) for part in entry.split())


def _vocab_regex(data: dict) -> Pattern:
    endings = data.get("endings", [])
    final_e = data.get("final_e_endings", [])
    alternatives = "|".join(_entry_pattern(entry, endings, final_e) for entry in data["vocab"])
    return re.compile(r"(?<![\w-])(?:" + alternatives + r")(?![\w-])")


def _closer_regex(entries: List[str]) -> Optional[Pattern]:
    if not entries:
        return None
    alternatives = "|".join(_phrase(entry) for entry in entries)
    # The closer ends the line, give or take two words ("Let me know in the comments below!").
    # With a question or exclamation mark of its own, the entry's ("Thoughts?") or one glued
    # on ("What do you think?"), it may carry a short sentence of up to three words
    # ("... Let me know!"). A full stop makes it a statement, not a closer, and
    # "what do you think about remote work?" is a question.
    return re.compile(r"(?<![\w-])(?:" + alternatives + r")(?:(?:(?<=[?!])|[?!]+)(?:\s+\S+){0,3}|(?:\s+\S+){0,2})"
                      r"[\s!?.…)»\"']*$")


@lru_cache(maxsize=None)
def load(code: str) -> Language:
    """Compile ``rules/<code>.json``; raises ``UnknownLanguage`` when there is none."""
    if code not in available():
        raise UnknownLanguage(f"unknown language {code!r}; available: {', '.join(available())}")
    path = rules_dir() / f"{code}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    problems = validate(data)
    if data.get("code") != code:
        problems.append(f"code {data.get('code')!r} differs from the file name {path.name!r}")
    if problems:
        raise ValueError(f"{path.name}: " + "; ".join(problems))
    return Language(
        code=code,
        name=data["name"],
        status=data["status"],
        vocab=_vocab_regex(data),
        closers=_closer_regex(data.get("closers", [])),
        contrast=tuple(re.compile(p, re.MULTILINE) for p in data.get("contrast", [])),
        negation_words=frozenset(data.get("negation_words", [])),
        negation_phrases=tuple(re.compile(p) for p in data.get("negation_phrases", [])),
        list_leads=frozenset(data.get("list_leads", [])),
        not_item_start=frozenset(data.get("not_item_start", [])),
        parentheticals=frozenset(data.get("parentheticals", [])),
        middle_only_parentheticals=frozenset(data.get("middle_only_parentheticals", [])),
        detect_markers=frozenset(data["detect_markers"]),
        thresholds=Thresholds(**data.get("thresholds", {})),
    )


def detect(text: str) -> Optional[str]:
    """The language whose markers the text uses most, or ``None`` when no language clearly leads.

    The best language needs at least ``DETECT_MIN_MARKERS`` distinct markers and a lead of at
    least ``DETECT_MIN_LEAD`` over the runner-up.
    """
    tokens = set(WORD.findall(normalize(text)))
    counts = sorted(((len(load(code).detect_markers & tokens), code) for code in available()), reverse=True)
    if not counts:
        return None
    best, code = counts[0]
    runner_up = counts[1][0] if len(counts) > 1 else 0
    if best >= DETECT_MIN_MARKERS and best - runner_up >= DETECT_MIN_LEAD:
        return code
    return None


@lru_cache(maxsize=None)
def _channels() -> Dict[str, Channel]:
    data = json.loads((rules_dir() / "channels.json").read_text(encoding="utf-8"))
    return {name: Channel(char_limit=spec["char_limit"], hashtag_max=spec["hashtag_max"])
            for name, spec in data.items()}


def channels() -> Dict[str, Channel]:
    """Channel facts from ``rules/channels.json``: character limit and hashtag maximum."""
    return dict(_channels())
