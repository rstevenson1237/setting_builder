# Locations.md - SAFE

## Purpose
The location table of one SAFE region, `setting/region/[Region Code]/Locations.md`: every
door a party goes to for something, as a row - named, tagged and given its prominence -
and the tables of what each place is.

## Context
Read first, every step:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- this region's Overview, `setting/region/[Region Code].md` - its People roster above all - and its die in `setting/region/Regions.md`

Then, by step:
- **4a** (names and tags): nothing more.
- **4b** (prominence): `patterns/safe/Settlement.md`'s PROMINENCE block.
- **4f** (the place tables): the stubs of § Settlement, § Dressing, § People and the kind tables; § Location; `patterns/safe/Settlement.md`, `patterns/safe/Dressing.md`, `patterns/safe/People.md` and the kind files `patterns/safe/Commerce.md`, `patterns/safe/Authority.md`, `patterns/safe/Social.md`, `patterns/safe/Wealth.md`, `patterns/safe/Garrison.md`, for their own lines.
- **4g** (naming): `patterns/setting/Naming.md`; `setting/Language.md`; every row in the region naming the location.

## Instructions

**Count and mix**, set against the region die - defaults, which `BRIEF.md` replaces where
it speaks:

```
SAFE
  count       about as many as the die - a d8 settlement holds about eight locations
  prominence  about one central location per settlement, a few working, and liner notes
              the rest
```

Locations are chosen against the Region Overview's Settlement and People: each is a door a
party goes to for something.

**Tags** - each location gets exactly three, one or two words each, written for it alone
against the setting's and this region's tag lines, the Region Overview and `BRIEF.md`.
They are the spark the location is later written to, so they push it away from the
settlement's average door: never its own name, never a fact every location in the region
shares, and no two locations in one region carrying the same three.

**The tables**, each in the format `templates/region/Allocation.md` sets:
- § Location - Code, Name, Tags, Weight (the prominence). Written at 4a with Weight empty.
- § Settlement - the class file's own lines, one row per location.
- § Dressing - one row per location.
- § People - one row per location: the gate's person, and for a `people` Kind the
  household itself.
- § Commerce, § Authority, § Social, § Wealth, § Garrison - one row per location of that
  Kind.
- § Naming - one row per location.

## Template
```
Locations of [Region Code] [Region Name]

## Location
| Code | Name | Tags | Weight |
|---|---|---|---|
| [Region Code].1 | [Location Name] | [tag], [tag], [tag] | [liner note/working/central] |

## Settlement
| Code | [patterns/safe/Settlement.md's labels] | Realized |

## Dressing
| Code | [patterns/safe/Dressing.md's labels] |

## People
| Code | [patterns/safe/People.md's labels] |

## Commerce
| Code | [patterns/safe/Commerce.md's labels] |

## Authority
| Code | [patterns/safe/Authority.md's labels] |

## Social
| Code | [patterns/safe/Social.md's labels] |

## Wealth
| Code | [patterns/safe/Wealth.md's labels] |

## Garrison
| Code | [patterns/safe/Garrison.md's labels] |

## Naming
| Code | [patterns/setting/Naming.md's labels] |
```
