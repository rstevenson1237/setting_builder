# Quests.md

## Purpose
The registry of quests - leads with a reward, each pointing at where its object lies or at
nothing on this map. Written against what the build holds.

## Context
```kdl
template scope="setting" writes="setting/Quests.md" shape="Quests"
read "setting/Rumours.md"
read "setting/region/[Region Code]/Seed.md" part="each region's"
run "--location [Location Code]"
field "Quests.Giver" from="Person.quest, Person.wants"
```

## Instructions
Write the quests `BRIEF.md` asks for, each following its fields in `patterns/Setting_Schema.md`.
A quest whose object lies at a location is written from what that location holds. A quest a
Person gives is set in that Person's `quest`, in the region's `People.md` (SAFE or WILD); a
Person who gives none keeps the slot empty. A giver in a DANGEROUS region is an Encounter's
faction or creature there, named in the Giver by its location. The Object is what that
location's entries hold, as they hold it: what the quest asks for is there.
