---
name: slop-check
description: Use when someone asks whether a post, draft or other short text sounds AI-written, generic or templated, wants AI tells, slop or cliches found in it, or wants a draft checked before publishing on LinkedIn, X, Threads, Telegram or a newsletter.
license: Apache-2.0
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/check.py *)
---

# Slop check

## Overview

A script in this skill reads a text and names the patterns that make prose read as machine-written:
stock vocabulary, "it's not X, it's Y", lists of three, runs of fragments, heavy dashes, and the
template of a whole post (a setup line, a list of slogans, a closing question to the reader). It
uses no model and sends nothing anywhere. It gives a score from 0 to 100 and a label.

This names patterns. It does not say who wrote the text. A human can write a `heavy` post and a model
can write a `clean` one, so never tell the person, or hint, that they or anyone else wrote it with AI.

## The script

- Claude Code: `python3 ${CLAUDE_SKILL_DIR}/scripts/check.py`
- Every other agent: `scripts/check.py` relative to this skill's folder, run with `python3`
  (for example `python3 <folder of this SKILL.md>/scripts/check.py`).

```
python3 ${CLAUDE_SKILL_DIR}/scripts/check.py [FILE | -] [--lang CODE] [--channel NAME] [--json]
```

Exit 0 means a report was printed, whatever the label. Exit 2 means a bad `--lang` or `--channel`
(the message lists the valid ones), an unreadable file, or an empty text.

## Steps

1. **Get the text.** A file path: pass it as `FILE`. Pasted text: send it on standard input through a
   quoted heredoc, so the shell changes nothing in it (no `$`, backtick or `\` expansion):

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/check.py --lang en --channel linkedin - <<'BYLINE_TEXT'
   the pasted text, exactly as given
   BYLINE_TEXT
   ```

   If a line of the text is exactly `BYLINE_TEXT`, pick another end word.

2. **Pass `--lang`.** Decide the text's language yourself. If `rules/<code>.json` exists in this skill's
   folder for that language code (today: `en`, `ru`), pass `--lang <code>`. Always do this: the script
   detects a language only from several common words, so a short post often comes back as "Language:
   unknown" and loses its vocabulary and contrast checks. If no rules file exists for the language,
   leave `--lang` out and tell the person that only structure was checked.

3. **Pass `--channel` only when the person named one:** `linkedin`, `x`, `threads`, `telegram` or
   `newsletter`. It adds the channel's character limit and hashtag maximum. Never guess a channel.

4. **Report in plain words.** Give the label and the score first, then each flagged place: quote it
   and say in one line what the pattern is. Use the table below, not the raw codes. Pass on any note
   the script printed (unknown language, beta rules). End with the script's last line, the sentence
   that it does not say who wrote the text.

5. **Offer a rewrite of the flagged places only.** Change only the flagged words and sentences.
   Keep every fact, number, name, date and claim as it is, keep the person's voice, and touch nothing
   outside the flagged places. Ask before rewriting; do not rewrite unasked.

6. **After a rewrite, run the check again** on the new text with the same options and show both
   results: "before: some AI tells (score 39/100), after: clean (score 0/100)". If a flag remains,
   say so; do not hide it.

## What the flags mean

The script prints whole-post patterns first, under `Whole post`, then flags by paragraph.

| Code | Say it like this |
|---|---|
| `vocab` | a stock word or phrase common in machine prose ("leverage", "here is what") |
| `contrast` | the "it's not X, it's Y" formula (the opening sentence is allowed one) |
| `triad` | a list of three short items or three short sentences in a row |
| `fragments` | three or more very short sentences in a row |
| `dash` | more than one dash per hundred words (and at least two) |
| `hashtags` | more hashtags than the channel takes (five with no channel) |
| `over_limit` | longer than the channel allows |
| `density` | this paragraph stacks several of the patterns above |
| `setup` | a short line ending in a colon that announces what follows, or a short question answered at once ("The result? Chaos.") |
| `maxim_list` | a list of three or more items that each open on a short slogan |
| `contrast_run` | the "it's not X, it's Y" formula used two or more times |
| `closer` | a closing cliche or a closing question to the reader ("Thoughts?") |
| `hashtag_row` | the post ends on a line of hashtags only |

Labels: `clean` (below 20), `some AI tells` (20 to 49), `heavy AI tells` (50 and above). For the score
formula and the limits of the check, see `docs/how-the-check-works.md` in the repository.

## Example

```
byline slop-check: some AI tells (score 39/100)
Language: English (measured), 22 words, 3 paragraphs, 5 markers

Whole post
  line 1    setup        "Here is what I learned:"
  line 5    closer       "What would you do?"

Paragraph 1
  line 1    vocab        "Here is what"

Paragraph 2
  line 3    contrast     "It's not about speed, it's"
  line 3    fragments    "We shipped. We learned. We grew."

This names patterns. It does not say who wrote the text.
```

Tell the person: "Some AI tells, 39 of 100. The opening line 'Here is what I learned:' announces
the post instead of starting it. 'It's not about speed, it's about trust' is the not-X-but-Y formula.
'We shipped. We learned. We grew.' is a run of very short sentences. The post ends on a question to the reader. Want
me to rewrite just these four places, keeping every fact?"

## No python3

If `python3` is not available, say so plainly, then do the pass by hand: read `rules/<code>.json` for
the text's language and look for its `vocab`, `contrast` and `closers` entries, plus the structural
patterns in the table above. Say that this was a manual pass with no score.

## Common mistakes

- Leaving out `--lang` on a short post: the language goes unrecognised and half the checks are skipped.
- Reading the label as a verdict on authorship. It is a count of patterns.
- Rewriting the whole post when asked to fix flags, or changing a fact while rewording.
- Showing only the new score after a rewrite: show before and after.
- Pasting text into the command without a quoted heredoc, so `$` or backticks in the post change it.
