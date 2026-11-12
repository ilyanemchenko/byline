---
name: post-writer
description: Use when someone wants a post, update or newsletter piece written in their own name for LinkedIn, X, Threads, Telegram or a newsletter, has an angle card or a claim they want to make, or asks for a first draft they will sign.
license: Apache-2.0
---

# Post writer

## Overview

This skill writes one post from an angle and the person's own material in `byline/person.md`. The
post must read like something the person would sign: their facts, their stories, their language,
none of the patterns that make a post read as templated.

Never invent a number, client, result, event or title. Every specific in the draft comes from an `F`
or `S` entry, or from an answer the person gives in this conversation.

## Rules

- One question per message. Write in the language of the `Language` line, or the language the person
  writes in if the line is empty.
- Every number, client, result, event and title in the draft comes from an `F` or `S` entry, or from
  an answer the person gave in this conversation.
- Nothing listed under `## Off limits` appears in the draft, not even as a hint. Never cite an `X` id.
- Stay inside the channel's hard limit, counted in characters. The limits are in `channels.md` next to
  this file.

## Step 1: read the person file

Read `byline/person.md` in the working folder.

If `byline/person.md` does not exist, or it has no `## Facts` section, say what is missing and offer
two ways on:

1. Run the `person-interview` skill (about ten minutes of questions), then come back.
2. Paste a few facts about their work now. If `byline/person.md` exists, never replace it: add the
   facts to it as a new `## Facts` section with `F1`, `F2`, ..., and keep every existing section,
   entry and id as it is, the `## Off limits` entries above all. Only if there is no file, save them
   as a minimal `byline/person.md` in the standard format (create the folder `byline/` if needed):
   the `# Person file` heading, the comment line
   `<!-- byline person file, format 1. Edit it by hand whenever you like. -->`, `## Basics` with the
   fields `Name`, `Role`, `Goal`, `Audience`, `Channels`, `Language` (empty where unknown),
   `## Facts` with `F1`, `F2`, ..., `## Stories`, `## Off limits`. Save only what they wrote; show the
   file before going on.

Do not write on guessed facts.

## Step 2: the angle and the channel

You need both. An angle card from `angle-brainstorm` carries them:

```
Angle
Topic:
Claim:
For:
Facts: F2, S1
Channel:
```

- **No angle:** ask what the post should claim, in one sentence. If they have no claim yet, offer the
  `angle-brainstorm` skill.
- **No channel:** if `Channels` in the file lists exactly one, use it. Otherwise ask which channel this
  post is for: `linkedin`, `x`, `threads`, `telegram` or `newsletter`.
- Check every id on the card exists in the file. Drop an id that does not, and say so.

## Step 3: the facts the post needs

Read the entries the angle stands on. If the claim needs a specific the file does not have (the
number behind a result, the kind of client, when it happened), ask the person one question for it.

- **They answer:** use the answer as given, and offer to append it to `byline/person.md` as a new `F`
  entry. Its id is the highest existing `F` number plus one; never reuse or renumber an id. Append
  only if they say yes. If they decline, the fact is still used and is listed as said in this
  conversation (Step 5).
- **They do not know or skip:** write without it. Do not soften the gap with a vague stand-in ("many
  clients", "a big result").

One question per missing specific, one message at a time; at most three before writing.

## Step 4: write

Open `channels.md` for the channel's limit, what shows before the fold, and what formatting works.

How the post reads:

- The first two lines say what this is about and for whom. They are all most readers see.
- One concrete example from the person's material: a case, a number, a moment. One, told properly,
  beats three mentioned.
- Plain verbs. Say what happened and what the person did.
- After the opening, no "it's not X, it's Y" and no "not X but Y" sentences.
- No list of three for rhythm. List only when there really are that many items.
- End when the point is made. No closing question to collect comments.
- No row of hashtags. If the channel's convention wants a tag, one or two in the text at most.
- No chain of dashes. Use full stops and commas.
- Formatting only where the channel supports it (see `channels.md`).

Check the length with a count, not by eye. If the `slop-check` skill is available, run its script on
the post with `--lang` and `--channel`: when the post is too long it shows an `over_limit` flag, and
the flagged text is the part beyond the limit. It prints no count. Otherwise count the characters
with a tool. If the post is over the channel's hard limit, cut
it; do not split it into a thread unless the person asks.

## Step 5: save and show

1. Create `byline/drafts/` if it is missing.
2. Save the post text, and nothing else, to `byline/drafts/YYYY-MM-DD-<slug>.md`: today's date, taken
   from the system or the environment (for example the `date` command), not guessed, and a
   slug of two to five lower-case words from the topic, joined by hyphens. If that file exists, add
   `-2`, `-3` and so on.
3. Show the post as saved.
4. Then one line listing the ids the post uses, any new id appended in Step 3 included, exactly in
   one of these two forms: `Facts used: F2, S1`, or, when a fact the person gave in Step 3 did not go
   into the file, with that fact in their words and marked:
   `Facts used: F2, S1, "about 30 clinics" (said in this conversation)`.
5. Then one line naming the three checks: `post-fact-check` for every claim about the person,
   `post-editor` for the opening, example and ending, and `slop-check` last, run with the post's
   language and channel.

## Example (invented person: a clinic software consultant)

Card: Claim "A clinic with 22% no-shows needs reminders before it needs more ads", For "owners of
small private clinics", Facts F1, S2, Channel linkedin.

```
Small clinic owners: before you pay for more ads, count your no-shows.

In September a dental practice in Leeds was losing 22% of its bookings to people who never came.
...
```

Saved to `byline/drafts/2026-11-11-clinic-no-shows.md`, then:

```
Facts used: F1, S2
Next: post-fact-check, post-editor, then slop-check (--lang en --channel linkedin).
```

## Common mistakes

- Rounding a number, naming a client the file does not name, or adding a title the person never gave.
- Filling a missing fact with "many", "several" or "a leading company" instead of asking or leaving it out.
- Opening with a scene or a question that does not say what the post is about.
- Saving the `Facts used` line or any note into the draft file. The file holds the post text only.
- Going over the limit on X or Threads because emoji and links count extra there (see `channels.md`).
- Writing in English for a person whose `Language` is another language.
