from __future__ import annotations

import pytest
from samples import HUMAN, SLOP

from slopcheck import scan


def codes(report):
    return [f.code for f in report.flags]


def test_human_text_is_clean():
    r = scan.scan(HUMAN, language="en")
    assert (r.label, r.score, r.flags) == ("clean", 0, [])


def test_slop_text_is_heavy():
    r = scan.scan(SLOP, language="en")
    assert r.label == "heavy" and len(r.flagged_paragraphs) >= 2
    assert {"vocab", "contrast", "triad", "closer", "density"} <= set(codes(r))


def test_quoted_marker_is_not_a_hit():
    assert codes(scan.scan('My boss says "leverage synergy to unlock value" every single day.', language="en")) == []


def test_rejected_marker_is_not_a_hit():
    assert codes(scan.scan("Please stop saying game-changer in every single update.", language="en")) == []


def test_contrast_is_allowed_in_the_opener_only():
    line = "It's not a tool. It's a habit."
    assert "contrast" not in codes(scan.scan(line + "\n\nWe learned that slowly.", language="en"))
    assert codes(scan.scan("We learned that slowly.\n\n" + line, language="en")).count("contrast") == 1


@pytest.mark.parametrize("ending,flagged", [
    ("Thoughts?", True), ("Thoughts?\n\n#work #life", True),
    ("What do you think about remote work?", False),
    ("It does not matter what you think. It matters what you do.", False),
])
def test_closer(ending, flagged):
    assert ("closer" in codes(scan.scan("We shipped the fix on Friday.\n\n" + ending, language="en"))) is flagged


def test_two_markers_do_not_flag_a_paragraph_three_do():
    assert scan.scan("We leverage a robust plan for the week.", language="en").flagged_paragraphs == []
    assert scan.scan("We leverage a robust, seamless plan for the week.", language="en").flagged_paragraphs == [0]


def test_two_lists_of_three_in_one_paragraph_flag_it():
    r = scan.scan("We made it faster, cheaper, calmer. No fluff, no jargon, no filler.", language="en")
    assert r.flagged_paragraphs == [0]


def test_dash_rate():
    many = "The plan — as written — failed on day one — and nobody noticed. " + "word " * 100
    assert "dash" in codes(scan.scan(many, language="en"))
    assert "dash" not in codes(scan.scan("One dash — is fine here. " + "word " * 50, language="en"))


def test_hashtags_and_limit_by_channel():
    assert "hashtags" in codes(scan.scan("Done. #a #b #c", language="en", channel="x"))
    assert "hashtags" not in codes(scan.scan("Done. #a #b", language="en", channel="x"))
    assert "hashtags" in codes(scan.scan("Done. #a #b #c #d #e #f", language="en"))
    r = scan.scan("a" * 300, language="en", channel="x")
    assert r.over_limit_by == 20 and "over_limit" in codes(r) and r.markers == 0


def test_unknown_channel():
    with pytest.raises(ValueError):
        scan.scan("text", channel="myspace")


def test_language_without_rules_gets_structure_checks_and_a_note():
    r = scan.scan("Simple. Rápido. Hecho.\n\nMañana hablamos con el equipo sobre el plan nuevo.")
    assert r.language is None and "triad" in codes(r)
    assert any("docs/add-a-language.md" in note for note in r.notes)


def test_flags_carry_line_and_paragraph():
    f = scan.scan("Fine line here.\n\nWe leverage it.", language="en").flags[0]
    assert (f.code, f.text.lower(), f.line, f.paragraph) == ("vocab", "leverage", 3, 1)


def test_dashes_inside_bullets_count():
    text = "Our week:\n\n- Speed — we ship weekly\n- Care — we answer fast\n- Focus — one goal\n\n" + "word " * 20
    assert scan.scan(text, language="en").dash_count == 3


def test_unknown_language_code_gets_structure_checks_and_a_note():
    r = scan.scan("Simple. Fast. Done.\n\nWe leverage it.", language="xx")
    assert r.language is None and r.language_status is None
    assert "triad" in codes(r) and "vocab" not in codes(r)
    assert any("docs/add-a-language.md" in note for note in r.notes)


@pytest.mark.parametrize("language", ["", "   "])
def test_blank_language_means_detect(language):
    r = scan.scan("We leverage the plan and that is it for the week, with this and you.", language=language)
    assert r.language == "en"


@pytest.mark.parametrize("text", ["", "  \n\n \t"])
def test_empty_text_is_clean(text):
    r = scan.scan(text, language="en")
    assert (r.label, r.score, r.flags) == ("clean", 0, [])
