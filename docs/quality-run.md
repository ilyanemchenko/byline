# Quality run

Before release, on 2026-11-11 and 2026-11-12, agents that had never seen the skills ran them on three
invented people: the six skills of the main chain for all three (the editor ran to the end for one of
them), `topic-scout` once, and `new-post` once, only up to its first stop. This page records what was
checked, what passed, what was not run, and what was changed afterwards. The checker script is measured
separately, in `reference/RESULTS.md`.

The run logs and instruction files are not published. What is published is this summary and the files
of one person's run, in `examples/tamsin/`.

## Method

- **Three invented people.** Tamsin Ashgrove, a warehouse consultant in Bristol (English, LinkedIn);
  Oskar Brindlewood, a mobile app accessibility auditor in Edinburgh (English, X); Agniya
  Belomestnova, a baker in Nizhny Novgorod (Russian, Telegram). They, their firms and their clients
  are invented. Each had a list of true facts, three off-limits items (among them a client under a
  non-disclosure agreement and a price) and a script of replies.
- **Fresh agents, one skill each.** Each run was a new Claude Sonnet 5.5 agent with one instruction
  file: which skill to follow, the person's opening request and the scripted replies to give. It
  wrote a log of every message and every file it created.
- **The chain, in order:** `person-interview`, `angle-brainstorm`, `post-writer`, then
  `post-fact-check`, `post-editor` and `slop-check` on the draft.
- **Two false claims in each draft.** Before the fact check, a script inserted two false sentences
  about the person into a copy of each draft: a bigger count, a better result, an award or a prize
  that the person file does not back.
- **Side runs:** the writer with no person file and with a file that has no facts, the `new-post`
  chain from an empty folder, and `topic-scout` with web search.
- **A separate checker.** One more agent, which ran none of the skills, read every log against the
  person's true facts, the planted claims and the skill's own rules, and recorded pass, fail or not
  run for each check. It also ran the install checks.

## Results

26 checks: 21 pass, 0 fail, 5 not run.

| Person | Interview | Angles | Writer | Fact check | Editor | Slop check | Rewrite after slop check |
|---|---|---|---|---|---|---|---|
| Tamsin (en, LinkedIn) | pass | pass | pass | pass | pass | pass | not run |
| Oskar (en, X) | pass | pass | pass | pass | not run | pass | not run |
| Agniya (ru, Telegram) | pass | pass | pass | pass | not run | pass | not run |

| Side run | Result |
|---|---|
| Writer with no person file (Agniya) | pass: said the file is missing, wrote no post, invented nothing |
| Writer with a file but no facts (Agniya) | pass: said the facts are missing, wrote no post |
| `new-post` from an empty folder (Tamsin) | pass: ran the interview first and stopped for confirmation |
| `topic-scout` with web search (Oskar) | pass: the topic it offered was tied to a fact id and to a link that opens (see D5) |
| Russian throughout (Agniya) | pass: questions, saved entries and post in Russian; headings and field names in English |

What "pass" covered, in short:

- **No invented specifics.** Every number, client, date and result in each of the three drafts maps to
  an entry in the person file.
- **Off limits held.** No off-limits item appeared in any angle, draft or note.
- **The planted claims.** All six were reported as unconfirmed: four as contradicting an entry in the
  file, two as not in the file.
- **Slop check.** All three drafts came out `clean`, 0 of 100, with the right `--lang` and `--channel`,
  and no run said or hinted who wrote the text.

**Not run (5).** The three rewrite steps had nothing to do: no draft had a flagged place. The editor
runs for Oskar and Agniya were stopped by the model provider's safety filter. Their instruction files
differ from Tamsin's, which ran cleanly, only in the folder, the log path, the channel and the
language of the replies, and nothing in the skill asks a model to reveal its reasoning; the stops look like false
positives. They were not repeated.

## Extra run: a rewrite

Because no draft had a flagged place, one more agent ran `slop-check` on a machine-written tuning text
from the reference set (`reference/en/machine/m05.txt`, on remote work productivity) and rewrote the
flagged places when asked. Before: `heavy`, 68 of 100, with a list of slogans, three "isn't X. It's Y"
sentences, a closing question to the reader and a row of hashtags. After the rewrite of those places
only: `clean`, 0 of 100. The agent reported both scores, as the skill says.

## Defects and what changed

No run invented or upgraded a fact, leaked an off-limits item or missed a planted claim. The checker
found eight minor defects in the wording of the skills, the checker's output and the test setup.

| # | Defect | Change |
|---|---|---|
| D1 | The "paste a few facts" way in five skills could be read as writing a new person file over an existing one, dropping its off-limits list. | All five now add the facts to the existing file and keep every section, entry and id; a new file is made only when there is none. |
| D2 | An off-limits client was saved as a description without its name, so a later skill could not match it in a draft. | `person-interview` saves an off-limits item with the name the person used, asks once if there is none, and says when an entry cannot be matched by name. |
| D3 | `post-writer` said the checker reports by how much a post is over the limit; it does not. | The skill now says what the checker shows: an `over_limit` flag on the part beyond the limit, with no count. |
| D4 | The fact check offered to cut or reword an unconfirmed claim without first asking whether it is true, and some runs asked two things in one message. | Every unconfirmed claim now gets one question per message, starting with whether it is true as written; a contradiction shows the file's entry and asks which is right. |
| D5 | `topic-scout` offered a single topic whose "why now" was a vendor's promotion. | A vendor's announcement or promotion is no longer a source; with fewer than three news topics, evergreen topics from the person file fill the list, each labelled. |
| D6 | Interview logs showed a summary of the saved file, not the file. | None in the skills: the run files were at fault. |
| D7 | An angle card's claim said slightly more than the fact it cited. | `angle-brainstorm` now allows no result, contrast or beneficiary that the cited entries do not state. |
| D8 | Installing from a local working folder in Claude Code copied git-ignored folders too. | None in the plugin: install from a clean clone or from GitHub. |

A reviewer then read the changed skills and found one more gap in the fact check's "not sure" branch;
it was fixed in the same round.

## What this run did not cover

- **The fact check after the D4 change.** A repeat of Tamsin's fact check on the changed skill was also
  stopped by the safety filter and not repeated. The change was checked by reading only.
- **Two editor runs**, as above.
- **Live sessions.** Every run used the skill text through an agent; nobody checked that Claude Code or
  Codex picks a skill by its description in a live session.
- **Other models.** All runs used one model.
