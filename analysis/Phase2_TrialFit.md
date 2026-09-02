# Phase 2 - Corpus Trial Fit

Routing corpus outputs backwards through **Weight/Classification/Kind/Scope → Features →
Dressing** to prove the structure before any pattern is written into it.

**Protocol.** Every element should land in exactly one file. None means a missing pattern.
Two means the boundary is wrong and moves.

**Complete:** cases 5, 1, 6. **Pending:** 2, 3, 4, 7.

---

## Case 5 — The lair, at three scales

**Source:** `witch cottage` and dependents. **Stresses:** D5, D10.

### Decomposition

| Element | Corpus table | File |
|---|---|---|
| Cottage exterior — gingerbread, chicken feet, hollowed mushroom | `witch cottage` | Dressing |
| Door — "Children welcome!", a door of smiling baby faces | `witch cottage door` | Dressing |
| Second way in — chimney, window, thatch | `witch cottage other entry` | **both, legitimately — F1** |
| The witch, named, with a standing goal | `witch`, `witch goal` | Features → Named Creature |
| Cauldron with body parts surfacing | `witch cottage cauldron` | Features |
| Room decoration — ceiling / shelf / table | `witch cottage decoration` | Dressing |
| Attic item — curse chest, caged lover, demon altar, guard broom | `witch attic` | Features → Unique Treasure |
| Cellar item — cursed apples, mirror of entrapment, terrible oven | `witch cellar` | Features → Unique Treasure |
| Prisoner in a hanging cage; thrall leashed to a ring | `witch prisoner`, `witch thrall` | Features |
| Vertical annex — ladder up, stairs down | `witch annex` | Kind/Weight (a space count, not a description) |
| Treasure | `terror treasure` | Features |

### The three scales

**A — one key.** `B.4 Hessa's Rookery (high)`. Attic and cellar become Feature lines
stating their own access. Seven features in one key. **Works** — the existing template
carries it unmodified, and its rule that trigger-gated access lives in a Feature rather
than Exits does the right thing unprompted.

**B — a cluster.** `B.4 Hessa's Rookery (high)` + `B.5 The Low Attic (medium)` + `B.6 The
Sweet Cellar (medium)`. **Works, and fits best** — the corpus's own structure is one main
room plus *optional* annexes each holding exactly one significant thing, which is already
shaped like a weighted cluster. That optionality is Shape choosing a location count.

**C — a region.** `D Hessa's Holding - DANGEROUS, d4`. **Works, but broke a different
rule** — see F3.

### Verdict

**D5 survives.** All three scales produce legible, materially different outputs from one
source, and only scale moves between them. No lair tier needed.

**D10 survives.** Scale A needs seven features in one key — illegal under the old one-pick
lock, and still illegal under a fixed high-weight cap of 2-3.

---

## Case 1 — Village and town

**Source:** `village`, `town`, `human houses`, `human companions`, `human defense`,
`village building`, `human leader`, `human friends`, `And a secret society`, `law and
order jobs`, `town feature`, `local smith`. **Stresses:** SAFE all three files; the roster
question; D10's prominence-over-scale claim.

### Decomposition

| Element | File |
|---|---|
| Population, settlement type | Kind |
| Whether the manor/tower/temple is its own key or a Feature of the village key | Kind (scale) |
| `human houses` — thatched huts, longhouses, mud huts | Dressing |
| `human defense` — ditch, palisade, river | **either, legitimately — F1.** A palisade that gates entry is a Feature; one that is just what the place looks like is Dressing |
| `human companions` — war dogs, sharpened stakes | Features |
| `human leader` + level + spellbook + treasure | Features → Named Creature, Treasure |
| `human friends`, `human retainer` — aides | Features |
| `And a secret society` — a named faction's local contact | Features |
| `law and order jobs` — "500gp to whoever brings back [nearby wanted]" | Features → **Quest** (textbook two-ended: giver here, target elsewhere) |
| `patron plot hook` — the patron's missing book, taken by `[nearby book thief]` | Features → **Quest** |
| `local smith` + inventory | Features |
| `town feature` — a gallows with eight hanged; a chained troll; an alchemist | Features |
| `settlement event` | see Case 6 |

**Result: decomposes cleanly.** Two contested elements, both resolved by F1's rule rather
than being boundary failures.

### D10 confirmed, and a place we beat the corpus

The corpus has **no way to make a town brief.** Every `town` pull emits the full 15-slot
tradesperson roster, the inner-bailey officer list, and the d10/d6 allegiance procedure —
whether the town is the campaign's hub or somewhere the party walks through on the way
elsewhere. Scale drives budget, and there is no lever to say "this one doesn't matter."

Prominence-driven budget is the lever. A d6 SAFE region can hold two prominent landmarks
and four liner notes, and a large town in a region that isn't about the town can be one
paragraph doing exactly what everyone expects a town to do. **This is a case where the
plan's approach is better than the source's, and it is worth stating in `safe/Kind.md`
directly** — the instruction is not "describe the settlement" but "decide first how much
this one matters."

### F5 — the roster belongs at region level

The corpus's town roster is fifteen optional slots, and the interesting information is
which slots are *empty*. That cannot be fifteen locations: a d6 SAFE region holds about
six, and inflating it would bury the two that matter.

`templates/Region.md`'s SAFE-only **People** field is the natural home and does not
currently do this job — it asks for customs, government, temperament and reaction to
outsiders, but never *who is here*. A settlement's roster is region-level fact; individual
landmarks draw from it and give a few of those people a scene.

**Proposed:** `region/Features.md` includes roster guidance for the People field — trades
present, trades conspicuously absent, and who holds standing — and `safe/Features.md`
draws from it rather than reinventing a cast per landmark.

---

## Case 6 — The ongoing situation

**Source:** `settlement event` → `war event` → `the presence of mercenaries is a problem`
(six escalation rungs), plus `disaster event`, `harvest event`, `holiday event`.
**Stresses:** whether these fit `safe/Features.md` or need their own Kind.

### Decomposition

| Element | File |
|---|---|
| That a situation is currently running at all | **region — F6** |
| Which situation (mercenaries / refugees / plague / festival) | region |
| Which rung of the escalation ladder it is on | Features |
| The named captain; the named dead or conscripted | Features → Named Creature |
| Tents outside the walls; drunk soldiers; parents weeping at the captain's tent | Dressing |
| What the party can be pulled into | Features |

### F6 — situations are region-scoped, not location-scoped

Mercenaries camped outside the settlement affect *every* landmark in the region: the inn
is full of them, the smith is working for them, the market has been stripped. Attaching
the situation to one location would make the other five read as though nothing were
happening.

So the answer to the plan's open question is **neither** — a situation is not a SAFE Kind
and not purely a Feature. It is a **region-level standing state, expressed locally at
Features.**

`templates/Region.md`'s SAFE d6 **Events** table is the nearest existing thing and is not
it: a random table rolled on entry is a *possible* event, not a current one. The Region
Overview needs a field for what is happening right now — and per GENRE.md that is a
standing situation with a visible trajectory, not an authored plot: it is true whether or
not the party engages, and it moves on its own.

**Proposed:** a **Situation** field in the Region Overview (SAFE and WILD; DANGEROUS runs
on its Danger countdown instead), with `region/Features.md` supplying the escalation-rung
discipline — name who is responsible, name who is affected, state which rung it is on now,
and state what the next rung looks like. That last clause is the corpus's real trick and
the thing `patterns/Safe.md`'s Tension bullet asks for without any mechanism.

---

## Findings

### F1 — Access: resolved, and the rule generalizes

*Superseded by the design pass.* The earlier reading — "existence is Features, description
is Dressing" — was too narrow. Both directions are legitimate:

- Features declares an egress → Dressing calls it a ladder.
- Features declares an empty room → Dressing puts a ladder there as dressing.

**The rule is: Features owns anything that changes what players can do; Dressing owns
everything else and may originate it freely.** The test is not which file mentions the
ladder — it is whether the ladder does anything. Folded into the plan's §2.

### F2 — Budget: resolved, correlation dropped

*Superseded.* The proposed "compound site: 4-8" band assumed size drives budget. It does
not. A single site may carry five features because it is doing real work; a settlement may
carry one because it is only there to be a settlement. **Budget is prominence, scale is an
outer bound of plausibility only.** Folded into the plan's §3, along with the open
question of whether SAFE and WILD need an explicit prominence axis the way DANGEROUS
already has one in its weights.

### F3 — The 3× die rule fights region-scale lairs

A d4 lair region wants five to seven locations; `Location_Gazetteer.md` demands twelve, and
padding to twelve produces exactly the filler weights exist to prevent. **Accepted:** the
count becomes a Shape-set range, with 3× surviving as the default for collection-kind
regions only.

### F4 — Container and data

The corpus writes the witch's goal inline; we cite `(Named Creature: Hessa)` at 4c and
write the motivation at 4d. **Intentional**, and now D14: the location file is a container
that cites, the registries hold the data, and consistency comes from keeping them apart.
Needs stating in `templates/Location.md` so the gap reads as designed rather than missing.

### F5 — The settlement roster belongs in the Region Overview's People field

New, from Case 1. See above.

### F6 — Ongoing situations are region-scoped

New, from Case 6. Proposes a **Situation** field in the Region Overview. See above.

---

## Plan amendments arising

| Finding | Amendment | Target | Status |
|---|---|---|---|
| F1 | Features owns what does something; Dressing owns the rest and may originate it | Plan §2 | folded in |
| F2 | Budget from prominence, not scale; prominence-axis question left open | Plan §3 | folded in |
| F3 | Count becomes a Shape-set range | Plan §8, `Location_Gazetteer.md` | folded in |
| F4 | Container/data split stated | D14, `templates/Location.md` | folded in |
| F5 | Roster guidance into the People field | `region/Features.md`, `templates/Region.md` | **new** |
| F6 | **Situation** field in the Region Overview | `templates/Region.md`, `region/Features.md` | **new** |

Still no amendment touches D1-D14. Three cases have moved numbers and added two Region
Overview fields; the structure itself has held.

**Note on F5 and F6 together:** both say the same thing from different directions — the
SAFE Region Overview is underspecified. It describes a place but not who is in it or what
is currently happening to it. That is the largest single gap the trial fit has surfaced so
far, and it is a `region/` problem, not a `safe/` one.
