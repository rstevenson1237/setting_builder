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

## What the history already held

The trial repeated a finding this repository had made twice. Had the history been read first, it would not have
been proposed.

| Commit | What it found | Here |
|---|---|---|
| 9c1354b, read in `archive/plans/table-pipeline/spec.md` E7 | "A 173-word Feature; rooms tripling in length", because "raw material and decisions [were] handed over together". The table pass and the write-up were split to stop it. | The proposal put them back together in one pass. |
| d75f614, 581a85c | Prose was budgeted, then the budgets calibrated against a clean-room generation. | A cap alone had been tried. |
| f4469bd, `fixtures/control/COMPARISON.md` item 5 | Under a checker, "the cheapest fix available was to insert a comma or swap a word to satisfy the checker". | The trial's sentences were written up to the cap. |
| ed9743f | The Feature segment and word caps were dropped. | |

f4469bd is also how this repository proves a change: one fixed map, several arms, a measured table and the
judgement items side by side. A later trial should take that shape, not one region written once.

## What remains worth a decision

The proposal as made is withdrawn. Of the two narrower changes first listed here, one was already built:

- **E1, withdrawn: staleness already leaves out placement.** A `drawn` member never marks a write-up stale
  (placement S17, typed-fields T0.3). What does: 25 of the 38 files stale today are stale on "the region's seed"
  alone, since any seed line dates every write-up of its region. Whether to narrow that is asked, not proposed.
- [ ] **E2.** The Exits line is generated: `--skeleton` prints it for step 4b, and a write-up whose Exits line
  differs from the generated one is an error naming the line to paste.
