# Pattern Restructure Plan

Phase 1 deliverable. Revised after the second design pass — tier renamed, `setting/`
detiered, shared mechanics relocated, feature budget opened up.

Supersedes the recommendation table in `analysis/HexDescribe_TableAnalysis.md` §6.

---

## 1. Decisions locked

| # | Decision | Consequence |
|---|---|---|
| D1 | `patterns/` splits into **five** folders: `setting/`, `region/`, `safe/`, `wild/`, `dangerous/` | Pattern guidance exists for every generation level, not just locations |
| D2 | Location and region folders carry **three tiers**: **Shape → Features → Detail** | A generation step reads three files from one folder, in order |
| D3 | **No `shared/` folder.** Restatement is deliberate | A trap in SAFE is a swindle; in WILD a snare; in DANGEROUS a deadfall. Writing them separately forces the differentiation |
| D4 | Voice lives in **two** places: an expanded `GENRE.md`, and the Detail tier of every folder | Setting-wide voice stated once; per-level application restated where applied |
| D5 | **No lair tier.** Scale is a Shape decision | A village or dungeon may be one keyed location, a cluster, or a region — all legal |
| D6 | Errands are **Quests**; a two-phase, two-ended registry | New `setting/Quests.md` + `templates/Quests.md` |
| D7 | Name coherence gets a living artifact, **seeded at 2h** | New `setting/Language.md`, seeded *from* the proper nouns already coined, then governing everything after |
| D8 | Templates relax to what the content needs, and no further | Consistent enough to parse at a glance; strictness beyond that is a defect |
| **D9** | **The classifications are a paradigm, not a rule.** low/medium/high and landmark/hidden/secret are convenient, not sacred | If content demands a fourth class or a binary, we change it. Phase 2 may return a different count and that is a success, not a breach |
| **D10** | **Feature budget scales with Shape.** No global one-pick lock | See §3 — the anti-mush guardrail moves from *count* to *coherence* |
| **D11** | Shared mechanics live in **`setting/Procedures.md`** | Trap resolution, search odds, time scale. Largely the same content even on a clean generation, so it seeds from defaults rather than generating cold |
| **D12** | `patterns/setting/` is **flat — no tiers** | Setting-level guidance is per-artifact, and the four existing registry pattern files move across intact |
| **D13** | Validator: **strict on format, relaxed on content and ratios** | Ratios and content judgements become warnings or judgement-check items, never CI errors |

### Corrections carried in from the analysis

- The framework is a **point crawl**. Connecting terrain is procedural, narrated from the
  Region's Terrain/Foraging/Layout fields. Withdrawn: "worked wilderness has no home" (it
  belongs in Terrain/Foraging) and micro-features-as-coordinates (region tier, not location).
- The corpus's value is **directing** output, not expanding it. Vocabulary lists are not a
  deliverable; constraints are — forced fresh draws, non-repetition within a region,
  causal attribution.

---

## 2. Target structure

```
patterns/
  setting/    Lore.md  Keys.md  NamedCreatures.md  UniqueTreasures.md  Quests.md
              Language.md  Procedures.md  Artifacts.md          (flat, per D12)
  region/     1_Shape.md   2_Features.md   3_Detail.md
  safe/       1_Shape.md   2_Features.md   3_Detail.md
  wild/       1_Shape.md   2_Features.md   3_Detail.md
  dangerous/  1_Shape.md   2_Features.md   3_Detail.md
```

Tier 2 is **Features**, not Patterns — no patterns inside patterns. The collision with
`templates/Location.md`'s `**Feature:**` output lines is deliberate and reads correctly:
`2_Features.md` is the file you read to write the Feature lines.

`patterns/setting/Artifacts.md` is the one new setting file — guidance for History,
Truths, Rumours, Bestiary, Factions and the Treasure tables, which today have no pattern
support at all. Split it later only if it gets unwieldy.

### The tier contract

**Tier 1 — Shape.** *What is this, how big, and how much goes in it?*
Three decisions, no content: which **kind** (a list, chosen from now — and per D9 that
list is revisable), at what **scale**, and with what **feature budget** (D10). Shape
classifies and sizes; it never describes.

**Tier 2 — Features.** *What's in it?*
The wide match list — the horizontal variety. Largest tier by volume, and what Phase 2
exists to fill. Also carries selection rules for creature, treasure, trap, puzzle, secret
and the registries, stated flat for this rating only, with no cross-rating branching in
view. Where a mechanic is genuinely shared, it cites `setting/Procedures.md` rather than
restating it (D11).

**Tier 3 — Detail.** *What is it like, and does it hold together?*
Three jobs in order: **round out** (dressing, ambiance, sensory and physical detail),
**integrate** (make the Tier 2 picks read as one place rather than a list — the job
nothing currently owns, and the real anti-mush guardrail under D10), and **refine the
verbiage** (this level's application of GENRE.md's voice). Clues live here, since a clue
is a detail made legible on purpose.

### What does *not* go in a pattern folder

**Format lives in `templates/`. Shared mechanics live in `setting/Procedures.md`.
Patterns hold only what varies by rating.**

Placement test: *does this change between SAFE and DANGEROUS?* If yes → pattern, written
three times, differently. If no → it is either format (`templates/`) or a mechanic
(`setting/Procedures.md`), written once.

This is what makes D3's duplication affordable. It also collapses an existing mess: the
units rule is stated three times today (`patterns/Dressing.md`, `templates/Location.md`,
`CLAUDE.md`) and drops to one.

### Managing the duplication risk

`checks/PatternJudgementCheck.md` already reviews `patterns/` for overlap. Its job
**inverts** — two restatements that read the same become a finding, not a convenience.
One new item in `templates/Pattern_Judgement_Check.md`.

---

## 3. The feature budget (D10)

One pick per generation is the current rule and it should not survive, for three reasons:

1. **It already contradicts our own weights.** `Dangerous_High.md` carries the bullet
   "combining multiple major features (creature, trap, and treasure together)" and
   `Location_Gazetteer.md` defines high weight as "one **or more** major features." The
   one-pick lock and the high-weight definition cannot both be true.
2. **D5 breaks it outright.** If a whole village is legally one keyed location, one
   feature pick is absurd.
3. **It is guarding the wrong thing.** What prevents a kitchen-sink location is not a low
   count — it is every element being attributable to the same Shape. A room with four
   features that all serve one purpose reads better than a room with one feature that
   serves none.

**So the budget moves into Shape**, alongside kind and scale, as a stated range rather
than a fixed number:

| Shape | Budget |
|---|---|
| DANGEROUS low | 0-1 |
| DANGEROUS medium | 1 |
| DANGEROUS high | 2-3 |
| WILD landmark / hidden / secret | 1-2 |
| SAFE, single-site | 1-2 |
| Any location realized at settlement or dungeon scale | many; governed by Shape's stated scale, not a cap |

The guardrail that replaces the count is Tier 3's **integrate** job: every feature must be
attributable to the same Shape, and Detail is where that gets enforced. Numbers above are
a starting position for Phase 2 to move.

---

## 4. Per-folder grid

| | **1_Shape** | **2_Features** | **3_Detail** |
|---|---|---|---|
| **region/** | Rating and die; one site or a collection; how many locations, at what scale; **connection density and when an edge is hidden** — in a point crawl the graph is the map, so that is a design call, not format | A paragraph per Region Overview field (13 fields) — what makes a good Features / Dangers / Creatures / Secrets / Treasure entry, and the d6 table per rating. **This is the big lift** | Ambiance; the Terrain / Foraging / Layout texture the referee narrates *between* points; region voice |
| **safe/** | Which kind of landmark; **what type of settlement this even is**; scale and budget | The 11 categories from today's `Safe.md`, widened; SAFE-flavoured creature/treasure/trap/secret; **ongoing situations** (present tense, named cast, stated next rung) | SAFE dressing; clue rules; integration of a settlement's features; SAFE voice |
| **wild/** | Landmark / Hidden / Secret × Site / Connection / Natural Feature; scale and budget | Today's three `Wild_*.md` sets, widened; WILD creature/treasure/trap/secret; search cost and odds cited from `Procedures.md` | WILD dressing; position-within-region; integration of a landmark with its hidden/secret children; WILD voice |
| **dangerous/** | Weight, and the ratio between weights (a **judgement-check** item, not a validator rule, per D13); scale and budget | Today's three `Dangerous_*.md` sets, widened; room purposes as a match list with a non-repetition rule; traps **with a required visible tell**; puzzles | DANGEROUS dressing and detail-by-weight; how rooms read as one built work; DANGEROUS voice |

---

## 5. Migration map

| Current | Destination |
|---|---|
| `Safe.md` | Categories → `safe/1_Shape.md`; sub-questions → `safe/2_Features.md` |
| `Wild_Landmark.md` | Site/Connection/Natural Feature → `wild/1_Shape.md`; bullets → `wild/2_Features.md` |
| `Wild_Hidden.md`, `Wild_Secret.md` | Classification → `wild/1_Shape.md`; bullets + Clue/Trigger/Payload → `wild/2_Features.md` |
| `Dangerous_Low/Medium/High.md` | Weights + ratio + budget → `dangerous/1_Shape.md`; bullets → `dangerous/2_Features.md` |
| `Dressing.md` | Splits three ways into `3_Detail.md`. Detail-by-Weight → `dangerous/` only. Position-within-region → `wild/` only. **Units rule → `templates/Location.md`** |
| `Secrets.md` | Inclusion rate → each rating's `2_Features.md`; clue legibility → each rating's `3_Detail.md` |
| `Traps.md` | Patterns restated three times, differentiated. **Resolution tiers → `setting/Procedures.md`** (D11) |
| `Puzzles.md` | `dangerous/2_Features.md`. Phase 2 decides whether a WILD variant is warranted |
| `Treasure.md`, `Creatures.md` | Selection restated per rating in `2_Features.md` |
| `Lore.md`, `Keys.md`, `NamedCreatures.md`, `UniqueTreasures.md` | **Move to `patterns/setting/` intact** (D12); per-rating reach-for-it guidance added to each `2_Features.md` |

**Path references to update:** 55 across 13 files — `CLAUDE.md` (16),
`templates/Location.md` (15), `STEPS.md` (4), `templates/Location_Gazetteer.md` (3), plus
singles and pairs elsewhere. `tools/validate_setting.py` does not reference `patterns/`,
so the move itself leaves CI untouched.

---

## 6. New setting artifacts

### `setting/Procedures.md` (D11)

The shared-mechanics home, and the corpus's `;procedures` block done properly. Holds:

- **Trap resolution** — Nuisance / Damaging / Lethal, TEST OF CONSTITUTION vs. TEST OF
  FATE, WOUND vs. CONDITION. Moved out of `patterns/Traps.md`.
- **Search odds and cost** — what it takes to find a Hidden or Secret location. This is
  the Finding 18 gap: our entire WILD tier system is about findability and nothing states
  the odds or the price of looking, so the tiers are nominal rather than procedural.
- **Time scale per rating** — currently buried in `templates/Region.md`'s Layout field.

Seeded from defaults rather than generated cold: the content is largely the same on a
clean generation, and a setting customizes rather than invents it. Must exist before
step 3, since Region Overviews cite it.

### `setting/Quests.md` + `templates/Quests.md` (D6)

A fifth registry: stub at 4c, full entry at 4d. What makes it different is that it is
**two-ended** — a giver location and a target location, both of which must exist. `Keys.md`
is the precedent ("every Key names exactly what it unlocks and where").

This breaks the bind that currently defeats errands: `Safe.md` asks for "a specific,
statable job" while `Location.md`'s Context denies the model the files it would need to
name a real target. A registry fixes it without widening Context — the location cites
`(Quest: [Name])`, and 4d resolves both ends with every referenced location in view.

### `setting/Language.md` + `templates/Language.md` (D7)

**Seeded at 2h, retroactively.** This is the important mechanic and it follows the same
shape as the other procedurally built tables: by 2h, steps 2a-2g have already coined
proper nouns across Setting, History, Truths, Rumours, Bestiary and Factions. 2h reads
what is already there and **systematizes the phonology already present** — extracting
tongues and root words from real coinages — rather than inventing a language cold and
forcing earlier artifacts to comply.

The setting's own name is therefore either plain common tongue, or itself a seed for what
follows. Either is fine.

It is the framework's first **living** artifact — appended to whenever a proper noun is
coined, where every other file is written once and revisited only at 4d. That property
needs stating in `CLAUDE.md` or it will be treated as write-once and quietly drift.

---

## 7. Validator posture (D13)

**Strict on format. Relaxed on content and ratios.**

| Keep as errors | Demote to warning | Move to judgement checks |
|---|---|---|
| Unknown region/location codes | Exit/edge mismatches already warned | Weight ratio across a region |
| Header ≠ filename ≠ gazetteer stub | — | Whether a Shape's budget was respected |
| Missing required lines and malformed syntax | — | Whether restatements across folders are differentiated |
| Orphaned graph nodes; broken citations | — | Prose quality, density, voice |
| Registry cross-references (incl. new Quests) | Quest rows naming fewer than two locations | — |

Sentence-count caps and prose-shape rules are neatness, not breakage — they go, per D8.
The §8 audit questions are answered with worked examples in Phase 2, not decided here.

---

## 8. `STEPS.md` and `CLAUDE.md` changes

- **No new steps.** 2h absorbs `Language.md`, `Procedures.md` and `Quests.md` alongside
  the four existing registry stubs. Numbering is untouched.
- Steps 2a-2i gain `patterns/setting/`; steps 3a-3c gain `patterns/region/` — neither
  level has any pattern support today.
- 4c's context becomes: `GENRE.md`, parent Region Overview, own stub, and the three tier
  files of the matching rating folder, read in order.
- `CLAUDE.md`'s `patterns/` section rewritten around five folders and three tiers.
- `templates/Pattern_Judgement_Check.md` gains the inverted-duplication check.
- `templates/Region.md` cites `Procedures.md` for time scale instead of stating it.

---

## 9. Phase 2 — trial fit against the corpus

The corpus is the test set. Phase 2 proves the tier structure before any pattern is
written into it, and mines the corpus for Tier 2's horizontal variety.

**Protocol.** Take a corpus output and route it backwards through Shape → Features →
Detail. Every sentence should land in exactly one tier. Landing in none means a missing
pattern; landing in two means the tier boundary is wrong and moves.

| Case | Corpus source | Stresses |
|---|---|---|
| Village | `village`, `town` | safe/ all tiers; the roster question; settlement-type Shape |
| Empty dungeon room | `interior room` + `empty dressing` | dangerous/3_Detail; whether a 0-budget room survives |
| Trapped room | `trap` | dangerous/2_Features; the required-tell rule |
| Wilderness landmark | `grass landmark`, `hills landmark` | wild/ all tiers; position-within-region |
| **Lair** | `witch cottage`, `giant ant lair` | **D5 and D10 — same lair at three scales** |
| Ongoing situation | `settlement event`, `the presence of mercenaries is a problem` | Whether these fit safe/2_Features or need their own Shape |
| Quest chain | `alchemist job` → `giant ant queen chamber` | D6 two-endedness end to end |

**Acceptance criteria:**

1. All seven cases decompose cleanly into three tiers.
2. The lair case produces three legible, materially different outputs at three scales.
   This is the direct falsifier for D5 — if it fails, a lair unit is back on the table.
3. Every Tier 2 file has enough breadth that two locations generated from it in the same
   region do not collide.
4. The §7 relaxation calls are backed by a worked example, not an opinion.
5. Any trap, treasure or creature guidance reading identically across two folders is
   either differentiated, or shown to be a mechanic and moved to `Procedures.md`.
6. **The classification counts are re-derived, not assumed** (D9). If the content wants
   four DANGEROUS weights or two WILD classes, Phase 2 says so.

---

## 10. Phase 3 — write and prove

Write the twelve tier files, the flat `setting/` files, the three new templates, the three
new setting artifacts, and the updated `GENRE.md`, `STEPS.md`, `CLAUDE.md` and validator.
Then generate from scratch, repeatedly, and tweak.

**Proof criteria:**

- Multiple full from-scratch generations, not one.
- Two regions of the same rating generated independently must not converge.
- `tools/validate_setting.py` at zero errors under the D13 posture.
- All three judgement checks re-run, with `PatternJudgementCheck` confirming
  cross-folder restatements are genuinely differentiated.
- Proper nouns across independently generated regions share a phonology traceable to
  `setting/Language.md`.

---

## 11. Scope posture

Remaining scope questions are Phase 2's to answer, empirically: **if we need it the answer
is yes, if we don't the answer is no.** Pragmatic over ideological. Nothing in this plan
is load-bearing enough to defend against evidence — D9 says so explicitly about the
classifications, and it applies to the rest.
