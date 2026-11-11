---
name: post-fact-check
description: Use when a draft post written in someone's name needs its claims about them checked before publishing, when someone asks whether a post says anything untrue or unsupported about them, or when a number, client, result, event or title in a draft might be made up.
license: Apache-2.0
---

# Post fact check

## Overview

A post in someone's name makes claims about them: what they did, for whom, with what result, when,
under what title. This skill lists every such claim in a draft and checks it against
`byline/person.md`. It changes no style; it only finds what the person's own file does not back.

Never invent a number, client, result, event or title. A fix is a cut, a question to the person, or
a rewording that says less; never a new specific.

## Rules

- One question per message. Talk in the language the person writes in; quote the draft as written.
- Check claims about the person only. General statements about the world are out of scope.
- Change no wording beyond the fix the person accepts. Do not polish, shorten or restyle.

## Step 1: read the person file

Read `byline/person.md` in the working folder.

If `byline/person.md` does not exist, or it has no `## Facts` section, there is nothing to check the
draft against. Say what is missing and offer two ways on:

1. Run the `person-interview` skill (about ten minutes of questions), then come back.
2. Paste a few facts about their work now. Save them as a minimal `byline/person.md` in the standard
   format (create the folder `byline/` if needed): the `# Person file` heading, the comment line
   `<!-- byline person file, format 1. Edit it by hand whenever you like. -->`, `## Basics` with the
   fields `Name`, `Role`, `Goal`, `Audience`, `Channels`, `Language` (empty where unknown),
   `## Facts` with `F1`, `F2`, ..., `## Stories`, `## Off limits`. Save only what they wrote; show the
   file before going on.

Do not check anything until one of the two is done.

## Step 2: the draft

Take a draft file (`byline/drafts/YYYY-MM-DD-<slug>.md`) or pasted text. If there is neither, ask for
one.

## Step 3: list the claims

Go through the draft sentence by sentence and list every claim about the person:

- **number:** any figure, percentage, amount, count or duration tied to their work
- **client:** a named client, employer, partner or kind of client ("a dental practice in Leeds")
- **result:** what changed because of their work
- **event:** something that happened, with or without a date
- **title:** a role, rank, award or credential

A sentence can hold several claims; list each one.

## Step 4: give each claim a status

| Status | When |
|---|---|
| `confirmed F3` | an `F` or `S` entry says the same thing (same number, same name, same time) |
| `not in the file` | no entry says it |
| `contradicts F3` | an entry says something different (22% in the file, 25% in the draft) |
| `off limits X1` | it touches an item under `## Off limits` |
| `confirmed by the person` | the draft came from `post-writer` and its `Facts used:` line lists this fact as `said in this conversation` |

Rounding, a bigger or vaguer unit, or a stronger verb ("led" for "helped") is a contradiction, not a
confirmation. A detail the entry does not give at all (a year when the entry says only "in
September") is `not in the file`.

## Step 5: report

Print one line per claim, in draft order. For example, an invented person whose file holds:

```
- F1: In September a dental practice in Leeds went from 22% to 9% no-shows after we added SMS reminders.
- X1: Northwind, my former employer
```

and a draft that claims:

```
1. "a dental practice in Leeds"     confirmed F1
2. "in September 2024"              not in the file (F1 gives no year)    suggest: reword to "in September"
3. "no-shows fell from 25% to 9%"   contradicts F1 (22%)    suggest: reword to "from 22% to 9%"
4. "for over 40 clinics"            not in the file    suggest: ask
5. "my years at Northwind"          off limits X1      suggest: cut
```

For every claim that is not confirmed, suggest one of:

- **cut:** the sentence works without it, or it is off limits (always cut an off-limits claim);
- **ask:** only the person knows whether it is true;
- **reword:** an entry supports a narrower version; give the narrower wording, built only from that entry.

End with a count: "5 claims: 1 confirmed, 4 need a decision."

## Step 6: the unconfirmed claims, one at a time

Go through every claim that is not confirmed, one claim per message, in draft order, using its
suggestion:

- **`ask`:** ask whether it is true and what exactly it is.
  - True, with the specific: offer to append it to `byline/person.md` as a new `F` entry. Its id is the
    highest existing `F` number plus one; never reuse or renumber an id. Append only on yes. The claim
    is now confirmed with that id (or confirmed by the person, if they decline to append it).
  - Not true, or not sure: offer the cut or a narrower wording built from an entry.
- **`cut` or `reword`:** show the suggestion and ask whether to apply it.
- **`off limits`:** always offer it as a cut, and ask whether to apply it.

Apply a cut or rewording to the draft only when the person agrees, and only to that claim's words. If
the draft came from a file, save the changed text back to the same file, post text only.

## Common mistakes

- Treating "about 20%" as confirming "22%", or "a clinic" as confirming "a leading clinic".
- Checking style, tone or length. That is `post-editor` and `slop-check`, not this skill.
- Suggesting a rewording that adds a new detail to make the sentence sound better.
- Asking about several claims in one message.
- Writing the fact check into the draft file.
