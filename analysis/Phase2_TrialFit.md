# Phase 2 - Corpus Trial Fit

Routing corpus outputs backwards through **Shape → Features → Detail** to prove the tier
structure before any pattern is written into it.

**Protocol.** Every element of a corpus output should land in exactly one tier. Landing in
none means a missing pattern. Landing in two means the tier boundary is wrong and moves.

**Status:** case 5 of 7 complete — run first because it is the D5 falsifier.

---

## Case 5 — The lair, at three scales

**Source:** `witch cottage` and its dependent tables (`witch`, `witch goal`, `witch
cottage door`, `witch cottage other entry`, `witch cottage main room`, `witch cottage
decoration`, `witch cottage cauldron`, `witch annex`, `witch attic`, `witch cellar`,
`witch prisoner`, `witch thrall`, `terror treasure`).

**Stresses:** D5 (scale is a Shape decision, no lair tier) and D10 (feature budget scales
with Shape).

### The corpus's raw material, decomposed

| Element | Corpus table | Proposed tier |
|---|---|---|
| Cottage exterior — gingerbread, chicken feet, hollowed mushroom, stone hut | `witch cottage` | **Detail** |
| Door — "Children welcome!", a door of smiling baby faces | `witch cottage door` | **Detail** |
| Second way in — chimney, window, thatched roof, or none | `witch cottage other entry` | **contested — see F1** |
| The witch, named, with a standing goal | `witch`, `witch goal` | **Features** (→ Named Creature) |
| Cauldron with body parts surfacing | `witch cottage cauldron` | **Features** |
| Room decoration — ceiling / shelf / table | `witch cottage decoration` | **Detail** |
| Attic item — curse chest, caged lover, skull mobile, demon altar, guard broom | `witch attic` | **Features** (→ Unique Treasure or Named Creature) |
| Cellar item — cursed apples, mirror of entrapment, spinning wheel, terrible oven | `witch cellar` | **Features** (→ Unique Treasure) |
| Prisoner in a hanging cage | `witch prisoner` | **Features** |
| Thrall cleaning the shelves, leashed to an iron ring | `witch thrall` | **Features** |
| Vertical annex — ladder up, stairs down | `witch annex` | **Shape** (it is a space count, not a description) |
| Treasure | `terror treasure` | **Features** |

Twelve elements. Ten land cleanly in one tier. One lands in two (F1). One reveals a
missing Shape decision (F2).

### Scale A — one keyed location

`B.4 **Hessa's Rookery** (high) - *thatch, lye, appetite*`

**Shape:** kind = inhabited lair; scale = compound site, one key; budget = compound (see
F2). **Features:** the witch (Named Creature), the cauldron, one attic item, one cellar
item, the prisoner, the thrall, treasure. Attic and cellar become Feature lines that state
their own access — "a rickety ladder in the north corner climbs to a low attic where…".
**Detail:** exterior, door, decoration; integration binds all of it to the witch's goal.

**Result: works.** The existing Location template carries it without modification —
Features already permit nested access, and `templates/Location.md`'s rule that
trigger-gated access lives in a Feature rather than Exits does the right thing here
unprompted.

### Scale B — a cluster of keyed locations

```
B.4 Hessa's Rookery (high)      - the main room, cauldron, thrall
B.5 The Low Attic (medium)      - one attic item, reached from B.4
B.6 The Sweet Cellar (medium)   - one cellar item, reached from B.4
```

**Shape:** three locations, one owner; B.5 and B.6 are dependents of B.4. **Features:**
budget of 2-3 at B.4, 1 each at B.5/B.6 — the corpus's own single-item attic and cellar
tables fall straight into a medium-weight budget. **Detail:** each gets its own dressing;
integration now works *across* the three, which is the harder version of the job.

**Result: works, and it is the best fit of the three.** The corpus's own structure — one
main room plus optional annexes, each holding exactly one significant thing — is already
shaped like a weighted cluster. Worth noting the annexes are `witch annex`, an *optional*
table: the cottage may have an attic, a cellar, or neither. That is Shape choosing a
location count, which is exactly what D5 claims Shape does.

### Scale C — a whole region

`D Hessa's Holding - DANGEROUS, d4, *thatch, lye, appetite*`

**Result: works, but breaks a different rule — see F3.** Decomposing further (approach
path, garden, main room, hearth, attic, cellar, the thing under the floor) yields five to
seven locations. `templates/Location_Gazetteer.md` requires a DANGEROUS region to hold
"about 3 times" its die — twelve for a d4. The cottage does not contain twelve rooms and
padding it to twelve would produce exactly the filler the weight system exists to avoid.

### Verdict on D5

**D5 survives.** All three scales produce legible, materially different outputs from the
same source, and the difference between them is entirely a Shape decision — kind and
budget stay constant, only scale moves. No lair tier is needed.

**D10 survives and is confirmed by evidence.** Scale A needs seven features in one key.
Under the old one-pick lock it would have been illegal; under a fixed high-weight budget
of 2-3 it would still have been illegal. The budget has to scale with Shape, exactly as
D10 claims.

---

## Findings

### F1 — Access is contested between Features and Detail

`witch cottage other entry` (a chimney, a window big enough to smash, a cuttable thatched
roof, or nothing) is simultaneously dressing on the building and a tactical alternative
that changes how the location plays. Under the current tier contract it has a claim on
both, which by protocol means the boundary is wrong.

**Proposed rule:** *the existence of a route is a Features decision; its description is
Detail.* Whether there is a second way in changes what players can do, so Features owns
it; whether that way in is a chimney or a rotten shutter is dressing, so Detail owns it.

This generalizes past this case — it is the same cut for a secret door, a collapsed wall,
or a window — and should go into the tier contract in §2 of the plan rather than into any
one rating folder.

### F2 — The budget table needs a compound-site band

The plan's §3 budget table jumps from "SAFE single-site / WILD landmark: 1-2" and
"DANGEROUS high: 2-3" straight to "settlement or dungeon scale: many." Scale A sits in the
gap: one key, seven features, and plainly not a settlement.

**Proposed band:** **compound site — 4-8.** A single key holding a whole small lair: a
cottage, a tower, a barrow, a camp. Below settlement scale, above a room.

This band is also what makes Scale A and Scale B genuinely different choices rather than
one being a workaround for the other's cap.

### F3 — The 3× die rule fights region-scale lairs

`Location_Gazetteer.md`'s "about 3 times the die type" is a good default for a dungeon and
a bad one for a lair-as-region. A d4 lair region wants five to seven locations, not twelve.

**Options, for decision:**

1. Make the count a **range tied to Shape** rather than a multiplier — Shape already sets
   scale, so it can set count, and the multiplier becomes the default for the "collection
   of rooms" kind only.
2. Keep 3× and let a lair region carry a smaller die. Rejected on inspection: the die also
   drives encounter danger, and a witch's holding is not less dangerous for being small.
3. Exempt lair-kind regions explicitly. Rejected as a special case where option 1 is a
   general rule.

**Recommendation: option 1.** It follows from D5 — if Shape owns scale, Shape owns count,
and a fixed multiplier in the gazetteer template is a scale decision living in the wrong
file. Per D13 this is a ratio, so it is judgement-check material rather than a validator
rule either way.

### F4 — Deferred motivation is a real difference from the corpus

The corpus writes the witch's goal inline ("stealing children and raising them as her
own"). We cite `(Named Creature: Hessa)` at 4c and write the motivation at 4d. Not a
defect — 4d resolves it with every referencing location in view, which the corpus cannot
do — but it means a location file is *not readable as a complete scene* until 4d
completes. Worth stating in `templates/Location.md` so the gap reads as intentional.

---

## Plan amendments arising

| Finding | Amendment | Target |
|---|---|---|
| F1 | Add the route-existence vs. route-description cut to the tier contract | Plan §2 |
| F2 | Add the **compound site: 4-8** band | Plan §3 |
| F3 | Location count becomes a Shape-set range; 3× survives as the default for collection-kind regions only | Plan §4, `Location_Gazetteer.md` |
| F4 | State that a location file completes at 4d, by design | `templates/Location.md` |

No amendment touches D1-D13. The structure held; three of its numbers moved.

---

## Remaining cases

| Case | Status |
|---|---|
| 1 Village | pending |
| 2 Empty dungeon room | pending |
| 3 Trapped room | pending |
| 4 Wilderness landmark | pending |
| **5 Lair** | **complete — D5 and D10 confirmed** |
| 6 Ongoing situation | pending |
| 7 Quest chain | pending |
