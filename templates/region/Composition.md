# Composition.md

## Purpose
One coordinated build across a region's rooms - clues, triggers, objects and interactive
features designed together and written in one pass - and its entry in the Region
Overview's Compositions field. Run before the table passes, it gets first claim on the
region's stubs; run after compile, it is a retrofit.

## Context
Read first:
- `GENRE.md`
- `STYLE.md` - the clue, secret and gate rules a composition exists to keep
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- this region's Overview, `setting/region/[Region Code].md`, including its Compositions field
- this region's `Locations.md` § Location and its connection diagrams
- every stub the build claims, and the pattern of each table a part lands in
- on a retrofit: the location file of every compiled room the build touches, and `templates/region/Location.md`

## Instructions
1. **Design the chain first**: what the party holds or knows at each link, where it is
   used, and what that yields - from the region's entrance to the last link.
2. **Claim stubs before writing new rows.** Each part fills a stub its room's class already
   allocated - a LOW room's concealed detail or treasure, a MEDIUM room's challenge. A part
   beyond its room's class is allowed only as a named exception, with its reason.
3. **Write every part in the one pass**: every cell of every row it fills or adds, in the
   format `templates/region/Allocation.md` sets, and any registry stub a part names.
4. **Write the Overview entry** in the Compositions field, per `templates/region/Region.md`.
5. **Prove it.** Every one of these holds before the pass ends:
   - every row id the entry names exists, filled;
   - solvable from the entrance: walking the diagrams from the region's way in, each
     link's inputs are reachable using only what earlier links yield - no part behind the
     gate it opens, and no cycle;
   - every link's clue is obvious in its own room, or one trigger from obvious there -
     never two triggers deep inside one room;
   - no link's clue and its answer share a room;
   - every part fills an allocated stub or is a listed exception;
   - the gate the build makes has a way round, and the way round is priced;
   - every part that is a key, lore, a quest object, a named creature or a unique treasure
     has its registry row;
   - on a retrofit, every compiled room touched is recompiled per `templates/region/Location.md`'s
     targeted rule, and every part's `Realized` cell names a line present in that room.

A build spanning regions is entered once, in the Overview of the region holding its last
link.

## Template
```
Compositions:
- [Name] - [part row ids, in the order met]; [chain: what is held or known -> where it is used -> what it yields, link by link]; way round: [the answer that is not the gate, and its price]; exceptions: [part ids beyond their room's class, with reasons, or none]
```
