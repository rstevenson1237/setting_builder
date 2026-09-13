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

## Open

- Whether the block tier is a new level or a rule that a vertical stack is one region.
- Whether the Truth-instance draw belongs on every weight file or only HIGH and MEDIUM.
- Where the house-rules artifact sits, and whether pattern files cite it or it is read
  unconditionally at 4c the way `dangerous/Dressing.md` is.
