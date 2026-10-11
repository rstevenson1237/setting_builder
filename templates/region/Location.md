# Location.md

## Purpose
One location's write-up, `setting/region/[Region Code]/[Location Number].md`.

## Context
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md`
- `setting/Truths.md`
- `setting/Procedures.md` - the mechanics a Feature cites
- `setting/Language.md` - roots for a coined name, and where it is recorded
- the Region Overview, `setting/region/[Region Code].md`
- the location's entries, from `python3 tools/validate_setting.py --location [Location Code]`, and the setting entries they name

## Instructions
- Write every entry, and nothing without one. An entry naming this location from
  elsewhere is written as what a party meets of it here.
- Each thing a party can look at, act on, take, fight or open is its own Feature.
- When entries change for a location already written, rewrite only the lines they touch.

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
- **Table roll** - `(Treasure [I-V], d20)` or `(Magic, d6)`
- **Forced damage**, on every hazard Feature - `(Test of Constitution, Xd, Type)`,
  `(Test of Sanity, Xd)`, `(Test of Fate, Condition)` or `(Test of Fate, Impact)`, per
  `setting/Procedures.md`
