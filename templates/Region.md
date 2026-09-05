# Region.md

## Purpose
A full Region Overview for a single region - the referee's "how do I find this" and "how do I run this" at a glance.

## Context
Read first:
- `GENRE.md`
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`, `setting/Rumours.md`, `setting/Bestiary.md`, `setting/Factions.md`
- `setting/region/Regions.md`
- `patterns/region/Safe.md`, `Wild.md`, or `Dangerous.md` - read only the one that matches this region's rating.
- `setting/Procedures.md`

## Instructions
Fill every field below - the Tables field is authored now, not deferred. Five fields are rating-specific and apply to one rating only: **People** and **Situation** (SAFE), **Terrain** and **Foraging** (WILD), **Architecture** (DANGEROUS) - skip whichever don't match this region's rating.

**Every field names things, not qualities.** A Region Overview is read once by the referee and then mined for the rest of the campaign, so each field earns its space by giving them something to hand the players: a named object, a named person, a specific number, a stated cost. Per GENRE.md, a field with no handle in it is scenery - and a region field is the easiest place in the framework to write four sentences of atmosphere that no location ever cashes out.

**A claim made here is a promise the locations have to keep.** If this file says the region leans on a treasure table, a creature lives in a particular part of it, or a motif repeats throughout, then at 4c the locations must actually carry it - a motif stated here and mentioned by a third of the rooms it applies to has been asserted rather than built. `checks/SettingJudgementCheck.md` audits exactly this; write the field knowing it will be checked against the rooms.

- **Overview**: **Three sentences, hard.** Why a party comes here, what it costs them, and the one thing true of this region that is not true of the others. Together with the tags, this is the Referee's "how do I find this" and "how do I run this" at a glance.

  This field is the framework's worst restatement magnet, and the cap is what fixes it. The region's name, rating, die and tags are in `setting/region/Regions.md`; its history is in `setting/History.md`; what is hidden in it is in Secrets below. **None of those is repeated here.** If a sentence in this field would still be true after deleting it - because the fact is already somewhere the referee will read - it was not a sentence, it was a summary of the other files, and per GENRE.md the fact belongs at the highest level where it is true and nowhere else.

  It also states the situation and never its meaning. "The place was built to keep something in rather than keep people out" is an Overview sentence. "Run this as a place that rewards knowing when to turn around" is the referee's conclusion and the players' decision, written down before either got to make it - cut it.
- **Ambiance**: What the players see, smell and hear, and how condition and layers of history have marked the place. For a SAFE or WILD region this includes architectural style and materials; for a DANGEROUS region it narrows to sensory atmosphere only - smell, sound throughout, temperature, and humidity - since material, quality, and structural style belong to Architecture below instead.
- **Architecture** (DANGEROUS only): What the place is built from and how well - material, and the quality of construction and upkeep. Any stylistic motif that repeats throughout (a recurring arch shape, a carved sigil, a masonry pattern) tying its rooms together as one built work rather than a random assortment. Typical ceiling height and passage width, so individual rooms can default to them per `setting/Procedures.md` unless a location's own Referee Notes says otherwise.
- **People** (SAFE only): The region's inhabitants. Any customs unique to them; a formalized system of government or religion, if one exists; goods or foodstuffs they're known for. Their general temperament and appearance, and how they react to outsiders - openly, warily, or somewhere between.
- **Situation** (SAFE only): What is happening in the settlement right now - a standing state affecting every location in the region, not a random event. Soldiers camped outside, a sickness, a festival, a disputed inheritance, a shortage, somebody missing. State who is responsible, who is affected, which rung of the ladder it is on now, and what the next rung looks like. It is true whether or not the party engages and it moves on its own; it is a condition, not a plot, per GENRE.md. Distinct from the Events table, which is what happens *to* the settlement on top of it.
- **Terrain** (WILD only): The region's general ground - a single descriptor (hills, mountains, plains, forest, swamp, desert, jungle) or a specific combination of several. How difficult it actually is to move through, beyond what Layout's stated distances already imply.
- **Foraging** (WILD only): Natural plants, animals, or geological goods that can be found here. Any purported healing or magical value they carry, per GENRE.md's Low Magic - rare and priced, never commonplace. Whether they're rare or abundant, and what name they're known by locally.
- **Layout**: The region's overall shape, the kinds of places it holds and how they connect. How a party moves through it, and how large it is - state distances between its landmarks in yards (short) or miles (long), per `setting/Procedures.md`. State the region's time assumption per its rating: WILD regions default to 4 hours per action (travel, tracking, foraging, and the like all cost a slot at that scale); SAFE regions aren't time-bound at all - don't track hours there unless something specific demands it; DANGEROUS regions run on the Danger table's countdown instead of real time.
- **Features**: The main elements a party will interact with. Challenges and rewards - environmental hazards, tricks, traps and puzzles that reward both character and player skill.
- **Dangers**: How the region answers intrusion. Not every region is antagonistic; some sleep and some are alive to the presence of intruders.
- **Creatures**: Who lives here, what they are doing, how they move, and how they meet the party. Reference the Bestiary by name rather than restating stats, then add what is specific to this group - what they guard, carry or know.
- **Secrets**: What may be revealed about the setting's past or the party's immediate problems. What hidden ways exist, where, and how they are concealed.
- **Treasure**: What rewards exploration here. Gems, jewelry, precious goods, magical items, artifacts, trade goods, armament and coin.
- **Tables**: A d6 table appropriate to the region's rating:
  - SAFE regions carry a d6 Events table, rolled on entry and each week thereafter.
  - WILD regions carry a d6 Encounter table, rolled on each failed Difficulty roll.
  - DANGEROUS regions carry a d6 Danger table, counting down from 6 with each failed Difficulty roll.

## Template
```
[Code] [Region Name]

Overview: [...]

Ambiance: [...]

Architecture: [DANGEROUS only - omit for SAFE/WILD]

People: [SAFE only - omit for WILD/DANGEROUS]

Situation: [SAFE only - omit for WILD/DANGEROUS]

Terrain: [WILD only - omit for SAFE/DANGEROUS]

Foraging: [WILD only - omit for SAFE/DANGEROUS]

Layout: [...]

Features: [...]

Dangers: [...]

Creatures: [...]

Secrets: [...]

Treasure: [...]

Tables: [d6 Events/Encounter/Danger Table]
1. [...]
2. [...]
3. [...]
4. [...]
5. [...]
6. [...]
```
