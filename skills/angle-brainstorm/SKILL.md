---
name: angle-brainstorm
description: Use when someone has a topic for a post but not the point it should make, asks for angles, hooks or takes on a subject, or wants to decide what a post in their name should argue before it is written.
license: Apache-2.0
---

# Angle brainstorm

## Overview

A topic ("hiring", "pricing") is not a post. An angle is: one claim the person can stand behind, the
facts or stories from their own work that support it, and the reader it is for. This skill turns a
topic into three such angles, lets the person pick one, and prints an angle card that the post writer
uses.

Never invent a number, client, result, event or title. Every angle stands on entries the person
already gave.

## Rules

- One question per message. Talk in the language the person writes in.
- Use only what is in `byline/person.md` and what the person says in this conversation.
- Nothing listed under `## Off limits` may appear in an angle, not even as a hint.

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

Do not continue on guessed facts.

If Goal or Audience is empty, ask for it, one question, and save it to the file before going on.

## Step 2: the topic

If the person already named a topic, use it. If not, ask what the post is about. If they have no
idea, offer the `topic-scout` skill.

## Step 3: the reader's takeaway

Ask what the reader should believe or do after reading the post. One answer is enough; do not argue
with it.

## Step 4: three angles

Offer exactly three angles, numbered. Each one has:

- **Claim:** one sentence the person could say out loud and defend. A position, not a summary.
- **Stands on:** the ids it uses (`F2, S1`). At least one id, and every id must exist in the file.
- **Why this reader cares:** one sentence tied to the `Audience` line and the takeaway from Step 3.

The claim and the "why this reader cares" line say no more than the entries the angle cites: no
result, contrast or beneficiary that the cited `F` and `S` entries do not state. If the person wants
the stronger wording, ask for the fact behind it and save it to the file first (Step 5).

Make the three differ in kind, for example one built on a result, one on a mistake or changed belief,
one that disagrees with common practice in the field.

An angle with no supporting id is not offered. If the file cannot support three different angles on
this topic, offer the ones it can support, say what kind of fact is missing for more (for example,
"a result with a number about pricing"), and offer to add it through `person-interview`. Never fill
the gap with a general claim.

## Step 5: the pick

The person picks one, changes one, or combines two. Apply their edits as they wrote them. If an edit
adds a new fact, ask whether to append it to `byline/person.md`. Its id is the highest existing
number in that section plus one; never reuse or renumber an id. Cite it only once it has an id.

Channel: if `Channels` lists one channel, use it. If it lists several, or it is empty, ask which one
this post is for (one question).

## Step 6: print the angle card

Print it exactly in this form, in a code block, with the field names in English and the values in the
person's language:

```
Angle
Topic:
Claim:
For:
Facts: F2, S1
Channel:
```

`For` is the reader, from the `Audience` line narrowed to this post. `Facts` lists the ids the angle
stands on. Then say the card can go to the `post-writer` skill.

## Example (invented person: a clinic software consultant)

Topic: SMS reminders. Takeaway: clinic owners should fix no-shows before buying more ads.

```
Angle
Topic: No-shows at small clinics
Claim: A clinic with 22% no-shows needs reminders before it needs more ads.
For: owners of small private clinics
Facts: F1, S2
Channel: linkedin
```

## Common mistakes

- Offering an angle on general knowledge with no id behind it.
- Citing an id that is not in the file, or a fact the file does not say.
- Three angles that are the same claim in different words.
- Asking the takeaway, the channel and the pick in one message.
- Using a client or number from `## Off limits`.
