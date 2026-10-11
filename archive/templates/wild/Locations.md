# Locations.md - WILD

## Purpose
The location table of one WILD region, `setting/region/[Region Code]/Locations.md`: every
location as a row - named, tagged and classified - and the tables of what each place is.

## Context
Read first, every step:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- this region's Overview, `setting/region/[Region Code].md`, and its die in `setting/region/Regions.md`

Then, by step:
- **4a** (names and tags): nothing more.
- **4b** (classifications): what each guarantees - `patterns/wild/Landmark.md`, `patterns/wild/Hidden.md`, `patterns/wild/Secret.md`.
- **4f** (the place tables): the stubs of the class, kind, Faction and Dressing tables; § Location; `patterns/wild/Dressing.md`, the three class files above, and the kind files `patterns/wild/Ruin.md`, `patterns/wild/Lair.md`, `patterns/wild/NaturalFeature.md`, `patterns/wild/Crossing.md` and `patterns/wild/Faction.md`, for their own lines; `setting/Bestiary.md` and `setting/Factions.md` entries the stubs name; the rows a Payload row names.
- **4g** (naming): `patterns/setting/Naming.md`; `setting/Language.md`; every row in the region naming the location.

## Instructions

**Count and mix**, set against the region die - defaults, which `BRIEF.md` replaces where
it speaks:

```
WILD
  count   about as many as the die. N locations at a 1-in-N Difficulty failure means a
          full traverse expects one encounter at every die, so the die sets texture - a d4
          is short and spiky, a d12 long and smooth
  mix     50-60% landmark, 30-40% hidden, 10-20% secret
```

**Classifications** - one per location, in the mix above:
- **landmark** - discoverable through open exploration anywhere in the region; a site, a connection, or a natural feature.
- **hidden** - directly discoverable from a specific Landmark, through a visible feature that connects to it - not found by roaming the region generally.
- **secret** - discoverable only through a trigger at a Landmark or Hidden location that reveals the connection.

**Tags** - each location gets exactly three, one or two words each, written for it alone
against the setting's and this region's tag lines, the Region Overview and `BRIEF.md`.
They are the spark the location is later written to, so they push it away from the
region's average place: never its own name, never a fact every location in the region
shares, and no two locations in one region carrying the same three.

**The tables**, each in the format `templates/region/Allocation.md` sets:
- § Location - Code, Name, Tags, Weight (the classification). Written at 4a with Weight
  empty.
- § Landmark, § Hidden, § Secret - the class files' own lines. A Hidden or Secret row's
  parent, lead and access cells are what its parent's entry shows, so the parent is
  compiled from its children's rows as well as its own.
- § Ruin, § Lair, § Natural Feature, § Crossing - one row per location of that Kind.
- § Faction - one row per location a Kind's faction line drew, keyed by Code.
- § Dressing - one row per location.
- § Naming - one row per location.

## Template
```
Locations of [Region Code] [Region Name]

## Location
| Code | Name | Tags | Weight |
|---|---|---|---|
| [Region Code].1 | [Location Name] | [tag], [tag], [tag] | [landmark/hidden/secret] |

## Landmark
| Code | [patterns/wild/Landmark.md's labels] | Realized |

## Hidden
| Code | [patterns/wild/Hidden.md's labels] | Realized |

## Secret
| Code | [patterns/wild/Secret.md's labels] | Realized |

## Ruin
| Code | [patterns/wild/Ruin.md's labels] |

## Lair
| Code | [patterns/wild/Lair.md's labels] |

## Natural Feature
| Code | [patterns/wild/NaturalFeature.md's labels] |

## Crossing
| Code | [patterns/wild/Crossing.md's labels] |

## Faction
| Code | [patterns/wild/Faction.md's labels] |

## Dressing
| Code | [patterns/wild/Dressing.md's labels] |

## Naming
| Code | [patterns/setting/Naming.md's labels] |
```
