# Results

The release bar, on a holdout that whoever tunes the rules never sees: no human text `heavy`, at most 2
human texts `some`, at least 7 of 10 machine texts not `clean`.

## Holdout runs

Runs 1–3 used the first holdout (the even ids of the first 40 texts); tuning used the odd ids only.

| # | Date | Commit | Human heavy | Human some | Machine not clean | Bar | What changed before this run |
|---|---|---|---|---|---|---|---|
| 1 | 2026-11-11 | 482a8e1 + reference set (uncommitted) | 0 | 0 | 0 | fail | nothing: the first rules, before any tuning |
| 2 | 2026-11-11 | 482a8e1 + round 1 (uncommitted) | 0 | 1 (h20) | 6 | fail | round 1: three markers added (closing question to the reader, "here is what/where" at a line start, contrast "isn't X. It's Y"); `MARKER_WEIGHT` 3 → 16 |
| 3 | 2026-11-11 | 482a8e1 + round 2 (uncommitted) | 0 | 0 | 6 | fail | round 2: "here is what/where" anywhere; `MARKER_WEIGHT` 16 → 17; vocabulary entry "simply" removed (fired on tune human h15) |

After run 3 the first holdout was folded into the tuning set, and a fresh holdout was collected by a
separate agent that did not tune the rules. The next row is the one run of that fresh holdout against the
frozen commit.

| # | Date | Commit | Human heavy | Human some | Machine not clean | Bar | What changed before this run |
|---|---|---|---|---|---|---|---|
| 4 | 2026-11-11 | 56b643a | 0 | 0 | 7 | **pass** | fresh holdout (h27–h36, m21–m30); whole-post template patterns, all 46 earlier texts as the tuning set |

## Fresh holdout (run 4)

This holdout was run once, on 2026-11-11, by the maintainer (not by the agent that tuned the rules),
with `check.py --lang en --json` against the frozen commit 56b643a. No rule, constant, pattern or tuning text
changed after that run.

| id | label | score | | id | label | score |
|---|---|---|---|---|---|---|
| h27 | clean | 0 | | m21 | some | 35 |
| h28 | clean | 1 | | m22 | some | 30 |
| h29 | clean | 1 | | m23 | some | 45 |
| h30 | clean | 2 | | m24 | some | 47 |
| h31 | clean | 2 | | m25 | some | 32 |
| h32 | clean | 1 | | m26 | some | 45 |
| h33 | clean | 0 | | m27 | clean | 2 |
| h34 | clean | 0 | | m28 | clean | 17 |
| h35 | clean | 15 (one `setup`) | | m29 | some | 30 |
| h36 | clean | 1 | | m30 | clean | 17 |

Bar: human `heavy` 0 (needs 0), human `some` 0 (at most 2), machine not `clean` 7 (at least 7).
**The bar passed, but only just on the machine side: 7 of 10 is exactly the minimum.** Three machine posts
read as clean: m27 (score 2), m28 and m30 (17 each, one template pattern and one marker). The human side
had room to spare: all 10 clean, the highest at 15.

Running `python3 -m pytest tests/test_reference_set.py` on this commit gives the same labels.

### The first checker on the same fresh texts

Runs 1 and 4 used different texts. For a comparison on the same texts, the checker of commit 482a8e1
(the one run 1 used) was run afterwards on the fresh holdout, on 2026-11-12. This is a comparison only:
it changes no rule and is not a second run of the bar.

| Commit | Human heavy | Human some | Machine not clean | Bar |
|---|---|---|---|---|
| 482a8e1 | 0 | 0 | 0 | would fail |

Its scores: h27–h36 0, 3, 1, 2, 2, 1, 2, 0, 0, 1; m21–m30 3, 0, 0, 0, 0, 2, 2, 2, 0, 0. All 20 are `clean`.

## Tuning set

All 46 texts in `manifest.json` (26 human, 20 machine) with `split: tune`, measured with the rules in
this commit: `MARKER_WEIGHT` back to 3, the five whole-post template patterns added with
`TEMPLATE_WEIGHT` = 15. Targets: no human `heavy`, at most 2 human `some`, at least 80% of machine texts
not `clean`.

| Class | clean | some | heavy |
|---|---|---|---|
| human (26) | 26 | 0 | 0 |
| machine (20) | 1 | 16 | 3 |

Machine texts not clean: 19 of 20 (95%). The one clean machine text is m19 (one template pattern, score 15).
Human scores, highest first: h21 18; h09, h22 17; h02, h04, h07, h12, h14, h17 15; the rest 3 or less.
Nine human texts carry one template pattern, mostly a `setup` line ("Here's what happens:",
"Is this easy? No."), so they score 15–18, just under the `some` band at 20.

`TEMPLATE_WEIGHT` on the tuning set: at 10 → humans 26 clean, machine 18 not clean; at 15 → 26 / 19;
at 18 → 3 humans `some` (h09, h21, h22). It stays 15.

### Admission check of the kept lexical changes

Once the first holdout was folded in, the three lexical changes kept from tuning rounds 1 and 2 were
checked again against the whole tuning set, with the same rule: at least 3 tuning machine texts, no
tuning human text.

- Contrast shape "X isn't Y. It's Z": the shape with `isn't|aren't|doesn't|don't|wasn't|won't` fired on
  human h14 ("don't feel like doing anything … It's almost as if"). It was narrowed to the copula only,
  `isn't|aren't … . It's|They're|That's`, which finds 6 machine texts (8 hits) and no human text.
- "here is what": it occurs in 8 machine texts and in no human text. The checker flags it in 7: in the
  eighth, m16, it is inside quotation marks, which the checker skips. It is kept.
- "here is where": 1 machine text, no human text. It falls short of 3 machine texts and is removed.
- The removal of "simply" stands.

The class totals above did not change. h14 went from 17 to 15, and m13 from 32 to 30.

## What the vocabulary list does on this set

On all 66 texts, the vocabulary list fires more often on the human texts than on the machine texts.
13 of 36 human texts have at least one `vocab` hit ("deeply", "empowering", "leverage", "tapestry",
"realm", "navigate" and others). In the 30 machine texts the only hit is "here is what", added during
tuning, in 10 of them. No text in the set has a flagged paragraph, so the paragraph weight of 25 is not
exercised here. The older entries stay because they weigh little (3 points a hit, less in a long post),
change no label in this set (every human text is `clean` with them), and still describe the stock words
of older machine text, which this set does not measure. "here is what" does change two labels: without
it m08 would be `some` (48) and m11 `clean` (18).
