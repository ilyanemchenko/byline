---
name: new-post
description: Use when someone wants a post in their name from start to finish, asks to write a new post without saying which step they are at, or wants the whole byline process run for them on LinkedIn, X, Threads, Telegram or a newsletter.
license: Apache-2.0
---

# New post

## Overview

This skill runs the byline skills in order, from the person file to a checked post. It adds no rules
of its own: each step follows its own skill exactly, and the chain only decides what comes next and
where to stop for the person's decision.

## How to run a step

For each step, invoke the step's skill by name where your environment allows it. Otherwise read
`../<skill>/SKILL.md` relative to this file (for example `../post-writer/SKILL.md`) and follow it as
written. Use the step's own instructions for questions, files and output; where this file and a
step's skill seem to differ, the step's skill wins.

## The order

1. **Person file.** Look for `byline/person.md` in the working folder.
   If `byline/person.md` does not exist, or it has no `## Facts` section, run `person-interview`.
   Stop: the person confirms the saved file.
2. **Topic.** If the person already named a topic, use it. If not, and they have no idea, run
   `topic-scout`; otherwise skip this step.
3. **Angle.** Run `angle-brainstorm` with the topic.
   Stop: the person picks an angle; the angle card is printed.
4. **Draft.** Run `post-writer` with the angle card.
   Stop: the person has seen the draft and wants to go on, or asks for changes first.
5. **Fact check.** Run `post-fact-check` on the saved draft file.
   Stop: one decision per unconfirmed claim (cut, ask, reword).
6. **Editor.** Run `post-editor` on the draft as it now stands.
   Stop: the person chooses which notes to apply.
7. **Slop check.** Run `slop-check` on the draft file, passing the post's language and channel.
   Stop: the person decides whether to rewrite the flagged places.

A stop means: ask, then wait for the answer before the next step. One question per message, as each
skill says.

If the person says to skip a step, skip it and say which one was skipped. If they come in at a later
step (they already have an angle card or a draft), start there.

## The end

Show the final post text, whether or not it is saved in a draft file. When it is, give the path
under `byline/drafts/` too: the file must hold this final text, every accepted change included. Then
one line: the person signs it and publishes it themselves. Byline never posts anything anywhere.

## Common mistakes

- Running a step from memory instead of its skill, or adding rules the skill does not have.
- Going past a stop without the person's answer.
- Running `topic-scout` when the person already has a topic.
- Running `slop-check` without the post's language and channel.
- Publishing, scheduling or offering to post on the person's behalf.
