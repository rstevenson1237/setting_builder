# Spec - the content loop

Each proposal has an id and a box: tick, strike or amend it. **Depends on** means the
proposal stands only if that one does too.

---

## 1. What the evidence says

Every judgement check run so far has found the same failures. Each comes from content
being decided **before** what it depends on exists, or being **rolled** where it should
be placed.

| # | Finding (source) | What produced it |
|---|---|---|
| E2 | Rates never realized at region scale: no second name in 30 rooms against 20%; 94% open edges against 60%; treasure 29 of 34 a table roll against 55% (Greywatch 5c, both addenda) | A percentage rolled per room, or not rolled at all. Nothing reads the region total |
| E4 | A household of "about ten" appears as one Khughik; encounters written with no draw, copied from the Overview's Alarm and Loot lines (addendum 2) | The Overview stated per-room occupants before any room existed. The rooms then either missed them or transcribed them |
| E6 | Keys drawn and never written; three keys named for locks at rooms where no key was drawn; one block's key leaking into the next (addendum 2) | Keys and locks discovered while writing, not placed |
| -- | Rumour 3 contradicts B.md and History; every Rumour's Settled-at pending until 5c (Greywatch 5c) | Rumours written at 2d, before any location existed |
| -- | Said once: C.17's hoard and guard transcribe C.md's Loot; C.11 and C.12 transcribe C.md's Alarm; C.18 transcribes the d6 unkeyed-rooms table (addendum 2) | The Overview held room facts, so it was written once above and again below |
| -- | Region A today: `A.md` names the pay chest's room (A.4), its key's room (A.6), the alarm's travel time, and two Secrets that `Rewards.md` and `Connections.md` also hold | The same: 3c is asked for Places, Loot, Alarm and Secrets before 4a has made a room |
| -- | Region A today: `metrics.py` MIX counts 3 treasures (2 keys) from the write-ups, where `Rewards.md` holds 5 (1 key); READ SET still names step 4f and "no pattern entry point" | metrics reads the write-ups, not the tables, so unwritten rooms are invisible to it |
| -- | Region A today: an entry with no members is an error ("is empty"), so the only to-do list is missing files; three write-ups exist with nothing to say whether their entries have moved since | No stub, and no record of what a write-up was written from |
| E1, E8 | Near-repeats a single writer cannot see; two blocks differing in dressing, not skeleton (both addenda) | Review happens once, at the end, and nothing between passes reads siblings |

The loop answers each of these in the same way:

- write the structure first;
- fill it;
- review what was written, from outside;
- place the setting's threads against what now exists;
- describe the region last.

---

## 2. The pipeline

Proposed `STEPS.md`, phases 2-6. Phase 1 is unchanged.

```
2. Build the setting            unchanged, except 2d retired (Rumours move to 5d)
3. Build the region
   3a  Regional Gazetteer                                      unchanged
   3b  Region graph                                            unchanged
   3c  Region seed - the Overview's seed fields only (L1)
4. Lay out locations - structure, no content
   4a  Locations.md - code, name, tags, type                   unchanged
   4b  Connections.mmd                                         unchanged
   4c  Stub tables - every entry each location will hold, placed to its type's rate
       targets, each a bare stub (L5, L6)
5. Content loop - 5a-5d repeat until a pass changes nothing; then 5e
   5a  Seed - fill every stub, Purpose first, one fresh context per table file; write
       every setting entry a table names (old 4c-4e)
   5b  Write - write or rewrite every location whose entries changed (L8); record
       coinages (old 4f-4g)
   5c  Review - validate and metrics; a fresh context judges this pass's write-ups (L9, L10)
   5d  Place - Rumours, Quests, Keys, Lore, Truths' Handles, History's Left lines, set
       against the locations that exist, adding the region entries each needs (L11-L15)
   5e  Brief - each Region Overview's brief fields, from the finished region (L16)
6. Judgement checks - the old step 5, trimmed (L19)
```

A pass is 5a → 5b → 5c → 5d. The next pass starts at 5a whenever the last one left any
of these:

- a stub, from 5d's new entries or 5c's findings;
- a stale write-up;
- an open review finding.

The loop exits when a pass's validate run shows no stubs and no stale write-ups, its
review raises nothing new, and its placement added nothing.

---

## 3. Proposals

### Steps

- [ ] **L1. 3c writes a Region seed; the rest of the Overview is the brief.** Each field
  of `patterns/region/*.md` is marked as either seed or brief.
  - **Seed** is what a table is written from: Kind/Settlement/Terrain, Overview, Approach,
    Conditions, Inhabitants or People (as a roster: who, how many, what they want),
    Services, Law, and the Situation with its rungs.
  - **Brief** is what can only be said once the rooms exist: Places, Alarm, Loot,
    Secrets, Tables, and what L16 adds.

  `templates/region/Region.md` writes the seed fields at 3c and the brief fields at 5e.
  The validator owes the brief fields to 5e. This is one file and one template, written
  in two passes.

- [ ] **L2. Step 4 ends at stubs (4a-4c).** The current 4c-4g move into 5a and 5b.
  **Depends on L5.**

- [ ] **L3. Step 5 is the loop (5a-5e), with the exit rule above.** **Depends on L2.**

- [ ] **L4. Renumbering.** The current step 5 becomes step 6, 2d is retired, and the
  current 4c-4g are retired into 5a and 5b. Every step-id citation in `templates/`, the
  validator's step regex and `README.md` moves with them. This is authorised by the
  request, under `README.md`'s rule. **Depends on L3.**

### Stubs, and rates as targets

- [ ] **L5. A stub is an entry with its code and no members**, for example
  `Encounter A.3`. The validator warns that it is owed to 5a, instead of raising "is
  empty". `--pending` lists stubs by file. A stub's one-of children are left out until
  5a, unless placement fixed them (L15).

- [ ] **L6. Percentages are region targets, placed rather than rolled.** At 4c, a type's
  `rate` line is met across the region:
  - `Rewards="50%"` means half that type's locations carry a Reward, and 4c chooses
    which half for a reason the tags or Purpose give;
  - a count or range (`Challenges="1-2"`) still bounds each location.

  The validator warns when a region's share is off its target by more than one location.
  `plans/location-schema`'s D3 (damage mix) and D4 (contents mix) keep their numbers, but
  as targets that metrics reports and the review reads, not rolls.

### Change tracking

- [ ] **L7. `metrics.py` reads the tables.**
  - MIX counts entries in the tables (connection types, contents, hazard damage,
    challenge kinds) per region, each against its target.
  - READ SET names 5b's context.
  - A new STUBS line counts stubs and stale write-ups.

- [ ] **L8. A write-up records what it was written from.** Its last line is
  `<!-- entries: [8 hex] -->`, a digest of the entries `--location` prints for it.
  - `validate_setting.py --stamp CODE` writes it.
  - `--pending` lists a write-up as stale when the digest no longer matches.
  - The site and PDF builders drop the comment.

  5b is then "every stale or missing write-up", and nothing else is rewritten.

### Review

- [ ] **L9. New `templates/checks/Location_Review.md`, run at 5c by a fresh context.**
  - **It reads:** `STYLE.md`, `GENRE.md`, the region seed, each write-up this pass
    changed with its `--location` entries, and the names and Player Summaries of its
    block's other write-ups, for distinctness.
  - **It judges:**
    - entries match: each entry is carried, and nothing is added beyond them;
    - the room reads as one room;
    - it is distinct from its siblings;
    - it says each thing once;
    - its tells, read;
    - it is actionable at the table.
  - **Every finding names its target:** an entry (back to 5a), a write-up (back to 5b),
    a placement (back to 5d), or the framework (to `plans/`).
  - **Output:** `setting/checks/Review.md`, one section per pass. It writes no content.

  These items leave the Setting Judgement Check, which keeps the cross-level ones (L19).

- [ ] **L10. Every pass opens its Review section with the tool readings.**
  - from validate: errors, warnings, stubs, stale write-ups;
  - from metrics: tells, and MIX against its targets.
  - what moved since the last pass, as a delta.

  A pass whose readings and findings match the last one's is the loop's exit, and the
  section says so. **Depends on L7, L9.**

### Placement

- [ ] **L11. Rumours are built at 5d, not 2d.** Each rumour is written from a location
  that holds its answer, so Settled at is filled when it is written, never left pending.
  The d20 shape (T/P/F/U shares, three pointing at a region, and so on) stands. A later
  pass replaces a rumour only for a reason the review names.

- [ ] **L12. Quests are placed at 5d.** Both the giver and the target are real codes. The
  giver end is an `Encounter` with `asks`, and the target is a `Reward` pulling `Quests:`.
  **Depends on location-schema D2.**

- [ ] **L13. Keys are placed for locks at 5d.** Every `Lock` gets a Key, as a `Reward`
  pulling `Keys:`, at a location reached by a separate trip and never behind the lock it
  opens. **Depends on location-schema D8, D9**, which become the checks that hold this.

- [ ] **L14. Old 5c bookkeeping moves to 5d.** Truths' Handles, History's Left lines and
  Lore's Found at are filled as each is placed. Step 6 then reads them as done, and a
  claim nothing delivers is a finding there, not pending.

- [ ] **L15. Placement writes the region entries it needs.** A Lock on a Connection, an
  `asks` on an Encounter, a Reward or a whole Encounter are written as stubs with the
  placed member set (`Reward A.6 contents="Keys: Tally Key"`). The locations touched go
  stale, and the next pass fills and rewrites them. Placement is the one step allowed to
  add entries to a location after 4c.

### Brief

- [ ] **L16. 5e writes each Region Overview's brief fields from the finished region.**
  - **Places:** the index, by code.
  - **Inhabitants:** as placed, with counts summed from the region's Encounters, which
    ends E4 by construction.
  - **Alarm**, and **Loot:** where the largest prize lies, as the Rewards hold it.
  - **Secrets:** each by the entry that holds it.
  - **Rumours pointing here**, by number, and **Quests that begin or end here.**
  - **The d6 tables.**

  The brief indexes and never restates: every fact it names is held by an entry, and the
  validator checks every code it cites. **Depends on L1.**

### Checks

- [ ] **L17. A table entry's text is never copied from the seed.** The Location review
  and the 6c check both flag a write-up or entry restating the seed or brief, as before.
  What is new is that 5a's template says so outright, since the seed is now in its
  Context.

- [ ] **L18. 5a reads siblings.** Each table file is filled in one context, with the
  whole file in view (as now), and with the region's Purpose and every other table's
  stub list. A table fill is the one place E1/E8 near-repeats are prevented, rather than
  only caught. This confirms the doctrine in place (table-pipeline F2) and puts it in 5a's
  template.

- [ ] **L19. Step 6 is trimmed.** `Setting_Judgement_Check.md` loses:
  - "Rates were rolled, not chosen", replaced by L6's target check;
  - its per-region write-up items: distinct, reads as a form, reads as one room, said
    once, tells. These move to L9.
  - its bookkeeping section, moved to L14.

  It keeps the brief, the genre, the tests at the top, secrets, contradictions,
  orphans, vocabulary, and the claims checked upward. The Pattern and Template checks
  change only their step ids.

### Order of work

- [ ] **L20. Prove it on region A before SAFE and WILD.** Region A is DANGEROUS and
  already built. Re-run it under the new steps: 4c stubs from its current entries, then
  passes until it exits, with 5d placing at least one quest and the rumour table. Its
  Review sections are the evidence for the step 6 check. The SAFE and WILD build-outs
  (location-schema S and W) then plug into 4c and 5a unchanged.

---

## 4. Effect on `plans/location-schema`

| Item | Under the loop |
|---|---|
| D2 (quests pathway) | Required by L12 |
| D3, D4 (damage and contents mixes) | Kept as targets per L6, not rolls |
| D5 (connection children per edge) | Unchanged; 4c places them per edge |
| D6, D7 (lethal signs; distinct rooms) | Unchanged; L9's review reads them |
| D8, D9 (key pairing; key not behind own lock) | Required by L13 |
| S8 (Purpose placed, not rolled) | Already the L6 rule; it reads as a case of it |
| S7, W5 (counts) | 4c defaults |

---

## 5. Not proposed

- **An iteration cap.** The exit rule ends the loop. A pass that keeps raising the same
  finding is a framework finding for `plans/`, not one more pass.
- **Restoring `draw.py` or `context.py`.** Placement is decided, not rolled, and
  `--location` already assembles 5b's context.
- **Keeping `Language.md`'s per-room "where it appears" out of 5b.** In a loop, a
  rewritten room should keep its coined names. The cross-build leak addendum 2 found came
  from rebuilding over an old `Language.md`, which wiping `setting/` prevents.
