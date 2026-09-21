# Location.md

## Purpose
The full write-up for a single location, saved as `[Location Code].md` inside its region's folder (e.g. `setting/region/A/1.md`).

## Context
Consult when drafting - and only this, deliberately narrow so the entry stays shaped by its stub and region rather than washed out by the full setting:
- `GENRE.md` - a Feature is something to react to on the spot, not a beat in a larger scripted arc.
- this location's class file, named by its rating and its stub's weight/classification. It is
  the **entry point for everything the pattern library contributes here**: every other pattern
  file is reached from its Spec, and none is pulled in directly.
  - SAFE - `patterns/safe/Settlement.md`
  - WILD - `patterns/wild/Landmark.md`, `patterns/wild/Hidden.md`, or
    `patterns/wild/Secret.md`
  - DANGEROUS - `patterns/dangerous/High.md`, `patterns/dangerous/Medium.md`, or
    `patterns/dangerous/Low.md`
- this location's parent Region Overview (`setting/region/[Region Code].md`).
- this location's own gazetteer stub (name, weight/classification, its two tags) from `setting/region/[Region Code]/Locations.md`. The two tags were drawn, not invented - one from `setting/Tags.md`, one from this region's own `setting/region/[Region Code]/Tags.md` - and are read here only for color; they name no Kind and carry no inclusion math.
- `setting/Truths.md` - read at every location, whatever its rating or weight. Availability is not a quota: where this location touches a truth it is an **instance** of it, in this room's own terms, never a restatement of it. A truth surfacing in every room is wallpaper.
- `setting/Procedures.md` - the shared mechanics the pattern files cite rather than restate: trap resolution, searching, time, and scaling.
- `setting/Language.md` - roots for any proper noun coined here, and where every coinage is recorded back; it is the one artifact that grows as generation proceeds.
- For a WILD Hidden or Secret location, its parent must already be generated, since its connection is written into the parent's own Exits or Features - generate WILD locations Landmark tier first, then Hidden, then Secret.
- If a Feature calls for a piece of Lore, a Key, a Quest, a Named Creature, or a Unique Treasure, record only a **stub** (name and this location) in the matching `setting/` file now. Its full content is written later, in step 4d. This is the container/data split: the location cites, the registry holds.

Consult `setting/Bestiary.md`, `setting/Factions.md`, `setting/History.md`, or `setting/Rumours.md` only to look up a name the stub or region overview already references - never to pull in new material wholesale.

## Instructions

1. Read the assigned class file for this location in patterns/
2. This pattern determines the minimum percentage that a feature or detail occurs in this location, consider '1' a mandatory entry
3. Sort the Features the pattern produced by prominence, most important first, and write them in that order - this is a per-Feature ordering within one entry, distinct from a SAFE location's own liner note/working/central Prominence
4. Give each thing the players can address its own Feature line. Where a line the pattern drew names something that can be looked at, acted on, taken, fought, or opened **as its own object**, it is its own Feature - treasure hidden in a pillar and guarded by a beast is three Features, not one complex one. A drawn line that only qualifies another thing - its condition, its position, how it is reached - stays on that thing's line. An entry is as long as the number of Features the pattern drew, which is the classifier's decision, not this line's. Where a Feature carries a registry citation it states only what is present and perceptible - what the thing means, what it was for, and what it opens is the registry entry's, written at 4d, per **A note on completeness** below
5. **A Feature is one sentence, and its punctuation is closed:**
   - Only `,` and `->` separate clauses.
   - No semicolon, no colon, no dash, no second sentence.
   - No parenthesis except a citation, which sits last.
   - The sentence ends in a period.
6. **Every entry displays information at three tiers, and each tier's way in sits in the tier above it.**
   - **Obvious** - what a party perceives on arriving, having done nothing: the Player Summary, the Referee Notes, and every Feature and Exit that states itself plainly.
   - **Trigger** - what acting on something obvious yields: a Feature line naming an action and its effect, a container opened, a stated detail investigated. Per `setting/Procedures.md` a stated detail investigated is a detail found, and no roll stands in for the looking.
   - **Secret** - what the class file's own concealment line drew: its Clue sits in the obvious tier, its Trigger is a stated act on that Clue, and its Payload is what the act produces. Per `GENRE.md` a secret is opened by an act, never by a roll.

   The chain is the rule, not the count. A location need not carry all three - the class file's rates decide that - but where a tier is present, what leads into it is stated in the tier above: a concealed detail whose Clue appears nowhere obvious is content the referee knows and the players cannot reach, and a Feature whose action is anchored to nothing visible is a lever in an empty room. An entry sitting wholly in one tier has flattened - everything in the summary leaves nothing worth doing, everything behind a clue leaves a room that reads empty.
7. Output the pattern generated exactly according to the template below

## Template
```
[Region Code].[Location Code] **[Location Name]** [(high/medium/low) for DANGEROUS, (landmark/hidden/secret) for WILD] - *[tag from setting/Tags.md], [tag from region Tags.md]*
[Player Summary - two sentences maximum, that can be spoken aloud to the players or paraphrased. Include any details that would be obvious glancing at the location. **Bold** any features mentioned in the summary]
*[Referee Notes - free to carry a specialist term unglossed. Important details the Referee will need to adjudicate player efforts to explore the location: size (feet indoors, yards outdoors), shape, former/current purpose. Include a sound or smell only when it points at a specific feature within the location - never as ambience alone]*
**[Feature Name, most prominent first]:** [Interactive or explorable detail for this one feature and nothing else, including where within the room it sits (a wall, a corner, the center) and, when spatially significant, its own dimension; if a specific action triggers something specify both the action and the effect. A hidden object that can be acted on is its own Feature, and its line states how it is reached; a hidden **exit**, or any exit needing a trigger to reveal or access, stays nested within an obvious feature's line along with how to access it. Written to instruction 5's constraints]
**[Feature Name]:** [Every following Feature, same content rules as above, same constraints]
**Exits:** [comma separated list of this space's mundane exits, each as "[exit type - material, construction, condition], [position - wall, corner, or direction] -> [Code] [Location Name]"; an exit that leaves the map entirely rather than connecting to another location - open water, an unstaked wilderness edge, a route with no fixed destination - is written the same way but with "-> [where it leads, in plain terms, with no Code]" in place of the Code and Location Name, and is always listed **last**, after every coded exit]
```

## Citations
Every citation below sits inside its own parentheses, exactly as written, so `tools/build_site.py` can find and link it. A citation that doesn't match one of these forms renders as plain, unlinked text.

- **Bestiary** - `(Demeanor, Number appearing, Bestiary : Entry Name)`. Demeanor is one word naming how it carries itself before a fight starts or doesn't, per `patterns/dangerous/Creature.md` or `patterns/wild/Creature.md` (whichever matches this location's rating); Number appearing is a count fitting the Bestiary entry's own Range; Entry Name must match a `setting/Bestiary.md` heading exactly. Example: `(Patient, 5, Bestiary : Road Toll Gang)`.
- **Lore** - `(Lore: Title)`
- **Keys** - `(Keys: Title)`
- **Quest** - `(Quest: Title)`
- **Named Creature** - `(Named Creature: Name)`
- **Unique Treasure** - `(Unique Treasure: Name)`
- **Treasure table** - `(Treasure [I-V], d20)`
- **Forced damage** - `(Test of Constitution, Xd, Type)`, `(Test of Sanity, Xd)`,
  `(Test of Fate, Condition)`, or `(Test of Fate, Impact)`, per `setting/Procedures.md`,
  which is where the Types, the Conditions and what `Xd` means are all defined. Every
  hazard Feature carries one. Unlike the forms above this one links nowhere, since
  `setting/Procedures.md` is not a rendered page; `tools/validate_setting.py` checks its
  grammar instead.

A location code mentioned in running text (`A.3`, `C.15`) is linked automatically wherever it already names a real location; nothing special is needed to write one.

## A note on completeness
A location file is a **container**, and it is finished at 4c only in that sense. What its
citations point at - what a piece of Lore says, what a Key opens, what a Named Creature
wants, what a Unique Treasure costs - is written at 4d, with every location that references
it in view. That gap is by design: it is what lets a registry entry be consistent across
the several locations that cite it, which is something no single location file could
achieve on its own.
