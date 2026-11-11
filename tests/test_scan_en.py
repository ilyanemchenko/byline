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
    ("What do you think about remote work?", True),
    ("What's one meeting on your calendar this week that could have been an email?", True),
    ("What will remote work look like in ten years?", False),
    ("1. Ask first.\n2. Which step fits you best?", False),
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


# ── whole-post template patterns ─────────────────────────────────────────────

OPEN = "We moved the weekly review to Tuesday.\n\n"
BODY = "\n\nWe kept the notes in one shared file after that."


@pytest.mark.parametrize("middle,hit", [
    ("Here is what the first year taught me:", True),
    ("Keep the meeting for what it's actually good at:", True),
    ("We tried it. The result? Chaos for two whole weeks.", True),
    ("One two three four five six seven eight nine ten eleven twelve thirteen:", False),
    ("One more thing: remote work shifts the burden of clarity onto the writer.", False),
    ("1. Here is the plan:", False),
    ("Why did it fail?\n\nBecause nobody owned it.", False),
])
def test_setup(middle, hit):
    assert ("setup" in codes(scan.scan(OPEN + middle + BODY, language="en"))) is hit


@pytest.mark.parametrize("items,hit", [
    ("1. Clarity beats speed. Write down what done means.\n2. Ask before you assume.\n3. Outcomes over hours.", True),
    ("- Clarity beats speed.\n\n- Ask before you assume.\n\n- Outcomes over hours.", True),
    ("1. Clarity beats speed every single time you plan the week.\n"
     "2. Ask before you assume anything at all about a quiet person.\n"
     "3. Outcomes matter more than hours spent at a desk each day.", False),
    ("1. Clarity beats speed.\n2. Ask before you assume.", False),
])
def test_maxim_list(items, hit):
    r = scan.scan(OPEN + items + BODY, language="en")
    assert (codes(r).count("maxim_list") == 1) is hit


def test_contrast_run_needs_two_contrasts_after_the_opener():
    two = "The fix isn't willpower. It's a rule. The plan isn't a list. It's a promise."
    one = "The fix isn't willpower. It's a rule we keep."
    r = scan.scan(OPEN + two, language="en")
    run = [f for f in r.flags if f.code == "contrast_run"]
    assert len(run) == 1 and run[0].start == [f for f in r.flags if f.code == "contrast"][1].start
    assert "contrast_run" not in codes(scan.scan(OPEN + one, language="en"))
    assert "contrast_run" not in codes(scan.scan("It isn't a tool. It's a habit.\n\n" + one, language="en"))


@pytest.mark.parametrize("ending,hit", [
    ("#work #life #focus", True), ("#work #life", False), ("Done. #work #life #focus", False),
])
def test_hashtag_row(ending, hit):
    assert ("hashtag_row" in codes(scan.scan(OPEN + "We kept the notes.\n\n" + ending, language="en"))) is hit


def test_template_codes_count_once_each():
    r = scan.scan(OPEN + "Here is the plan:\n\nWe ship on Monday. After that:\n\nWe rest.", language="en")
    assert codes(r).count("setup") == 2 and r.markers == 1 and r.score == 15 and r.label == "clean"


def test_whole_post_template_is_heavy():
    post = ("I thought burnout meant working too much.\n\n"
            "Here is what finally helped:\n\n"
            "1. I named it early.\n"
            "2. I cut one thing.\n"
            "3. I told one person.\n\n"
            "Rest isn't a reward. It's maintenance.\n"
            "Recovery isn't a retreat. It's small corrections.\n\n"
            "You are allowed to change the load.\n\n"
            "What's one thing you could take off your plate this week?\n\n"
            "#burnout #work #health")
    assert len(post.splitlines()) >= 12
    r = scan.scan(post, language="en")
    assert {"setup", "maxim_list", "contrast_run", "closer", "hashtag_row"} <= set(codes(r))
    assert r.label == "heavy"
