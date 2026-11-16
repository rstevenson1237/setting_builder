# Spec - play structure

Tick a line to approve it. Each is one member, one target or one check.

## 1. What moves

- [ ] **P1. `roams` on an Encounter.** One optional member: the locations it walks besides its own, or its
  region's code for all of them. `BRIEF.md` sets the share that roam, per rating: `target Encounter.roams "25%"`.
- [ ] **P2. The wandering table is drawn, never written.** A region's brief gains a drawn section beside
  Inhabitants: each roaming Encounter with its citation and the room it comes from. The Danger table's rows 3 to 1
  point at it in place of naming creatures of their own; rows 6 to 4 stay signs and sounds.
- [ ] **P3. `Rung` on a Faction.** The node a region already holds, in `setting/Factions.md`: what the faction
  does when a named thing happens, in the same `if` and `then`. `BRIEF.md`'s `Factions` line sets how many.
  It states a condition, not a count of days, so the rule against clocks holds.

## 2. How many ways through

- [ ] **P4. Targets on the graph.** `BRIEF.md` holds them as it holds every other, and `metrics.py` reads them
  from the Connections tables, where `TOPOLOGY` is computed now:
  - in a DANGEROUS region: `loops`, the independent loops, and `dead-ends`, the share of its locations;
  - between each joined pair of DANGEROUS regions: `ways`, the count;
  - across the setting: `entrances`, the ways into DANGEROUS regions from any other, and `skips`, the ways
    joining two DANGEROUS regions that a third lies between.

  Today's readings, for setting the defaults against: loops 1 to 7; dead ends 0% to 60%; ways 1 for eight of nine
  joined pairs; entrances 3 (A to C, and B to G and H); skips 0.
- [ ] **P5. A key is reached before its lock.** The validator walks the setting from its origin region's way in,
  taking each way whose Lock it holds the key for, until nothing new opens. A key or location never reached is
  an error naming the lock that bars it.

## Asked

1. P4's defaults: should a level be asked for two ways down, or is one way per level the Lost City's shape and
   the target a later build's to set?
