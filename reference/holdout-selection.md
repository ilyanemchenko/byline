# Selection log: human holdout set h21-h30

Collected 2026-11-11. Nothing was scored or run through any checker. Word counts are plain whitespace-separated
tokens of the saved file (list numbers and `- ` markers count), not the checker's tokenizer.
Pages were fetched with `curl -sL`, one folder per page. The text was extracted and cut by scripts kept
outside the repository; they are not included.

## Licences (each page re-fetched today)

| Author | Licence page | Sentence that grants it |
|---|---|---|
| Leo Babauta | https://zenhabits.net/uncopyright/ | "This entire blog, and all my ebooks, are uncopyrighted (since January 2008). That means I've put them in the public domain, and released my copyright on all these works." |
| Steve Pavlina | https://stevepavlina.com/uncopyright/ | "I hereby release my copyrights to, and place into the public domain, all of the following: The hundreds of articles I've posted on this website since it launched on October 1, 2004 through May 20, 2024 (text content only)." |
| Gwern Branwen | https://gwern.net/about | "This site is licensed under the Creative Commons public domain (CC-0) license." |

All three confirmed. Every Pavlina post chosen is dated before 2024-05-20.

## Rules as applied (decisions the collection rule left open)

- "First post listed": zenhabits archive (https://zenhabits.net/archives/) lists each month newest first under the
  month heading; the first link under the heading is taken. Pavlina month archive pages
  (https://stevepavlina.com/blog/YYYY/MM/) list newest first; first link in page order is taken.
- Dates: the zenhabits archive prints a day number beside each post, so `published` is a full date for zenhabits
  (the earlier 20 rows use year-month). Pavlina: `datePublished`. Gwern: `dc.date.issued`.
- Start: first body paragraph. The byline line ("By Leo Babauta") and any heading that comes before the first
  paragraph are not text. Subheadings after that are kept as their own line; a subheading is written only together
  with the paragraph after it (a heading is never left dangling at the end).
- Gwern pages: the abstract box, "note" admonition boxes, epigraphs, figure captions and tables are page furniture,
  not the body flow, and are skipped (same for both pages). The earlier set also started socks after the abstract.
- Blockquote paragraphs and reader submissions count as "mostly a quotation of someone else" and are dropped.
- Footnote marks removed. Gwern's inline date annotations removed ("4" and "11ya" scripts in date ranges, so
  "2011-2015" stays as the author wrote it). Other sub/superscripts stay as plain text (`log2`).
- None of the 10 URLs is in `reference/manifest.json` (human rows checked by a script kept outside the repository).

## Zenhabits (4)

Archive page: https://zenhabits.net/archives/ (first post under each month heading).

- **h21**: March 2013 -> "The 38 Best Methods of Successful Exercisers" (2013-03-29), https://zenhabits.net/fit-habit/.
  No skip. The post is the author's intro (about 190 words) followed by 39 numbered reader submissions
  (signed "~Name" or anonymous). All 39 are someone else's words and were dropped (blocks 10-48, including one
  continuation paragraph starting ">What works instead"). Own prose in the whole post = 193 words (>= 120), so no
  skip. Text = blocks 1-9, 193 words, no cut by the word cap. It ends on the lead-in "They answered (note ...):"
  because everything after it is dropped. Flag: this is the shortest text and ends on a colon.
- **h24**: June 2015 -> "How Taking Care of My Finances Changed My Life" (2015-06-29), https://zenhabits.net/financial-care/.
  No skip, nothing dropped. 396 words; includes a numbered list 1-8. Cut before "It was a slow process, but these
  small steps of self-care changed my life..." (356 chars, would pass 450).
- **h27**: September 2017 -> "The Ideal vs. the Reality of Changing Your Life" (2017-09-26), https://zenhabits.net/realism/.
  No skip. Dropped the opening epigraph (Ram Dass quotation, before the byline). 359 words, no list. Cut before
  "I can become disappointed with my body, ..." (522 chars).
- **h29**: February 2020 -> "Coming Back to Powerful Habits (plus 6 Powerful Habits)" (2020-02-28), https://zenhabits.net/coming-back/.
  No skip, nothing dropped. 448 words; includes a numbered list 1-4 and two subheadings ("How to Start Again",
  "Some Powerful Habits to Come Back To"). Cut before list item 1 of the second list ("Meditation. This one is
  obvious..."), so the text ends on the lead-in "Here are some habits ... for me:".

## Steve Pavlina (4)

Archive pages: /blog/2012/05/, /blog/2014/08/, /blog/2016/11/, /blog/2019/04/ on stevepavlina.com.

- **h22**: May 2012 -> "How to Earn Passive Income From Intellectual Property" (2012-05-31),
  https://stevepavlina.com/blog/2012/05/how-to-earn-passive-income-from-intellectual-property/. No skip. 440 words,
  headings "Intellectual Property" and "Self-Publishing" kept, no list. Cut before "Note that putting up free content
  on a website with no traffic ..." (426 chars).
- **h25**: August 2014 -> "Selecting Projects Wisely" (2014-08-29), https://stevepavlina.com/blog/2014/08/selecting-projects-wisely/.
  Only one post that month. No skip. 359 words, no list. Cut before "I knew that both of these skill paths could
  also be used ..." (553 chars). The Steve Jobs blockquote later in the post lies after the cut.
- **h28**: November 2016 -> "30 Days of Disneyland - Day 30" (2016-11-25), https://stevepavlina.com/blog/2016/11/30-days-disneyland-day-30/.
  No skip (a diary-style post, but prose, 2,600+ words). 450 words exactly (not past the cap), headings none inside
  the text. Cut before the heading "Engineering Emotionalism" and its paragraph.
- **h30**: April 2019 -> "Creating the Peer Group I've Always Longed for" (2019-04-28),
  https://stevepavlina.com/blog/2019/04/creating-the-peer-group-ive-always-longed-for/. 431 words, no list.
  Cut before "For many people the idea of connecting with interesting, ambitious, growth-oriented people ..." (473 chars).
  **Skips in this month (announcements, by the site's own "Announcements" category tag):**
  1. "Why Would 100+ People Pay $2K to Join Conscious Growth Club?" (2019-04-30): category announcements.
  2. "Conscious Growth Club Q&A" (2019-04-29): category announcements.
  The third listed post (this one) has no announcements tag and was taken.

## Gwern (2)

Index of essays: https://gwern.net/index, listing order from the first section ("Newest"). Pages fetched in order and
the `dcterms.modified` meta read; the first two with modified < 2022-11 and not in the manifest were taken. Skipped
because modified after 2022-11 (entries 1-11 of the listing): /fiction/mirror (2026-10-07), /lean-scaling (2026-06-23),
/fiction/walking (2026-06-12), /fiction/molting (2026-06-10), /guardian-angel (2026-06-05), /llm-catapult (2026-06-05),
/generating-style (2026-05-21), /vaping (2026-05-16), /polish (2026-05-11), /rl-children (2026-05-09),
/fiction/astrology (2026-04-23). None of the manifest Gwern pages (socks, console-insurance, choosing-software,
complement) came before the two chosen.

- **h23**: /scaling-hypothesis, "The Scaling Hypothesis" (issued 2020-05-28, modified 2022-01-02), https://gwern.net/scaling-hypothesis.
  Skipped as furniture: the abstract, the "Read The Samples" note box, the Dorian Gray epigraph under "Flexing GPT",
  the cake figure caption. Text starts at "Learning to learn. In May 2020, OA released..." (the heading "Meta-Learning"
  before it is not text). 421 words; heading "Flexing GPT" kept. Cut before the heading "Baking The Cake" with its paragraph (3 + 154 words
  would pass 450). No list.
- **h26**: /death-note-anonymity, "Death Note: L, Anonymity & Eluding Entropy" (issued 2011-05-04, modified 2017-12-15),
  https://gwern.net/death-note-anonymity. Skipped as furniture: the abstract (including its numbered list of mistakes).
  Text starts at "I have called the protagonist of Death Note, Light Yagami, "hubristic"...". 408 words, heading
  "Detective Stories As Optimization Problems" kept, no list. Cut before "We should first point out that Light is
  always going to leak some bits..." (725 chars).

## Order and files

Authors alternate: h21 Babauta, h22 Pavlina, h23 Gwern, h24 Babauta, h25 Pavlina, h26 Gwern, h27 Babauta, h28 Pavlina,
h29 Babauta, h30 Pavlina. Within an author, files follow the listing order (months ascending; Gwern in
index order). Word counts 193 to 450.

Texts containing a list: h24 (numbered 1-8) and h29 (numbered 1-4).
