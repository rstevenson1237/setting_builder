# Location.md

## Purpose
The full write-up for a single location, saved as `[Location Code].md` inside its region's folder (e.g. `setting/region/A/1.md`).

## Context
Consult when drafting - and only this, deliberately narrow so the entry stays shaped by its stub and region rather than washed out by the full setting:
- `GENRE.md` - a Feature is something to react to on the spot, not a beat in a larger scripted arc.
- this location's parent Region Overview (`setting/region/[Region Code].md`).
- this location's own gazetteer stub (name, weight/classification, tags) from `setting/region/[Region Code]/Locations.md`.
- **the three files of this location's rating folder, in order.** `patterns/safe/`, `patterns/wild/`, or `patterns/dangerous/`:
  1. The class file - `Settlement.md` for SAFE; `Landmark.md`, `Hidden.md`, or `Secret.md` for WILD by classification; `High.md`, `Medium.md`, or `Low.md` for DANGEROUS by weight. It carries the **inclusion spec**: which lines are mandatory, which are a stated percentage, and what each draws from. A class is defined by what it guarantees, never by a ceiling on what may appear.
  2. The element files the spec's lines draw from. **Read only the ones the spec actually drew, and only from this location's own rating folder** - the folders do not hold the same set, and a file borrowed from another folder is guidance written for a different kind of place.
     - `patterns/safe/` - `Commerce.md`, `Authority.md`, `Social.md`, `Situation.md`, `People.md`, `Faction.md`, `Quest.md`, `Key.md`, `Lore.md`.
     - `patterns/wild/` - `Ruin.md`, `Lair.md`, `NaturalFeature.md`, `Creature.md`, `Trap.md`, `Treasure.md`, `Mystery.md`, `Quest.md`, `Key.md`, `Lore.md`.
     - `patterns/dangerous/` - `Creature.md`, `Trap.md`, `Treasure.md`, `Mystery.md`, `Faction.md`, `Quest.md`, `Key.md`, `Lore.md`.
  3. `Dressing.md`, then `Secrets.md`, then `Naming.md` - all three consulted unconditionally, not just when a spec line calls for them. Dressing may originate content of its own: **Features owns anything that changes what players can do; Dressing owns everything else.**
- `setting/Procedures.md` - the shared mechanics the pattern files cite rather than restate: trap resolution, searching, time, and scaling.
- `setting/Language.md` - roots for any proper noun coined here. **Record every coinage back into it**, per the rating's `Naming.md`; it is the one artifact that grows as generation proceeds.
- For a WILD Hidden or Secret location, its parent must already be generated, since its connection is written into the parent's own Exits or Features - generate WILD locations Landmark tier first, then Hidden, then Secret.
- If a Feature calls for a piece of Lore, a Key, a Quest, a Named Creature, or a Unique Treasure, record only a **stub** (name and this location) in the matching `setting/` file now. Its full content is written later, in step 4d. This is the container/data split: the location cites, the registry holds.

Consult `setting/Bestiary.md`, `setting/Factions.md`, `setting/History.md`, `setting/Truths.md`, or `setting/Rumours.md` only to look up a name the stub or region overview already references - never to pull in new material wholesale.

## Instructions

1. Read the assigned class file for this location in patterns/
2. This pattern determines the minimum percentage that a feature or detail occurs in this location, consider '1' a mandatory entry
3. Output the pattern generated exactly according to the template below

## Template
```
[Region Code].[Location Code] **[Location Name]** [(high/medium/low) for DANGEROUS, (landmark/hidden/secret) for WILD] - *[three, thematic, tags]*
[Player Summary - two sentences that can be spoken aloud to the players or paraphrased. Include any details that would be obvious glancing at the location. **Bold** any features mentioned in the summary]
*[Referee Notes - important details the Referee will need to know to adjudicate player efforts to explore the location: size (feet indoors, yards outdoors), shape, former/current purpose, and at least one sound or smell]*
**[Feature Name]:** [interactive or explorable detail for this one feature, including where within the room it sits (a wall, a corner, the center) and, when spatially significant, its own dimension; if a specific action triggers something specify both the action and the effect; hidden features, including any exit that needs a trigger to reveal or access, are nested within the detail of an obvious feature's line, along with how to access them]
**[Feature Name]:** [...]
**Exits:** [comma separated list of this space's mundane exits, each as "[exit type - material, construction, condition], [position - wall, corner, or direction] -> [Code] [Location Name]"; an exit that leaves the map entirely rather than connecting to another location - open water, an unstaked wilderness edge, a route with no fixed destination - is written the same way but with "-> [where it leads, in plain terms, with no Code]" in place of the Code and Location Name, and is always listed **last**, after every coded exit, since `tools/validate_setting.py` reads exits by splitting on each "-> [Code] [Name]" match in order and an uncoded exit placed earlier would shift every description after it]
```

## A note on completeness
A location file is a **container**, and it is finished at 4c only in that sense. What its
citations point at - what a piece of Lore says, what a Key opens, what a Named Creature
wants, what a Unique Treasure costs - is written at 4d, with every location that references
it in view. That gap is by design: it is what lets a registry entry be consistent across
the several locations that cite it, which is something no single location file could
achieve on its own.
