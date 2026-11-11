# Add a language

A language is one JSON file, `skills/slop-check/rules/<code>.json`. The checker's code does not change.
Read `how-the-check-works.md` first: it explains what each list is used for.

## Steps

1. **Copy** `skills/slop-check/rules/en.json` to `skills/slop-check/rules/<code>.json`. The code is two
   lower-case letters (ISO 639-1, such as `de` or `es`): the checker only picks up files named
   `[a-z][a-z].json`, and the `code` inside the file must equal the file name.
2. **Fill the lists** for your language (keys below). Write every entry the way the checker normalises
   text: lower case, straight quotes (`'` and `"`), no Latin diacritics (`día` → `dia`), `ё` as `е`.
3. **Set `"status": "beta"`.** The report then tells the reader that the rules are not measured yet.
4. **Validate the file:**

   ```bash
   python3 -c "import json, sys; sys.path.insert(0, 'skills/slop-check/scripts'); from slopcheck import rules; print(rules.validate(json.load(open('skills/slop-check/rules/<code>.json', encoding='utf-8'))) or 'ok')"
   ```

   It names every problem: a missing key, an unknown status, an entry not in normalised form (with the
   form it expects), a regular expression that does not compile, an unknown threshold.
5. **Add `tests/test_scan_<code>.py`** with, for each marker family, one text that hits and one that
   misses: `vocab`, `contrast`, `triad`, `fragments`, `dash` and `closer`. Call
   `scan.scan(text, language="<code>")`. `tests/test_scan_ru.py` is a model.
6. **Update the language list** in `tests/test_rules.py` (`test_available_languages`), and add a sample
   of your language to the detection test there.
7. **Run the suite:** `python3 -m pytest`. A new `detect_markers` list can steal detection from another
   language, so fix any detection test that breaks by choosing more distinctive words, not by deleting
   the test.

## Keys

`code`, `name`, `status`, `detect_markers` and `vocab` are required; every other key is optional. An
optional list that is missing is empty.

| Key | Type | What it does |
|---|---|---|
| `code` | string | The language code; equal to the file name. |
| `name` | string | The name printed in the report, such as `German`. |
| `status` | `"beta"` or `"measured"` | `beta` until the language passes the release bar (below). |
| `detect_markers` | list of words | Common, distinctive words of the language. Detection needs 3 distinct ones in a text and a lead of 2 over the next language. Avoid words that other languages share. |
| `vocab` | list of entries | Words and phrases common in machine prose. Entry forms below. |
| `endings` | list of suffixes | Endings a plain single-word `vocab` entry may take (`["s", "ed", "ing"]`). |
| `final_e_endings` | list of suffixes | For a single word ending in `e`: the `e` is replaced by one of these (`["e", "es", "ed", "ing"]`, so include `e` itself). |
| `closers` | list of phrases | Closing clichés, matched at the end of the last line (`"thoughts?"`, `"what do you think"`). A phrase may be followed by up to two words, or, after its own `?` or `!`, a short sentence of up to three words. |
| `reader_words` | list of words | Words that address the reader (`you`, `your`). A last-line question with one of them is a `closer`. A word ending in `*` is a stem (`ваш*`). |
| `contrast` | list of regular expressions | Shapes of "it's not X, it's Y". Matched on normalised text, multi-line mode. |
| `negation_words` | list of words | If one of these is among the six words before a `vocab` hit in its clause, the hit is not counted ("stop saying ..."). |
| `negation_phrases` | list of regular expressions | Same, matched against the 60 characters before the hit (`\bno\s+more\b`). |
| `list_leads` | list of words | Words stripped from the start of a comma item before it is judged (`and`, `or`, as in "faster, cheaper, and calmer"). |
| `not_item_start` | list of words | A comma item that opens on one of these is not a list item (`that`, `because`, `yes`). |
| `parentheticals` | list of words or phrases | A comma item that is only one of these is not a list item (`honestly`, `of course`). |
| `middle_only_parentheticals` | list of words | Entries of `parentheticals` that are skipped only as the middle item; as the first or last item they count. |
| `thresholds` | object | Overrides by name: `density_markers` (3), `dash_per_100_max` (1.0), `dash_min_count` (2), `fragment_run` (3), `fragment_max_words` (3), `triad_item_max_words` (4), `triad_line_max_words` (12), `hashtag_max` (5, used with no channel). Any other name is an error. |

**`vocab` entry forms:**

- A single word takes `endings`, or `final_e_endings` if it ends in `e`: `leverage` matches
  "leveraged" and "leveraging".
- A single word ending in `*` is a stem that takes any ending: `optimi*`.
- A phrase of several words matches across any whitespace, as written: `lean into`.
- `re:` starts a raw regular expression: `re:the future of \w+ is here`.

Each entry matches whole words only. In JSON, double every backslash (`"\\b"`).

## From beta to measured

A language becomes `measured` only with a reference set and a holdout that passes the release bar.
`reference/README.md` describes how the English set was built; follow the same rules:

- Human texts published by at least three authors before the date that model-written text became
  common (for English, November 2022), under a licence that allows them in this repository, and
  machine texts written from a one-line prompt. Record each in `reference/manifest.json`.
- Files go to `reference/<code>/human/` and `reference/<code>/machine/`.
- A tuning set to tune on, and a holdout of **10 human and 10 machine texts** collected by someone who
  does not tune the rules, run once.
- **The bar, on the holdout:** no human text `heavy`, at most 2 human texts `some`, at least 7 of 10
  machine texts not `clean`. Record the run, pass or fail, in `reference/RESULTS.md`.
- Only then set `"status": "measured"`. `tests/test_reference_set.py` checks that a measured language has
  `reference/<code>/human/`; extend its bar test to your language's holdout rows.

**Admitting a new marker once a reference set exists.** A new `vocab` entry, contrast shape or other
marker word is admitted only if it occurs in at least 3 tuning machine texts and in no tuning human text.
A whole-post pattern may be tightened when it fires on tuning human texts. Thresholds, weights and bands
may change, but only on the tuning set: a holdout that has been run is spent, and any later change to a
rule, constant or pattern has to be judged on a new holdout.
