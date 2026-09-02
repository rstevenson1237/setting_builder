# Pattern Restructure Plan

Phase 1 deliverable. Revised through three design passes.

Supersedes the recommendation table in `analysis/HexDescribe_TableAnalysis.md` §6.

---

## 1. Decisions locked

| # | Decision | Consequence |
|---|---|---|
| D1 | `patterns/` splits into **five** folders: `setting/`, `region/`, `safe/`, `wild/`, `dangerous/` | Pattern guidance exists for every generation level, not just locations |
| D2 | Location and region folders hold **three files**, named for what they are and do — **no numbering, no shared "tier" name for the first one** | See §2. `high/medium/low` is not `landmark/hidden/secret`; forcing them into a common label buys nothing |
| D3 | **No `shared/` folder.** Restatement is deliberate | A trap in SAFE is a swindle; in WILD a snare; in DANGEROUS a deadfall |
| D4 | Voice lives in **two** places: an expanded `GENRE.md`, and the Dressing file of every folder | Setting-wide voice once; per-level application where applied |
| D5 | **No lair tier.** Scale is a Shape decision | A village or dungeon may be one keyed location, a cluster, or a region — all legal. **Confirmed by trial fit** |
| D6 | Errands are **Quests**; a two-phase, two-ended registry | New `setting/Quests.md` + `templates/Quests.md` |
| D7 | `Language.md` and `Procedures.md` have a **three-stage lifecycle**: seeded at step 1, fleshed out at 2h, grown at 4d | See §6. The seed is generic scaffolding; the flesh-out is setting-specific; the growth is continuous |
| D8 | Templates relax to what the content needs, and no further | Strictness beyond parseability is a defect |
| D9 | **The classifications are a paradigm, not a rule** | If content demands a fourth class or a binary, we change it |
| D10 | **Feature budget is set by prominence, not scale** | See §3. A small site can be dense; a large settlement can be a liner note |
| D11 | Shared mechanics live in **`setting/Procedures.md`** | Trap resolution, search odds, time scale |
| D12 | `patterns/setting/` is **flat** | Per-artifact; the four existing registry pattern files move across intact |
| D13 | Validator: **strict on format, relaxed on content and ratios** | Ratios and content become warnings or judgement-check items, never CI errors |
| **D14** | **Container and data are separate.** A location file is a container that cites; the registries hold the data | Explains 4c/4d, and why a Treasure citation never names the item. Consistency comes from the split |

### Corrections carried in from the analysis

- The framework is a **point crawl**. Connecting terrain is procedural, narrated from the
  Region's Terrain/Foraging/Layout fields.
- The corpus's value is **directing** output, not expanding it. Vocabulary lists are not a
  deliverable; constraints are.

---

## 2. Target structure

```
patterns/
  setting/     Lore.md  Keys.md  NamedCreatures.md  UniqueTreasures.md  Quests.md
               Language.md  Procedures.md  Artifacts.md          (flat, per D12)
  region/      Scope.md            Features.md  Dressing.md
  safe/        Kind.md             Features.md  Dressing.md
  wild/        Classification.md   Features.md  Dressing.md
  dangerous/   Weight.md           Features.md  Dressing.md
```

**On the names (D2).** The first file in each folder is named for the thing it actually
decides, because those things are genuinely different: DANGEROUS decides **weight**, WILD
decides **classification**, SAFE decides **kind**, region decides **scope**. Numbering
them `1_` and calling them all "Shape" would assert a similarity that isn't there. Read
order lives in `templates/Location.md`'s Context section, where every other ordering in
this framework already lives.

The second and third files keep one name across folders because they *are* the same job
everywhere: `Features.md` is what it is, `Dressing.md` is what it does.

`patterns/setting/Artifacts.md` is the one wholly new file — guidance for History, Truths,
Rumours, Bestiary, Factions and the Treasure tables, which have no pattern support today.

### What each file does

**Weight / Classification / Kind / Scope.** Decides, and never describes: which class
this is, at what **scale** it is realized, and with what **prominence** (which sets the
feature budget, per D10). Scale is what makes D5 work — the same lair is legal as one key,
a cluster, or a region.

**Features.** The wide match list — the horizontal variety, and the largest file by
volume. Also carries selection rules for creature, treasure, trap, puzzle, secret and the
registries, stated flat for this rating only. Where a mechanic is genuinely shared it
cites `setting/Procedures.md` rather than restating it.

**Dressing.** Three jobs in order: **round out** (ambiance, sensory and physical detail),
**integrate** (make the picks read as one place — the real anti-mush guardrail under D10),
and **refine the verbiage** (this level's application of GENRE.md's voice). Clues live
here; a clue is a detail made legible on purpose.

**Dressing may originate content.** It is not merely subordinate to Features. Features
owns anything that changes what players can do; Dressing owns everything else and may
introduce it freely. Both of these are correct and neither is a boundary violation:

- Features declares an egress → Dressing calls it a ladder.
- Features declares an empty room → Dressing puts a ladder there as dressing.

The test is never which file mentions the ladder. It is whether the ladder *does*
anything.

### What does not go in a pattern folder

**Format lives in `templates/`. Shared mechanics live in `setting/Procedures.md`.
Patterns hold only what varies by rating.**

Placement test: *does this change between SAFE and DANGEROUS?* If yes → pattern, written
three times, differently. If no → format or mechanic, written once. This is what makes
D3's duplication affordable, and it collapses an existing mess: the units rule is stated
three times today and drops to one.

`checks/PatternJudgementCheck.md`'s job **inverts** — two restatements that read the same
become a finding, not a convenience.

---

## 3. The feature budget (D10)

One pick per generation does not survive. It contradicts our own definitions
(`Dangerous_High.md` already has a "combining multiple major features" bullet;
`Location_Gazetteer.md` already says high weight is "one **or more**"), D5 breaks it
outright, and it guards the wrong thing — what prevents a kitchen-sink location is every
element being attributable to the same Shape, not a low count.

**Budget is driven by prominence, and is independent of scale.** A single site may carry
five features because it is doing real work in the campaign; a whole settlement may carry
one because it is only there to do what everyone expects a settlement to do. Both are
correct, and the variance between them is the point.

So the first file in each folder states a budget per location, guided by prominence.
Scale sets only an outer bound of plausibility, never the number.

**Open structural question for Phase 2.** DANGEROUS already has an explicit prominence
axis — that is exactly what low/medium/high is. SAFE and WILD do not: WILD's
landmark/hidden/secret is a *discoverability* axis, not a prominence one, and SAFE has
neither. Either SAFE and WILD gain an explicit prominence axis, or prominence stays a
per-location judgement stated at Shape time. Phase 2 decides on evidence; do not add
machinery before it earns its place.

---

## 4. Per-folder grid

| | **Weight / Classification / Kind / Scope** | **Features** | **Dressing** |
|---|---|---|---|
| **region/** | Rating and die; one site or a collection; location count as a Shape-set range; **connection density and when an edge is hidden** — in a point crawl the graph is the map | A paragraph per Region Overview field (13 fields), and the d6 table per rating. **The big lift** | Ambiance; the Terrain / Foraging / Layout texture narrated *between* points; region voice |
| **safe/** | Which kind of landmark; what type of settlement is even under discussion; scale and prominence | The 11 categories from today's `Safe.md`, widened; SAFE creature/treasure/trap/secret; **ongoing situations** | SAFE dressing; clue rules; settlement integration; SAFE voice |
| **wild/** | Landmark / Hidden / Secret × Site / Connection / Natural Feature; scale and prominence | Today's three `Wild_*.md` sets, widened; WILD creature/treasure/trap/secret; search cost cited from `Procedures.md` | WILD dressing; position-within-region; integration of a landmark with its children; WILD voice |
| **dangerous/** | Weight, and the ratio between weights (judgement-check material, not a validator rule) | Today's three `Dangerous_*.md` sets, widened; room purposes with a non-repetition rule; traps **with a required visible tell**; puzzles | DANGEROUS dressing and detail-by-weight; rooms reading as one built work; DANGEROUS voice |

---

## 5. Migration map

| Current | Destination |
|---|---|
| `Safe.md` | Categories → `safe/Kind.md`; sub-questions → `safe/Features.md` |
| `Wild_Landmark.md` | Site/Connection/Natural Feature → `wild/Classification.md`; bullets → `wild/Features.md` |
| `Wild_Hidden.md`, `Wild_Secret.md` | Classification → `wild/Classification.md`; bullets + Clue/Trigger/Payload → `wild/Features.md` |
| `Dangerous_Low/Medium/High.md` | Weights + budget → `dangerous/Weight.md`; bullets → `dangerous/Features.md` |
| `Dressing.md` | Splits three ways into each folder's `Dressing.md`. Detail-by-weight → `dangerous/` only. Position-within-region → `wild/` only. **Units rule → `templates/Location.md`** |
| `Secrets.md` | Inclusion rate → each `Features.md`; clue legibility → each `Dressing.md` |
| `Traps.md` | Patterns restated three times, differentiated. **Resolution tiers → `setting/Procedures.md`** |
| `Puzzles.md` | `dangerous/Features.md`. Phase 2 decides whether a WILD variant is warranted |
| `Treasure.md`, `Creatures.md` | Selection restated per rating in `Features.md` |
| `Lore.md`, `Keys.md`, `NamedCreatures.md`, `UniqueTreasures.md` | **Move to `patterns/setting/` intact**; per-rating reach-for-it guidance added to each `Features.md` |

**Path references to update:** 55 across 13 files — `CLAUDE.md` (16),
`templates/Location.md` (15), `STEPS.md` (4), `templates/Location_Gazetteer.md` (3), plus
singles and pairs elsewhere. `tools/validate_setting.py` does not reference `patterns/`.

---

## 6. New setting artifacts

### Lifecycle (D7)

`Procedures.md` and `Language.md` are both **seeded, fleshed out, then grown** — the same
shape as the other procedurally built tables:

| Stage | Step | What happens |
|---|---|---|
| **Seed** | **1b / 1c** (framework) | Base-level content. Procedures gets working default procedures; Language gets a few tongues and a starter root set — enough that the setting name and every coinage from 2a onward has something to draw on |
| **Flesh out** | **2h** | Tailored to this setting, now that Setting/History/Truths/Factions exist |
| **Grow** | **4d** | Language gains every proper noun coined during generation; Procedures gains anything the content turned out to need |

Seeding at step 1 rather than 2a is what makes the language generative rather than
retrofitted: names coined at 2a-2g draw from real roots instead of being systematized
after the fact.

### `setting/Procedures.md` (D11)

The shared-mechanics home, and the corpus's `;procedures` block done properly:

- **Trap resolution** — Nuisance / Damaging / Lethal, TEST OF CONSTITUTION vs. TEST OF
  FATE, WOUND vs. CONDITION. Moved out of `patterns/Traps.md`.
- **Search odds and cost** — what it takes to find a Hidden or Secret location. Our whole
  WILD tier system is about findability and nothing today states the price of looking, so
  the tiers are nominal rather than procedural.
- **Time scale per rating** — currently buried in `templates/Region.md`'s Layout field.

### `setting/Quests.md` + `templates/Quests.md` (D6)

A fifth registry: stub at 4c, full entry at 4d. **Two-ended** — a giver location and a
target location, both of which must exist. `Keys.md` is the precedent.

This breaks the bind that defeats errands today: `Safe.md` asks for "a specific, statable
job" while `Location.md`'s Context denies the model the files it would need to name a real
target. A registry fixes it without widening Context — per D14, the location is a
container citing `(Quest: [Name])`, and 4d fills in the data with every referencing
location in view.

### `setting/Language.md` + `templates/Language.md` (D7)

The framework's first **living** artifact — appended to whenever a proper noun is coined,
where every other file is written once and revisited only at 4d. That property needs
stating in `CLAUDE.md` or it will be treated as write-once and quietly drift.

---

## 7. Validator posture (D13)

**Strict on format. Relaxed on content and ratios.**

| Keep as errors | Move to judgement checks |
|---|---|
| Unknown region/location codes | Weight ratio across a region |
| Header ≠ filename ≠ gazetteer stub | Whether a stated budget was respected |
| Missing required lines, malformed syntax | Whether cross-folder restatements are differentiated |
| Orphaned graph nodes; broken citations | Prose quality, density, voice |
| Registry cross-references, including Quests | — |

Sentence-count caps and prose-shape rules are neatness, not breakage — they go, per D8.

---

## 8. `STEPS.md` and `CLAUDE.md` changes

- **New steps 1b and 1c**: seed `setting/Procedures.md` and `setting/Language.md`.
  Step 1 becomes framework establishment proper — genre, procedures, language.
- **2h** absorbs the flesh-out of both, plus `Quests.md` alongside the four registry
  stubs. Steps 2a-2g are untouched.
- **4d** gains the growth pass for `Language.md`.
- Steps 2a-2i gain `patterns/setting/`; steps 3a-3c gain `patterns/region/`.
- 4c's context becomes: `GENRE.md`, parent Region Overview, own stub, and the three files
  of the matching rating folder, read in order.
- `CLAUDE.md`'s `patterns/` section rewritten around the five folders; D14's
  container/data split stated explicitly.
- `templates/Pattern_Judgement_Check.md` gains the inverted-duplication check.
- `templates/Region.md` cites `Procedures.md` for time scale instead of stating it.
- `templates/Location_Gazetteer.md`'s 3× rule becomes a Shape-set range, with 3×
  surviving as the default for collection-kind regions only.

---

## 9. Phase 2 — trial fit against the corpus

Route a corpus output backwards through the three files. Every element should land in
exactly one. None means a missing pattern; two means the boundary is wrong and moves.

Progress and findings: `analysis/Phase2_TrialFit.md`.

| Case | Status |
|---|---|
| 1 Village / town | complete |
| 2 Empty dungeon room | pending |
| 3 Trapped room | pending |
| 4 Wilderness landmark | pending |
| 5 Lair at three scales | complete — D5 and D10 confirmed |
| 6 Ongoing situation | complete |
| 7 Quest chain | pending |

**Acceptance criteria:**

1. All seven cases decompose cleanly.
2. The lair case produces three legible, materially different outputs. *(met)*
3. Every `Features.md` has enough breadth that two locations in one region do not collide.
4. The §7 relaxation calls are backed by a worked example.
5. Any guidance reading identically across two folders is differentiated or moved.
6. **The classification counts are re-derived, not assumed** (D9).

---

## 10. Phase 3 — write and prove

Write the twelve rating/region files, the flat `setting/` files, the new templates and
setting artifacts, and the updated `GENRE.md`, `STEPS.md`, `CLAUDE.md` and validator.
Then generate from scratch, repeatedly, and tweak.

**Proof criteria:**

- Multiple full from-scratch generations, not one.
- Two regions of the same rating generated independently must not converge.
- `tools/validate_setting.py` at zero errors under the D13 posture.
- All three judgement checks re-run.
- Proper nouns across independently generated regions share a phonology traceable to
  `setting/Language.md`.

---

## 11. Scope posture

Remaining scope questions are Phase 2's, answered empirically: **if we need it the answer
is yes, if we don't the answer is no.** Nothing here is load-bearing enough to defend
against evidence.
