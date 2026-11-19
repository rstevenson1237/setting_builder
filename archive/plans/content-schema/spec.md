# Spec - content schema

Tick a line to approve it. Each of C1 to C4 is one word on a `folder` line, a node copied into that rating's
schema as 3c24a31 has each rating hold its own, and a default `rate` of 0, so a build that does not ask gets what
it gets today.

## 1. What each rating may hold

- [x] **C1. WILD holds Rewards.** A lair's treasure, a ruin's key, lore in the open: the hook layer's "WILD
  carries" (bdc375e) and the archived spec's W4, with its W7 as the node's rule - a container says what weather
  has done to it, and lore outdoors is cut, never written.
- [x] **C2. A Named Creature is met by name.** A faction's leader a party bargains with by name, in place of
  DANGEROUS holding People: its entry gains `Asks`, `Member` and `Quest`, as a Person's `wants`, `member` and `quest`.
- [x] **C3. WILD holds Purchases**, the lake city's market. DANGEROUS keeps no shop: a Named Creature met
  there may sell one thing, a `Purchase` under it.
- [x] **C4. SAFE holds Rewards**, the archived spec's S6: what is there to be stolen. And Challenges, for a
  `Secret` location only.

## 2. What the writer is shown

- [x] **C5. No step's surface widens.** `--skeleton` prints a table for a location only where its type's `rate`
  is above 0. No tag, pool or new field appears in `setting/` beyond C2's three; a file a region does not hold is never created.
- [x] **C6. Proof as f4469bd made it.** One fixed region built twice from the same brief, with and without the
  new rates, and compared on a measured table (words a location, validator warnings, tells) and on the Setting
  Judgement Check's items. The readings are `proof.md`. Accepted only if nothing measured gets worse.

## 3. Withdrawn after the history was read

- **Shared nodes in `Region_Schema.md`.** It is #71's state, which #72 undid on purpose. Of the nodes more than
  one rating holds, five have not drifted by a line in the month since and four by one to three lines; that is
  recorded here as a reading, and proposed as nothing.
- **A build shadowing a vocabulary enum.** Built twice (tag pools, genre lists) and retired twice. A build that
  needs a word adds it to the schema's enum, as #95 did.
- **Form apart from danger.** Too large to propose on one build's evidence.

## Asked

1. C1 to C4: which does the next build want? Any left unticked costs nothing. - All four, C2 and C3 as amended above, each at a rate of 0 until a build asks.

Answered: WILD's Rewards and DANGEROUS's People were never declined. The schema was built one setting at a time,
each proving or widening the workflow, and no build since #68 has asked for them.
