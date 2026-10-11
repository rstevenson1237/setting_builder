# Brief.md

## Purpose
A region's brief, `setting/region/[Region Code]/Brief.md`: a run sheet written once the
region's locations exist. A referee holding it and the seed can run an excursion into the
region without opening a location.

## Context
Read first:
- `GENRE.md`
- `BRIEF.md`
- `patterns/region/Safe.md`, `patterns/region/Wild.md`, or `patterns/region/Dangerous.md` - read only the one that matches this region's rating.
- this region's seed, `setting/region/[Region Code].md`
- this region's table files and `Connections.mmd`
- `setting/Rumours.md` and `setting/Quests.md`

## Instructions
Write the BRIEF block of this region's rating file, every field filled, from the tables
alone. Each rating has its own field set, shown below; write only this region's.

Every fact about a location names it by code; a count is summed from the
entries. A fact no entry holds is a placement for step 5d, not a line here. Nothing the
seed says is repeated.

A field that holds several things - places, secrets, leads - writes each as its own `- `
line under the field's label. Every other field is prose, and short. Each Tables entry
holds two d6 tables.

## Template
```
Places:
- [Code or codes] [Name] - [...]

Alarm: [DANGEROUS]

Loot: [WILD, DANGEROUS]

Secrets:
- [the fact] - [who knows it]; [the entry that brings it out]

Leads:
- [Rumour N or Quest Name] - [...]

Tables:
d6 [Events / Encounter / Danger], [when it is rolled]
1. [...]
2. [...]
3. [...]
4. [...]
5. [...]
6. [...]
d6 [what is met where nothing is keyed]
1. [...]
2. [...]
3. [...]
4. [...]
5. [...]
6. [...]
```
