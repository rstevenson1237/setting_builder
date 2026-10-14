# Quests.md

## Purpose
The registry of quests - leads with a reward, each pointing at where its object lies or at
nothing on this map. Written at step 5d, against what the build holds.

## Context
Read first:
- `GENRE.md`
- `BRIEF.md`
- `patterns/Common_Schema.md` and `patterns/Setting_Schema.md`
- `setting/Rumours.md`
- each region's seed, `setting/region/[Region Code].md`
- the location entries or setting entries a quest points to

## Instructions
Write the quests `BRIEF.md` asks for, each following its fields in `patterns/Setting_Schema.md`.
A quest whose object lies at a location is written from what that location holds.

## Template
```
Quests of [Setting Name]

| Name | Ask | Giver | Reluctance | Object | Obstacle | Terms | Points to |
|---|---|---|---|---|---|---|---|
| [Quest Name] | [ASK] | [who wants it, and how a party hears of it] | [RELUCTANCE] | [what specifically] | [OBSTACLE] | ["stated in the giver's own words"] | [Location Code, Table: Title, or nowhere on this map] |
```
