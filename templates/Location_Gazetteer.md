# Location_Gazetteer.md

## Purpose
Lists the explorable locations within a single region - a lightweight target list for building the region's Connections diagram, not a place for content.

## Context
Read first:
- `GENRE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- `setting/region/[Region Code].md`

## Instructions
List the locations within a single region - each location is an explorable area within that region. In SAFE and WILD regions, locations are major landmarks; in DANGEROUS regions, one location per room is a good standard. The count and the mix below are defaults, set against the region die from
`setting/region/Regions.md`:

```
SAFE
  count   about as many as the die - a d8 settlement holds about eight locations

WILD
  count   about as many as the die. N locations at a 1-in-N Difficulty failure means a
          full traverse expects one encounter at every die, so the die sets texture - a d4
          is short and spiky, a d12 long and smooth
  mix     50-60% landmark, 30-40% hidden, 10-20% secret

DANGEROUS
  count   a collection: 3x the die, which across a full clear burns 3 of the Danger
          track's 6 steps at every die size. A single holding: what the home actually
          contains, usually 5-8, never padded to the multiplier
  mix     30% high, 50% medium, and low the rest - the residue, not a quota
  entrances   1-2 at about 12 locations, 2 at about 24, 2-3 at about 36
```

Each location in a DANGEROUS region is assigned a weight; each location in a WILD region is
assigned a classification instead. Both are skipped for SAFE regions, whose locations are
the doors a party goes to for something, chosen against the Region Overview's Settlement
and People.

DANGEROUS weight, in the proportions above. Enough to assign
one here; what each guarantees is in its own file, read at 4c:
- **low** - connective areas, empty rooms, or areas that contain detail but do not demand action. See `patterns/dangerous/Low.md`.
- **medium** - one major reactive element, such as a trap, a monster, or a puzzle to solve. See `patterns/dangerous/Medium.md`.
- **high** - an area that is central to the theme of the region and contains one or more major features. See `patterns/dangerous/High.md`.

WILD classification, in the proportions above:
- **landmark** - discoverable through open exploration anywhere in the region; a site, a connection, or a natural feature. See `patterns/wild/Landmark.md`.
- **hidden** - directly discoverable from a specific Landmark, through a visible feature that connects to it - not found by roaming the region generally. See `patterns/wild/Hidden.md`.
- **secret** - discoverable only through a trigger at a Landmark or Hidden location that reveals the connection. See `patterns/wild/Secret.md`.

Keep entries to a name, weight/classification, and two tags only - no Pattern and no
descriptive sentence. This file is a map skeleton, feeding the region's Connections
diagram; pattern selection and content happen later, per location, in
`templates/Location.md`.

Each location draws exactly **two** tags, not three and not freely invented: one from
`setting/Tags.md`, one from this region's own `setting/region/[Code]/Tags.md`. Draw, don't
invent - a tag repeated across several locations in the same region is fine and expected,
since the pool is meant to be drawn from more than once.

## Template
```
Locations of [Region Code] [Region Name]

[Region Code].1 [Location Name] [(high/medium/low) for DANGEROUS, (landmark/hidden/secret) for WILD] - [tag from setting/Tags.md], [tag from region Tags.md]
```
