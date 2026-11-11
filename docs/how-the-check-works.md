# How the check works

`skills/slop-check/scripts/check.py` reads a post and names the patterns that make prose read as
machine-written. It uses no model, needs nothing outside the Python standard library, and sends the text
nowhere. The rules for each language are data in `skills/slop-check/rules/<code>.json`; the code is in
`skills/slop-check/scripts/slopcheck/`.

This names patterns. It does not say who wrote the text.

## How a text is read

1. **Normalised.** Lower case; typographic quotes, guillemets and no-break spaces folded to plain ones;
   Latin diacritics dropped; `ё` read as `е`. Every character maps to exactly one character, so every
   flag points at the original text.
2. **Split.** Paragraphs are separated by blank lines. Sentences end at `.`, `!`, `?`, `…` or a line break.
3. **Prose only.** The list, fragment and setup checks read a copy where headings, `>` quote lines,
   list items, any line that opens on a symbol or emoji, links, hashtags and `*`/`_`/`` ` `` markup are
   blanked out. A bullet list is not three fragments, and a heading is not a sentence.

## Local markers

Each of these is found where it occurs and counts as one marker.

| Code | What it finds | Example |
|---|---|---|
| `vocab` | A word or phrase from the language's `vocab` list, in any listed form ("leverage", "leveraged", "leveraging"). Not counted inside quotation marks or on a `>` line, nor when one of the six words before it in its clause rejects it ("stop saying game-changer"). | "We **leverage** our data." |
| `contrast` | The "it's not X, it's Y" formula and its relatives. The opening sentence of the post may have one. | "It's not about speed, it's about trust." |
| `triad` | A list of three: three comma items of up to four words; one line holding exactly three short sentences; or three one-sentence paragraphs in a row that open on the same word or all end on `?` or `!`. | "We made it faster, cheaper, calmer." |
| `fragments` | Three or more sentences in a row of up to three words each, in one paragraph, outside a list of three. | "We shipped. We learned. We grew." |
| `dash` | More than one dash per 100 words and at least two dashes (Russian: more than four per 100 and at least four). An em dash, an en dash or a hyphen with spaces on both sides counts, except a dash that opens its line, one right after `.`, `!`, `?`, `…` or `,` (dialogue attribution) and a number range (2019–2021). Counted on the whole text, list items included. One flag per post. | "Speed — and trust — and focus." in a 30-word post |
| `hashtags` | More hashtags than the channel takes: LinkedIn 5, X 2, Threads 1, Telegram 3, newsletter 0, and 5 with no channel. | Six hashtags on LinkedIn |

`over_limit` marks text past the channel's character limit (LinkedIn 3000, X 280, Threads 500,
Telegram 4096, newsletter none). It is shown, but it is not a marker and does not change the score.

## Whole-post patterns

These are the template of a whole post. Each code counts once, however many times it occurs.

| Code | What it finds | Example |
|---|---|---|
| `setup` | A line of 2 to 12 words ending in a colon, with prose somewhere after it in the post; or a question of up to five words answered on the same line by a sentence that is not a question. | "Here is what I learned:" / "The result? Chaos." |
| `maxim_list` | Three or more list items in a row whose first sentence has at most eight words. Blank lines between items are fine; a paragraph of prose or an item with a long first sentence ends the run. | "1. Ship small. 2. Ask early. 3. Sleep well." |
| `contrast_run` | Two or more `contrast` flags in one post (the exempt opener is not among them). | Two "it's not X, it's Y" sentences |
| `closer` | On the last line that has letters (hashtags and links ignored): a closing cliché from the language's `closers` list, or a question that addresses the reader with one of the language's `reader_words`. A last line that is a list item is never a closer. With no language, any closing question counts. | "Thoughts?" / "What would you do?" |
| `hashtag_row` | The last non-empty line is three or more hashtags and nothing else. | "#leadership #growth #mindset" |

## When a paragraph is flagged

A paragraph is flagged (`density`) when it holds three or more of `vocab`, `contrast`, `triad` and
`fragments`. The `dash` flag adds one to the paragraph with the most dashes. Lists of three also flag on
their own: two in one paragraph, or three anywhere in the post, flag the paragraph that has the most of
them. One marker is never a verdict.

## Score and label

```
score = min(100, 25 * flagged_paragraphs
                 + round(3 * local_markers * min(1.0, 200 / max(words, 1)))
                 + 15 * template_patterns)
```

- `flagged_paragraphs`: paragraphs flagged as above.
- `local_markers`: the flags with codes `vocab`, `contrast`, `triad`, `fragments`, `dash`, `hashtags`.
  In a post longer than 200 words each one weighs less, in proportion.
- `template_patterns`: the number of distinct whole-post codes found, from 0 to 5.

| Score | Label | Printed as |
|---|---|---|
| 0–19 | `clean` | clean |
| 20–49 | `some` | some AI tells |
| 50–100 | `heavy` | heavy AI tells |

One whole-post pattern alone scores 15 and stays `clean`: a single setup line is something people write
too. The `markers` number in the report is local markers plus distinct template patterns.

Worked example, 22 words: a `setup`, a `closer`, one `vocab`, one `contrast` and one `fragments`, no
flagged paragraph. Score = 0 + round(3 × 3 × 1.0) + 15 × 2 = 39, `some`.

The constants live at the top of `slopcheck/scan.py` (`PARAGRAPH_WEIGHT`, `MARKER_WEIGHT`,
`WORDS_SCALE`, `TEMPLATE_WEIGHT`, `SOME_FROM`, `HEAVY_FROM`) and in `slopcheck/template.py`.

## Languages

| Code | Language | Status |
|---|---|---|
| `en` | English | `measured`: passed the release bar on a holdout (see below) |
| `ru` | Russian | `beta`: rules written, not measured on a reference set; the report says so |

**Detection.** Without `--lang`, the script counts each language's `detect_markers` (common words) in the
text. A language is chosen only with at least 3 distinct markers and a lead of 2 over the next language.
Otherwise the language is unknown, a note says so, and only structure is checked: dashes, lists of three,
fragments, hashtags and the whole-post patterns, but no vocabulary and no contrast. Short posts often go
unrecognised, so pass `--lang` whenever a rules file exists for the text's language; it always wins over
detection.

To add a language, see `add-a-language.md`.

## Known limits

- **It names patterns. It does not say who wrote a text.** People write setup lines and lists of three;
  a model can write a post with none. A label is a count of patterns, never a finding about authorship.
- **Built for posts of up to about 600 words.** Longer texts are scored, but the weights were set on
  posts, and loose markers weigh less the longer the text.
- **Quoted text is skipped.** Vocabulary inside quotation marks or on a `>` line is not counted, and a
  `>` line is left out of every structure check. A contrast formula inside inline quotation marks is
  still counted.
- **A setup line counts only when prose follows it somewhere later in the post.** So a colon line
  followed only by a list ("Three things matter:" and then bullets) is not flagged.
- **A short question counts as a setup only when it is answered on the same line.** "The result? Chaos."
  is flagged; the same question with its answer on the next line is not.
- **List items are lines that start with a number (`1.` or `1)`) or with `-`, `*` or `•`.** Emoji
  bullets are not seen as lists, so a list of slogans behind emoji is not a `maxim_list`, and a closing
  question in an emoji item still counts as a closer.
- **The reader words for a closing question are a fixed list** per language (English: you, your,
  you've, you're, yours). A closing question that addresses the reader without one of them is not caught.
- **The numbers come from one model family and from blog essays.** The machine texts were written by
  Claude models (Haiku, Sonnet, Opus 5.5) through an agent harness from a one-line prompt; the human
  texts are blog essays by three authors published before November 2022. `reference/README.md`
  explains both limits. Other models and other kinds of human writing may score differently.

## Where the reference numbers live

- `reference/README.md`: the reference set, its sources and licences, the tuning rules and the release
  bar (on the holdout: no human text `heavy`, at most 2 human texts `some`, at least 7 of 10 machine texts
  not `clean`).
- `reference/RESULTS.md`: every holdout run, including the failed ones, and the tuning-set numbers. The
  English rules passed on a fresh holdout of 10 human and 10 machine texts: human 10 `clean`; machine 7
  `some` and 3 `clean`, exactly the minimum.
- `python3 -m pytest tests/test_reference_set.py` re-runs the bar.
