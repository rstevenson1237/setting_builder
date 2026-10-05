# Challenges.md - DANGEROUS

## Purpose
Everything in one DANGEROUS region that stands between a party and what it wants,
`setting/region/[Region Code]/Challenges.md`: every encounter, creature, faction position,
hazard and mystery the region's rooms hold, one row each.

## Context
Read first:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- this region's Overview, `setting/region/[Region Code].md` - its Inhabitants, Conditions and Alarm
- the `setting/Bestiary.md` and `setting/Factions.md` entries the stubs name
- `setting/Procedures.md` - the forced-damage tiers a hazard's Damage cell names
- `patterns/dangerous/Encounter.md`, `patterns/dangerous/Hazard.md`, `patterns/dangerous/Mystery.md`, and the files they draw
- this file's stub rows, and the `Exits.md` rows a trap or a ward sits on

A row's room is its `Location` code and that room's § Location row - name, weight, tags.
Nothing else of the room is read: a row is a fact about one thing in one place.

## Instructions
- Which rooms get a row, and every tag on it, was settled at allocation, so this pass
  writes every empty cell of every stub no composition has claimed, and never re-decides
  a tag. The format is `templates/region/Allocation.md`'s.
- Write § Creature before § Encounter, so an encounter's Who names a written creature.
- Every row of a table is written in view of the others. Across the region the creature
  rows add up to the Overview's Inhabitants, and within one block no two hazards share a
  Mechanism and a Clue.

## Template
```
# Challenges of [Region Code] [Region Name]

## Encounter
| ID | Location | [patterns/dangerous/Encounter.md's labels] | Realized |

## Creature
| ID | [patterns/dangerous/Creature.md's labels] |

## Faction
| ID | [patterns/dangerous/Faction.md's labels] |

## Hazard
| ID | Location | [patterns/dangerous/Hazard.md's labels] | Realized |

## Trap
| ID | [patterns/dangerous/Trap.md's labels] |

## Environmental
| ID | [patterns/dangerous/Environmental.md's labels] |

## Residual
| ID | [patterns/dangerous/Residual.md's labels] |

## Mystery
| ID | Location | [patterns/dangerous/Mystery.md's labels] | Realized |
```
