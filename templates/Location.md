# Location.md

## Purpose
The full write-up for a single location, saved as `[Location Code].md` inside its region's folder (e.g. `setting/region/A/1.md`).

## Context
Consult when drafting - and only this, deliberately narrow so the entry stays shaped by its stub and region rather than washed out by the full setting:
- `GENRE.md` - a Feature is something to react to on the spot, not a beat in a larger scripted arc.
- this location's parent Region Overview (`setting/region/[Region Code].md`).
- this location's own gazetteer stub (name, weight/classification, tags) from `setting/region/[Region Code]/Locations.md`.
- `setting/Procedures.md` - the shared mechanics the pattern files cite rather than restate: trap resolution, searching, time, and scaling.
- `setting/Language.md` - roots for any proper noun coined here, and where every coinage is recorded back; it is the one artifact that grows as generation proceeds.
- For a WILD Hidden or Secret location, its parent must already be generated, since its connection is written into the parent's own Exits or Features - generate WILD locations Landmark tier first, then Hidden, then Secret.
- If a Feature calls for a piece of Lore, a Key, a Quest, a Named Creature, or a Unique Treasure, record only a **stub** (name and this location) in the matching `setting/` file now. Its full content is written later, in step 4d. This is the container/data split: the location cites, the registry holds.

Consult `setting/Bestiary.md`, `setting/Factions.md`, `setting/History.md`, `setting/Truths.md`, or `setting/Rumours.md` only to look up a name the stub or region overview already references - never to pull in new material wholesale.

## Instructions

1. Read the assigned class file for this location in patterns/
2. This pattern determines the minimum percentage that a feature or detail occurs in this location, consider '1' a mandatory entry
3. Sort the Features the pattern produced by prominence, most important first, and write them in that order - this is a per-Feature ordering within one entry, distinct from a SAFE location's own liner note/working/central Prominence
4. Budget each Feature's own line by its position in that order: 15 words for the first (most prominent) Feature, 8-12 words for every Feature after it - a ceiling, not a target. State every Feature in the minimum number of words that convey it completely; never pad a line to reach its budget
5. Output the pattern generated exactly according to the template below

## Template
```
[Region Code].[Location Code] **[Location Name]** [(high/medium/low) for DANGEROUS, (landmark/hidden/secret) for WILD] - *[three, thematic, tags]*
[Player Summary - two sentences maximum, that can be spoken aloud to the players or paraphrased. Include any details that would be obvious glancing at the location. **Bold** any features mentioned in the summary]
*[Referee Notes - important details the Referee will need to know to adjudicate player efforts to explore the location: size (feet indoors, yards outdoors), shape, former/current purpose. Include a sound or smell only when it points at a specific feature within the location - never as ambience alone]*
**[Feature Name, most prominent first]:** [15 words maximum for this line, the entry's first Feature. Interactive or explorable detail for this one feature, including where within the room it sits (a wall, a corner, the center) and, when spatially significant, its own dimension; if a specific action triggers something specify both the action and the effect; hidden features, including any exit that needs a trigger to reveal or access, are nested within the detail of an obvious feature's line, along with how to access them. State it in the fewest words that convey it fully - the budget is a ceiling, not a target]
**[Feature Name]:** [8-12 words maximum for this and every following Feature, same content rules as above, stated in the fewest words that convey it fully]
**Exits:** [comma separated list of this space's mundane exits, each as "[exit type - material, construction, condition], [position - wall, corner, or direction] -> [Code] [Location Name]"; an exit that leaves the map entirely rather than connecting to another location - open water, an unstaked wilderness edge, a route with no fixed destination - is written the same way but with "-> [where it leads, in plain terms, with no Code]" in place of the Code and Location Name, and is always listed **last**, after every coded exit, since `tools/validate_setting.py` reads exits by splitting on each "-> [Code] [Name]" match in order and an uncoded exit placed earlier would shift every description after it]
```

## Citations
Every citation below sits inside its own parentheses, exactly as written, so `tools/build_site.py` can find and link it. A citation that doesn't match one of these forms renders as plain, unlinked text.

- **Bestiary** - `(Demeanor, Number appearing, Bestiary : Entry Name)`. Demeanor is one tag from `GENRE.md`'s Creatures (demeanors) bank; Number appearing is a count fitting the Bestiary entry's own Range; Entry Name must match a `setting/Bestiary.md` heading exactly. Example: `(Patient, 5, Bestiary : Road Toll Gang)`.
- **Lore** - `(Lore: Title)`
- **Keys** - `(Keys: Title)`
- **Quest** - `(Quest: Title)`
- **Named Creature** - `(Named Creature: Name)`
- **Unique Treasure** - `(Unique Treasure: Name)`
- **Treasure table** - `(Treasure [I-V], d20)`

A location code mentioned in running text (`A.3`, `C.15`) is linked automatically wherever it already names a real location; nothing special is needed to write one.

## A note on completeness
A location file is a **container**, and it is finished at 4c only in that sense. What its
citations point at - what a piece of Lore says, what a Key opens, what a Named Creature
wants, what a Unique Treasure costs - is written at 4d, with every location that references
it in view. That gap is by design: it is what lets a registry entry be consistent across
the several locations that cite it, which is something no single location file could
achieve on its own.
