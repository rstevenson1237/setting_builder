# Pattern Restructure Plan

Phase 1 deliverable: the top-down plan. Written before any file moves.

Supersedes the recommendation table in `analysis/HexDescribe_TableAnalysis.md` §6, which
was written before the point-crawl and direction-vs-expansion corrections.

---

## 1. Decisions locked

Settled in discussion; recorded here so later phases don't relitigate them.

| # | Decision | Consequence |
|---|---|---|
| D1 | `patterns/` splits into **five** folders: `setting/`, `region/`, `safe/`, `wild/`, `dangerous/` | Pattern guidance now exists for every generation level, not just locations |
| D2 | Every folder carries **three tiers**: Shape → Patterns → Detail | A generation step reads exactly three files from one folder, in order |
| D3 | **No `shared/` folder.** Restatement is deliberate | A trap in SAFE is a swindle; in WILD a snare; in DANGEROUS a deadfall. Writing them separately forces the differentiation |
| D4 | Voice/verbiage lives in **two** places: an expanded `GENRE.md`, and the Detail tier of every folder | Setting-wide voice stated once; per-level application restated where it's applied |
| D5 | **No lair tier.** Scale is a Shape-tier decision | A whole village or dungeon may be one keyed location, or one region — both legal, the Shape tier is where it's chosen |
| D6 | Errands are called **Quests**; they become a two-phase registry | New `setting/Quests.md` + `templates/Quests.md`, stubbed at 4c, written at 4d |
| D7 | Name coherence gets a **living** setting artifact | New `setting/Language.md`, seeded early, appended to whenever a proper noun is coined |
| D8 | Templates relax to what the content needs, and no further | Format stays consistent enough to parse at a glance; strictness beyond that is a defect to remove |

### Corrections carried in from the analysis

- The framework is a **point crawl**. Connecting terrain is procedural, narrated by the
  referee from the Region's Terrain/Foraging/Layout fields. Withdrawn: the "worked
  wilderness has no home" finding (it belongs in Terrain/Foraging) and the
  micro-features-as-coordinates recommendation (region tier, not location tier).
- The corpus's value is **directing** output, not expanding it. The model already holds
  the vocabulary. What it lacks is constraint: forced fresh draws, non-repetition within a
  region, and causal attribution. Vocabulary lists are not a deliverable; constraints are.

---

## 2. Target structure

```
patterns/
  setting/    1_Shape.md   2_Patterns.md   3_Detail.md
  region/     1_Shape.md   2_Patterns.md   3_Detail.md
  safe/       1_Shape.md   2_Patterns.md   3_Detail.md
  wild/       1_Shape.md   2_Patterns.md   3_Detail.md
  dangerous/  1_Shape.md   2_Patterns.md   3_Detail.md
```

Fifteen files, numbered so read-order is visible in a directory listing. Tier names are
taken verbatim from the design discussion — *shape*, *patterns to match against*,
*detail* — to keep the vocabulary in one dialect. None of the three collides with the
existing low/medium/high **weight** vocabulary in DANGEROUS.

### The tier contract

Every tier file, in every folder, answers the same question at its own level.

**Tier 1 — Shape.** *What is this, and how big?*
Two decisions and no content: which **kind** of thing this is (a closed list, chosen from
now), and at what **scale** it is being realized. Scale is the tier's real work and the
reason D5 needs no lair unit: the same lair is a legal answer as one keyed location, as a
cluster of locations, or as a whole region, and the Shape tier is where a user's chosen
style of game picks one. Shape never describes; it classifies and sizes.

**Tier 2 — Patterns.** *What's in it?*
The wide list of specific, concrete patterns to match against — the horizontal variety.
This is the largest tier by volume in every folder and the one Phase 2 exists to fill.
Also carries the selection rules for the things a chosen pattern calls for: creature,
treasure, trap, puzzle, secret, and the registries. Stated flat, for this rating only,
with no cross-rating branching in view.

**Tier 3 — Detail.** *What is it like, and does it hold together?*
Three jobs, in order: **round out** (dressing, ambiance, sensory and physical detail),
**integrate** (make the Tier 2 picks read as one place rather than a list of features —
the job nothing currently owns), and **refine the verbiage** (this level's application of
GENRE.md's voice). Clues live here too, since a clue is a detail that has been made
legible on purpose.

### What does *not* go in a pattern folder

The line that makes D3's duplication affordable: **format lives in `templates/`;
patterns hold only what varies.**

Anything genuinely invariant was never pattern content. Units (feet indoors, yards
outdoors, miles between regions), the Location header format, the Exits line syntax, the
citation formats — these are format, they belong in `templates/` and `CLAUDE.md`, and
they must not be restated in fifteen places. Today the units rule is stated three times
(`patterns/Dressing.md`, `templates/Location.md`, `CLAUDE.md`); the restructure collapses
it to two, both of them format files.

So the test when placing a line is: *does this change between SAFE and DANGEROUS?* If yes,
it is a pattern and it gets written three times, differently. If no, it is format and gets
written once, in `templates/`.

### Managing the duplication risk

D3 accepts drift risk in exchange for differentiation. The mechanism that manages it
already exists: `checks/PatternJudgementCheck.md` reviews `patterns/` for "overlap or
contradiction." Its job inverts — **two restatements that read the same are now a
finding**, not a convenience. `templates/Pattern_Judgement_Check.md` needs one new
checklist item saying so.

---

## 3. Per-folder grid

| | **1_Shape** | **2_Patterns** | **3_Detail** |
|---|---|---|---|
| **setting/** | What kind of setting, and at what scale — how many regions, what span of world, what the party's altitude is | Content patterns for History events, Truths, Rumours, Bestiary entries, Factions, the five Treasure tables; and the criteria for the five registries (Lore, Keys, Named Creatures, Unique Treasures, Quests) | Voice and naming at setting level; `Language.md`'s seeding and growth rules; how tone is kept across artifacts written weeks apart |
| **region/** | Rating and die; whether this region is one site or a collection; how many locations and at what scale | Region Overview field patterns — what makes a good Features / Dangers / Creatures / Secrets / Treasure entry, and the d6 table per rating | Ambiance; the Terrain/Foraging/Layout texture the referee narrates *between* points (the point-crawl connective layer); region-level voice |
| **safe/** | Which kind of landmark, and its scale (a stall, a building, a whole village as one key) | The 11 categories from today's `Safe.md`, expanded into a wide match list; SAFE-flavoured selection for creature/treasure/trap/secret; **ongoing situations** (present tense, named cast, stated next rung) | SAFE dressing; the clue rules; how a settlement's features integrate into one place; SAFE voice |
| **wild/** | Landmark / Hidden / Secret, and Site / Connection / Natural Feature; scale of each | Today's three `Wild_*.md` bullet sets, widened; WILD-flavoured creature/treasure/trap/secret; the search cost and odds that make the three tiers procedural rather than nominal | WILD dressing; position-within-region; integration of a landmark with its hidden/secret children; WILD voice |
| **dangerous/** | Weight (low/medium/high) **and the ratio between them, currently stated nowhere**; scale of the region as a whole | Today's three `Dangerous_*.md` bullet sets, widened; room purposes as a match list with a non-repetition rule; traps **with a required visible tell**; puzzles; DANGEROUS creature/treasure/secret | DANGEROUS dressing and the detail-by-weight budget; how rooms read as one built work; DANGEROUS voice |

**Note on the registries.** `patterns/setting/2_Patterns.md` holds the *criteria* — what
makes a Key a Key rather than treasure, what earns a Named Creature a slot. Each rating's
`2_Patterns.md` holds *when to reach for one here*, in its own words. This is not a
`shared/` folder by the back door: the registries are setting-level artifacts, and
`setting/` is one of the five folders by D1.

---

## 4. Migration map

Every current file accounted for. Nothing is deleted without a destination.

| Current | Destination |
|---|---|
| `Safe.md` | Categories → `safe/1_Shape.md`; sub-questions → `safe/2_Patterns.md` |
| `Wild_Landmark.md` | Kinds (Site/Connection/Natural Feature) → `wild/1_Shape.md`; bullets → `wild/2_Patterns.md` |
| `Wild_Hidden.md`, `Wild_Secret.md` | Classification → `wild/1_Shape.md`; bullets + Clue/Trigger/Payload → `wild/2_Patterns.md` |
| `Dangerous_Low/Medium/High.md` | Weight definitions + new ratio → `dangerous/1_Shape.md`; bullets → `dangerous/2_Patterns.md` |
| `Dressing.md` | Splits three ways into `safe/`, `wild/`, `dangerous/` `3_Detail.md`. Detail-by-Weight → `dangerous/` only. Position-within-region → `wild/` only. **Units rule leaves patterns entirely** → `templates/Location.md` + `CLAUDE.md` |
| `Secrets.md` | Inclusion rate → each rating's `2_Patterns.md`; clue legibility → each rating's `3_Detail.md` |
| `Traps.md` | Restated three times, differentiated. Resolution tiers (Nuisance/Damaging/Lethal, TEST OF CONSTITUTION / TEST OF FATE, WOUND / CONDITION) are **format** → `templates/Location.md` |
| `Puzzles.md` | `dangerous/2_Patterns.md`. Phase 2 to determine whether a WILD variant is warranted |
| `Treasure.md`, `Creatures.md` | Selection guidance restated per rating in `2_Patterns.md` |
| `Lore.md`, `Keys.md`, `NamedCreatures.md`, `UniqueTreasures.md` | Criteria → `patterns/setting/2_Patterns.md`; reach-for-it guidance → each rating's `2_Patterns.md` |
| — | **New:** `patterns/setting/` and `patterns/region/` tiers have no current source and are written fresh |

**Path references to update:** 55 across 13 files — `CLAUDE.md` (16),
`templates/Location.md` (15), `STEPS.md` (4), `templates/Location_Gazetteer.md` (3), and
singles/pairs in the Region, Lore, Keys, NamedCreatures, UniqueTreasures and both
Judgement Check templates. `tools/validate_setting.py` does **not** reference `patterns/`
at all, so the validator and CI are untouched by the move itself.

---

## 5. New artifacts

### `setting/Quests.md` + `templates/Quests.md` (D6)

A fifth registry, following the existing four exactly: stub row at 4c, full entry at 4d.

What makes it different from the four: a Quest is **two-ended**. It has a giver location
and a target location, and both must exist. `Keys.md` is the precedent — "Every Key names
exactly what it unlocks and where" — and a Quest inherits that discipline: *every Quest
names who wants it, what specifically, and which location holds it.*

This is the mechanism that fixes the errand gap. Today `patterns/Safe.md`'s Task bullet
asks for "a specific, statable job" while `templates/Location.md`'s Context forbids the
model the setting files it would need to name a real target — so tasks point at invented,
unreachable nouns. A registry breaks that bind without widening the Context section: the
location cites `(Quest: [Name])`, and 4d resolves both ends with every referenced location
in view.

Validator extension: cross-check `(Quest: [Name])` citations against stub rows, same as
the four existing registries, plus a check that each Quest row names at least two
locations.

### `setting/Language.md` + `templates/Language.md` (D7)

Seeded with a small set of tongues and root words; **grown** as proper nouns are coined.
This is the framework's first living artifact — every other file is written once and
revisited only at 4d — and that property needs stating explicitly in `CLAUDE.md`, or it
will be treated as write-once and quietly stop matching the content.

Placement in the build order: it must precede `Setting.md`, since that artifact coins the
setting's own name. Proposed as a new **step 2a**, pushing today's 2a-2h down one.

Validator: no check initially. A "proper noun not found in Language.md" rule is
attractive but would fire constantly on legitimate coinages during early generation.
Revisit in Phase 3 once there is real content to measure against.

---

## 6. Template and validator relaxation (D8)

D5 means a single keyed location may legitimately be an entire village or dungeon.
Today's `templates/Location.md` shape — two-sentence Player Summary, one italic Referee
Notes line, flat Feature list, one Exits line — was written for a room, and the validator
enforces it. Phase 2 must establish whether that shape survives contact with a
village-scale location or needs to flex.

Audit list, to be answered with evidence in Phase 2 rather than guessed at now:

1. Does a village-scale location need sub-entries, or do Features carry it?
2. Is the two-sentence Player Summary cap right at every scale?
3. Does a whole-dungeon location's Exits line mean the dungeon's external exits only?
4. Which validator rules are load-bearing (they catch real breakage) versus merely tidy?

The standard from D8 is the deciding one: **consistent enough for the user to parse at a
glance, and no more.** A rule that only enforces neatness is a rule to drop.

---

## 7. `STEPS.md` and `CLAUDE.md` changes

- New step **2a**: create `setting/Language.md`, seeded. Renumber today's 2a-2h to 2b-2i.
- New step for `setting/Quests.md` alongside the four registry stubs (today's 2h).
- Every step's context list re-pointed at the three-tier files of its folder — a step now
  names one folder and reads its three files in order, instead of naming a scattered set.
- Steps 3a-3c gain `patterns/region/` in context (they currently have no pattern folder
  at all).
- Steps 2a-2i gain `patterns/setting/` for the same reason.
- 4c's context becomes: GENRE.md, parent Region Overview, own stub, and the three tier
  files of the matching rating folder.
- `CLAUDE.md`'s `patterns/` section is rewritten around the five folders and three tiers.
- `templates/Pattern_Judgement_Check.md` gains the inverted-duplication check from §2.

---

## 8. Phase 2 — trial fit against the corpus

The corpus is the test set. Phase 2 proves the tier structure before any pattern gets
written into it, and mines the corpus for Tier 2's horizontal variety.

**Test protocol.** Take a generated output from the corpus and route it backwards through
Shape → Patterns → Detail. If every sentence lands in exactly one tier, the structure
holds. If a sentence lands in none, there is a missing pattern. If one lands in two, the
tier boundary is wrong and moves.

**Test cases, chosen to stress different parts of the grid:**

| Case | Corpus source | What it stresses |
|---|---|---|
| A village | `village` | safe/ all three tiers; the roster question; ongoing situations |
| A dungeon room, empty | `interior room` + `empty dressing` | dangerous/3_Detail; whether low-weight rooms survive without a Tier 2 pick |
| A dungeon room, trapped | `trap` | dangerous/2_Patterns; the required-tell rule |
| A wilderness landmark | `grass landmark`, `hills landmark` | wild/ all three; position-within-region |
| **A lair** | `giant ant lair`, `witch cottage` | **D5 — the same lair routed at all three scales: one location, a cluster, a region** |
| A settlement event | `settlement event`, `the presence of mercenaries is a problem` | Whether ongoing situations fit safe/2_Patterns or need their own Shape |
| A quest chain | `alchemist job` + `giant ant queen chamber` | D6 two-endedness end to end |

**Acceptance criteria for Phase 2:**

1. All seven cases decompose cleanly into three tiers.
2. The lair case produces three legible, materially different outputs at three scales —
   this is the direct test of D5, and if it fails, D5 fails and a lair unit is back on
   the table.
3. Every Tier 2 file has enough breadth that two locations generated from it in the same
   region do not collide.
4. The four §6 relaxation questions are answered with a worked example, not an opinion.
5. Any trap, treasure or creature guidance that reads identically across two rating
   folders is either differentiated or shown to be format and moved to `templates/`.

---

## 9. Phase 3 — write and prove

Write the fifteen tier files, the two new templates, the two new setting artifacts, and
the updated `GENRE.md`, `STEPS.md`, `CLAUDE.md` and validator. Then generate from scratch,
repeatedly, and tweak.

**Proof criteria:**

- Multiple full from-scratch generations, not one.
- Two regions of the same rating generated independently must not converge — the
  non-repetition and forced-draw constraints are what Phase 2 sized, and this is where
  they get tested.
- `tools/validate_setting.py` at zero errors.
- All three judgement checks re-run, with `PatternJudgementCheck` specifically confirming
  that restatements across folders are genuinely differentiated (§2).
- Proper nouns across independently generated regions share a phonology traceable to
  `setting/Language.md`.

---

## 10. Open questions

Three forks I'd rather have answered than assume.

1. **Does `patterns/setting/` really need three tiers?** Region and the three ratings map
   onto Shape/Patterns/Detail naturally. Setting is the one where Tier 1 might be thin —
   "what kind of setting, at what scale" could reasonably be one paragraph rather than a
   file. I have planned for three for symmetry, on the argument that a predictable
   read-three-files-in-order rule is worth a short file. Worth confirming before I write
   fifteen rather than fourteen.

2. **How far does the validator relax?** §6 lists the audit but not the appetite. My
   default reading of D8 is aggressive: keep rules that catch real breakage (unknown
   codes, name mismatches, orphaned graph nodes, broken citations), drop rules that only
   enforce neatness (prose shape, sentence counts). Say if that is further than you want
   to go.

3. **Does `patterns/region/` cover the region gazetteer and the connection graphs, or
   only the Region Overview?** The gazetteer and `Connections.mmd` are arguably pure
   format and belong wholly to `templates/`. I have assumed region/ covers all three
   artifacts, with the graph's *shape* decisions (how densely to connect, when to use
   hidden edges) landing in `region/1_Shape.md` — since in a point crawl the connection
   graph is the map, and that is a design decision rather than a format one.
