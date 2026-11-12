---
name: person-interview
description: Use when someone wants posts written in their name and there is no byline/person.md yet, when they ask to be interviewed about their work, or when they want to add facts, stories or off-limits topics to their person file.
license: Apache-2.0
---

# Person interview

## Overview

Every other byline skill writes from one file: `byline/person.md` in the person's working folder. It
holds what the person actually said about their work: facts with a number, a name, a date or an
event, and stories in their own words. This skill fills that file through a short interview.

The file is only as good as its specifics. A post built on "I help companies grow" reads like anyone's;
a post built on "In March we cut onboarding from 14 days to 3 for a 40-person clinic" reads like theirs.

## Rules for the whole interview

- **One question per message.** Never stack two questions, and never send the list of questions ahead.
- **The person's language.** Talk in the language they write in, and save facts and stories in that
  language. Section headings and field names in the file stay in English, exactly as in the template.
- **Record only what the person said.** No rounding up ("about 30" stays "about 30"), no titles or
  results they did not state, no context from general knowledge, no guessing a company's size or field.
  If something is unclear, ask; do not fill it in.
- **At most one follow-up per question.** An answer with no number, name, date or event gets one
  follow-up that asks for the specific ("Which client was that, or what changed in numbers?"). Whatever
  the second answer is, move on. Never a second follow-up on the same question. If the answer is
  still vague, save it as an `S` entry only if it is a case told as a sequence of events; otherwise
  save nothing from it.
- **Private means off limits.** If at any point the person asks to keep something private or out of
  posts, do not put it in a fact or story; add it to the off-limits list at once, by name (see
  "Off limits" under "Turning answers into entries").
- **"Skip" is a fine answer.** Move to the next question without comment.

## Start: is there a file already?

Look for `byline/person.md` in the working folder.

- **It exists:** go to "Adding to an existing file" below.
- **It does not exist:** run the interview.

## The interview

### 1. Four basics, one per message

1. What are the posts for? (Goal: for example, find clients for a consultancy, get hired as a CTO,
   build an audience for a book.)
2. Who should read them? (Audience: the people whose opinion or decision matters for that goal.)
3. Where will you post? Record the ones from this list: `linkedin, x, threads, telegram, newsletter`.
   If they name another place, say that byline writes for these five and record those that apply.
4. Which language will the posts be in? Record it as a language code (`en`, `ru`, `de`, ...).

Name and Role: fill them in from what the person says along the way (Role usually comes from
question 1 below). If the name never comes up, leave the field empty and mention it at the review.

### 2. Five questions, in this order

Ask each in your own words, in the person's language, one per message.

| # | Intent | What to listen for |
|---|---|---|
| 1 | What you do and for whom, told through one recent concrete case | Role, the kind of client, one real situation |
| 2 | A result you can put a number or a name on | The number, the unit, the time frame, who it was for |
| 3 | A mistake you made, or a belief you dropped, and what changed your mind | The old belief, the event that changed it |
| 4 | Something people in your field get wrong, and what you saw that shows it | The claim and the case behind it |
| 5 | The story you tell when someone asks why you do this work | The story in their words |

Apply the one-follow-up rule to each.

### 3. Last question: off limits

Ask what must never be mentioned in a post: a client, an employer, a number, a topic. Each item
becomes one `X` entry. If an item is also in a fact or story you recorded, keep the fact and ask
whether to remove it; remove it only if they say yes.

## Turning answers into entries

- **Fact (`F`):** one sentence that carries a number, a name, a date or an event, as the person said
  it. One answer can give several facts. A statement with none of these is not a fact: do not save it
  as `F`.
- **Story (`S`):** two to six sentences, kept close to the person's own words. Use it for answers 3, 4
  and 5 and for any case told as a sequence of events. Trim filler; do not polish or add.
- **Off limits (`X`):** one line per item, in the person's own words and with the name they used (a
  client, an employer, a product). The other skills recognise the item in a draft by that name, so a
  description without the name is not enough: "a logistics client" is a description, the name is what
  that client is called. If they gave no name, ask for it once; if they will not
  give it, save their wording and tell them the entry cannot be matched by name.
- Ids start at `F1`, `S1`, `X1` and count up in the order you record them.

## Saving

1. Create the folder `byline/` in the working folder if it is missing.
2. Write `byline/person.md` in exactly this format (the comment line included):

```markdown
# Person file
<!-- byline person file, format 1. Edit it by hand whenever you like. -->

## Basics
- Name:
- Role:
- Goal:
- Audience:
- Channels:
- Language:

## Facts
- F1: one sentence with a number, a name, a date or an event

## Stories
- S1: two to six sentences in the person's own words

## Off limits
- X1: a topic, client, number or employer never to mention
```

   The `F1`, `S1` and `X1` lines above are examples of the shape. Replace the example entries with
   the person's real ones; delete an example line if there is nothing to put in its place. Never
   save an example line as an entry. `Channels` is a comma list such as `linkedin, newsletter`. A
   section with nothing in it keeps its heading and has no entries.
3. Show the whole file to the person.
4. Ask whether anything is wrong or missing, and fix what they point out.
5. Tell them the file is plain text at `byline/person.md` and they can edit it by hand at any time.

## Adding to an existing file

1. Read `byline/person.md`. If it has no `## Facts` section or does not follow the format above, do
   not rewrite it silently: say what is missing or different and ask whether to repair it. A repair
   keeps every existing entry and id as it is.
2. Summarise it in one line ("You: Role, writing for Audience on Channels, 6 facts, 2 stories, 1
   off-limits item").
3. Ask what they want to add: a new result, a story, an off-limits item, or a change to the basics.
4. Ask for it with the same rules (one question per message, one follow-up for specifics).
5. Append new entries after the last one in their section. A new id is the highest existing number in
   that section plus one. Never renumber, never reuse an id, never reorder.
6. Change or delete an existing entry only when the person asks for that entry by name or content.
7. Show the changed lines, then the path, and remind them they can edit the file by hand.

## Example (invented person)

> Agent: What did you do for a client recently? Pick one case.
> Person: I help small clinics with their booking systems.
> Agent: Which clinic was the last one?
> Person: A dental practice in Leeds, in September. No-shows went from 22% to 9% after we added SMS reminders.

Saved as `- F1: In September a dental practice in Leeds went from 22% to 9% no-shows after we added SMS
reminders.` Role: helps small clinics with booking systems. The first answer alone would not have
made a fact.

## Common mistakes

- Asking two questions in one message, or the four basics all at once.
- A second follow-up after a vague answer. One, then move on.
- Writing "over 20%" when they said "22%", or "a leading clinic" when they said "a dental practice".
- Saving a general opinion as a fact. Facts carry a number, a name, a date or an event.
- Translating the person's answers into English, or translating the headings out of English.
- Renumbering ids after adding or removing entries. Other skills cite ids in drafts and angle cards.
- Overwriting an existing file instead of reading it and appending.
