---
name: topic-scout
description: Use when someone does not know what to post about, asks for post ideas or topics, or wants to know what is being discussed in their field this month that they could write about from their own experience.
license: Apache-2.0
---

# Topic scout

## Overview

A good topic sits where something current in the person's field meets something they have actually
done. This skill searches the web for recent news in their field and ties each item to a fact or
story from `byline/person.md`. Without a web search tool, it offers evergreen topics from the file
alone and says so.

Never invent a number, client, result, event or title.

## Rules

- One question per message. Talk in the language the person writes in.
- Nothing listed under `## Off limits` may appear in a topic.
- Never present a topic's news as fact without its link. A news item you cannot link is not offered.

## Step 1: read the person file

Read `byline/person.md` in the working folder. You need `Role`, `Goal`, `Audience`, and the
`## Facts` and `## Stories` sections.

If `byline/person.md` does not exist, or it has no `## Facts` section, say what is missing and offer
two ways on:

1. Run the `person-interview` skill (about ten minutes of questions), then come back.
2. Paste a few facts about their work now. Save them as a minimal `byline/person.md` in the standard
   format (create the folder `byline/` if needed): the `# Person file` heading, the comment line
   `<!-- byline person file, format 1. Edit it by hand whenever you like. -->`, `## Basics` with the
   fields `Name`, `Role`, `Goal`, `Audience`, `Channels`, `Language` (empty where unknown),
   `## Facts` with `F1`, `F2`, ..., `## Stories`, `## Off limits`. Save only what they wrote; show the
   file before going on.

Do not guess the person's field or experience.

## Step 2: do you have web search?

Check your own tools for anything that searches the web (a web search tool, a search MCP server, a
browser you are allowed to use). A tool that only fetches a URL you already have is not search.

- **Yes:** Step 3a.
- **No:** Step 3b.

## Step 3a: with web search

1. Build searches from `Role`, the field implied by the facts, and the `Audience`. Search in the
   post language and in English if the field's news is mostly in English.
2. Keep only items published in the last 30 days. Check the date on the page itself; if you cannot
   find a date, drop the item.
3. Open each candidate source before using it. Report only what the source says.
4. For each item, find the fact or story id it connects to: the person has done, seen or measured
   something that bears on it. No id, no topic.
5. Drop items that do not serve the `Goal` line: news the target reader would not care about, or
   that pulls the person toward a field they did not name.
6. Offer five to seven topics. If fewer than five survive, offer what you have and say why the list
   is short; do not pad with older or unlinked items.

Format each topic like this:

```
1. <topic in a few words>
   Why now: <one sentence on what happened, with the date>
   Source: <link>
   Connects to: F3 (<a few words of the fact>)
```

## Step 3b: with no web search

Say it in the first line of your reply, plainly: "I have no web search tool here, so these topics come
from your person file only, not from this month's news."

Then offer three to five evergreen topics, each built on one or more ids from the file:

```
1. <topic in a few words>
   Why it works: <one sentence tied to the Audience or Goal>
   Connects to: S1, F2
```

Do not present anything from memory as recent news, and do not write "lately" or "this year" about
events you cannot link.

## Step 4: next step

Ask which topic they want to take further, then offer the `angle-brainstorm` skill with that topic.

## Example (invented person: a clinic software consultant, Goal: find clinic clients)

```
1. Patients booking by message app
   Why now: A national survey published on 3 November found most patients under 40 prefer to book by message.
   Source: https://example.org/survey-2026
   Connects to: F1 (no-shows from 22% to 9% after SMS reminders)
```

(The link above is a placeholder for the format; real topics carry the real link you opened.)

## Common mistakes

- Offering news without a link, or with a link you did not open.
- Including items older than 30 days, or items with no date.
- A topic with no id: interesting news the person has nothing of their own to say about.
- Topics that suit the field but not the `Goal` (a hiring trend for someone who wants clients).
- Hiding the lack of a search tool, or filling the gap with remembered "recent" events.
