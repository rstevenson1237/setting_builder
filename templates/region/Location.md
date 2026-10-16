# Location.md

## Purpose
One location's write-up, `setting/region/[Region Code]/[Location Number].md`.

## Context
Read first:
- `GENRE.md`, `STYLE.md` and `BRIEF.md`
- `setting/Truths.md`
- `setting/Procedures.md`'s Forced Dangers, Conditions and Time and Distance - the mechanics a Feature cites
- `setting/Language.md` - roots for a coined name, and the coinages already recorded
- the region's seed, `setting/region/[Region Code].md`
- the location's entries, from `python3 tools/validate_setting.py --location [Location Code]`, and the setting entries they name

## Instructions
- Write every entry, and nothing without one. An entry naming this location from
  elsewhere is written as what a party meets of it here.
- Each thing a party can look at, act on, take, fight or open is its own Feature.
- A Dressing's `mark` is the faction's Identity, shown on something in the room.
- A Person is a Feature named for them: what they want and know come out in what they say
  and do, never as a list, and a `quest` they hold is cited there. A `member` is the
  referee's: the Feature shows only what the faction's Identity would show a party. A
  Garrison or a Faction's members are one Feature citing their Bestiary entry. A Purchase is written
  with its price in the Feature that sells it, a menu or sale as the goods, a service as
  the act.
- A Local Procedure is the thing a party can start - the table, the game - cited from its
  Feature; its rules stay in the entry.
- When entries change for a location already written, rewrite only the lines they touch.
- A location with no Connections entry has no Exits line.

## Template
```
[Location Code] **[Location Name]** ([type]) - *[tag], [tag], [tag]*
[Player Summary - what a party sees on arriving, to be read aloud, with each Feature it names in **bold**]
*[Referee Notes - size, shape, and what the referee needs to run the location]*
**[Feature Name]:** [the feature, where it sits, and any act on it with its effect; a hidden exit is written here, in the Feature that hides it]
**Exits:** [each exit as "[make and condition], [position] -> [Location Code] [Location Name]"; an exit off the map ends "-> [where it leads]" and comes last]
```

## Citations
Written exactly as below, so `tools/build_site.py` can link them.

- **Bestiary** - `(Demeanor, Number appearing, Bestiary : Entry Name)` - Demeanor one word, from the Encounter's reaction; Number appearing its Creature count
- **Lore** - `(Lore: Title)`
- **Keys** - `(Keys: Title)`
- **Quest** - `(Quest: Title)`
- **Named Creature** - `(Named Creature: Name)`
- **Unique Treasure** - `(Unique Treasure: Name)`
- **Magical Tome** - `(Magical Tome: Title)`
- **Hoard** - `(Hoard: Name)`
- **Local Procedure** - `(Local Procedure: Name)`
- **Table roll** - `(Treasure [I-V], d[N])` or `(Magic, d[N])`, N the table's rolls
- **Forced damage**, on every hazard Feature - `(Test of Constitution, Xd, Type)`,
  `(Test of Sanity, Xd)` where `setting/Procedures.md` has a Madness table, or
  `(Test of Fate, Condition)`; X is the count of Tests
