# Results

The release bar, on a holdout the tuner never sees: no human text `heavy`, at most 2 human texts `some`,
at least 7 of 10 machine texts not `clean`.

## Holdout runs

Runs 1–3 used the first holdout (the even ids of the first 40 texts); tuning used the odd ids only.

| # | Date | Commit | Human heavy | Human some | Machine not clean | Bar | What changed before this run |
|---|---|---|---|---|---|---|---|
| 1 | 2026-11-11 | c784869 + reference set (uncommitted) | 0 | 0 | 0 | fail | nothing: the rules as shipped by Tasks 1–6 |
| 2 | 2026-11-11 | c784869 + round 1 (uncommitted) | 0 | 1 (h20) | 6 | fail | round 1: three markers added (closing question to the reader, "here is what/where" at a line start, contrast "isn't X. It's Y"); `MARKER_WEIGHT` 3 → 16 |
| 3 | 2026-11-11 | c784869 + round 2 (uncommitted) | 0 | 0 | 6 | fail | round 2: "here is what/where" anywhere; `MARKER_WEIGHT` 16 → 17; vocabulary entry "simply" removed (fired on tune human h15) |

After run 3 the first holdout was folded into the tuning set, and a fresh holdout was collected by agents
the tuner does not control. The next row is the one run of that fresh holdout against the frozen commit.

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
at 18 → 4 humans `some`. It stays 15.

### Admission check of the kept lexical changes

Once the first holdout was folded in, the three lexical changes kept from Task 7 were checked again
against the whole tuning set, with the same rule: at least 3 tuning machine texts, no tuning human text.

- Contrast shape "X isn't Y. It's Z": the shape with `isn't|aren't|doesn't|don't|wasn't|won't` fired on
  human h14 ("don't feel like doing anything … It's almost as if"). It was narrowed to the copula only,
  `isn't|aren't … . It's|They're|That's`, which finds 6 machine texts (8 hits) and no human text.
- "here is what": 8 machine texts, no human text. It is kept.
- "here is where": 1 machine text, no human text. It falls short of 3 machine texts and is removed.
- The removal of "simply" stands.

The class totals above did not change. h14 went from 17 to 15, and m13 from 32 to 30.
