# Location_Gazetteer.md

## Purpose
Lists the explorable locations within a single region - a lightweight target list for building the region's Connections diagram, not a place for content.

## Context
Read first:
- `GENRE.md`
- `setting/region/[Region Code].md`

## Instructions
List the locations within a single region - each location is an explorable area within that region. In SAFE and WILD regions, locations are major landmarks; in DANGEROUS regions, one location per room is a good standard. **Take the location count and the class mix from the region's pattern file** - `patterns/region/Safe.md`, `patterns/region/Wild.md`, or `patterns/region/Dangerous.md` - which states both as ranges and gives the cost of deviating. Don't reason them out here.

Each location in a DANGEROUS region is assigned a weight; each location in a WILD region is assigned a classification instead. Both are skipped for SAFE regions, whose list of locations comes from `patterns/safe/Settlement.md` - the settlement type it reads off the Region Overview's Layout field states which locations a place like this can plausibly hold.

DANGEROUS weight, in the proportions `patterns/region/Dangerous.md` sets. Enough to assign
one here; what each guarantees is in its own file, read at 4c:
- **low** - connective areas, empty rooms, or areas that contain detail but do not demand action. See `patterns/dangerous/Low.md`.
- **medium** - one major reactive element, such as a trap, a monster, or a puzzle to solve. See `patterns/dangerous/Medium.md`.
- **high** - an area that is central to the theme of the region and contains one or more major features. See `patterns/dangerous/High.md`.

WILD classification, in the proportions `patterns/region/Wild.md` sets:
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
