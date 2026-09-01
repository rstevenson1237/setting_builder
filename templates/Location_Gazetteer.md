# Location_Gazetteer.md

## Purpose
Lists the explorable locations within a single region - a lightweight target list for building the region's Connections diagram, not a place for content.

## Context
Consult when drafting:
- `GENRE.md` - mythic underworld means DANGEROUS-region locations should read as ruin and chaos, not a designed conspiracy; points of light means SAFE/WILD landmarks should feel sparse, not densely urban.
- `setting/region/[Region Code].md` - this region's Overview, the source for how many locations it should hold and what they broadly cover.

## Instructions
List the locations within a single region - each location is an explorable area within that region. In SAFE and WILD regions, locations are major landmarks; in DANGEROUS regions, one location per room is a good standard. A SAFE or WILD region should contain about as many locations as its die type (e.g. a d6 SAFE region has about 6 locations); a DANGEROUS region should contain about 3 times as many (e.g. a d8 DANGEROUS region has about 24 locations).

Each location in a DANGEROUS region is assigned a weight; each location in a WILD region is assigned a classification instead. Both are skipped for SAFE regions.

DANGEROUS weight:
- **low** - connective areas, empty rooms, or areas that contain detail but do not demand action.
- **medium** - one major reactive element, such as a trap, a monster, or a puzzle to solve.
- **high** - an area that is central to the theme of the region and contains one or more major features.

WILD classification - roughly half or more of a region's locations are Landmark, at least a third Hidden, and the remainder (usually under a fifth) Secret:
- **landmark** - discoverable through open exploration anywhere in the region; a site, a connection, or a natural feature. See `patterns/Wild_Landmark.md`.
- **hidden** - directly discoverable from a specific Landmark, through a visible feature that connects to it - not found by roaming the region generally. See `patterns/Wild_Hidden.md`.
- **secret** - discoverable only through a trigger at a Landmark or Hidden location that reveals the connection. See `patterns/Wild_Secret.md`.

Keep entries to a name, weight/classification, and tags only - no Pattern and no descriptive sentence. This file is a map skeleton, feeding the region's Connections diagram; pattern selection and content happen later, per location, in `templates/Location.md`.

## Template
```
Locations of [Region Code] [Region Name]

[Region Code].1 [Location Name] [(high/medium/low) for DANGEROUS, (landmark/hidden/secret) for WILD] - [three, thematic, tags]
```
