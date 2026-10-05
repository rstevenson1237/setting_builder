# Location.md

## Purpose
The full write-up for a single location, saved as `[Location Code].md` inside its region's folder (e.g. `setting/region/A/1.md`).

## Context
Read first - the same for every location in a region, so read once per session:
- `GENRE.md` - a Feature is something to react to on the spot, not a beat in a larger scripted arc.
- `STYLE.md` - the three tests, which outrank everything below.
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak.
- `setting/Truths.md` - where this location touches a truth it is an **instance** of it, in this room's own terms, never a restatement of it. A truth surfacing in every room is wallpaper.
- `setting/Procedures.md` - the shared mechanics a Feature cites rather than restates.
- `setting/Language.md` - roots for any proper noun coined here, and where every coinage is recorded back.
- this location's parent Region Overview, `setting/region/[Region Code].md`.

Then, per location, read **every row naming it** across the region's table files - its row in each `Locations.md` table it has one in, keyed by its code; every row in `Exits.md`, `Challenges.md`, `Treasures.md` and `Links.md` whose `Location`, `From` or `To` is this code; every WILD Hidden or Secret row whose Parent is this code, since a child's lead or access clue is shown in its parent's entry - and the rows those rows name by id. Its § Location row's three tags are the spark the entry is written to. Open no pattern file and no sibling location file: the rows are already settled, and what a registry entry means is the registry's.

Consult `setting/Bestiary.md`, `setting/Factions.md`, `setting/History.md`, or `setting/Rumours.md` only to look up a name a row or the region overview already references - never to pull in new material wholesale.

## Instructions

1. **Every row is realized, and nothing without a row is written.** Each row's `Realized` cell gets the Feature label - or `Exits`, `Summary` or `Notes` - that carries it. Cells are notes, never copied as text: write each Feature from its cells in the grammar below, adding no fact and dropping none. A row that cannot share the room goes back to the pass that wrote it, never quietly left out
2. **The rows are raw material and the entry is a few sentences.** Each row's facts reach the page in the fewest words that still let a party see, take or decide something - most lines are a clause on another thing's Feature, not a Feature of their own. A Feature runs at most 30 words before its citation, the Referee Notes at most three sentences
3. Sort the Features by prominence, most important first, and write them in that order - this is a per-Feature ordering within one entry, distinct from a SAFE location's own liner note/working/central Prominence
4. Give each thing the players can address its own Feature line. Where a row or a cell names something that can be looked at, acted on, taken, fought, or opened **as its own object**, it is its own Feature - treasure hidden in a pillar and guarded by a beast is three Features, not one complex one. A cell that only qualifies another thing - its condition, its position, how it is reached - stays on that thing's line. An entry is as long as the number of Features its rows hold, which allocation decided, not this line. Where a Feature carries a registry citation it states only what is present and perceptible - what the thing means, what it was for, and what it opens is the registry entry's, per **A note on completeness** below
5. **A Feature is one sentence, and its punctuation is closed:**
   - Only `,` and `->` separate clauses.
   - No semicolon, no colon, no dash, no second sentence.
   - No parenthesis except a citation, which sits last.
   - The sentence ends in a period.
6. **Every entry displays information at three tiers, and each tier's way in sits in the tier above it.**
   - **Obvious** - what a party perceives on arriving, having done nothing: the Player Summary, the Referee Notes, and every Feature and Exit that states itself plainly.
   - **Trigger** - what acting on something obvious yields: a Feature line naming an action and its effect, a container opened, a stated detail investigated. Per `setting/Procedures.md` a stated detail investigated is a detail found, and no roll stands in for the looking.
   - **Secret** - what its class table's concealed-detail cells hold: its Clue sits in the obvious tier, its Trigger is a stated act on that Clue, and its Payload is what the act produces. Per `STYLE.md` a secret is opened by an act, never by a roll.

   The chain is the rule, not the count. A location need not carry all three - allocation decided that - but where a tier is present, what leads into it is stated in the tier above: a concealed detail whose Clue appears nowhere obvious is content the referee knows and the players cannot reach, and a Feature whose action is anchored to nothing visible is a lever in an empty room. An entry sitting wholly in one tier has flattened - everything in the summary leaves nothing worth doing, everything behind a clue leaves a room that reads empty.
7. Output the entry exactly according to the template below
8. **What holds for every entry, whatever its class:**
   - One history per room - a part that could not share the room with the rest is changed, not explained.
   - Name a thing that has a name - a term, trade, material, landform or species - rather than describing it.
   - Never a bare noun for an exit or a container - its make and condition are what a party can test.
   - A hazard or a trap is one Feature - its tell and its effect on one line, its forced damage cited last.
   - A concealed detail never pays out a route the diagram did not draw.
   - Never two triggers deep - no clue reached only by acting on another clue.

9. **Retrofit is targeted.** When rows are added to or changed in a room already written - a composition run after compile, or any edit to a filled row - each new row gets a new Feature line, placed by prominence; each changed row's line is rewritten, and only that line; the Player Summary and the Referee Notes are revisited only when a new or changed row is obvious, and every bolded noun still has its Feature. Every other line stays exactly as it was.

## Template
```
[Region Code].[Location Code] **[Location Name]** [(high/medium/low) for DANGEROUS, (landmark/hidden/secret) for WILD] - *[tag], [tag], [tag]*
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
- **Treasure table** - `(Treasure [I-V], d20)` - a table roll is cited, never described, and each citation is one pull.
- **Forced damage** - `(Test of Constitution, Xd, Type)`, `(Test of Sanity, Xd)`,
  `(Test of Fate, Condition)`, or `(Test of Fate, Impact)`, per `setting/Procedures.md`,
  which is where the Types, the Conditions and what `Xd` means are all defined. Every
  hazard Feature carries one. Unlike the forms above this one links nowhere, since
  `setting/Procedures.md` is not a rendered page; `tools/validate_setting.py` checks its
  grammar instead.

A location code mentioned in running text (`A.3`, `C.15`) is linked automatically wherever it already names a real location; nothing special is needed to write one.

## A note on completeness
A location file is a **container**. What its citations point at - what a piece of Lore
says, what a Key opens, what a Named Creature wants, what a Unique Treasure costs - is the
registry entry's, written with every row that places it in view. That split is by design:
it is what lets a registry entry be consistent across the several locations that cite it,
which no single location file could achieve on its own.
