# Pattern Judgement Check - after the region-overview, tag and defaults rework

Run against `patterns/` at commit dc4bd44, with Greywatch (98 locations, through 4c) and
`tools/context.py 4c` resolutions of C.12, C.33, C.2, A.21, B.4, B.8 and C.48 as evidence.
The per-file blocks below cover only files with a finding; every other file was read
against the six per-file items and is Confirmed on all of them.

## Cross-pattern
- No overlap or contradiction: Confirmed - Hazard/Mystery, Trap/Environmental/Residual and
  wild Hazard (living)/Creature each state their boundary in Constraints.
- Three tiers supplied across the class files: Confirmed - HIGH's lack of a concealed
  detail is stated and deliberate.
- Concealment triples stated per class, and not converged: Needs Attention - the three WILD
  class files draw the same Clue set, `{growth | ground | weather | wear}`, and differ only
  in the qualifier after it (where it is legible from). The Payload sets differ; the Clue
  set has converged.
- Gaps in coverage: Needs Attention -
  - nothing specifies the space a DANGEROUS region's entrances open onto (a ravine floor,
    a cave mouth, a courtyard): `dangerous/Block.md` specifies a quarter, and every room is
    in one. Greywatch's ravine had no hub and two outside entrances;
  - no pattern produces a magic item of GENRE.md's ordinary kind (a potion, a scroll):
    `patterns/setting/Treasure.md`'s QUALITY carries an "effect" only on Table II, and
    nothing else reaches one;
  - `dangerous/Block.md`'s household line - "where they sleep, eat, keep their stores,
    stand guard, and put their dead" - is the same room list for every household; nothing
    varies it by occupant, and Greywatch's households came out with the same rooms.
- Unhoused user-requested content: Needs Attention - the reference's stock creatures by
  their stock names (orcs, kobolds, ogres) have no pattern line asking whether they are
  used; `patterns/setting/Bestiary.md` asks for a Type and a Description, and the Naming
  answer routes every non-human people through a coined name. Standing mysteries and
  referee-left gaps are now housed as Truth Kinds.
- Rates compound sensibly: Needs Attention -
  - `dangerous/Door.md`'s 40% gate is rolled per exit: a room with four exits is gated on
    at least one about 87% of the time, and C.12 resolves with three of four exits gated;
  - `dangerous/High.md` stacks a mandatory challenge, a 50% second, a 30% mystery, a
    mandatory treasure and a 40% second treasure: a typical HIGH room resolves to two
    challenges and two treasures, which is where Greywatch's 50-word Features came from;
  - `dangerous/Medium.md` gives treasure at 50% where the challenge is an encounter, but
    Greywatch's encounter rooms carried treasure in nearly every case - the rate was not
    the problem, the absence of a roll was.
- Nothing contradicts STYLE.md: Needs Attention - `dangerous/High.md`'s "Never leave a HIGH
  room empty-handed" forbids what STYLE.md's "Withholding is content" requires at least
  once per region: a genuinely rich-looking room with nothing in it.
- Neutral and permanent: Needs Attention - Sanity is written into
  `dangerous/Trap.md`'s DAMAGE, `dangerous/Residual.md`'s Damage line and
  `dangerous/Environmental.md`'s Constraints, and `patterns/setting/Procedures.md` requires
  "Wounds and madness". A reference without a sanity mechanic (B/X) still gets one.
- Spec notation: Needs Attention - `dangerous/Mystery.md` and `wild/Mystery.md` rate a line
  `2`, and `patterns/setting/Language.md` rates lines `3-6` and `15+`. `patterns/SPEC.md`
  allows `1` or a percentage; the validator and `tools/context.py` read the first as a
  continuation of the line above.

## patterns/dangerous/Block.md
- Tier coverage - obvious / trigger / secret: N/A - a block is a quarter, not a room.
- Specific: Needs Attention - the household room list is fixed across occupants.
- Discoverable: N/A
- Interactive: N/A
- Not overly generic: Needs Attention - as above; six Khughik warrens under one occupant
  passed the "never two household blocks for one occupant" constraint by name alone.
- Missing relevant features: Needs Attention - no line for how the block opens onto the
  region outside it.

## patterns/dangerous/Door.md
- Tier coverage: Confirmed.
- Specific: Confirmed.
- Discoverable: Confirmed.
- Interactive: Confirmed.
- Not overly generic: Confirmed.
- Missing relevant features: Needs Attention - the 40% gate is per exit with no cap per room.

## patterns/dangerous/High.md
- Tier coverage: Confirmed.
- Specific: Confirmed.
- Discoverable: Confirmed.
- Interactive: Confirmed.
- Not overly generic: Confirmed.
- Missing relevant features: Needs Attention - no room for a HIGH room that withholds.

## patterns/setting/Treasure.md
- Tier coverage: N/A
- Specific: Confirmed.
- Discoverable: N/A
- Interactive: N/A
- Not overly generic: Needs Attention - Greywatch's Table III is a generic gem list with no
  line reaching setting/History.md; the "what it is made of, or struck in" line is met by
  material alone.
- Missing relevant features: Needs Attention - no magic item of the ordinary kind.

## patterns/setting/Bestiary.md
- Tier coverage: N/A
- Specific: Confirmed.
- Discoverable: N/A
- Interactive: N/A
- Not overly generic: Confirmed.
- Missing relevant features: Needs Attention - no line asking whether an entry is one of
  the reference's stock creatures.

## Open Items
- A pattern for the space a DANGEROUS region's entrances open onto. (pattern gap)
- A slot for ordinary magic items. (pattern gap)
- Vary Block.md's household room list by occupant. (pattern)
- Cap Door.md's gate per room, or rate it per room rather than per exit. (pattern rate)
- Reconcile High.md's "never empty-handed" with STYLE.md's withholding. (pattern vs STYLE)
- Move Sanity out of the pattern files into a GENRE.md-answered option. (pattern neutrality)
- Differentiate the WILD Clue sets, or move the shared set to one file. (pattern)
- Bring `2`, `3-6`, `15+` rates into SPEC.md's notation, or SPEC.md to them. (notation)
- A Bestiary line for the reference's stock creatures. (unhoused)

## Addendum 2026-09-28 - Constraints audit, for approval

Every Constraint a 4c sheet can reach: the `dangerous/`, `wild/` and `safe/` files and the
five `patterns/setting/` files their Specs cite - 122 entries. Each is judged against what
the location writer now has in hand: the template's static reads (`GENRE.md`, `STYLE.md`,
`BRIEF.md`, the setting docs, the Region Overview), the template's own Instructions, and a
`tools/context.py` sheet whose draws are already settled. Nothing here has been applied; each
row is a proposal.

**Applied 2026-09-28.** 61 entries cut; the seven generalized lines are
`templates/Location.md` instruction 8 and its Treasure table citation; Door's two block-scale
rules merged; three DRAW-TIME rules folded into menu item definitions (Environmental
`collapse` and `growth`, WILD Hazard `living`), the rest cut. Two rows stay as they were:
`safe/Wealth.md`'s hidden-Protection rule, since the concealed-detail rate resolves before
the Protection is drawn and `context.py` cannot enforce it; and the `patterns/setting/`
NOT-4C rows needed no change, since `context.py` never opens a file another step's template
writes. The `warded` weighting is not applied: named menus are drawn unweighted, so it needs
`tools/draw.py` support first. Cutting High.md's "never empty-handed" removes its conflict
with `STYLE.md`'s Withholding. Median sheet after: A 2,969, B 1,009, C 1,969 tokens.

| Verdict | Count | Meaning |
|---|---|---|
| KEEP | 43 | closes a pathway nothing else closes, at write time - stays |
| GENERALIZE | 19 | the same writing rule in several files - one line in `templates/Location.md`, cut from each file |
| NOT-4C | 17 | governs another step's artifact - stays in its file, never printed on a sheet |
| DRAW-TIME | 15 | a rule for whoever picks a draw, which is now arithmetic - folded into the menu item's definition, or cut |
| CUT-STYLE | 10 | restates one of `STYLE.md`'s tests or consequences - cut |
| CUT-SPEC | 9 | restates the file's own Spec, or is a note on its structure - cut |
| CUT-TEMPLATE | 4 | restates a `templates/Location.md` instruction - cut |
| CUT-TOOL | 3 | enforced by `context.py` or the validator - cut |
| CUT-GENRE | 2 | restates `GENRE.md` - cut |

Applied in full, the Constraints a median sheet prints fall from 1,034 to 397 tokens in C,
578 to 226 in B and 720 to 428 in A, by simulation over every stub.

### Proposed template lines (the GENERALIZE rows, collapsed)

Each replaces the rows named after it. Written for `templates/Location.md`'s Instructions or
Citations, as one line each:

1. **One history per room.** A part that could not share the room with the rest is changed,
   not explained. (dangerous/, wild/, safe/ Dressing)
2. **Name a thing that has a name** - a term, trade, material, landform or species - rather
   than describing it. (the three Dressing files, Residual)
3. **Never a bare noun for an exit or a container.** Its make and condition are what a party
   can test. (Door, Treasure)
4. **A hazard or a trap is one Feature** - its tell and its effect on one line, its forced
   damage cited last. (Hazard, Trap, Wealth)
5. **A concealed detail never pays out a route the diagram did not draw.** (Low, Hidden,
   Landmark)
6. **Never two triggers deep** - no clue reached only by acting on another clue. (Hidden,
   Secret)
7. Citations: **a table roll is cited, never described, and each citation is one pull.**
   (dangerous/ and wild/ Treasure)

Door's two block-scale exit rules merge into one and stay in Door.md, since they are
DANGEROUS-only.

### Decisions this needs

- **Step 5b's inversion.** Rows 1, 2 and 7 exist in all three rating folders on purpose, and
  5b counts two folders' versions reading the same as a finding. Generalizing them retires
  that for rules about writing a line rather than about a rating. Recommended: the test for
  a rating folder is whether the rule would read differently for another rating; these do
  not.
- **DRAW-TIME rows.** Once the draw is arithmetic, a classification rule ("growth that acts
  on its own account is a creature") guides no one at write time. Recommended: fold each into
  the definition of the menu item it separates, which CLAUDE.md allows, and cut the entry.
- **NOT-4C rows.** Recommended: `context.py` stops printing Constraints of `patterns/setting/`
  files whose artifact another step writes (Treasure, NamedCreatures, UniqueTreasures,
  Bestiary). The five NOT-4C rows in rating folders (Block, Key, Treasure, Landmark,
  Secret) stay, at about 150 tokens on the sheets that reach them.

### Found along the way

- `dangerous/High.md`'s "Never leave a HIGH room empty-handed" contradicts `STYLE.md`'s
  Withholding consequence (at least one rich-looking room per region holds nothing). The
  last SettingJudgementCheck traced its missing withholding here.
- `dangerous/Door.md`'s GATE menu weights `warded` equal to a lock, so one gate in six is
  sorcery. The C addendum above counted 7 wards in 22 rooms against a scarce Magic level.
  A Spec fix: weight the menu (`warded 5%`), which `tools/draw.py` already reads.
- `safe/Wealth.md`'s "A hidden Protection has spent its concealed detail" is not enforced:
  `context.py` still fires Settlement's concealed-detail rate against it.
- A SAFE sheet prints every prominence-dependent line, since prominence is the template's
  decision and no stub records it; `--set prominence=...` settles it.

### Every row

| File | Constraint | Verdict | Reason |
|---|---|---|---|
| dangerous/Block.md | Never two purpose blocks... | NOT-4C | block design is 4a/4b's; no room can act on it |
| dangerous/Creature.md | A shape that contradicts... | KEEP |  |
| dangerous/Creature.md | Rivals belonging... | DRAW-TIME | the kind is drawn; fold into the kind menu's definition |
| dangerous/Creature.md | Terrain that only costs... | DRAW-TIME | as above |
| dangerous/Creature.md | Never give a swarm... | KEEP |  |
| dangerous/Creature.md | Never let an unbeatable... | CUT-SPEC | Encounter.md's Spec already asks for a Sign a room early |
| dangerous/Creature.md | Never name what rivals... | CUT-STYLE | the player's-decision test |
| dangerous/Door.md | No written exit description repeats... | KEEP | merge with the next into one block-scale rule |
| dangerous/Door.md | Two exits of the same kind... | GENERALIZE | merge into the rule above |
| dangerous/Door.md | Never reclassify an edge... | CUT-TOOL | the sheet prints each exit's kind; the validator checks both ends |
| dangerous/Door.md | Where an exit commits... | CUT-STYLE | the player's-decision test |
| dangerous/Door.md | Never write a bare... | GENERALIZE | template: never a bare noun for an exit or a container |
| dangerous/Door.md | Never move a gate... | KEEP |  |
| dangerous/Door.md | A ward is sorcery... | CUT-GENRE | GENRE.md's Magic level; Mystery.md keeps the one sorcery rule |
| dangerous/Door.md | Never state what an exit means... | CUT-STYLE | the player's-decision test |
| dangerous/Dressing.md | Never a detail the Region... | CUT-STYLE | say a fact once |
| dangerous/Dressing.md | Do not reuse a purpose... | KEEP |  |
| dangerous/Dressing.md | Do not let every room... | DRAW-TIME | Condition is drawn |
| dangerous/Dressing.md | Never leave a feature... | GENERALIZE | template: one history per room - same rule in all three Dressing files |
| dangerous/Dressing.md | Never describe an architectural... | GENERALIZE | template: name a thing that has a name - same rule in all three Dressing files and Residual |
| dangerous/Encounter.md | Kind is exactly one... | DRAW-TIME | the kind is drawn once |
| dangerous/Encounter.md | Never an encounter met... | CUT-SPEC | the Spec's own Sign line |
| dangerous/Environmental.md | A fall that has finished... | DRAW-TIME | classification |
| dangerous/Environmental.md | Growth that acts... | DRAW-TIME | classification |
| dangerous/Environmental.md | A condition the Dressing... | DRAW-TIME | classification |
| dangerous/Environmental.md | Never invent region-scale... | KEEP |  |
| dangerous/Environmental.md | Sanity is rarely... | KEEP |  |
| dangerous/Hazard.md | The whole hazard is one Feature... | GENERALIZE | template: a hazard or trap is one Feature (also Trap.md, Wealth.md) |
| dangerous/Hazard.md | Never raise a tier... | KEEP |  |
| dangerous/High.md | Never add a discovery... | CUT-TEMPLATE | instruction 1: nothing the sheet did not draw is added |
| dangerous/High.md | Never leave a HIGH room... | CUT-SPEC | the Spec draws its treasure; and it contradicts STYLE.md's Withholding - see note |
| dangerous/Key.md | A key is drawn from two... | CUT-SPEC | rationale, not a prohibition |
| dangerous/Key.md | Nothing is owed... | NOT-4C | bookkeeping the validator already errors on |
| dangerous/Lore.md | Never a document that knows... | KEEP |  |
| dangerous/Low.md | Never let a room that simply ends... | GENERALIZE | template: a concealed detail never pays out a route the diagram did not draw (also Hidden.md, Landmark.md) |
| dangerous/Low.md | A LOW room whose concealed... | CUT-TEMPLATE | instruction 6: each tier's way in sits in the tier above |
| dangerous/Low.md | Never a search roll... | CUT-STYLE | a secret is opened by an act |
| dangerous/Medium.md | A challenge the party cannot see... | CUT-SPEC | the Spec's present-and-visible line |
| dangerous/Medium.md | Mystery is not a MEDIUM... | DRAW-TIME | the challenge menu already excludes it |
| dangerous/Medium.md | The Payload is not... | KEEP |  |
| dangerous/Mystery.md | Ward and illusion... | KEEP | the one sorcery rule; points at GENRE.md |
| dangerous/Mystery.md | A fixture whose answer... | KEEP |  |
| dangerous/Mystery.md | A fixture that costs... | DRAW-TIME | classification |
| dangerous/Mystery.md | Never write what the fixture... | KEEP |  |
| dangerous/Quest.md | Never a giver here... | KEEP |  |
| dangerous/Residual.md | Never a residual hazard... | KEEP |  |
| dangerous/Residual.md | It cannot be reasoned... | DRAW-TIME | classification |
| dangerous/Residual.md | A residual hazard is held... | CUT-GENRE | GENRE.md's Magic level; Mystery.md keeps the rule |
| dangerous/Residual.md | Never atmospheric... | GENERALIZE | template: name a thing that has a name |
| dangerous/Trap.md | Never pick a damage type... | KEEP |  |
| dangerous/Trap.md | Never reach up a tier... | KEEP |  |
| dangerous/Trap.md | A trap is one Feature... | GENERALIZE | template: a hazard or trap is one Feature |
| dangerous/Treasure.md | Never name or describe... | GENERALIZE | template Citations: a table roll is cited, never described (also wild/Treasure.md) |
| dangerous/Treasure.md | One pull per citation... | GENERALIZE | template Citations |
| dangerous/Treasure.md | A region's stated table-lean... | NOT-4C | settled at 5c |
| dangerous/Treasure.md | A container is never... | GENERALIZE | template: never a bare noun for an exit or a container |
| dangerous/Treasure.md | Never write a lesser guard... | KEEP |  |
| wild/Creature.md | Never state what going around... | CUT-STYLE | the player's-decision test |
| wild/Creature.md | Never a lone individual... | KEEP |  |
| wild/Dressing.md | No detail budget... | CUT-TEMPLATE | instruction 2's length cap |
| wild/Dressing.md | Never restate the Region... | CUT-STYLE | say a fact once |
| wild/Dressing.md | Never give a detail its causal... | KEEP |  |
| wild/Dressing.md | Never leave a part... | GENERALIZE | template: one history per room |
| wild/Dressing.md | Never describe a landform... | GENERALIZE | template: name a thing that has a name |
| wild/Dressing.md | Purpose is supplied... | CUT-SPEC | structure note |
| wild/Hazard.md | A living hazard... | DRAW-TIME | classification |
| wild/Hazard.md | Never a set hazard... | KEEP |  |
| wild/Hidden.md | A Hidden way in... | KEEP |  |
| wild/Hidden.md | Never a clue reached only... | GENERALIZE | template instruction 6: never two triggers deep (also wild/Secret.md) |
| wild/Hidden.md | A concealed detail never... | GENERALIZE | template: no route the diagram did not draw |
| wild/Lair.md | A den nobody could find... | KEEP |  |
| wild/Landmark.md | A Landmark can be named... | NOT-4C | classification made at 4a |
| wild/Landmark.md | Never roll for children... | CUT-TOOL | the sheet prints one lead line per child |
| wild/Landmark.md | A Crossing is chosen... | DRAW-TIME | the kind is drawn |
| wild/Landmark.md | Crossing is a Landmark... | DRAW-TIME | the kind is drawn |
| wild/Landmark.md | A concealed detail never... | GENERALIZE | template: no route the diagram did not draw |
| wild/Lore.md | Outdoors, lore is cut... | KEEP |  |
| wild/Mystery.md | Never cost anything short... | KEEP |  |
| wild/Secret.md | Never write one triple... | KEEP |  |
| wild/Secret.md | A Secret location carries... | NOT-4C | graph shape, 4b's |
| wild/Treasure.md | Never name or describe... | GENERALIZE | template Citations |
| wild/Treasure.md | Never a pristine find... | KEEP |  |
| safe/Authority.md | No authority defaults... | KEEP |  |
| safe/Commerce.md | Never leave a price... | KEEP |  |
| safe/Dressing.md | Never explain a fixture... | CUT-STYLE | the player's-decision test |
| safe/Dressing.md | Never describe the place... | KEEP |  |
| safe/Dressing.md | Never a fact of the whole... | CUT-STYLE | say a fact once |
| safe/Dressing.md | Never leave a part... | GENERALIZE | template: one history per room |
| safe/Dressing.md | Never describe a trade... | GENERALIZE | template: name a thing that has a name |
| safe/Dressing.md | Purpose is supplied... | CUT-SPEC | structure note |
| safe/Faction.md | Never a presence... | KEEP |  |
| safe/Garrison.md | A garrison watches... | KEEP |  |
| safe/Lore.md | Spoken word is not... | KEEP |  |
| safe/People.md | Never invent a cast... | KEEP |  |
| safe/Quest.md | Never a target that is not... | CUT-TOOL | the validator errors on an unknown code |
| safe/Settlement.md | Decide prominence first... | KEEP |  |
| safe/Settlement.md | Never write a location heavier... | KEEP | trim: instruction 2 now carries the length half |
| safe/Settlement.md | Never a liner-note Wealth... | KEEP |  |
| safe/Settlement.md | The gate is one line... | CUT-SPEC | structure note |
| safe/Settlement.md | Never conceal something... | KEEP |  |
| safe/Situation.md | A situation is a condition... | CUT-STYLE | situations, not stories |
| safe/Social.md | A Kind never draws a hook... | CUT-SPEC | structure note |
| safe/Social.md | A rumour is repeated... | KEEP |  |
| safe/Wealth.md | A hidden Protection... | DRAW-TIME | context.py should suppress the concealed rate - see note |
| safe/Wealth.md | Never invent a Bestiary... | KEEP |  |
| safe/Wealth.md | A lethal trap here... | KEEP | trim: the one-Feature half generalizes |
| safe/Wealth.md | Its lore has no living... | KEEP |  |
| setting/Naming.md | Name only what will be... | KEEP |  |
| setting/Naming.md | Never let a region's names... | DRAW-TIME | the mouth is drawn |
| setting/Treasure.md | Never decide the container... | NOT-4C | governs the tables (2g) |
| setting/Treasure.md | Never shrink a weight... | NOT-4C | 2g |
| setting/Treasure.md | Nothing past two orders... | NOT-4C | 2g |
| setting/NamedCreatures.md | A motivation is... | NOT-4C | 4d |
| setting/NamedCreatures.md | Never let a second meeting... | NOT-4C | 4d |
| setting/UniqueTreasures.md | Never an invented origin... | NOT-4C | 4d |
| setting/UniqueTreasures.md | The location names... | CUT-TEMPLATE | A note on completeness |
| setting/Bestiary.md | One stat block... | NOT-4C | 2e |
| setting/Bestiary.md | Never size a creature... | NOT-4C | 2e |
| setting/Bestiary.md | What does not go here... | NOT-4C | 2e |
| setting/Bestiary.md | Ordinary wildlife... | NOT-4C | 2e |
| setting/Bestiary.md | Mundane human threats... | NOT-4C | 2e |
| setting/Bestiary.md | Guardian and hazard... | NOT-4C | 2e |
