# -*- coding: utf-8 -*-
"""Regenerates the word list markdown and the word data embedded in index.html.

Source of truth: vocabulary/everyday-english-500.json. Run after editing it:
    python3 tools/build_vocab.py
"""

import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "vocabulary", "everyday-english-500.json")
MD_PATH = os.path.join(ROOT, "vocabulary", "everyday-english-500.md")
HTML_PATH = os.path.join(ROOT, "index.html")
VOCAB_START = "/* == VOCAB START == */"
VOCAB_END = "/* == VOCAB END == */"

DATA = json.load(io.open(JSON_PATH, encoding="utf-8"))
# (title, note, [(english, swedish, example), ...]) -- the shape the markdown writer expects.
SECTIONS = [
    (s["name"], s["note"], [(w["en"], w["sv"], w.get("example", "")) for w in s["words"]])
    for s in DATA["sections"]
]

total = sum(len(rows) for _, _, rows in SECTIONS)

md = []
md.append("# 500 everyday English words for a 10-year-old\n")
md.append(
"Research for Alice's word game: a list of **%d** ordinary English words and short "
"phrases, with Swedish translations, chosen for a child who already knows the very "
"basic words but whose sentences stay short and stuck.\n" % total)

md.append("""## Who this list is for

A 10-year-old who can name things (*cat, red, ball*) but freezes when the words have
to be joined into a sentence. That is not a shortage of nouns. Naming words are what
children pick up first and fastest; what is missing is the **glue** — the joining
words, helper verbs, prepositions, time words and common verbs that hold a sentence
together. So this list is deliberately front-loaded with function words and verbs, and
light on nouns she can already point at.
""")

md.append("""## How the list was chosen

Four filters, applied in this order:

1. **Frequency.** Words drawn from the high-frequency core that published corpus lists
   agree on — the New General Service List (the ~2,800 words that cover over 92% of
   everyday English text) and the A1/A2 levels of the Oxford 3000, which is the
   beginner-to-elementary core graded against the CEFR.
2. **Sentence-building power.** Literacy research calls connectives and prepositions
   *mortar words*: they hold the *brick* words (nouns) together and signal how ideas
   relate — cause, time, contrast. They are exactly what a child with a naming
   vocabulary but no sentences is missing, and they have to be taught explicitly
   because they are not picturable.
3. **A 10-year-old's own day.** Home, school, food, friends, weather, feelings,
   the trip to town. Words she can use the same afternoon she learns them.
4. **Teachability in pairs.** Each entry is one English word or fixed phrase with one
   clear Swedish partner, so it can be dropped straight into the memory game.

What was deliberately left out: rare animals, colours, numbers and other
already-known starter vocabulary; school-subject jargon; and anything needing grammar
she has not met yet.

## How the game uses it

The list is built into the app, so nothing here has to be typed in by hand.

- **Today's 10** builds the round: everything due for review (most overdue first, so easy and
  hard words mix), topped up with new words in the teaching order below. Every word carries a box
  from 1 to 5. A word answered right all through a round moves up a box and comes back later; a
  word missed anywhere in the round drops to box 1 and returns the same day. Box 5 counts as
  learned.
- **Choose a topic** runs any section below as sets of ten, in any order.
- One round is one session: meet the new words (example sentence read aloud) -> memory game ->
  typing, asked English-to-Swedish until a word reaches box 3 and Swedish-to-English after that
  -> a sentence task -> summary.
- **Sentence tasks** use the example sentences: fill the gap from four words of the same section,
  or put a scrambled sentence back in order. They cover the 83 words that carry an example, which
  are exactly the sentence-building sections (1, 2, 4, 7).
- **My own words** still takes ten typed pairs for homework and spellings, kept out of the
  progress record.

Progress is saved in the browser on that one device, so keep her on the same browser.

## Teaching order

The app follows the order below, and it is the order to pick topics in by hand:

1. **Start with sections 1–7** (glue, questions, pronouns, prepositions, time,
   quantity, helper verbs) — about 150 words and the fastest route to longer
   sentences.
2. **Then sections 8–11**, the verbs. A verb is the one thing no sentence can do
   without.
3. **Then 12–14**, adjectives, feelings and adverbs, to add detail to sentences she
   can already make.
4. **Sections 15–22** are the nouns and phrases — useful, but the least urgent, and
   the easiest to pick up from context.

## Editing the list

`vocabulary/everyday-english-500.json` is the source of truth. Edit it, then run:

```
python3 tools/build_vocab.py
```

That rewrites this file and the copy of the words embedded in `index.html`. It refuses to build
if an English or a Swedish word is used twice, because the memory game needs every pair to be
one-to-one. Where two English words would otherwise land on the same Swedish word, the Swedish
side carries a clarifier in brackets (*tall — lång (om person)*, *light — lätt (vikt)*). The app
ignores anything in brackets when it marks a typed answer, along with case, trailing punctuation,
a leading *att*, and any comma-separated alternative; a word needing something else accepted takes
an `accept` list in the JSON.
""")

md.append("## The list\n")
for i, (title, blurb, rows) in enumerate(SECTIONS, 1):
    md.append("### %d. %s (%d)\n" % (i, title, len(rows)))
    md.append(blurb + "\n")
    has_ex = any(r[2] for r in rows)
    if has_ex:
        md.append("| English | Swedish | Example |")
        md.append("| --- | --- | --- |")
        for en, sv, ex in rows:
            md.append("| %s | %s | %s |" % (en, sv, ex))
    else:
        md.append("| English | Swedish | English | Swedish |")
        md.append("| --- | --- | --- | --- |")
        half = (len(rows) + 1) // 2
        left, right = rows[:half], rows[half:]
        for n in range(half):
            a = left[n]
            b = right[n] if n < len(right) else ("", "", "")
            md.append("| %s | %s | %s | %s |" % (a[0], a[1], b[0], b[1]))
    md.append("")

md.append("""## Sources

- [New General Service List](https://www.newgeneralservicelist.com/new-general-service-list) — corpus-based core of ~2,800 words; [overview](https://en.wikipedia.org/wiki/New_General_Service_List)
- [The Oxford 3000, by CEFR level](https://www.oxfordlearnersdictionaries.com/external/pdf/wordlists/oxford-3000-5000/The_Oxford_3000_by_CEFR_level.pdf) and [about the list](https://www.oxfordlearnersdictionaries.com/about/wordlists/oxford3000-5000) — 900 words graded A1, 800 A2
- [Tier 2 words: brick and mortar vocabulary](https://www.voyagersopris.com/vsl/blog/tier-2-words) — why connectives and prepositions need explicit teaching
- [Choosing Words to Teach, Reading Rockets](https://www.readingrockets.org/topics/vocabulary/articles/choosing-words-teach) — the three-tier framework behind filter 2
- [Connectives and conjunctions word lists (KS2)](https://www.teachit.co.uk/resources/primary/connectives-word-lists) — the connective categories used in section 1
""")

with io.open(MD_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(md).rstrip() + "\n")


# --- the word data embedded in index.html -------------------------------------

def js_string(value):
    return json.dumps(value, ensure_ascii=False)


def build_block():
    """One JS array literal: sections, each word as [en, sv, example, accept?]."""
    lines = [
        VOCAB_START,
        "// Generated from vocabulary/everyday-english-500.json by tools/build_vocab.py.",
        "// Edit the JSON and re-run the script -- do not edit the words below by hand.",
        "const VOCAB_SECTIONS=[",
    ]
    for i, section in enumerate(DATA["sections"], 1):
        words = []
        for w in section["words"]:
            parts = [js_string(w["en"]), js_string(w["sv"]), js_string(w.get("example", ""))]
            if w.get("accept"):
                parts.append(js_string(w["accept"]))
            words.append("[%s]" % ",".join(parts))
        lines.append("{n:%d,name:%s,note:%s,w:[" % (i, js_string(section["name"]), js_string(section["note"])))
        lines.append(",".join(words))
        lines.append("]},")
    lines.append("];")
    lines.append(VOCAB_END)
    return "\n".join(lines)


def inject(html, block):
    start, end = html.find(VOCAB_START), html.find(VOCAB_END)
    if start == -1 or end == -1:
        raise SystemExit("index.html is missing the %s / %s markers" % (VOCAB_START, VOCAB_END))
    return html[:start] + block + html[end + len(VOCAB_END):]


html = io.open(HTML_PATH, encoding="utf-8").read()
new_html = inject(html, build_block())
if new_html != html:
    with io.open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(new_html)

# --- checks -------------------------------------------------------------------

from collections import Counter
all_en = [r[0] for _, _, rows in SECTIONS for r in rows]
all_sv = [r[1] for _, _, rows in SECTIONS for r in rows]
dup_en = [w for w, c in Counter(all_en).items() if c > 1]
dup_sv = [w for w, c in Counter(all_sv).items() if c > 1]
assert not dup_en and not dup_sv, "words must be unique on both sides: %s %s" % (dup_en, dup_sv)
assert all(r[0] and r[1] for _, _, rows in SECTIONS for r in rows), "every word needs both sides"

print("total words:", total)
print("sections:", len(SECTIONS))
print("duplicate english:", dup_en)
print("duplicate swedish:", dup_sv)
print("with example:", sum(1 for _, _, rows in SECTIONS for r in rows if r[2]))
print("wrote:", MD_PATH)
print("wrote:", HTML_PATH, "(%d bytes)" % len(new_html))
