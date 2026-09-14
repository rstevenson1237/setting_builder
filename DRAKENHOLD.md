# Drakenhold

Working notes on the predecessor project, `rstevenson1237/drakenhold`, read at the source
rather than at its published site. Two directions, and the second is the one that matters:
what its corpus looks like measured against this framework's current artifacts, and - if
its content were harvested as inspiration for a clean rebuild here - where the friction
would actually be. Like `PLANS.md` this is running state, not authority; `STEPS.md` and
`patterns/SPEC.md` remain the authorities wherever this file disagrees with them.

The corpus audited is what Drakenhold publishes: its setting outline, `outlines/`,
`regions/`, `blocks/`, and the setting diagram. Its own `DESIGN_PATTERNS.md` and
`patterns/` are process documents there, excluded from its deliverable, and they are read
here anyway because they are the direct ancestor of `patterns/` in this repo and they are
the most useful thing in it.

## Part one: what fits

### The three tests hold

Drakenhold passes `GENRE.md`'s **What a line has to earn** more consistently than anything
this framework has generated. Three mechanisms are doing that work, and all three are
reproducible:

- **Every History event carries a `Trace:`** - this framework's `Left:` field under another
  name, and filled with a findable physical thing rather than left at `[pending 4d]`. *"The
  seam is visible - everything above the Main Level is finer, later work in a different
  stone, and the join runs clean around all three peaks."*
- **Its Truths are mechanisms, not propositions.** Tiles gate lateral movement and never
  vertical; rods gate action; the dark is hostile to light, so a torch below the Under
  Levels is a declaration. Each is a rule a party can plan against, which is what a Handle
  is for.
- **The genre position is stated as a refusal.** *"Vermakith is weather"*; *"Rumours of his
  deeper purpose should be seeded generously and are all wrong."* That is `give situations,
  not stories` written into the setting outline as policy, and the regions keep it.

### Structural correspondence

| Drakenhold | This framework |
|---|---|
| `Drakenhold_Setting_Outline.md` Overview | `setting/Setting.md` |
| `outlines/01`-`06` | `Truths` `Rumours` `History` `Factions` `Bestiary` `Treasure` |
| `regions/00_INDEX.md` | `setting/region/Regions.md` - rating and die, correct |
| `diagrams/T1`-`T4` | `Connections.mmd` and per-region `Connections.mmd`, and T3/T4 go below what this framework specifies |
| `## LOCATION STUBS` | `Locations.md` |
| per-region `## TABLES` | the mandated d6, correct type per rating in all 22 regions, DANGEROUS counting down from 6 |
| location entries | `templates/Location.md`'s Player Summary / Referee Notes / Features shape |

The rating vocabulary and the HIGH/MEDIUM/LOW weights are this framework's own, inherited.
The Feature decomposition rule - one bolded name, one thing per line, no connective prose -
was arrived at independently there and is confirmation rather than coincidence.

## Part two: what does not fit

Ordered by how much work the divergence represents, not by severity.

1. **Five rating-specific Region Overview fields are absent.** All 22 region files carry
   exactly `Overview, Ambiance, Layout, Features, Dangers, Creatures, Secrets, Treasure`.
   None carries **Architecture** (DANGEROUS), **People** or **Situation** (SAFE),
   **Terrain** or **Foraging** (WILD), or **Factions** - which `templates/Region.md`
   requires be answered even when the answer is none. The People and Situation content
   exists in `A Thornhaven`; it is dissolved into Overview and Creatures, where the referee
   will not look for it.

2. **Region Overview runs five-plus sentences against a three-sentence hard cap**, and
   fails the way the cap exists to prevent: Thornhaven's restates the die, the layout and
   the tags, then writes the referee's conclusion twice (*"Its job is resupply, rumour,
   downtime and the module's first lesson"*, *"which is the register the whole region plays
   in"*).

3. **No `Tags.md` at either level.** Every location carries three freely-authored tags
   (388 of 393 stubs, three each). This framework draws exactly two, from a 25-tag setting
   pool and a 25-tag region pool. Drakenhold's are better prose and worse structure: nothing
   binds the setting at the tag layer, and step 1b has no pool to compile against.

4. **No `Language.md`.** The root inventory lives as bullets inside `01_TRUTHS.md`. The
   roots are good and already generative - they gloss every region name - but as part of
   Truths they cannot receive coinage back at 4c/4d, which is the job the artifact exists
   for, and Truths is carrying content that is not a truth.

5. **The five registries do not exist.** No `Lore.md`, `Keys.md`, `Quests.md`,
   `NamedCreatures.md`, `UniqueTreasures.md`. `LORE_INDEX.md` is the nearest thing and
   declares itself *"an index and not a source"*. The container/data split is therefore
   inverted: Vermakith, the lance, the tiles and the rods are each described in several
   places instead of cited from one.

6. **No citation format.** `(Predatory, 5, Bestiary : Goblin)`, `(Treasure III, d20)`,
   `(Lore: Title)` appear zero times in the corpus. References are backticked plain names.
   Location codes would still link; nothing else would, and demeanor and number-appearing
   are simply absent.

7. **Locations live inside region files** rather than as `setting/region/A/1.md`, and every
   entry states its edges twice, once as `**Exits:**` and once as `**Connections:**` - a
   restatement at the same level.

8. **Weight is applied to SAFE locations** (`A.1` HIGH, `A.2` MEDIUM, `A.3` LOW), where
   this framework assigns weight to DANGEROUS only. The three WILD regions inside the
   mountain use no landmark/hidden/secret classification at all.

9. **Four outline fields have no home here.** `07_TRAPS` (a setting-level catalogue; this
   framework distributes traps to `dangerous/Trap.md` and `dangerous/Hazard.md` per
   location), `08_GRAFFITI` (a d20 setting-wide table; no analogue), `09_PROCEDURAL_TABLES`
   (extra colour tables beyond the one mandated d6 per region), and `10_STANDING_MYSTERIES`
   (what the module refuses to answer, scoped `[local]` or `[setting]`; no analogue - the
   nearest concept is `checks/SettingJudgementCheck.md`'s Room to Grow, and it is not the
   same act).

10. **`blocks/` has no analogue at all.** Five connective documents between setting and
    region, carrying room budgets, the tribute chain, cross-peak wake conditions and shared
    routes. This framework has setting, region, location and nothing between. For 22 regions
    where four stack vertically into one peak, that middle tier is load-bearing.

11. **Procedures are outsourced** to a read-only mirror of another project's design notes,
    where 1c seeds `setting/Procedures.md` and 2h tailors it. The traps outline's *"No trap
    here introduces a mechanic"* is the right instinct with no local file to cite.

## Part three: harvesting it here, and where the friction is

The stated motivation for this project is that location-level detail does not reliably come
out adhering to the design patterns, and washes out. That reframes the harvest: the friction
is not mostly in moving the content, it is in what the content turns out to depend on.

### The mechanical friction, briefly

Real, tedious, and none of it interesting:

- **Pools before stubs.** Drakenhold authored tags per location; this framework draws them
  from pools fixed at 1b and 3c. The two setting-level and 22 region-level pools have to be
  invented first and the 393 stubs re-tagged down to two each. The existing three-tag lines
  are not a source for the pools - they are per-location theses, which is a different thing.
- **Registry extraction is a rewrite.** Pulling the tiles, the rods, the lance and Vermakith
  out of 22 region files into five registries, then rewriting every mention as a citation,
  touches every file that mentions them and is lossy in exactly the places the prose is best.
- **WILD classification cannot be assigned post-hoc.** `hidden` means reached from a
  specific named Landmark and `secret` means revealed by a trigger, so classifying FB, I and
  J means redoing 4b's connection graph for them, not labelling what is there.
- **Genre collision.** `GENRE.md` here is Howard's Hyborian Age, and the compiled
  `## Design patterns` in all 33 compile-list files are Conan-flavoured. Drakenhold is
  Hobbit-on-the-road plus Conan-in-the-halls over a dwarven hold. Harvesting its content
  under the current `GENRE.md` is genre drift, which `CLAUDE.md` names as failure mode one;
  doing it properly means re-running 1a and 1b and discarding the current compiled content.
- **Four artifacts land on the floor.** Traps, Graffiti, Procedural Tables and Standing
  Mysteries have no destination, and `blocks/` has no tier. That is five bodies of good
  content with nowhere to go.
- **A name collision that will cause real damage.** Drakenhold's **Landmark / Hidden /
  Secret** are three *registers layered inside a single location entry* - what arriving
  shows, what asking reveals, what a named physical action opens. This framework's
  landmark/hidden/secret are three *classes of WILD location*. Same three words, two
  unrelated meanings, and the Drakenhold sense is the one doing the anti-washout work.

### The real friction: what the density is actually made of

Drakenhold's location detail is dense because of things that are not in its location files.

**Detail is causal, not decorative.** `A.1`'s Inverted Lintel is one block carrying two
roots, *ost* and *gir*, and it is the town's dwarven name set upside down at its own front
door, *"and the full reading waits at the third waystone on the trail."* Nothing about that
feature could be drawn from a menu. It requires a setting Truth (names compound and are a
claim about a line), a root inventory, a second location three regions away, and a decision
that the town does not know what it is standing on. `A.3`'s trade weights are worth almost
nothing and are content because *"they match the standards a party will meet inside the
hold."* In both cases the detail is a **consequence of a commitment made upstream**.

This framework's compiled `## Design patterns` cannot produce that, and the reason is
structural rather than a quality problem. `dangerous/Dressing.md`'s Purpose section is a
list of fifty nouns; drawing *granary* returns a granary. Drakenhold's Peak 1 Under Level is
also granaries, and its content is that kobolds hold them and would rather trade than fight
- which came from a faction decision made at block level. **A menu returns a member of a
category. It cannot return a consequence.** Compiled patterns raise the floor of vocabulary,
and washout is a failure at the floor of meaning.

Four specific consequences follow, and they are the findings worth acting on.

**1. The Spec contract is quantitative where the density is relational.**
`1  Treasure {guarded | hidden | discarded}` guarantees that a treasure exists and how it
sits. No line in the library draws *a thing that will be recognised again somewhere else*,
and recognition is where most of Drakenhold's good features live. Its house rule for this is
**repetition before explanation**: show the same stone four times across two regions before
anything names it. There is currently no way to express that in a Spec at all.

**2. `templates/Location.md`'s deliberately narrow Context cuts both ways.** It is narrow so
the entry stays shaped by its stub and region *"rather than washed out by the full
setting"*, which is a real defence against one failure. But it also withholds what the
region's other thirty rooms already did, and the density in Drakenhold comes from authoring
a whole peak in one pass with four levels in view - which is how *"the escort turns back
here, and their refusal to go further is the clearest warning in the module"* becomes
writable at `GE.1`. Concretely: `dangerous/Dressing.md`'s constraint **do not reuse a
purpose already used in this region** is not checkable by a generator that cannot see the
region's other locations. That is a named constraint the process cannot honour today.

**3. The registries arrive after the locations that need them.** 4c writes a stub row and 4d
writes the content, so at the moment a location is authored the Key it cites has no content
and the location can only say there is a lock. Drakenhold fixes the *grammar* up front -
rods come in House, Guild, Runemaster and Royal tiers, the Royal locks answer to no single
rod - so every lock any location invents is already an instance of a known system. The
container/data split is right for consistency and is deferring the thing that would make the
container specific. The missing piece is a third stage: **grammar at step 2, instance at 4c,
content at 4d.**

**4. Truths are audited downward but never drawn downward.** A Truth's Handle is filled with
real Location Codes at 5c, after the fact. Nothing at 4c requires a location to *be an
instance of* a Truth. Nearly every strong feature in Thornhaven is an instance of one - that
names compound, or that runic script is legible to anyone who paid attention on the way in.
A registry-block line of the form `40%  An instance of a setting Truth, in this room's own
terms (setting/Truths.md)` would invert the mechanism from audit to generation, and on this
evidence it is the highest-leverage single change available.

### What Drakenhold's own pattern library does that this one dropped

This is the finding that most directly addresses the washout complaint.

Drakenhold's `patterns/` is nine files, one per mode x weight cell, and a writer opens
exactly one. Ours is sixty-odd files in five folders, reached through a validated tree. Ours
is better *architecture* - the tree is real, the edge/question rule is real, and the
neutral/compiled separation is the thing that makes a rebuild possible at all. But the two
libraries hold different *kinds* of content, and the difference is not one of resolution:

- **Ours holds draw contracts.** `50%  Second challenge {encounter | hazard | mystery}` -
  what a location contains, and at what rate.
- **Theirs holds binding rules with named failure modes and cited evidence.** *"No puzzle
  resolves on an attribute roll"*, and then the control case from the corpus: the same
  author, on the same level, wrote one puzzle with a placed clue and no roll and a second
  that places its clue honestly - eighteen chessboards all showing the same mate - and then
  gates *recognising* it on a roll under Intelligence. *"The second undoes itself. If a
  player can look at the thing and reason about it, the reasoning is the mechanic."*

A draw contract can guarantee composition. It cannot guarantee quality, and washout is a
quality failure. Their House Rules are the clearest examples of rules that do bear on
quality, and every one of them is neutral, permanent, and cross-cutting:

- The clue lives outside the location holding the secret. *"A secret whose only evidence is
  inside itself is not a secret; it is a die roll wearing a costume."*
- Every gate has an answer that is not the gate, and the answer is priced. Not a second
  door - a longer road, a worse road, a road that arrives in the wrong place. Both branches
  are costed and the module never says which is the mistake.
- A guardian is usually a condition, not a monster. A beast that will not touch anyone
  wearing the right mask; a thing that escalates through four refusals before it strikes.
- Withholding is content. The first genuinely rich-looking room contains nothing.
- Trope is free structure; defiance is funded by convention held elsewhere, and each
  deliberate defiance names the straight instances that fund it.
- State the nil. A field resolving to nothing says so, because an omitted field is
  ambiguous - did the author decide, or forget?
- Every bolded noun in the Player's Overview appears below as a feature. *"This is the
  module's most common real failure, and it is exactly checkable."*
- No secret is gated on a search roll. Gates are physical: standing somewhere, clearing
  something, opening something, speaking a name, looking back.

**And this framework has nowhere to put any of them.** They are neutral and permanent, so
by `patterns/SPEC.md`'s governing distinction they cannot go in `## Design patterns`, which
step 1b rewrites per genre. Several are prohibitions and could go in `Constraints`, but
*repetition before explanation* and *withholding is content* are positive generative rules,
and cross-cutting ones - restating them across thirty files is exactly what "never restate a
rule another file owns" forbids. `GENRE.md`'s three tests are the top of this ladder and the
rung below it is empty.

**The gap, stated once:** there is no neutral, permanent, setting-independent artifact
holding cross-cutting authorial rules that every location-level pattern file can cite. That
is where the House Rules belong, and their absence is a better explanation of washed-out
location output than any shortage of compiled vocabulary.

Two smaller carries from the same source, both cheap:

- **Tell / trigger / effect / decision**, from `07_TRAPS`, generalises past traps to any
  interactive feature, and is a sharper operationalisation of *the solution is never written
  into the problem* than the pattern files currently carry.
- **Standing Mysteries as an artifact.** "The setting declines to answer this, and here is
  the scope of the refusal" is a different act from "not written yet", and this framework
  can currently express only the second.

## Part four: connectedness, and why it is written backwards

The finding above - that this framework has no way to draw *a thing that will be recognised
again somewhere else* - is correct about the gap and wrong about the fix. Drakenhold's own
experience of building that connectedness is the correction, and it is worth recording
because it inverts the obvious remedy.

**Forward-declaring connections does not work.** Maintaining the link count and finding
adequate placements for every detail was the hardest single problem in that build. A
generator that emits a cross-reference whenever a feature would be richer for having one
produces open threads faster than any pass can close them, and the far ends accumulate
unwritten. The end state of that approach is a large ledger of details owed and a corpus
that cannot be checked, because every unresolved thread looks identical to a deliberate one.

**What worked was retroactive reinforcement.** Write a baseline region, and baseline
locations within it. Then, where a human decides a specific element needs reinforcing, go
back and place the supporting detail into locations that already exist. The far end is
written second, deliberately, into known ground - which is why the placements are adequate
rather than approximate, and why the count stays bounded: nothing is owed until somebody
decides it is owed.

Two consequences for this framework.

**The reinforcement pass already exists structurally and is scoped as bookkeeping.**
STEPS.md 5c is the only step that reads upward: it fills `Truths.md`'s Handles and
`History.md`'s Left lines with real Location Codes and names unfulfilled claims under Room
to Grow. That is the right step at the right place in the order, doing a strictly smaller
job than the one described above - it *records* where a claim landed and *reports* where it
did not, but it never authors the supporting detail that would make it land. Promoting it
from audit to authoring is the concrete change: a pass that takes a chosen element and
writes its placements into locations that are already on disk. `repetition before
explanation` - show the same stone four times across two regions before anything names it -
is then implementable without any forward declaration at all, because the repetitions are
placed after the stone is known to matter.

**The open-detail problem is a ledger problem, and Drakenhold solved it with a split this
framework does not have.** `OPEN_QUESTIONS.md` holds what the authors have not yet settled;
`10_STANDING_MYSTERIES` holds what the setting has decided not to answer, scoped `[local]`
or `[setting]`, and is explicit that the two never mix: *"Questions the authors have not yet
settled are not kept here."* That split is what keeps unresolved threads from hiding among
deliberate ones. This framework has neither file, and adding the Standing Mysteries artifact
without also adding the tracking file would produce exactly the confusion the split exists
to prevent.

## Part five: two-ended elements, confirmed and unconfirmed

The question of whether a named destination reliably picks up the thread pointed at it has
three different answers in the current library, and only one of the three is safe.

**Safe, by generation order.** `dangerous/Medium.md` and `Low.md` carry *a detail that
foreshadows a HIGH location elsewhere in the region*, at 25% and 10%. This one cannot
dangle: 4c generates HIGH first, then MEDIUM, then LOW, precisely so lower tiers can
foreshadow what is already decided. The far end exists before the near end is written. This
is the model the other two should be measured against.

**Safe, by registering supply and drafting demand later.** `dangerous/Quest.md` is explicit:
*"Register supply, do not wait for demand. When a location holds something a person
elsewhere would want [...] record it as a Quest stub now, even if no giver exists yet.
Givers are drafted from what has been registered."* A DANGEROUS location is the target end;
it writes a stub row naming itself, and the giver is written afterwards out of the registry.
Nothing is owed by anyone at the time the stub is written, which is Part four's discipline
already implemented. This is correct and should not change.

**Not safe: `dangerous/Key.md`.** Its supply end carries a mandatory line - `1  What it
opens, named by location code and feature`. So a key found at `A.3` names the lock at
`C.11`, by code and by feature, at the moment `A.3` is written. The demand end - the lock
itself - is a *separate, independently rated* draw on the far location's own weight file:
25% at HIGH, 10% at MEDIUM, 5% at LOW. The two draws are unrelated events. `C.11` has no
idea a key named it: `templates/Location.md`'s Context does not include `setting/Keys.md`,
and 4c's order is by region and by class, so `C.11` may well have been written already.

The file states the assumption it is relying on: *"Every location stub in the setting exists
before any location file is written, so a key found here can name its lock by code and name
at 4c, in another region, in a location not yet drafted."* The stub does exist - but a stub
is a name, a weight and two tags. **It has no features.** So the key names a location that
exists and a feature that does not, and whether that feature ever appears is a 5-25% roll
made elsewhere, independently. At LOW it is a 1-in-20 chance the lock is ever written.

This is the open-thread failure from Part four, produced by the library rather than by the
generator, and it is a defect rather than a judgement call.

### The fix: obligations, not deferral

Two candidate fixes, and the choice is not close.

**Deferring every two-ended element to a later layer-in pass is the wrong one**, for a
reason `dangerous/Key.md` states about itself: two-ended elements "are the reason a point
crawl is a network rather than a list." Strip them from 4c and 4c produces a list, with every
network property bolted on afterwards. And bolted on is literal - `dangerous/Dressing.md`'s
Integration is explicitly the last pass, the one checking that everything in the room was put
there by the same history. A lock added to a finished room after that pass has run cannot
participate in the room's design; it can only sit on top of it. Deferral buys safety by
giving up the thing the elements are for.

**The obligation is the right one.** The near end names its target as it does today, and that
naming writes a binding obligation against the far location. When the far location is
generated, the obligation is drawn at rate `1`, overriding the percentage. The percentages
stop being two independent gambles and become what they should always have been: a
**supply-side seeding rate**, with the demand side guaranteed rather than re-rolled.

That means the demand-side lines are **deleted, not lowered** - `25% / 10% / 5% A lock, and
the key that opens it is elsewhere` and `The target of a quest given elsewhere` come off all
three weight files, replaced by a single line reading *any obligation recorded against this
location, at rate 1*. A spontaneously drawn lock whose key was never written anywhere is an
orphan nobody can open, which is strictly worse than not drawing one.

**One discipline makes it sound: obligations point forward only.** An obligation may name a
location in the current generation batch - written atomically, both ends in view - or in a
batch not yet generated, where the override fires when that batch comes up. It may never
point backwards into a finished batch, because there is no longer anywhere for the override
to fire; that case, and only that case, waits for the reinforcement pass. Batch ordering is
already fixed (region order, and HIGH before MEDIUM before LOW within a region), so which
direction a given obligation points is a mechanical question with a mechanical answer.

**And it yields the invariant that was missing: zero unconsumed obligations at the close of
4c.** Every obligation is created when a near end is written and consumed when its far end is
generated, so anything still outstanding is a dangling thread, by definition, detectable by
`tools/validate_setting.py` rather than by reading. That is a hard error, not a judgement
call - which also settles where the open-thread ledger lives. It is not a standing prose
file: it is a field in the topology data with a closed lifecycle, and the closed lifecycle is
what stops it accumulating.

Quest needs no change under any of this. It names no far end - it registers supply and lets
givers be drafted from the registry - so it creates no obligation and can dangle nothing.
The HIGH-foreshadow line needs no change either: generation order already guarantees its far
end.

One smaller incoherence, noted while confirming this: the weight files draw *the target of a
quest given elsewhere*, which reads as though the giver already exists, while
`dangerous/Quest.md` says the opposite - that DANGEROUS registers supply first and givers
are drafted from it. The line and the file it cites describe opposite directions of travel.
The file is right; the line should be reworded.

## Resolved

**The block tier is a generation batch, not a level of the setting.** It was a deliberate
compromise for regions of 50-100 locations, on the reasoning that both a person and a
generator handle a block and then the wiring between blocks better than one undifferentiated
pass. That is a statement about *how much is generated at once*, not about the artifact
hierarchy - so nothing new is owed between `setting/` and `region/`. What is owed is a
batching concept in STEPS.md 4c: a partition of a region's locations that is generated
together.

**A block is a functional quarter, and that is what holds it together.** A block is not an
arbitrary slice of N locations - it is a set of locations sharing a purpose: the former
barracks, the dining and food preparation rooms, the private quarters. Each purpose sharpens
the design of its own locations while all of them sit in one conceptual region. That gives a
block the thing an arbitrary partition lacks - a reason its members belong together, which is
also the thing that makes them specific.

This maps directly onto `dangerous/Dressing.md`'s existing Purpose taxonomy - Keeping,
Working, Living, Holding, Meeting, Believing, Dying, Moving - so the concept needs no new
vocabulary, only a scope. And the predecessor is the evidence it works: Drakenhold's regions
*are* functional quarters (Trade Hall, Granaries, Workshop, Forge, Guildmaster Manse;
Judgement Hall, Prison and Barracks, Throne, Treasure Vaults, Dragon's Lair), running 16 to
65 rooms each. That is a size range for a block, taken from a build that shipped, and it is
worth correcting an earlier claim in these notes: Drakenhold's blocks did **not** group only
regions. They grouped at both scales, giving five nested levels - setting groups region
blocks, region blocks group regions, regions group location blocks, location blocks group
locations, and locations group features. Its diagram tiers encode exactly that ladder: T1 is
setting to blocks, T2 block to regions, T3 region to location groups, T4 group to locations,
and the location entry itself is the last rung. So the proposal here is not the same idea one
level down - it is the *second* half of an arrangement that shipped whole, and the tiering is
proven at both scales rather than inferred from one.

It also settles what to do with a constraint that is currently unsatisfiable rather than
merely unchecked. `dangerous/Dressing.md` says **do not reuse a purpose already used in this
region**, and its Purpose list holds 63 nouns across eight families - so a region of 50-100
locations cannot obey it, and Drakenhold's FA alone is 65 rooms. The resolution is not to
rescope it to the block and keep it absolute. It is **step 5 judgement material**: the
failure it names is real (a region with three storerooms has told the party rooms do not
matter) but whether a given repeat is that failure or is two granaries in a hold that
plausibly had two needs a person to look. So it belongs in the judgement checks, with
`tools/validate_setting.py` raising a **warning** on purpose-repeat density and never an
error - which is the validator's stated posture anyway: strict on format, relaxed on content
and ratios, warning on what needs a human glance but might be intentional. Blocks still help,
by making the repeat legible at the scale a person can actually assess.

The batch is likewise the natural unit for Part four's reinforcement pass, and for Part
five's atomic rule - "both ends in the same batch" is only a usable test because a batch is a
bounded, nameable thing.

**And it exposes a format question worth taking seriously: mermaid is a rendering format
currently being used as the data model.** The evidence is already in the repo.
`templates/Region_Connections.mmd` cannot express a node role, so it instructs the build to
append a markdown table *beneath the graph, inside the `.mmd` file* - and
`tools/validate_setting.py` never reads that table. The consequence is that
`patterns/region/Dangerous.md`'s CLASS MIX and LOW NODE ROLE MIX figures - 8-15% HIGH by
count, 60%+ of LOW carrying a role other than simple connection, the dead-end and one-way
rates - are stated as binding rules with no enforcement anywhere, while the validator does
check the things mermaid *can* say, such as every Exits line matching a real edge.

**Decided: the topology gets an internal format and the `.mmd` is generated from it.** The
governing argument is that two tables serving one purpose in one file is asking for trouble,
and the repo is already carrying that exact arrangement - a graph that cannot express a node
role, and a markdown role table appended beneath it that nothing reads.

It is worse than two, which strengthens the case rather than weakening it. There are **three**
representations of the same connections today: the mermaid graph, the node-role table inside
the same file, and every location's own `**Exits:**` line. The validator already cross-checks
the third against the first - an Exits line naming an edge that no `Connections.mmd` carries
is a hard error, and one crossing a hidden `-.-` edge is a warning. So two of the three are
reconciled by code and the third is reconciled by nobody. An internal format should be the
single source all three are rendered or checked from.

The honest detractors, none of which look decisive:

- **Hand-editability and native GitHub rendering are lost** for the source of truth.
  Mitigated by committing the generated `.mmd`, which keeps it rendering exactly where it
  renders today, and by a generated-do-not-edit header so a hand edit is not silently
  overwritten. The repo already has the precedent - two builders rendering one source.
- **Format choice is less constrained than it first looked.** `README.md`'s "stdlib-only
  Python throughout" is a description of what the repo happens to contain, not a rule it is
  held to, so a dependency is on the table. JSON and `tomllib` remain the zero-dependency
  options.
- **A generator emits mermaid more reliably than a bespoke schema.** Probably true, and it
  cuts the other way on balance: a malformed bespoke file is caught by the validator, while
  a plausible-but-wrong mermaid graph is not caught by anything. Errors that surface are
  cheaper than errors that do not.
- **Merge behaviour** is roughly a wash if the format keeps one edge per line, and worse if
  it nests.

**Is there a library that does this?** Not as one piece, and the split is clean. Checked
against PyPI from this session:

- **`networkx` (3.6.1)** is the data model and the algorithms, and it is a close fit.
  Arbitrary attribute dicts on nodes and edges carry role, edge type, gating condition, block
  membership and obligations with no schema work; `node_link_data` round-trips the whole graph
  to JSON; and the mix rules that currently go unenforced - dead-end counts, entrance counts,
  reachability, the 60%-of-LOW role spread - are ordinary graph queries rather than bespoke
  parsing. It has no mermaid exporter, and emitting flowchart text from a graph is on the
  order of thirty lines.
- **`mermaid-py` (0.8.4)** and **`python-mermaid` (0.1.6)** are emitters and renderers, not
  data models. Their node objects are presentation-shaped - shape, style, position - so they
  would sit downstream of the real model, replacing the thirty lines and adding a dependency
  that also wants network access to render. Not worth it for text output.

So: `networkx` for the model and hand-rolled emission, or plain JSON and hand-rolled
everything. The former buys the checks; the latter buys zero dependencies.

**Could mermaid itself be the single source of truth?** Closer than these notes first
implied, and still no. Mermaid can carry more than the templates currently use: `classDef`
plus `class A1,A5 entryway` assigns node roles and *renders* them as styling, so the role
table could be eliminated today at low cost; `subgraph` maps exactly onto a location block
and renders as a visual grouping; edge type fits an edge label or an arrow form. Node
metadata syntax (`A@{ ... }`) exists in recent versions but takes a fixed key set, not
domain fields.

Where it fails is not topology. It is that the graph file now has to hold **authoring
state** - obligations, and whether each has been consumed - which is not a property of a node
or an edge or a drawing, and has no expression in a diagram language at any version. That is
the argument that actually decides it, and it only appeared once Part five's obligations did.
The prerequisite ordering stands: the internal format is what makes block membership and
obligations fields rather than conventions.

**The house rules go into `GENRE.md`'s fixed block.** It is the right home on the
governing distinction - neutral, permanent, already reproduced verbatim and never
reauthored - and it is the rung below **What a line has to earn**, which is exactly where
the ladder was empty. No new artifact is needed.

The known objection stands and is the real work: broad rules dilute as context grows, and a
rule that is read but not applied is indistinguishable from one that was never written. The
mitigation is not repetition, which "never restate a rule another file owns" forbids - it is
that **a rule survives distance in proportion to how checkable it is at the point of
writing**, and Drakenhold's own house rules split cleanly on that axis:

- *Mechanically checkable, and should become validator rules or judgement-check line items
  on top of their `GENRE.md` statement*: every bolded noun in the Player Summary appears
  below as a Feature (Drakenhold calls this *"the module's most common real failure, and it
  is exactly checkable"*); no secret gated on a search roll; every gate has an answer that
  is not the gate; state the nil.
- *Judgement, not checkable, and these are the ones that actually dilute*: withholding is
  content; repetition before explanation; trope is free structure and defiance is funded by
  convention held elsewhere.

The second set is what `checks/` is for, and the one cheap lever the repo already has for
the first is `CLAUDE.md` - whose entire remit is what must be actively re-checked every
request. A single line there, naming the `GENRE.md` block as the rung below the three tests
rather than as background, costs almost nothing and is the difference between a rule that is
in context and a rule that is in force.

**Truths are read at every location, and `templates/Location.md`'s Context line changes.**
Taking `setting/Truths.md` as an extension of `GENRE.md` - where `GENRE.md` connects
outward to its references and `Truths.md` states what *this* world does - makes the earlier
proposal of a rated draw on HIGH and MEDIUM wrong. The right shape is the one
`dangerous/Dressing.md` already uses: **Mode: second pass**, read unconditionally at 4c for
every location regardless of rating or weight.

Two things follow, and both are edits rather than new structure.

*Availability is not a quota.* Reading Truths at every location must not mean instantiating
one at every location - a truth that surfaces in every room is wallpaper, and restating it
downward fails all three tests at once. The contract is that where a location touches a
Truth it is an **instance** of it in that room's own terms, never a restatement of it.

*The Context section currently forbids this.* `templates/Location.md` says to consult
`setting/Truths.md` *"only to look up a name the stub or region overview already references
- never to pull in new material wholesale"*, which is the correct instruction for
`Bestiary`, `Factions`, `History` and `Rumours` and now the wrong one for `Truths`. Truths
moves up into the narrow consult list proper, alongside `GENRE.md` and
`setting/Procedures.md`. Ordering is already fine: Truths is written at 2c, locations at 4c.

One note worth keeping. This makes `Truths.md` *specific to this setting* yet *not
recompiled* by step 1b - it is authored at 2c and then read like a permanent rule. That is a
third category alongside `patterns/SPEC.md`'s neutral-and-permanent and
specific-and-compiled. The distinction governs pattern-file content and `Truths.md` is
generated content, so this is not a spec violation; it is worth watching anyway, because a
recompile for a new genre will leave Truths untouched while everything around it changes.

## Open

- The concrete format: JSON or TOML, and whether block membership is a field on the
  location or a separate partition list.
- Whether blocks are authored or derived once the format exists. Current lean is authored,
  since a functional quarter is a design decision and not a graph property.
- `networkx` plus hand-rolled emission, or plain JSON and no dependency.
- Whether obligations may cross regions or only batches within a region. Cross-region
  obligations are what make keys interesting and are also the ones most likely to point
  backwards into finished ground.
