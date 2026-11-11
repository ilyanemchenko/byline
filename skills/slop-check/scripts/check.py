"""Check a post for patterns that read as AI-written.

    python3 check.py [FILE | -] [--lang CODE] [--channel NAME] [--json]

With no FILE, or with ``-``, the text comes from standard input. Exit 0 when a report
was printed, whatever its label; exit 2 for a bad argument, an unreadable file or an
empty text.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

from slopcheck import report, rules, scan  # noqa: E402

EMPTY = "nothing to check: the text is empty"


class Problem(Exception):
    """A message for standard error and exit code 2."""


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="check.py", description="Check a post for patterns that read as AI-written.")
    parser.add_argument("file", nargs="?", default="-", metavar="FILE",
                        help="text file to check; '-' or nothing reads standard input")
    parser.add_argument("--lang", metavar="CODE", help=f"language code: {', '.join(rules.available())}; "
                        "default: detect from the text")
    parser.add_argument("--channel", metavar="NAME", help=f"channel: {', '.join(sorted(rules.channels()))}")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    return parser


def _read(name: str) -> str:
    """The text as UTF-8 without a byte-order mark and with \\n line ends."""
    try:
        data = sys.stdin.buffer.read() if name == "-" else Path(name).read_bytes()
    except OSError as error:
        raise Problem(f"cannot read {name}: {error.strerror or error}") from None
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise Problem(f"cannot read {'standard input' if name == '-' else name}: the text is not UTF-8") from None
    return text.replace("\r\n", "\n")


def _language(code: Optional[str]) -> Optional[str]:
    if code is None or not code.strip():
        return None
    code = code.strip().lower()
    if code not in rules.available():
        raise Problem(f"unknown language {code!r}; valid languages: {', '.join(rules.available())}")
    return code


def _channel(name: Optional[str]) -> Optional[str]:
    if name is None or not name.strip():
        return None
    name = name.strip().lower()
    if name not in rules.channels():
        raise Problem(f"unknown channel {name!r}; valid channels: {', '.join(sorted(rules.channels()))}")
    return name


def main(argv: Optional[List[str]] = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        args = _parser().parse_args(argv)
        language, channel = _language(args.lang), _channel(args.channel)
        text = _read(args.file)
        if not text.strip():
            raise Problem(EMPTY)
        result = scan.scan(text, language=language, channel=channel)
        output = report.render_json(result) if args.json else report.render_text(result)
    except Problem as problem:
        print(f"check.py: {problem}", file=sys.stderr)
        return 2
    except ValueError as error:  # a broken language or channel file
        print(f"check.py: {error}", file=sys.stderr)
        return 2
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
