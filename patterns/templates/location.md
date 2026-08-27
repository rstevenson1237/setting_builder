---
code: <R##-L##>
name: <The location's name. Decomposes into roots recorded in T-LNG.>
tags: [<three>, <thematic>, <tags>]
region: <R##>
container: <the region-level container this location sits in>
cell: <TYPE_WEIGHT. The region's type, then this location's weight.>
pattern: <report only, never fails a check. The shape this location takes.>
sources: [<T table entry IDs, never S>]
schema_version: 1
---

## Player Overview

<Player register, written at step 12. What arriving and looking gives, in the
order a party meets it. Shows, never concludes, carries no token. Every bolded
noun here appears below as a feature (M17), and the length band is the cell's.>

## Referee Overview

<Referee register. The fields the region's type requires, as `**Label:** value`
lines, written at step 11. `None` is a legal value with a reason after it (M22).
Then the prose a referee rules from, written at step 12: what is true that the
Player Overview withholds, the reactions and their branches, the gate and both
prices, what the place costs in the region's time unit, and the straight
instances funding any reversal, by code.>

**<Approach | Service | Reactions>:** <value>

**<Terrain | Cost | Gate>:** <value>

**<Refusal, on SAFE only>:** <value>

## Features

<Written at step 11. One `### Name` per feature, in the order the Player
Overview names them. Each opens with what the thing is, then what it does, then
what a named physical action reaches inside it. A connection pointer `-> R##-L##`
appears inside a feature and nowhere else in the file (M23).>

### <Feature name>

<What it is, what it does, and what is inside it. Mechanics as tokens beside the
sentence they belong to, referee-facing (M21).>

## Exits

<Every edge this location carries, and the region's `connections.md` is the
source of truth for the edges themselves (M7, M8). One row per exit, and every
cue is what a party notices from inside this location looking that way.>

| To | Type | Cue |
| :--- | :--- | :--- |
| <R##-L##> | <the connection type, as written in connections.md> | <what is noticed from here, sensory, at a stated distance where there is one> |
