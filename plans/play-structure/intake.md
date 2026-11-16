# Intake - play structure: what moves, and how many ways through

## The request, verbatim

> We can design 7.

## How it is read

Review item 7. `spec.md` numbers each proposal for approval; none is built.

## What the build holds today

| A published module | This build |
|---|---|
| Wandering monsters come from keyed lairs, and a lair emptied stays empty. | Every Encounter stands in one room. A region's d6 Danger table is six prose rows written at step 4e; who walks the halls is whatever those rows happen to say. |
| A level has more than one way in and more than one way down; some ways skip a level. | One way into the pyramid. Level 1 to 2 has three ways; every other pair of levels has one. No way skips a level; the lake city (G to B to H) is the one other route. |
| A key can be reached before its lock. | The tables hold that a placed key has a lock and none is locked inside itself; nothing walks the graph to see that a key can be reached. |
| A faction acts when something happens to it. | A region holds two `Rung`s; a faction holds Goals, Tactics and Reactions in prose. |

The validator already prints each region's loops and dead ends (`TOPOLOGY`), and nothing is held to them:
level 3 has one loop and nine dead ends among fifteen rooms, which the Map Judgement Check records as "It plays:
Confirmed".

## Out of scope

Timelines and countdowns, which `patterns/Setting_Schema.md` rules out; named leaders, which follow from the
content-schema plan (C4).
