This person is invented. Any likeness to a real person or company is accidental.

# Example: one post for an invented person

Tamsin Ashgrove runs a one-person warehouse consultancy in Bristol. She, her firm and her clients were
invented for the quality run (see `docs/quality-run.md`). An agent played her and answered from a
script; separate agents ran the skills, one skill each.

Files in `tamsin/`:

| File | What it is | Made by |
|---|---|---|
| `person.md` | Her person file: basics, facts `F1`–`F7`, stories `S1`–`S3`, off-limits items `X1`–`X3` | `person-interview` |
| `angle-card.txt` | The angle she picked, standing on `F7` and `S1` | `angle-brainstorm` |
| `byline-post.md` | The post | `post-writer` |
| `byline-check.txt` | The checker's report on `byline-post.md` | `slop-check` (its script) |
| `plain-request-post.md` | A post on the same topic from a plain one-line request, with no person file | Claude Sonnet 5.5, see below |
| `plain-request-check.txt` | The checker's report on `plain-request-post.md` | `slop-check` (its script) |

After `post-writer`, three more skills ran and changed nothing. `post-fact-check` ran on a copy of the
draft with two false claims added on purpose, and reported both. `post-editor` gave one note
(repetition); it was not applied. `slop-check` found nothing to flag. So the post is the first draft.

Every specific in `byline-post.md` traces to the person file: the reader line to `Audience` under
`## Basics`; 2023, the two clients, the weeks of setup, the three months and the return to
spreadsheets to `S1`; "under 1,000 orders a month" and "the shelves and the labels" to `F7` and `S1`.
Nothing from `## Off limits` appears.

The plain-request post was written on 2026-11-12 by a fresh Claude Sonnet 5.5 agent from the prompt
`Write a LinkedIn post in English about why a small e-commerce brand should sort out its warehouse before buying warehouse software.`
and an instruction to save the post and nothing else. Its brand, its $18,000 and its 8% come from no
one's work.

Both reports came from this command, run on the post text before the two-line notice at the top of
each file was added:

```bash
python3 skills/slop-check/scripts/check.py <file> --lang en --channel linkedin
```

To rerun it on a file here, drop the notice first:

```bash
tail -n +3 examples/tamsin/byline-post.md | python3 skills/slop-check/scripts/check.py - --lang en --channel linkedin
```
