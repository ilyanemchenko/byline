from __future__ import annotations

from slopcheck import text as t


def test_normalize_folds_and_keeps_length():
    assert t.normalize("Ёж") == "еж"
    assert t.normalize("“Café”") == '"cafe"'
    assert t.normalize("й") == "й"
    for s in ("İstanbul — ﬁne", "A B", "naïve ‘quote’"):
        assert len(t.normalize(s)) == len(s)


def test_words_counts_contractions_and_hyphens_once():
    assert t.words("don't re-do it 3 times") == 5


def test_paragraphs_split_on_blank_lines_only():
    assert len(t.paragraph_spans("a\nb\n\nc\n \n\nd")) == 3


def test_sentences_start_on_a_letter():
    text = "One. Two!\n- three"
    assert [text[s:e] for s, e in t.sentence_spans(text)] == ["One", "Two!", "three"]


def test_line_of_is_one_based():
    assert t.line_of("a\nb\nc", 4) == 3


def test_quotes_and_blockquotes_are_spans():
    norm = t.normalize('say "game-changer" now\n> leverage it')
    spans = t.quoted_spans(norm)
    assert t.inside_any(norm.index("game"), norm.index("game") + 12, spans)
    assert t.inside_any(norm.index("leverage"), norm.index("leverage") + 8, spans)


def test_rhythm_text_blanks_structure_but_keeps_offsets():
    norm = t.normalize("# Title\nReal prose here.\n- bullet one\nhttps://x.io #tag")
    out = t.rhythm_text(norm)
    assert len(out) == len(norm) and "real prose here." in out
    assert "title" not in out and "bullet" not in out and "x.io" not in out and "tag" not in out
