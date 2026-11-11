# Reference set

These are the texts that the English rules of the slop check are measured on. Human texts are posts that
real people published before November 2022. Machine texts are LinkedIn posts that a language model wrote
from a one-line prompt. A language counts as `measured` only if it has a reference set and passes the
release bar on a holdout that the tuner never saw.

This names patterns. It does not say who wrote the text.

## Files

- `manifest.json` has one row per text: `id`, `class` (`human` | `machine`), `split` (`tune` | `holdout`),
  `file` and `words`. Human rows add `author`, `title`, `url`, `published`, `licence`, `licence_url` and
  `retrieved`. Machine rows add `model`, `tool`, `prompt`, `generated` and `wrapper_removed`.
- `en/human/h01.txt` … `h26.txt` and `en/machine/m01.txt` … `m20.txt` are plain UTF-8, with paragraphs
  separated by blank lines.
- `RESULTS.md` records every holdout run and the numbers on the tuning set.

## Human texts: sources and licences

All pages were fetched on 2026-11-11. The licence statement of each source was read on its own page on
the same day.

| Author | Licence | Licence page |
|---|---|---|
| Leo Babauta (zenhabits) | Public domain: the whole blog has been "uncopyrighted" since January 2008 | https://zenhabits.net/uncopyright/ |
| Steve Pavlina | Public domain: articles on the site from 2004-10-01 to 2024-05-20, text only | https://stevepavlina.com/uncopyright/ |
| Gwern Branwen | CC0 (Creative Commons public domain) | https://gwern.net/about |

| id | Author | Post | Published | Words |
|---|---|---|---|---|
| h01 | Leo Babauta | [Give Up Comfort](https://zenhabits.net/comfort/) | 2018-09 | 261 |
| h02 | Steve Pavlina | [Showing Up](https://stevepavlina.com/blog/2006/12/showing-up/) | 2006-12-26 | 231 |
| h03 | Gwern Branwen | [On Having Enough Socks](https://gwern.net/socks) | 2017-11-22 | 182 |
| h04 | Leo Babauta | [The Best Things I've Learned About Raising Children](https://zenhabits.net/childs/) | 2019-01 | 264 |
| h05 | Steve Pavlina | [Never Put Profits First](https://stevepavlina.com/blog/2013/12/never-put-profits-first/) | 2013-12-21 | 280 |
| h06 | Gwern Branwen | [Console Insurance Is A Ripoff](https://gwern.net/console-insurance) | 2009-03-10 | 417 |
| h07 | Leo Babauta | [Cooking Healthful Joyful Meals with a Picky Family](https://zenhabits.net/picky/) | 2019-02 | 401 |
| h08 | Steve Pavlina | [How Many Days Can You Go Without Checking Email or Social Media?](https://stevepavlina.com/blog/2013/11/how-many-days-can-you-go-without-checking-email-or-social-media/) | 2013-11-18 | 159 |
| h09 | Leo Babauta | [Simplify Technology with Limits](https://zenhabits.net/tech-limits/) | 2018-12 | 317 |
| h10 | Steve Pavlina | [Mile Wide, Mile Deep](https://stevepavlina.com/blog/2016/12/mile-wide-mile-deep/) | 2016-12-27 | 274 |
| h11 | Gwern Branwen | [Choosing Software](https://gwern.net/choosing-software) | 2008-09-26 | 328 |
| h12 | Leo Babauta | [The Incredible Progress of Daily Practice](https://zenhabits.net/progress/) | 2017-10 | 415 |
| h13 | Steve Pavlina | [Turning Weaknesses Into Strengths](https://stevepavlina.com/blog/2016/12/turning-weaknesses-strengths/) | 2016-12-13 | 364 |
| h14 | Leo Babauta | [The Practice of Truly Enjoying Time Off](https://zenhabits.net/time-off/) | 2021-06 | 386 |
| h15 | Steve Pavlina | [Little Luxuries](https://stevepavlina.com/blog/2019/11/little-luxuries/) | 2019-11-27 | 339 |
| h16 | Gwern Branwen | [Laws of Tech: Commoditize Your Complement](https://gwern.net/complement) | 2018-03-17 | 207 |
| h17 | Leo Babauta | [The Destructive Habit of Evaluating Everything We Do](https://zenhabits.net/evaluating/) | 2017-08 | 370 |
| h18 | Steve Pavlina | [Social Networking: Rethinking Productivity](https://stevepavlina.com/blog/2009/11/social-networking-rethinking-productivity/) | 2009-11-23 | 156 |
| h19 | Steve Pavlina | [Learning About Fashion](https://stevepavlina.com/blog/2009/12/learning-about-fashion/) | 2009-12-02 | 411 |
| h20 | Leo Babauta | [Becoming Nimble at Dealing with Ever-Changing Plans](https://zenhabits.net/everchange/) | 2021-08 | 383 |
| h21 | Leo Babauta | [Moving From Desire to Action](https://zenhabits.net/action-star/) | 2022-09 | 433 |
| h22 | Steve Pavlina | [Setting Your Primary Focus](https://stevepavlina.com/blog/2006/12/setting-your-primary-focus/) | 2006-12-31 | 384 |
| h23 | Gwern Branwen | [A/B testing long-form readability on Gwern.net](https://gwern.net/ab-test) | 2012-06-16 | 355 |
| h24 | Leo Babauta | [The Ridiculous Effectiveness of Singleminded Devotion to a Purpose](https://zenhabits.net/devotion/) | 2022-09 | 402 |
| h25 | Steve Pavlina | [Triage](https://stevepavlina.com/blog/2006/12/triage/) | 2006-12-21 | 426 |
| h26 | Gwern Branwen | [Hydrocephalus and Intelligence: The Hollow Men](https://gwern.net/hydrocephalus) | 2015-07-28 | 346 |

How the excerpts were cut:

- **Whole paragraphs only.** Nothing inside a paragraph is changed, except for two marks the HTML
  carries and the author did not write as prose. Gwern's footnote numbers are removed, and so is the
  "years ago" subscript the site generates (for example "13ya" after "2013"). Whitespace is collapsed and
  HTML entities are decoded.
- **h01–h20:** contiguous paragraphs from the start of the post, 120–450 words. Headings are left out.
  Each excerpt stops before a list. In h03 (socks) the excerpt starts after the abstract. In h07 (picky)
  the reader's quoted question and its one-line lead-in are cut: that paragraph was someone else's words.
- **h21–h26 (texts with lists):** cut by a fixed rule. Start at the first paragraph of the post body
  (on Gwern pages, the first paragraph after the abstract and the table of contents). Take paragraphs
  and list items in order, each list item on its own line with its number or a leading `- `. Skip
  headings and quotations. Stop before the block that would pass 450 words.
- **How the list posts were chosen:** candidate posts were walked in a fixed order, and the first two
  per source whose cut held a list were taken. They were not chosen by how they score. The orders:
  zenhabits archive from October 2022 backwards; Pavlina's November–December 2006 archive; Gwern pages
  whose last-modified date is before 2022-11. `gwern.net/zeo` was skipped because it is now a directory
  page, not an essay.
- **Dates.** Zenhabits posts show no date, so `published` is the year and month from the zenhabits
  archive page. Pavlina dates are the page's `datePublished`. Gwern dates are the page's issue date, and
  only pages last modified before 2022-11-01 were used, because Gwern revises pages over time.

## Machine texts

On 2026-11-11, twenty independent Claude subagents in Claude Code wrote one post each. Each started
from a fresh context and was given exactly two lines: the prompt `Write a LinkedIn post in English about
{topic}.` and an instruction to save the post, and nothing else, to a file. There was no system prompt of
ours, no style hint and no example. No chat wrapper line was found, so every row has
`wrapper_removed: false`.

**Limits of this set:**

- It covers **one model family** (Claude: Haiku 5.5, Sonnet 5.5, Opus 5.5).
- The texts came through an **agent harness**, not a chat window.
- Texts from other model families are welcome as contributions.

The original plan was `claude -p` for topics 1–10 and `codex exec` for 11–20. Neither tool could run on
the build machine that day.

| id | Model | Topic |
|---|---|---|
| m01 | Claude Haiku 5.5 | lessons from my first year as a team lead |
| m02 | Claude Sonnet 5.5 | why most meetings should be emails |
| m03 | Claude Opus 5.5 | what I learned from a failed product launch |
| m04 | Claude Haiku 5.5 | the importance of customer feedback |
| m05 | Claude Sonnet 5.5 | remote work productivity |
| m06 | Claude Opus 5.5 | how AI is changing marketing |
| m07 | Claude Haiku 5.5 | hiring your first employee |
| m08 | Claude Sonnet 5.5 | dealing with burnout |
| m09 | Claude Opus 5.5 | the value of mentorship |
| m10 | Claude Haiku 5.5 | why startups fail |
| m11 | Claude Sonnet 5.5 | building a personal brand |
| m12 | Claude Opus 5.5 | what running a marathon taught me about business |
| m13 | Claude Haiku 5.5 | the future of software engineering |
| m14 | Claude Sonnet 5.5 | how to give better feedback |
| m15 | Claude Opus 5.5 | pricing your services as a freelancer |
| m16 | Claude Haiku 5.5 | what makes a great manager |
| m17 | Claude Sonnet 5.5 | learning to say no |
| m18 | Claude Opus 5.5 | data-driven decision making |
| m19 | Claude Haiku 5.5 | my morning routine |
| m20 | Claude Sonnet 5.5 | changing careers at 35 |

## Splits, tuning and the bar

The first 40 texts were split into odd ids (`tune`) and even ids (`holdout`). Three holdout runs failed
the bar (see `RESULTS.md`). The checker then gained whole-post template patterns, and all 46 texts here
became the tuning set. A fresh holdout of 10 human and 10 machine texts was collected by agents the tuner
does not control. It is run once against the frozen commit.

Tuning rules:

- Tune on the tuning set only.
- A new marker word or shape is admitted only if it occurs in at least 3 tuning machine texts and in no
  tuning human text.
- A template pattern may be tightened when it fires on tuning human texts.
- Thresholds, weights and bands may be changed.

**Release bar, on the holdout:** no human text `heavy`, at most 2 human texts `some`, at least 7 of 10
machine texts not `clean`.

## Reproduce

From the repository root:

```bash
python3 -m pytest tests/test_reference_set.py
```

The manifest checks always run. The holdout checks run once holdout rows are in `manifest.json`; until
then they are skipped. To see the label of one text:

```bash
python3 skills/slop-check/scripts/check.py reference/en/machine/m01.txt --lang en
```
