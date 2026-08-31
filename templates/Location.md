# Location.md

## Purpose
The full write-up for a single location, saved as `[Location Code].md` inside its region's folder (e.g. `setting/region/A/1.md`).

## Context
Consult when drafting - and only this, deliberately narrow so the entry stays shaped by its stub and region rather than washed out by the full setting:
- `GENRE.md` - a Feature is something to react to on the spot, not a beat in a larger scripted arc.
- this location's parent Region Overview (`setting/region/[Region Code].md`).
- this location's own gazetteer stub (name, weight, tags) from `setting/region/[Region Code]/Locations.md`.
- the matching `patterns/` file (`Safe.md`, `Wild.md`, `Dangerous_Low.md`, `Dangerous_Medium.md`, or `Dangerous_High.md`, picked by the region's rating and this location's weight) - choose one bullet now, at generation time, and shape the Feature(s) around only that bullet; do not draw on other patterns.

Consult `setting/Bestiary.md`, `setting/Factions.md`, `setting/History.md`, `setting/Truths.md`, or `setting/Rumours.md` only to look up a name the stub or region overview already references - never to pull in new material wholesale.

## Instructions
- **Player Summary**: Two sentences that can be spoken aloud to the players or paraphrased. Include any details that would be obvious glancing at the location. **Bold** any features mentioned in the summary.
- **Referee Notes**: Italicized. Important details the Referee will need to know to adjudicate player efforts to explore the location - shape and size, noteworthy smells or sounds.
- **Features**: One bolded line per interactive or explorable element, labeled with the feature's own name (e.g. **Thorn Tangle:**, not **The Thorn Tangle:**) - drop leading articles ("The", "A") from the label, they're needlessly repetitive across a list. If a specific action triggers something, specify both the action and the effect. Hidden features are nested within the detail of an obvious feature's line, along with how to access them. An exit that requires a trigger to reveal or access (a secret door, a hidden lever) belongs here as a Feature, not under Exits.
- **Exits**: A comma separated list of this space's mundane exits only - anything requiring a trigger to reveal or access belongs under Features instead. Each entry names what indicates the exit (a door, a ladder, the path leading north) and points to its destination with `->`, e.g. `door -> A.2 Salvage Market`.

## Template
```
[Region Code].[Location Code] **[Location Name]** - *[three, thematic, tags]*
[Player Summary - two sentences that can be spoken aloud to the players or paraphrased. Include any details that would be obvious glancing at the location. **Bold** any features mentioned in the summary]
*[Referee Notes - important details the Referee will need to know to adjudicate player efforts to explore the location: shape and size, noteworthy smells or sounds]*
**[Feature Name]:** [interactive or explorable detail for this one feature; if a specific action triggers something specify both the action and the effect; hidden features, including any exit that needs a trigger to reveal or access, are nested within the detail of an obvious feature's line, along with how to access them]
**[Feature Name]:** [...]
**Exits:** [comma separated list of this space's mundane exits, each as "[what indicates the exit] -> [Code] [Location Name]"]
```
