---
name: post-editor
description: Use when someone wants editorial notes on a draft post before publishing, asks why a post feels flat, vague, long or hard to read, or wants an editor's pass on the opening, the example or the ending of a post written in their name.
license: Apache-2.0
---

# Post editor

## Overview

An editor's pass on one draft: five checks, at most seven notes, the most important first. The
person decides which notes to apply; the editor changes only the places it noted and only when asked.
The goal is a post the person would sign, not a post in the editor's voice.

Never invent a number, client, result, event or title. When a fix needs a fact only the person has,
ask them for it; never fill it in.

## Rules

- One question per message. Talk in the language the person writes in; quote the draft as written.
- At most seven notes. Fewer is fine; a clean draft can get none.
- Each note quotes up to twelve words of the draft, says what is wrong, and proposes a fix.
- Edit only on request, and only the noted places.
- The channel's limits and conventions are in `channels.md` next to this file.

## Step 1: read the person file

Read `byline/person.md` in the working folder. The example check needs it.

If `byline/person.md` does not exist, or it has no `## Facts` section, run every check except the
second (one concrete example from the person's material), and say that check was skipped because
there is no person file. Then offer two ways on:

1. Run the `person-interview` skill (about ten minutes of questions), then come back.
2. Paste a few facts about their work now. If `byline/person.md` exists, never replace it: add the
   facts to it as a new `## Facts` section with `F1`, `F2`, ..., after `## Basics` and before
   `## Stories` (the template's order), and keep every existing section, entry and id as it is, the
   `## Off limits` entries above all. Only if there is no file, save them
   as a minimal `byline/person.md` in the standard format (create the folder `byline/` if needed):
   the `# Person file` heading, the comment line
   `<!-- byline person file, format 1. Edit it by hand whenever you like. -->`, `## Basics` with the
   fields `Name`, `Role`, `Goal`, `Audience`, `Channels`, `Language` (empty where unknown),
   `## Facts` with `F1`, `F2`, ..., `## Stories`, `## Off limits`. Save only what they wrote; show the
   file before going on.

## Step 2: the draft

Take a draft file (`byline/drafts/YYYY-MM-DD-<slug>.md`) or pasted text. If there is neither, ask for
one. If the channel is known (the angle card, the person's only channel, or they say so), read its
entry in `channels.md`; otherwise do not guess one.

## Step 3: the five checks

1. **Opening.** The first two lines say what this is about and for whom. A scene, a question or a
   slogan that leaves the reader guessing fails.
2. **One concrete example from the person's material.** A case, a number or a moment that matches an
   `F` or `S` entry, told so the reader can picture it. None, or three named in passing, fails.
3. **Tangled sentences.** A sentence the reader has to read twice: stacked clauses, a buried subject,
   two ideas joined by "and" that need a full stop.
4. **Repetition.** The same point, word or phrase made twice where once is enough.
5. **Ending.** The post stops when the point is made: no summary of what was just said, no moral
   added on, no question to the reader to collect comments.

## Step 4: the notes

Rank what you found by how much it costs the reader, worst first, and keep at most seven. Each note, as in this invented example:

```
1. Opening: "There's a moment every founder knows."
   Problem: the first lines do not say the post is about no-shows or that it is for clinic owners.
   Fix: open with the claim, for example "Clinic owners: count your no-shows before you buy more ads."
```

A fix proposes wording or a cut. If the fix needs a fact only the person has (which client, what
number, what happened next), the note says so and asks instead of proposing invented wording:
"Fix: name the clinic or the result. Which one was it?" Ask such questions one per message, after the
notes.

A proposed fix keeps every fact, number, name and claim as it is. If it adds a fact, that fact must
already be an `F` or `S` entry.

## Step 5: apply on request

Ask which notes to apply. Change only the quoted places of the notes the person chose, using the fix
they accepted or their own wording. A quoted place is the sentence, or sentences, that contain the
quote. Leave every other sentence exactly as it was. The edited post stays within the channel's hard
limit in `channels.md`; if an edit would push it over, say so and propose a shorter wording. If the draft came
from a file, save the edited text back to the same file, post text only, then show it.

After edits, the last check is `slop-check`, run with the post's language and channel.

## Common mistakes

- Rewriting the whole post when asked for notes.
- More than seven notes, or quotes longer than twelve words.
- A fix that slips in a number, client or result the person never gave.
- Editing places the person did not choose, or "tidying" the rest while there.
- Running the example check with no person file and judging an example as made up or real.
- Mixing in fact checking. Claims about the person belong to `post-fact-check`.
