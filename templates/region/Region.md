# Region.md

## Purpose
A region's seed, `setting/region/[Region Code]/Seed.md`: what its locations are written from -
how a party gets in, who is there and how they answer a stranger, and what is changing.

## Context
```kdl
template scope="[Region Code]" writes="setting/region/[Region Code]/Seed.md" shape="seed"
read "setting/Setting.md"
read "setting/History.md"
read "setting/Truths.md"
read "setting/Bestiary.md"
read "setting/Factions.md"
read "setting/region/Regions.md"
read "setting/Procedures.md" part="Time and Distance, Weather"
field "Seed.who" from="Bestiary, Factions"
field "Rung" from="Truths.Truth, History.Event"
field "Ruling" from="Seed.terrain"
```

## Instructions
Write every node the rating's `seed` names, as many as it says, each opening with the
region code. `who` names who lives here by `setting/Bestiary.md` or `setting/Factions.md`
title; the tables place them. Where `BRIEF.md` gives an `architecture` line (SAFE) or a
`construction` line (DANGEROUS), a View's outline and shows, or the Conditions, start from it and
state only what this region changes.

No location exists yet: name no location code, and place nothing in a room. A question
`setting/Truths.md` holds open, or a gap it leaves to the referee, is cited there, never
answered here.

Cut anything repeated from `setting/region/Regions.md` or `setting/History.md`, and any
value stating what the referee should conclude or the players should do.
