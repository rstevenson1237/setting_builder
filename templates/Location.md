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

### Three rules before the fields

These govern every line below, and they are where location entries actually go wrong. The
fields tell you *what* to include; these tell you how much of it survives to the table.

**1. Every sentence is a thing, an action, or an effect.** A thing present in the room, an
action available to the party, or what happens when they take it. A sentence that is none
of those three is commentary - and commentary is the bulk of what a bad entry weighs.
Specifically, cut: why a detail is there, what it means, what it reveals about the region,
what the party will realise from it, what the room is "really" about, and what the correct
play is. Per `GENRE.md`, the referee draws those conclusions faster than they can read your
account of them, and the players are entitled to draw them at all. **State it; do not
explain it, justify it, or resolve it.**

The commonest form of this failure is writing the answer to the room's own problem. If a
groove is worn into the floor and something heavy walks it, the table works out to stand
aside; an entry that says *the whole of surviving this room is knowing where the groove
goes* has spent thirty words taking that away from them.

**2. Anything findable is written as a chain, not as prose.** What is visible → what the
party does → what they get:

`**Cut Face:** ... nine wedge slots cut and never driven → the third holds an iron
feather-and-wedge set, unrusted → work it free, one action → (Treasure II, d20)`

This is the same notation `patterns/dangerous/Trap.md` already uses for a tell, generalized
to every discoverable: treasure, secrets, keys, lore, a hidden exit, a puzzle's solution.
The arrow is diagnostic. **If you cannot write the chain, one of the links is missing** -
either there is no visible clue (so it is not findable and the entry is broken), or there is
no action (so it is dressing, and belongs in a clause rather than its own Feature line), or
there is no result (so cut it).

**3. Length is the smoke alarm.** Per each rating's `Dressing.md`, an entry has a word
budget by class. Going over almost never means the room holds too much - it means the things
it holds have been explained. When over budget, find the commentary and delete it before
touching a single fact.

- **Player Summary**: Two sentences that can be spoken aloud to the players or paraphrased. Include any details that would be obvious glancing at the location. **Bold** any features mentioned in the summary.
- **Referee Notes**: Italicized. Important details the Referee will need to know to adjudicate player efforts to explore the location. Every location states: a size (X by Y, even roughly - **feet for an enclosed space, yards for an outdoor one**; a vertical drop or climb stays in feet either way, and distance between two points runs yards for a short hop and miles for a long trek), a shape (geometric or an approximation of an irregular space), its former and/or current purpose, and at least one sound or smell. A WILD Landmark also states roughly where within the region it sits (a cardinal direction, or a bearing/distance from another named Landmark or the region's entry point) - Hidden and Secret locations skip this, since their position is already defined by the parent they connect from.
- **Features**: One bolded line per interactive or explorable element, labeled with the feature's own name (e.g. **Thorn Tangle:**, not **The Thorn Tangle:**) - drop leading articles ("The", "A") from the label, they're needlessly repetitive across a list. If a specific action triggers something, specify both the action and the effect. Hidden features are nested within the detail of an obvious feature's line, along with how to access them. An exit that requires a trigger to reveal or access (a secret door, a hidden lever) belongs here as a Feature, not under Exits. State where within the room the Feature sits (a wall, a corner, the center) and, when its footprint is spatially significant, its own dimension (e.g. "a fountain 10' across," not just "a fountain") - a Feature's location and scale shouldn't have to be improvised at the table.
  - **Secrets**: when the rating's `Secrets.md` calls for one, state all three parts inline within the obvious Feature it's nested in, as a chain - `Clue → Trigger → Payload`. The Clue is already part of that Feature's visible detail; the Trigger is the specific action that acts on it; the Payload is what it produces (a secret door/exit, a neutralized effect, a solved puzzle, a revealed trap, or uncovered treasure - formatted per that content type's own rule below). A Secret is never a bare "there's a hidden switch here" - the Clue has to already be legible to a player paying attention, which is exactly what writing it as a chain forces you to check.
  - **Treasure**: write it as a chain - what is visible → the search or trigger that reaches it → the citation. The container and what conceals it are the visible link; do not spend a sentence on either. Never name or describe the item itself - the cited table roll determines contents, and stating an item here would conflict with whatever gets rolled. Cite the contents as a single d20 pull from the matching table: `(Treasure [I-V], d20)`. A location may cite more than one table across its Features, but never more than one pull per citation - if a location warrants more, add a second citation elsewhere rather than multiplying one.
  - **Creatures**: name the creature directly by its `setting/Bestiary.md` entry name within the Feature - no separate citation syntax needed. State how many; number is half the pitch.
  - **Traps**: write the trigger and effect inline, same as any other Feature. A Lethal trap's resolution is stated in the prose using `setting/Procedures.md`'s terms - `TEST OF CONSTITUTION` for a single character, `TEST OF FATE` when the whole party is exposed - followed by its consequence, a `WOUND` or a freeform `CONDITION` (poisoned, bloodied, blinded, etc.).
  - **Puzzles**: give at least two specific physical details the trigger can be reasoned out from - more than a Trap needs, since a Puzzle should be solvable by investigation rather than guessed at. State the trigger explicitly, that leaving it uninvestigated or attempting-but-stopping-short is neutral, what a genuinely wrong attempt does (a stated negative effect, same style as a Trap), and what the correct trigger accomplishes (a revealed Feature, an unlocked Exit, a Treasure citation, or similar).
  - **Lore, Keys, Quests, Named Creatures, Unique Treasures**: name the item or creature and describe its container/clue/trigger inline, same as Treasure - but never write its actual content (what the Lore reveals, what the Key unlocks, the creature's motivation, what the Unique Treasure does) here; that's written later, in step 4d, in the matching `setting/` file. Cite it as `(Lore: [Title])`, `(Keys: [Object Name])`, `(Quest: [Name])`, `(Named Creature: [Name])`, or `(Unique Treasure: [Name])`, and add the stub row to that file now. If a Named Creature is already stubbed at another location, add this location to its existing row rather than creating a second one.
- **Exits**: A comma separated list of this space's mundane exits only - anything requiring a trigger to reveal or access belongs under Features instead. Each entry names what indicates the exit, states where it sits in the room, and points to its destination with `->`, e.g. `thick oaken door, banded in rust-streaked iron, set into the east wall -> A.2 Salvage Market`. Every exit states a type - material, construction, and condition - not just "a door" or "a ladder" - and a position: which wall or corner it opens from, or which direction it leads outdoors. Position is what keeps two exits of the same type distinguishable - never list two exits reading identically with nothing but their destination to tell them apart. When the distance to the next location is worth calling out (most exits don't need it), state it the same way - yards for a short hop, miles for a long trek.

## Template
```
[Region Code].[Location Code] **[Location Name]** [(high/medium/low) for DANGEROUS, (landmark/hidden/secret) for WILD] - *[three, thematic, tags]*
[Player Summary - two sentences that can be spoken aloud to the players or paraphrased. Include any details that would be obvious glancing at the location. **Bold** any features mentioned in the summary]
*[Referee Notes - important details the Referee will need to know to adjudicate player efforts to explore the location: size (feet indoors, yards outdoors), shape, former/current purpose, and at least one sound or smell]*
**[Feature Name]:** [interactive or explorable detail for this one feature, including where within the room it sits (a wall, a corner, the center) and, when spatially significant, its own dimension; if a specific action triggers something specify both the action and the effect; hidden features, including any exit that needs a trigger to reveal or access, are nested within the detail of an obvious feature's line, along with how to access them]
**[Feature Name]:** [...]
**Exits:** [comma separated list of this space's mundane exits, each as "[exit type - material, construction, condition], [position - wall, corner, or direction] -> [Code] [Location Name]"]
```

## A note on completeness
A location file is a **container**, and it is finished at 4c only in that sense. What its
citations point at - what a piece of Lore says, what a Key opens, what a Named Creature
wants, what a Unique Treasure costs - is written at 4d, with every location that references
it in view. That gap is by design: it is what lets a registry entry be consistent across
the several locations that cite it, which is something no single location file could
achieve on its own.
