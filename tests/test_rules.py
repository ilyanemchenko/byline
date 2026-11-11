from __future__ import annotations

import json

import pytest

from slopcheck import rules

EN = ("The team shipped this feature last week, and you could see that it worked. "
      "We have fewer tickets now, but there are still two bugs with the export for big files.")
RU = ("Мы выпустили эту функцию на прошлой неделе, и это уже видно по цифрам. "
      "Если клиент пишет в поддержку, то только когда что-то сломалось или как минимум тормозит.")


def test_available_languages():
    assert rules.available() == ["en", "ru"]


@pytest.mark.parametrize("path", sorted(rules.rules_dir().glob("[a-z][a-z].json")))
def test_every_language_file_is_valid(path):
    assert rules.validate(json.loads(path.read_text(encoding="utf-8"))) == []


def test_validate_names_the_problem():
    bad = {"code": "en", "name": "English", "status": "done", "detect_markers": [], "vocab": ["Leverage", "re:("]}
    problems = " ".join(rules.validate(bad))
    assert "status" in problems and "Leverage" in problems and "re:(" in problems


def test_status_and_thresholds():
    assert rules.load("en").status == "measured" and rules.load("en").thresholds.dash_per_100_max == 1.0
    assert rules.load("ru").status == "beta" and rules.load("ru").thresholds.dash_min_count == 4


def test_unknown_language():
    with pytest.raises(rules.UnknownLanguage):
        rules.load("xx")


@pytest.mark.parametrize("text,expected", [
    (EN, "en"), (RU, "ru"),
    ("Hola, esto es una prueba de texto para ver que pasa con el idioma aqui.", None),
    ("Het huis is in de stad of in het dorp en het is groot.", None),
    ("Shipping is hard. Do it anyway.", None),
])
def test_detect(text, expected):
    assert rules.detect(text) == expected


@pytest.mark.parametrize("code,text,hit", [
    ("en", "we are leveraging it", "leveraging"), ("en", "navigating change", "navigating"),
    ("en", "lean\ninto it", "lean\ninto"), ("en", "the future of work is here", "the future of work is here"),
    ("ru", "ключевой момент", "ключевой"), ("ru", "в современном мире", "в современном мире"),
])
def test_vocab_pattern_matches_forms(code, text, hit):
    assert rules.load(code).vocab.search(text).group(0) == hit


def test_vocab_pattern_needs_word_boundaries():
    assert rules.load("en").vocab.search("the unrealm of pre-leverage") is None


def test_channels():
    ch = rules.channels()
    assert ch["x"].char_limit == 280 and ch["newsletter"].char_limit is None and ch["threads"].hashtag_max == 1
