# byline

Posts you would put your name on: eight skills for Claude Code and Codex, and a checker for AI tells
that needs no model.

## What we found

We first checked posts with the usual markers: a list of AI vocabulary ("leverage", "delve") and
phrases like "it's not X, it's Y". They flagged none of ten LinkedIn posts written by current Claude
models. Those posts share a template instead: a setup line that ends in a colon, a numbered list of
slogans, "isn't X. It's Y", and a closing question to the reader. The checker now looks for the
template. On a fresh holdout, run once, 10 of 10 human texts came out clean and 7 of 10 machine texts
were flagged: exactly the bar we set beforehand, at its minimum.
The set is small and narrow: posts from one model family (Claude Haiku, Sonnet and Opus 5.5) written
through an agent harness, and human blog essays published before November 2022.

| Holdout run | What the checker looked for | Human texts flagged | Machine texts flagged |
|---|---|---|---|
| 1 | local markers only: vocabulary, phrases, lists of three, dashes | 0 of 10 | 0 of 10 |
| 4 (fresh texts) | the same, plus the whole-post template | 0 of 10 | 7 of 10 |

"Flagged" means a label other than `clean`. Every run, including the three that failed, is in
[`reference/RESULTS.md`](reference/RESULTS.md).

## Try it in a minute

You need Python 3.9 or later and nothing else. From a copy of this repository, check the plain-request
post from the example (`tail` drops the two-line notice at the top of the file):

```bash
tail -n +3 examples/tamsin/plain-request-post.md | python3 skills/slop-check/scripts/check.py - --lang en --channel linkedin
```

```
byline slop-check: some AI tells (score 30/100)
Language: English (measured), 247 words, 10 paragraphs, 2 markers

Whole post
  line 9    setup        "Before you buy anything, do the unglamorous work:"
  line 11   maxim_list   "1. Give every location a name. Aisle, shelf, bin. Label the…"

This names patterns. It does not say who wrote the text.
```

To check your own text, run the same command with `-` and paste the text, then press Ctrl-D. For a
file, give its path:

```bash
python3 skills/slop-check/scripts/check.py my-post.md --lang en --channel linkedin
```

`--lang` is `en` or `ru`; `--channel` is `linkedin`, `x`, `threads`, `telegram` or `newsletter`;
`--json` prints JSON.

## Install

**Claude Code.** The marketplace is `byline-skills` and the plugin is `byline`:

```bash
claude plugin marketplace add ilyanemchenko/byline
claude plugin install byline@byline-skills
```

**Codex:**

```bash
codex plugin marketplace add ilyanemchenko/byline
codex plugin add byline@byline-skills
```

Both routes were run with a local clone of this repository as the source, under temporary
configuration folders, and both installed version 0.1.0 with its eight skills. The GitHub form above
is the same command with the repository's address; it could not be run before the repository was
public.

**Other agents.** The cross-agent installer from the `skills` project documents
`npx skills add ilyanemchenko/byline`. It was not tested here.

**No agent.** The checker is one Python script with no dependencies:
`python3 skills/slop-check/scripts/check.py`.

## The eight skills

| Skill | What it does | Reads | Writes |
|---|---|---|---|
| `person-interview` | Interviews you about your work, one question at a time, and saves only what you said | `byline/person.md` if it exists | `byline/person.md` |
| `topic-scout` | Finds topics where recent news in your field meets something you did; with no web search it says so and works from your file | `byline/person.md`, the web | nothing |
| `angle-brainstorm` | Offers three angles on a topic, each standing on your own facts, and prints the one you pick as an angle card | `byline/person.md` | the angle card, in the chat |
| `post-writer` | Writes the post from the angle card and your facts, inside the channel's limit | `byline/person.md`, the angle card | `byline/drafts/YYYY-MM-DD-<slug>.md` |
| `post-fact-check` | Lists every claim about you in a draft, checks it against your file and asks about each one it cannot confirm | the draft, `byline/person.md` | the draft, only where you decide |
| `post-editor` | Gives at most seven editorial notes on the opening, the example, tangled sentences, repetition and the ending | the draft, `byline/person.md` | the draft, only the notes you choose |
| `slop-check` | Runs the checker and explains each flag in plain words; offers to rewrite only the flagged places | the draft or pasted text | nothing unless you ask for a rewrite |
| `new-post` | Runs the others in order and stops for your decision at each step | as each step | as each step |

A skill that finds a basic missing from your file, or hears a new fact from you, asks before adding it
to `byline/person.md`. No skill posts anything anywhere: you sign and publish the post yourself.

The chain: `person-interview` (if there is no person file), `topic-scout` (if you have no topic),
`angle-brainstorm`, `post-writer`, `post-fact-check`, `post-editor`, `slop-check`.

## Before and after

The example person is invented: Tamsin Ashgrove, a warehouse consultant. Both posts below were checked
with `--lang en --channel linkedin`.

| Post | Label | Score |
|---|---|---|
| From a plain one-line request, no person file | some AI tells | 30/100 |
| From byline, with her person file | clean | 0/100 |

The byline post in full:

> Founders and ops leads shipping 500 to 5,000 orders a month: before you buy warehouse software, make sure someone knows where everything lives.
>
> In 2023 I told two clients to buy a warehouse system. They spent weeks setting it up. Within three months both had gone back to spreadsheets.
>
> The software was fine. Nobody knew where anything lived.
>
> I used to push software on people too early. Since then I don't recommend it to brands under 1,000 orders a month. I fix the shelves and the labels first.

It differs because it was written from her own numbered facts, and each specific in it traces to one
of them (`S1` and `F7`). The plain-request post invents a brand, a price and a percentage. Every file
of the run is in [`examples/tamsin/`](examples/tamsin/).

## How the check works

- It finds local markers: stock vocabulary, the "it's not X, it's Y" formula, lists of three, runs of
  very short sentences, too many dashes, too many hashtags.
- It finds the template of a whole post: a setup line, a list of slogans, two or more contrast
  formulas, a closing cliché or question to the reader, a last line of hashtags.
- Score: 25 for each flagged paragraph (one that stacks several markers), plus 3 for each local marker (each
  weighs less in a post over 200 words), plus 15 for each template pattern, at most 100. Below 20 is
  `clean`, below 50 `some`, from 50 `heavy`.

This names patterns. It does not say who wrote the text.

Details: [`docs/how-the-check-works.md`](docs/how-the-check-works.md). The texts it was measured on:
[`reference/`](reference/).

## How it was tested

- **Unit tests:** `python3 -m pytest` runs 166 tests, all passing, on Python 3.9.6. The CI workflow is set
  up to run them on 3.9 and 3.12.
- **Reference set:** 46 tuning texts (26 human, 20 machine) and a holdout of 20 (10 human, 10 machine).
  The bar, fixed before the holdout run: no human text `heavy`, at most 2 human texts `some`, at least
  7 of 10 machine texts not `clean`. The holdout gave 10 human texts `clean`, and 7 machine texts
  `some` with 3 `clean`. That holdout is now spent: a change to any rule needs a new one.
- **Quality run:** fresh agents ran each skill for three invented people (English for LinkedIn, English
  for X, Russian for Telegram) who answered from a script, with two false claims planted in each draft
  for the fact check, and a separate agent judged the results. Of 26 checks, 21 passed, none failed and
  5 were not run: two editor runs were stopped by the model provider's safety filter, and three
  rewrite steps had nothing to rewrite. The record and the fixes it led to are in
  [`docs/quality-run.md`](docs/quality-run.md).
- **Install:** `claude plugin validate .` passes, and both install routes above worked from a local
  clone. Not verified: that Claude Code or Codex loads and triggers the skills in a live session (no
  model call could be made from the test machine), the ChatGPT app, uploading a skill folder to the
  Claude app, and the cross-agent installer.

## Languages

- **English:** measured on the reference set above.
- **Russian:** beta. The rules are written but not measured; the report says so.
- **Add one:** a language is one JSON file of word lists and patterns. See
  [`docs/add-a-language.md`](docs/add-a-language.md).

## Limits

- It names patterns; it does not say who wrote a text. People write setup lines too.
- The numbers come from one model family and from blog essays. Other models and other human writing
  may score differently.
- Built for posts of up to about 600 words.
- Some patterns slip through: emoji bullets are not read as a list, and a closing question without
  "you" or "your" is not caught.

The full list is under [Known limits](docs/how-the-check-works.md#known-limits).

## Contributing

False alarms, new languages and reference texts are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md),
and [`docs/blind-test.md`](docs/blind-test.md) for a reader test you can run yourself.

## Licence

Apache-2.0. See [`LICENSE`](LICENSE).

Made by [Ilya Nemchenko](https://github.com/ilyanemchenko).
