# Spec - content schema

Tick a line to approve it. C1 and C2 change no generated file; C3 onward each widens what a build may ask for.

## 1. The nodes, once

- [ ] **C1. Shared content nodes move to `patterns/Region_Schema.md`, defined once.** `Encounter`, `Creature`,
  `NamedCreature`, `Faction`, `Hazard`, `Mystery`, `Secret`, `Person`, `Procedure`, `Lock`, each with every member
  any rating gives it today; a rating's schema keeps a node only where it differs, by the shadowing
  `tools/tables.py` already does. `Dressing` stays per rating: its ten differing lines are layout.
  - `Hazard` and `Mystery`: `sign`, `act` and `tell` become optional beside `one-of Secret opt`; the rule that a
    WILD hazard shows itself and a DANGEROUS one hides stays as each rating's shadow.
  - Each rating keeps its own `Hazard_Type` and `Mystery_Type`.
- [ ] **C2. A rating's `folder` line is the only thing that says which tables it holds.** It is so already; C1
  makes it sufficient, so giving a rating a table is one word on that line and a `rate` in `BRIEF.md`.

## 2. What each rating may then hold

Each is one word on a `folder` line and a default `rate` of 0, so a build that does not ask gets what it gets today.

- [ ] **C3. WILD holds Rewards.** A lair's treasure, a ruin's key, lore in the open.
- [ ] **C4. DANGEROUS holds People.** A faction's leader a party bargains with by name.
- [ ] **C5. DANGEROUS and WILD hold Purchases.** A shop in a faction's hall, the lake city's market.
- [ ] **C6. SAFE holds Challenges**, for a `Secret` location only.

## 3. What the writer is shown

- [ ] **C7. No step's surface widens.** `--skeleton` prints a table for a location only where its type's `rate`
  is above 0. No tag, marker or new field appears in `setting/`; a file a region does not hold is never created.
- [ ] **C8. Proof before migration.** Region B is rebuilt through step 4 with `rate`s for Rewards and Purchases,
  on a branch. It is accepted only if the validator's warnings, `metrics.py --tells` and words per location do not
  rise against B as it stands; the readings go in this folder. The entry-text trial is why: a change that reads
  well on paper wrote longer and worse.

## 4. Later, and only if wanted

- [ ] **C9. A build may shadow a vocabulary enum.** An `enum` line in `BRIEF.md`'s fence replaces the schema's
  enum of that name (`Hazard_Type`, `Mystery_Type`, `Connection_Type`, `Safe_Type`, `Bestiary_Type`), so another
  genre's doors and traps are a brief's to name. This amends "it never overrides a schema's rules": an enum's
  items are vocabulary, a node's members are rules.
- [ ] **C10. Form apart from danger.** A region states `form` (settlement, country, interior) beside its rating;
  form picks the layout nodes, the rating the rates. The lake city becomes a WILD settlement. Largest change here.

## Asked

1. What was the earlier attempt with tags, and what did the generation get wrong: the wrong table chosen, tags
   left off, or entries that fit no room? C7 and C8 are written against the first two.
2. C3 to C6: which of these does the next build want? Any left unticked costs nothing.
