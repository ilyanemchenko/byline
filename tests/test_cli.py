from __future__ import annotations

import io
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest
from samples import SLOP

CHECK = Path(__file__).resolve().parent.parent / "skills" / "slop-check" / "scripts" / "check.py"


@pytest.fixture
def run(tmp_path):
    def _run(args, stdin=None):
        return subprocess.run([sys.executable, str(CHECK), *args], input=stdin if stdin is not None else "",
                              capture_output=True, text=True, encoding="utf-8", cwd=tmp_path)
    return _run


def test_text_output_frame(run):
    out = run(["--lang", "en"], stdin=SLOP).stdout.strip().splitlines()
    assert re.fullmatch(r"byline slop-check: (clean|some AI tells|heavy AI tells) \(score \d+/100\)", out[0])
    assert out[-1] == "This names patterns. It does not say who wrote the text."


def test_every_flag_is_printed_with_its_line(run):
    out = run(["--lang", "en"], stdin="Fine line here.\n\nWe leverage it.").stdout
    assert re.search(r"line 3\s+vocab\s+\"leverage\"", out)


def test_json_output(run):
    data = json.loads(run(["--json", "--lang", "en"], stdin=SLOP).stdout)
    assert set(data) == {"label", "score", "language", "language_status", "words", "paragraphs", "markers",
                         "flagged_paragraphs", "flags", "notes", "disclaimer"}
    assert data["label"] == "heavy" and set(data["flags"][0]) == {"code", "line", "paragraph", "start", "end", "text"}


def test_file_argument_and_dash(run, tmp_path):
    (tmp_path / "post.md").write_text(SLOP, encoding="utf-8")
    assert run(["post.md", "--json"]).stdout == run(["-", "--json"], stdin=SLOP).stdout


def test_bom_and_crlf_change_nothing(run, tmp_path):
    (tmp_path / "win.md").write_bytes(b"\xef\xbb\xbf" + SLOP.replace("\n", "\r\n").encode("utf-8"))
    assert run(["win.md", "--json"]).stdout == run(["--json"], stdin=SLOP).stdout


@pytest.mark.parametrize("stdin", ["", "   \n\n ", "﻿"])
def test_empty_input(run, stdin):
    r = run([], stdin=stdin)
    assert r.returncode == 2 and "nothing to check" in r.stderr and "Traceback" not in r.stderr


@pytest.mark.parametrize("stdin", ["🔥🔥🔥", "Hi", "#tag"])
def test_tiny_input_is_checked_not_crashed(run, stdin):
    r = run(["--json"], stdin=stdin)
    assert r.returncode == 0 and json.loads(r.stdout)["label"] == "clean"


def test_bad_arguments(run):
    r = run(["--lang", "xx"], stdin="text")
    assert r.returncode == 2 and "en" in r.stderr and "ru" in r.stderr
    assert run(["--channel", "myspace"], stdin="text").returncode == 2
    assert run(["no-such-file.md"]).returncode == 2


def test_file_that_is_not_utf8(run, tmp_path):
    (tmp_path / "latin.md").write_bytes("caf\xe9".encode("latin-1"))
    r = run(["latin.md"])
    assert r.returncode == 2 and "latin.md" in r.stderr and "Traceback" not in r.stderr


def test_long_text_is_fast(run):
    start = time.monotonic()
    assert run(["--lang", "en"], stdin=(SLOP + "\n\n") * 400).returncode == 0   # about 20,000 words
    assert time.monotonic() - start < 5


def test_runs_from_another_folder(run):          # the fixture's cwd is tmp_path
    assert run(["--lang", "en"], stdin="Fine.").returncode == 0


def test_broken_language_file_is_a_message_not_a_traceback(monkeypatch, capsys):
    import check
    from slopcheck import scan

    def broken(*_args, **_kwargs):
        raise ValueError("en.json: vocab entry 'x(' is not a valid pattern")

    monkeypatch.setattr(scan, "scan", broken)
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(b"Some text."), encoding="utf-8"))
    assert check.main(["--lang", "en"]) == 2
    assert "en.json" in capsys.readouterr().err
