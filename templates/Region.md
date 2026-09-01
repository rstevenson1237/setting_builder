# Region.md

## Purpose
A full Region Overview for a single region - the referee's "how do I find this" and "how do I run this" at a glance.

## Context
Consult when drafting:
- `GENRE.md` - Dangers and Secrets should be standing conditions of the place, not a scripted arc pointed at the party; magic within the region stays rare, mysterious, and priced.
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`, `setting/Rumours.md`, `setting/Bestiary.md`, `setting/Factions.md` - the material this region's fields should be drawn from and tie back to.
- `setting/region/Regions.md` - this region's Code, Name, rating, die, and tags.

## Instructions
Fill every field below - the Tables field is authored now, not deferred. Four fields are rating-specific and apply to one rating only: **People** (SAFE), **Terrain** and **Foraging** (WILD), **Architecture** (DANGEROUS) - skip whichever don't match this region's rating.

- **Overview**: A referee-facing paragraph. What this region is, how it is run, and what it is for within the module. Together with the tags, this is the Referee's "how do I find this" and "how do I run this" at a glance.
- **Ambiance**: What the players see, smell and hear, and how condition and layers of history have marked the place. For a SAFE or WILD region this includes architectural style and materials; for a DANGEROUS region it narrows to sensory atmosphere only - smell, sound throughout, temperature, and humidity - since material, quality, and structural style belong to Architecture below instead.
- **Architecture** (DANGEROUS only): What the place is built from and how well - material, and the quality of construction and upkeep. Any stylistic motif that repeats throughout (a recurring arch shape, a carved sigil, a masonry pattern) tying its rooms together as one built work rather than a random assortment. Typical ceiling height and passage width, so individual rooms can default to them per `patterns/Dressing.md` unless a location's own Referee Notes says otherwise.
- **People** (SAFE only): The region's inhabitants. Any customs unique to them; a formalized system of government or religion, if one exists; goods or foodstuffs they're known for. Their general temperament and appearance, and how they react to outsiders - openly, warily, or somewhere between.
- **Terrain** (WILD only): The region's general ground - a single descriptor (hills, mountains, plains, forest, swamp, desert, jungle) or a specific combination of several. How difficult it actually is to move through, beyond what Layout's stated distances already imply.
- **Foraging** (WILD only): Natural plants, animals, or geological goods that can be found here. Any purported healing or magical value they carry, per GENRE.md's Low Magic - rare and priced, never commonplace. Whether they're rare or abundant, and what name they're known by locally.
- **Layout**: The region's overall shape, the kinds of places it holds and how they connect. How a party moves through it, and how large it is - state distances between its landmarks in yards (short) or miles (long), per `patterns/Dressing.md`. State the region's time assumption per its rating: WILD regions default to 4 hours per action (travel, tracking, foraging, and the like all cost a slot at that scale); SAFE regions aren't time-bound at all - don't track hours there unless something specific demands it; DANGEROUS regions run on the Danger table's countdown instead of real time.
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
