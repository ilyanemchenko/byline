# Contributing

Thank you for helping. The most useful contributions are false alarms with their text, new languages,
and reference texts from models other than Claude.

## Run the tests

You need Python 3.9 or later and `pytest`. The checker itself uses only the standard library.

```bash
python3 -m pip install pytest
python3 -m pytest
```

`pyproject.toml` puts `skills/slop-check/scripts` on the import path, so run the command from the
repository root. `tests/test_reference_set.py` re-runs the release bar on the reference holdout, and
`tests/test_skills_lint.py` checks the skill files: front matter, size and the sentences every skill must keep.

Ground rules for code: the checker stays dependency-free and runs on Python 3.9; every module starts
with `from __future__ import annotations`; every file stays under 400 lines.

## Add a language

A language is one JSON file in `skills/slop-check/rules/`. Follow
[`docs/add-a-language.md`](docs/add-a-language.md): copy `en.json`, fill the lists, set
`"status": "beta"`, validate the file, add `tests/test_scan_<code>.py`, run the suite. A language
becomes `measured` only after its own reference set passes the release bar on a holdout.

## Add reference texts

The reference set is in `reference/`, described in [`reference/README.md`](reference/README.md).

- **Human texts** must be published before model-written text became common (for English, before
  November 2022), and under a licence that lets them be copied into this repository: public domain or
  CC0, as the current set is. Record the author, title, URL, publication date, licence, licence URL and
  the date you fetched it. Cut whole paragraphs only and change nothing inside them.
- **Machine texts** are written from the one-line prompt `Write a LinkedIn post in English about
  {topic}.` with no system prompt, style hint or example. Record the model, the tool, the prompt and the
  date. Posts from model families other than Claude are the most wanted: today every machine text comes
  from Claude.
- Add one row per text to `reference/manifest.json` with `split: "tune"`. New texts join the tuning
  set; they do not change the spent holdout.

**A change to a rule, constant or pattern needs a new holdout.** The current holdout has been run and
is spent. Tune on the tuning set only. A new marker is admitted only if it occurs in at least 3 tuning
machine texts and in no tuning human text. Then collect a fresh holdout of 10 human and 10 machine
texts, by someone who did not tune the rules, run it once, and record the result in
`reference/RESULTS.md`, pass or fail.

## Report a false alarm

Open an issue with:

1. **The text**, exactly as you checked it. Share only text you may share: your own post, or a public
   one with its link. Remove anything private.
2. **The command** you ran, with its `--lang` and `--channel`.
3. **The full report** the checker printed (or its `--json` output).
4. **Which flag is wrong and why**, in a sentence: for example, "this colon line is a heading, not a
   setup".

A report with the text and the output can be turned into a test. A report without them usually
cannot.

## Skills

Each skill is one folder in `skills/` with a `SKILL.md` under 400 lines. Its front matter uses only
`name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`, and `name` equals
the folder name. A change to a skill's wording should come with a run of the skill by an agent that has
not seen it, as in [`docs/quality-run.md`](docs/quality-run.md).
