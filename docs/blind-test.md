# Blind test

The checker counts patterns. It cannot say whether a person would put their name on a post. This test
asks a reader that question directly, without telling them where each post came from. It has not been
run for 0.1; this page is how to run it and how to record the result.

## What you need

- **One person file** (`byline/person.md`), real or invented, and one channel.
- **Ten posts** on topics that person could write about:
  - five from byline: the `new-post` chain, or `angle-brainstorm` then `post-writer`, each on a
    different topic;
  - five from a plain request, one per topic, in a fresh chat with no person file, no style hint and
    no example: `Write a LinkedIn post in English about {topic}.` (change the channel and language to
    match).
- **A reader** who did not make the posts: the person themselves, or someone who knows their field.
- **A helper** who shuffles and labels the posts, and keeps the key away from the reader.

Use the same model for both sets, and the same five topics, so that the only difference is the method.

## Steps

1. **Collect.** Save each post as plain text with nothing around it: no file name that gives the
   source away, no "Facts used" line, no notes.
2. **Shuffle.** The helper numbers the posts 1 to 10 in a random order (for example
   `python3 -c "import random; print(random.sample(range(1, 11), 10))"`) and writes the key, number to
   source, in a file the reader does not see.
3. **Read.** The reader gets the ten texts, numbered, in one document. For each one they answer:
   - **Would you sign this?** yes, with small edits, or no.
   - **One line why.**
4. **Unblind.** Only after all ten answers are written down, the helper opens the key.
5. **Record** the result in the table below, with every answer, not only the totals.

Do not let the reader see the checker's scores before they answer. If you want them, run the checker
on all ten after unblinding.

## Record

Add one section per run to this file, or keep it with your own notes:

```
Run: YYYY-MM-DD
Person file: invented / real (no names if real and private)
Channel and language:
Model for both sets:
Reader: the person / a colleague in the field / other

| No. | Source | Would sign | Why (reader's words) | Checker label and score |
|---|---|---|---|---|
| 1 | byline / plain | yes / edits / no | | |
...

Totals: byline yes __, edits __, no __; plain yes __, edits __, no __
```

Report the totals as counts out of five, not as percentages: ten posts are too few for more. One run
is one reader's view; say so when you quote it.
