from __future__ import annotations

from slopcheck import scan


def codes(report):
    return [f.code for f in report.flags]


def test_russian_vocab_contrast_and_closer():
    text = ("Мы запустили продукт в марте.\n\n"
            "В современном мире важно отметить ключевые тренды. Дело не в деньгах, а в людях.\n\n"
            "Что думаете?")
    r = scan.scan(text, language="ru")
    assert r.language == "ru" and r.language_status == "beta"
    assert codes(r).count("vocab") == 3 and "contrast" in codes(r) and "closer" in codes(r)
    assert any("beta" in note for note in r.notes)


def test_russian_copula_dashes_are_not_flagged():
    text = "Москва — столица. Работа — это не всё. Команда — главное, что у нас есть. " + "слово " * 90
    assert "dash" not in codes(scan.scan(text, language="ru"))


def test_russian_dialogue_is_not_dashes():
    text = "— Ты уверен? — спросил он.\n— Да, — сказал я.\n" + "слово " * 40
    assert scan.scan(text, language="ru").dash_count == 0


def test_russian_question_to_the_reader_is_a_closer():
    assert "closer" in codes(scan.scan("Мы запустили продукт в марте.\n\nЧто вы думаете?", language="ru"))
    assert "closer" not in codes(scan.scan("Мы запустили продукт в марте.\n\nЧто будет через год?", language="ru"))


def test_without_a_language_file_a_final_question_is_a_closer():
    r = scan.scan("Hecho. Mañana hablamos con el equipo.\n\n¿Qué opinas del plan?", language="xx")
    assert r.language is None and "closer" in codes(r)
