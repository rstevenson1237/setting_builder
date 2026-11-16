# Intake - entry text: a location rendered from its tables

## The request, verbatim

> 1 we need to prove an improvement, the two step process was intentional to provide constraints to llm
> verbosity that the simple question and design pattern approach struggled with.

## How it is read

The review proposed writing each Feature's sentence in the table entry it comes from and rendering a location's
page from the tables, in place of step 4b's write-up file. It is not to be built unless it is shown to be better
than the two steps that stand: tables in terse cells (4a), then a write-up from them (4b).

## The trial

Region K, eight locations, whose write-ups had not been read. From K's tables alone, one sentence was written
for each entry under a word cap (read-aloud 40, referee note 45, Feature 28), and `render.py` here built each
location's page from the tables and those sentences: header, citations and Exits were generated, never typed.
The rendered pages were put in place of K's write-ups, run through the validator and `metrics.py --tells`, and
taken out again.

| | Step 4b's write-ups | Rendered from capped sentences |
|---|---|---|
| Words, eight locations | 923 | 1,171 |
| Read-aloud | 145 | 215 |
| Features | 21, 314 words, longest 38 | 26, 502 words, longest 28 |
| Validator | 0 errors, 0 warnings | 0 errors, 6 warnings |
| Tells | 0 | 2 |

## What it shows

- **No improvement.** The cap held the longest Feature and raised the average: the sentences were written up to
  it. The six warnings and both tells are in the authored sentences. The two steps wrote less and wrote it cleaner.
- **The generated parts were right by construction**: every citation and every exit passed the validator untyped.
  Header, Exits and citations are 310 of K's 923 write-up words.
- **Staleness is mostly about placement.** Seven of the eight stale write-ups the last Setting Judgement Check
  lists "name no direction and still hold": a re-plan moved a wall or a room, which the prose does not carry.

## What remains worth a decision

The proposal as made is withdrawn. Two narrower changes follow from the trial, neither built:

- [ ] **E1.** A write-up is stale only when a field it carries changes: a Dressing's `xyz`, and a Connection's
  `wall`, `bearing` and `distance`, stop marking it stale. The validator's direction check still holds any
  direction the prose names.
- [ ] **E2.** The Exits line is generated: `--skeleton` prints it for step 4b and the validator rewrites nothing,
  but a write-up whose Exits line differs from the generated one is an error naming the line to paste.

One trial, one region, written by the model that made the proposal: it is evidence, not proof either way.
