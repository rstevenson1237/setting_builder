---
code: <R##>
name: <The region's name. Decomposes into roots recorded in T-LNG.>
tags: [<three>, <thematic>, <tags>]
type: <SAFE | WILD | DANGEROUS. The primary classifier. Read it first.>
difficulty: <d4 | d6 | d8 | d10 | d12. A larger die is easier; d8 is average.>
weight: <low | medium | high. Sets the location count band at Milestone 6.>
container: <the setting-level container this region sits in>
containers:
  - id: <lowercase-slug>
    name: <The region-level container's name. It groups locations and nothing more.>
sources: [<T table entry IDs, never S>]
schema_version: 1
---

## Overview

<Player register, written at step 8. What a person standing anywhere in this
region sees, hears and is walking on. Shows, never concludes, carries no token.
Three or four paragraphs, and every noun in it is true across the whole region:
anything true of one location belongs in that location.>

## Fields

<Referee register, written at step 7. The region's working numbers as
`**Label:** value` lines: extent, the rates a party moves at, the unit time is
counted in, and what the difficulty die measures here. `None` is a legal value
with a reason after it. The units are the ones the region's type requires.>

## Tables

### <Events | Encounters | Dangers, by region type>

<Six rows on a d6. Events and Encounters count up; Dangers count down from 6 to
1, each rung a step further into the region.>

| Roll | <Event \| Encounter \| Danger> |
| :--- | :--- |
| <1> | <Entry register: a fragment a referee reads aloud from the table at speed.> |

### Weather

<Six rows, and only where the region has outdoor extent.>

| Roll | Weather |
| :--- | :--- |
| <1> | <What the sky is doing, and what it does to sight, sound and the rate.> |

## Connections

<Referee register, written at step 6. What the region's shape is and how its
containers divide it. The edges themselves live in this region's
`connections.md`, which is the source of truth for every diagram below.>

## Diagram

<!-- DIAGRAM: T3_<R##>.md -->

<!-- DIAGRAM: T4_<R##>_<CONTAINER>.md -->
