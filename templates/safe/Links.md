# Links.md - SAFE

## Purpose
What ties one SAFE region's locations to the rest of the settlement and beyond,
`setting/region/[Region Code]/Links.md`: every hook - quest, lore, key, faction - and every
place the region's Situation shows, one row each.

## Context
Read first:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- this region's Overview, `setting/region/[Region Code].md` - its People roster and Situation
- the `setting/Factions.md` entries the stubs name
- `patterns/safe/Quest.md`, `patterns/safe/Lore.md`, `patterns/safe/Key.md`, `patterns/safe/Faction.md`, `patterns/safe/Situation.md`
- this file's stub rows, and the registry stubs and far locations they name

## Instructions
- A hook names a location or a registry entry elsewhere, so this file is written once
  every location its rows name has its tables filled, in the pass that fills the setting's
  connected stubs. The format is `templates/region/Allocation.md`'s.
- Write every empty cell; never re-decide a tag allocation settled. Every person named is
  on the Overview's People roster.
- Every row is written in view of the others: one settlement's hooks send a party to
  different doors, and its Situation shows differently at each place that shows it.

## Template
```
# Links of [Region Code] [Region Name]

## Quest
| ID | Location | [patterns/safe/Quest.md's labels] | Realized |

## Lore
| ID | Location | [patterns/safe/Lore.md's labels] | Realized |

## Key
| ID | Location | [patterns/safe/Key.md's labels] | Realized |

## Faction
| ID | Location | [patterns/safe/Faction.md's labels] | Realized |

## Situation
| ID | Location | [patterns/safe/Situation.md's labels] | Realized |
```
