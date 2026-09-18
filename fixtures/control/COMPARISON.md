# P0.2: the control, three arms, read

The same twelve-room map, three ways. This file is the acceptance artifact P0.2 names: an
item-by-item, arm-by-arm table, and one sentence per item saying which framework artifact
produced the difference, or that nothing did.

---

## Methodology, and what deviated

- **Arms 0 and 1 were written before any framework file was opened in this session.** The
  framework was read only afterwards, for arm 2. What could not be undone is that
  `INTROSPECTIVE.md` Part two, read first as the task instruction, describes the endorsed
  baseline's register in some detail. Arms 0 and 1 are therefore a fair test of the
  *prompts*, and a slightly generous one.
- **Arm 1 ran without its Notes.** `Rules_Light_TTRPG_Design_Notes.md` is out of tree per
  D1 and was not supplied to this session. `arm1-prompt.md` itself calls the Notes "the
  major context piece, since they carry the baseline content, genre included," so arm 1
  here is the eighty-word prompt alone. **Every row below that credits the framework with
  beating arm 1 on setting content has to be discounted by that,** and the rows where arm 1
  wins anyway are the load-bearing ones.
- **Arm 1b was not regenerated.** Per P0.2 it is a reading, and it is used here only as the
  register the user has endorsed.
- Arm 2 is `STEPS.md` 3c and 4c as they stand: one DANGEROUS region of one block, twelve
  locations, on a two-line brief. It also had to do 4a and 4b by hand, because the map
  conversion `tools/map.py` (P4.3) does not exist. Its registry rows are held at
  `arm2/registry-stubs.md` so the control does not alter the corpus the checks are tuned
  against; the validator run below was done on a scratch copy with them spliced into
  `setting/`.

## Measured

| | Arm 0 | Arm 1 | Arm 2 | Arm 1b (endorsed) |
|---|---|---|---|---|
| Words of prompt / context | 10 | ~80 (Notes missing) | 2-line brief + ~24,000-word read set | ~70 |
| Keyed rooms | 12 | 12 | 12 | 26 + a 4-location town |
| Output words | 1,171 | 1,381 | 4,312 (2,787 in the room entries) | 11,192 |
| Words per keyed room | 98 | 115 | 232 | 322 |
| Mean words per sentence | 15.7 | **9.6** | **27.9** | 13.8 |
| Addressable things per room | not itemized (prose) | **4.7** (56 bullets) | 4.2 (50 Features) | not itemized (prose) |
| `rather than` | 1 | 0 | 8 -> 2 after a pass | 3 |
| Absence claims | 1 | 5 | 8 -> 1 after a pass | 4 |
| Conclusion tells | 2 | 0 | 2 -> 0 after a pass | 11 |
| Validator | n/a | n/a | **0 errors, 14 warnings** | n/a |
| Tags | no | yes, 10 in a key | yes, 2 per room, drawn from two pools | no |
| B/X stat lines | prose blockquote, no numbers | **yes, full** | **no** - AD citations only | - |

The tell columns show first draft, then after one correction pass against
`tools/metrics.py --tells`. Arms 0 and 1 got no such pass, because they have no tool to
run one against - that asymmetry is itself a result and is row 11 of the table below.

---

## Item by item

Judged on `templates/Setting_Judgement_Check.md`'s items, plus P0.2's own question.

| # | Item | Arm 0 | Arm 1 | Arm 2 | What produced the difference |
|---|---|---|---|---|---|
| 1 | Locations reinforce their region | n/a - no region exists | n/a - no region exists | **Confirmed** | `templates/Region.md`'s "a claim made here is a promise the locations have to keep": the region's hauled-stone motif is carried by nine of twelve rooms, not asserted once. Arms 0 and 1 have no level above the room, so there is nothing to reinforce - not a failure, an absence of the tier. |
| 2 | Regions reinforce the setting | **Fail** - invents its own history from nothing | **Fail** - same | **Confirmed** | `setting/History.md`'s Left lines. Arm 2 did not invent a backstory: it filled the one Left mark History already owed and no location carried (the old crown seat), and `setting/Lore.md`'s existing Old Seat Milestone at B.6 already names it and its distance. Nothing in arms 0 or 1 could do this, because there is nothing for them to attach to. |
| 3 | Discrete and discoverable, not vague | **Needs attention** - "lights move behind the hillside", an ending that states the moral | **Confirmed** | **Confirmed** | Nothing the framework owns. Arm 1 hit this off eighty words: every room got a named object, a stated trigger and a position. `dangerous/Dressing.md`'s Position guidance did not beat the instruction "use tags and short descriptive sentences to provide enough information to make rulings." |
| 4 | Information is tiered, and the chain holds | **Fail** - room 4 wakes a guardian with no clue anywhere; room 12's book has no visible way in | **Confirmed** | **Confirmed** | `patterns/dangerous/Low.md`'s split concealment rates and `templates/Location.md` instruction 6. Arm 1 reached the same place without them, by writing a clue into every trap. What the framework adds over arm 1 is the *rationing* - arm 1 puts something behind a clue in eight of twelve rooms, which teaches a party to search everything; arm 2 does it in six, four of them concealment structures proper, because the rate is written down. |
| 5 | Recurring elements actually recur | **Fail** - nothing recurs beyond one room | **Needs attention** - the count motif recurs in 3 rooms, invented and dropped | **Confirmed** | The five registries and the 4c stub rule. Arm 2 produced four Lore rows, one Key with a real two-ended obligation (F.4 supplies, F.12 demands), one Quest stub and one Named Creature - all of which survive into a second session because they live outside the location files. **This is the framework's single clearest win and it is the one Part two predicted.** |
| 6 | Genre held across levels | **Fail** - an authored plot with a written ending | **Confirmed** | **Confirmed** | `GENRE.md`. Arm 1 held the genre on the four words "do not create a story" - the same four words `GENRE.md` spends a section on. Arm 0 shows what happens without them, and it is the largest single quality gap in this table. |
| 7 | The three tests, hardest at the top | **Fail** | **Needs attention** - 5 absence claims, all in room text | **Needs attention** - 1 absence claim left, and it is *mandated* | `GENRE.md`'s tests catch arm 1's five. But arm 2's last one is `templates/Region.md`'s Overview field demanding "the one thing true of this region that is not true of the others," which is an absence claim across space by construction. **A template requires a line the authorities forbid, and the corpus obeys the template: E.md carries the identical construction.** This is a finding for P1 and it is the sharpest thing in this table. |
| 8 | Claims made upward are kept downward | n/a | n/a | **Confirmed** | `tools/validate_setting.py` plus the check's own upward read. Arm 2 closed a Room to Grow item that has been open since the History was written. Unavailable to arms 0 and 1 for the same reason as item 1. |
| 9 | Reinforcement candidates are named | n/a | n/a | **Confirmed** - Ranik appears once; Sarnar is coined once | The check itself. No arm-0/1 equivalent exists. |
| 10 | Vocabulary is precise, and precise is not decorative | **Needs attention** - "saddest", "fearsome", mood adjectives | **Confirmed** | **Confirmed** - but 10 first-draft gloss hits, which `tools/metrics.py` itself documents as the loosest of its four checks and prone to over-report | `dangerous/Dressing.md`'s and `Door.md`'s compiled vocabulary lists (jamb, pintle, corbel, revetment, plank-and-batten) are visibly drawn on in arm 2 and absent from arms 0 and 1 - but arm 1 was not *worse* for it at the table, because it named plain things precisely instead. |
| 11 | Coinage is tracked, not orphaned | **Fail** - "Ashcroft" is coined from nothing | **Fail** - "Morthek"-style names coined ad hoc | **Confirmed** | `setting/Language.md`. Sarnar is sarn + ar from the Marchspeech root list, glossed, and recorded back. Arms 0 and 1 have no root system, so their names are untraceable - which costs nothing in a one-shot and everything across a campaign. |
| 12 | Mechanical validation | **None possible** | **None possible** | **0 errors, 14 warnings** | `tools/validate_setting.py`. It caught 11 real errors and 49 warnings on arm 2's first draft - a semicolon in a Feature, a leading article in a label, a Player Summary promising a feature that did not exist below it, seven missing registry stubs, and an unrealized region edge. **Nothing in arms 0 or 1 could have caught any of them, and nothing in arms 0 or 1 needed to, because they have no invariants to break.** |
| 13 | **Could a referee run it tonight?** | **No** - the ending decides the session in advance, and two rooms have no stated way in | **Yes** | **Yes, with one page of setup** | Arm 1 is runnable as printed. Arm 2 is runnable only with `setting/Procedures.md` open, because every hazard is written as `(Test of Constitution, 1d, Crushing)` rather than as a number - and it is *not* runnable without also knowing Telar. The framework buys campaign coherence by making the page non-portable. |

---

## The three things the prompt asks for and the framework claims to supply

P0.2 names this as the sharpest reading in the table. It is, and two of the three go
against the framework.

**Tags.** Arm 2 is better, narrowly. Arm 1 invented ten tags to suit the dungeon and used
them well. Arm 2 drew two per room from a setting pool and a region pool that already
existed, so a tag means the same thing in F.9 as in A.3 and a referee who has read one
region can read the next. For one twelve-room dungeon this buys nothing at all; across five
regions it is the difference between a vocabulary and a habit. **Verdict: framework, and
only at scale.**

**Short descriptive sentences.** Arm 1 is better, and not narrowly. Arm 1 averages 9.6
words per sentence; the endorsed baseline averages 13.8; arm 2 averages 27.9. The cause is
not prose style, it is a rule: `templates/Location.md` instruction 5 makes a Feature exactly
one sentence, so every fact about a thing - its material, its position, its trigger and its
cost - is comma-welded into a single clause. The instruction was written to *stop* trailing
explanatory clauses, and the eight-word segment cap does hold the pieces short, but the
sentence the pieces add up to is three times the length of the register the user endorsed.
**Verdict: arm 1, decisively, and P1.3 should set its sentence budget from arm 1b's measured
14 rather than from the Feature grammar.**

**B/X stat lines.** Arm 1 is better, and it is not close. The prompt says "B/X style stat
lines for creatures" and arm 1 prints `AC 8, HD 2, hp 9 each, MV 60'(20'), #AT 1 grapple, D
special, Sv F2, ML 12, AL C, XP 20` - which a referee runs from the page. Arm 2 prints
`(Ancient, 1, Bestiary : Bound Dead)` and the referee goes and looks it up, and what they
find is `AD: 3d6+2 [MA: 1]` in a scale that is this framework's own. The framework does not
supply B/X stat lines at all; it supplies a citation to a bespoke one.
**Verdict: arm 1, and this is the clearest case in the table of the framework charging for
something the control gets free.**

---

## What this decides for Phases 3 and 6

1. **The registries earn their keep and nothing else measured here does at this scale.**
   Items 2, 5, 8 and 11 are the four the framework wins outright, and all four are the same
   mechanism: content that lives outside the location file and survives the context window.
   Part two predicted exactly this. Phase 3 should cut toward that and away from prose rules.
2. **The prose rules lost their own contest.** Arm 1, on eighty words and no rules document,
   passed items 3, 4, 6 and 10 - four of the five items the 45,774 words of `patterns/`
   exist to secure. `patterns/` did not make arm 2 better on those items; it made arm 2
   *checkable* on them, which is item 12 and is a different claim.
3. **The validator is the framework's second real product, and it is under-tuned.** It
   caught eleven genuine errors. It also emitted the same uninformative warning nine times
   in the baseline corpus and four more times on arm 2 - `Exits lists X -> Y as mundane, but
   the region Connections.mmd marks it hidden` fires on *every* secret edge in the setting,
   so it carries no signal at all. P1 should fix or drop it.
4. **Two rules in the framework fight each other**, and P1 has to settle both:
   `templates/Region.md`'s Overview field mandates an absence claim `GENRE.md` forbids
   (item 7), and `templates/Location.md`'s one-sentence Feature rule produces the sentence
   length the user's own endorsed output does not have.
5. **The correction pass is worth watching.** Arm 2's first draft had 19 tells; a single
   pass against `tools/metrics.py --tells` took it to 4. Twice during that pass the cheapest
   fix available was to insert a comma or swap a word to satisfy the checker without
   changing the sentence - which is the failure `INTROSPECTIVE.md` F2 names, reproduced
   under laboratory conditions. Both were rewritten properly instead, but the temptation was
   real and a tired generator will not resist it.
6. **The map format needs `tools/map.py` before anything else in Phase 4.** Converting
   twelve rooms by hand surfaced three decisions the room list cannot carry - an unkeyed
   corridor with five mouths, no vertical or one-way edges anywhere, and two doors from one
   room leading to the same neighbour. See `arm2-prompt.md`'s conversion notes. All three
   will recur on every map the user draws.
