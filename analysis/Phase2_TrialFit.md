# Phase 2 - Corpus Trial Fit

Routing corpus outputs backwards through **Weight/Classification/Kind/Scope → Features →
Dressing** to prove the structure before any pattern is written into it.

**Protocol.** Every element should land in exactly one file. None means a missing pattern.
Two means the boundary is wrong and moves.

**Complete: all seven cases, plus case 8.** Phase 2 closed — see Conclusion.

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

## Case 8 — The inclusion spec, against corpus stocking data

**Source:** `room feature`, `rooms`, `encounter treasure`, `trap treasure`, `empty
treasure`, and the file's own Moldvay stocking comment. **Stresses:** D15 — whether a
weighted spec can be set from evidence rather than taste.

### What the corpus actually stocks

Its dungeon is 1 entrance + N-2 interior + 1 boss room, with N weighted 5(×5), 7(×4),
10(×3), 12(×2), 14(×1) — a mean of **8.1 rooms**. Interior rooms roll `room feature`:

| Interior content | Corpus weight | Share |
|---|---|---|
| Creature + treasure | 2 | 33% |
| Trap + treasure | 1 | 17% |
| Special + feature | 1 | 17% |
| Empty dressing + feature | 2 | 33% |

And treasure attaches at a rate set by what holds it — `encounter treasure` 1-in-2,
`trap treasure` 1-in-3, `empty treasure` 1-in-7. Those are **50% / 33% / 14%**, which is
Moldvay's 50/33/16 implemented exactly. The corpus is not improvising these numbers and
neither should we.

### Mapping onto our classes

Boss room → HIGH. Interior creature or trap → MEDIUM (one reactive element). Interior
special or empty → LOW. Entrance is special-cased in both systems.

For the mean 8-room dungeon: **12.5% entrance, 12.5% HIGH, 37.5% MEDIUM, 37.5% LOW.**

Against the proposed 10 / 50 / 30, HIGH lands almost exactly and the missing 10% is the
entrance. MEDIUM and LOW are inverted.

### F7 — our LOW class must be larger than the corpus's, not smaller

The corpus draws corridors, junctions and stairwells **on its map** and never keys them.
We have no map, so `Dangerous_Low.md`'s "connective corridor, junction, or stairwell"
rooms have to be keyed locations. Our LOW class therefore absorbs a category the corpus
does not count as rooms at all.

It compounds with size: our DANGEROUS regions run 12-36 locations against the corpus's
8, and connective tissue grows faster than set-pieces do. A 36-room region with 50%
MEDIUM would carry eighteen reactive rooms, which is not a dungeon, it is a gauntlet.

**Proposed, and scaled by region size rather than fixed:**

```
DANGEROUS location classes
  small region  (~12)   1 entrance   15% HIGH   40% MEDIUM   45% LOW
  large region  (~36)   1-2 entrances 8% HIGH   32% MEDIUM   60% LOW
```

### Evidence-backed draft specs

```
DANGEROUS - HIGH
  1     Challenge            {creature | trap | puzzle}
  50%   Secondary Challenge  {creature | trap | puzzle}   - not the first one
  30%   Mystery              {secret door | standing effect | lore carrying a clue}
  1     Architecture detail, unique to this room
  50%   Ambiance detail, unique to this room
  80%   Treasure             {hidden | trapped | discarded}   - boss rooms are stocked

DANGEROUS - MEDIUM
  1     Reactive element     {creature | trap}               - guaranteed, and obvious
  50%   Treasure if the reactive element is a creature; 33% if it is a trap
  1     Ambiance or architecture detail
  25%   A detail that foreshadows a HIGH room elsewhere in the region

DANGEROUS - LOW              (parameterized by node role - see F9)
  1     Purpose - what this space was for, and whether that use still holds
  1     Ambiance detail                                      - never leave a room empty
  1     Node role honoured   {empty | dead end | branch | loop leg | divide}
  14%   Treasure                                             - Moldvay's unguarded rate
  20%   A detail that rewards looking without demanding action
```

The MEDIUM treasure line is conditional on an earlier pick — the corpus's own rule, and
worth keeping because it means the reward follows the fiction rather than a flat roll.

### F12 — a class is defined by what it guarantees, not by what it permits

The classification describes **what is obvious and mandatory**, never a ceiling on what may
appear. An empty room may hide a secret door; what makes it LOW is that *it looks empty*.
A MEDIUM room is automatically assigned a detail and a challenge, and everything past that
is left to chance. A LOW room that rolls three percentage lines is still LOW.

This is a presentation distinction, not a content one, and it is the right one for this
genre. The class describes the **player-facing surface** — how much the room announces
itself — while the referee-facing contents vary underneath. Three consequences:

1. **It is what makes searching meaningful.** If LOW rooms could never hide anything,
   players would learn to skip them and the class would be dead weight. Because LOW is
   defined as *looking* empty rather than *being* empty, attention becomes a resource
   spent under uncertainty — which is the whole game.
2. **The spec's mandatory lines are constitutive, not just anti-blank.** F8 argued for at
   least one mandatory line so a room could not roll empty. That was right for a weaker
   reason: the mandatory lines *are* the class definition, and the percentage lines are
   variance that never reclassifies.
3. **Weight cannot be validated by counting.** A LOW room may legitimately end up holding
   four things. "Did this room respect its class" is a judgement about how it presents,
   not an arithmetic check — which independently confirms D13's decision to keep ratios
   and budgets out of the validator.

### F8 — every class needs at least one mandatory line

If a class is all percentages, it can roll a location with nothing in it. The corpus never
hits this because its empty branch makes `empty dressing` mandatory. Our LOW draft above
therefore carries two mandatory lines (purpose, ambiance) and the percentages sit on top.

**Rule: every inclusion spec states at least one mandatory line.** Cheap, and it removes
the only way the mechanism can produce a blank.

### Verdict

**D15 works, and the percentages are derivable rather than arbitrary.** Two of the three
proposed numbers moved on evidence, and the reason they moved — that we key what the
corpus draws — is a structural difference between the two systems worth recording.

## Case 2 — The empty room, and the decision structure of LOW

**Source:** `empty dressing` (33 entries), `special` (12), `interior room`, plus the
node-role taxonomy. **Stresses:** the LOW spec, F7, F8.

### F9 — LOW is where the dungeon's decisions live, not where its filler goes

The Case 8 framing of LOW as "connective tissue we are forced to key" was too grudging.
Connective space carries its own content, and it is the content players actually act on:

| Node role | What the player is deciding | What the room must supply |
|---|---|---|
| **Empty room** | Is it actually empty, or is something hiding? | Enough dressing that searching is tempting and not obviously futile |
| **Dead end** | Is there a secret door here? | A reason to suspect one — and a rate at which there genuinely is |
| **Branch** | Which way first? Everything returns here | Distinguishable exits, so it is a decision and not a coin flip |
| **Loop leg** | Where am I relative to where I have been? | A detail that makes the loop recognizable when it closes |
| **Divide** | Which way? We do not come back | The highest-stakes choice in the region — and legible stakes |

A LOW room is "low" because it holds no reactive element, not because it holds nothing
worth doing. That is a materially different instruction to write patterns against.

**On dead ends specifically:** if a dead end never hides a secret, players stop checking
and the class dies; if it always does, it is not a secret. It needs a real rate.
`patterns/Secrets.md` already sets DANGEROUS low weight at >30%, which is about right and
should be applied *at the node role* rather than flat across the class.

### F10 — three of the five roles are graph properties, not room properties

Branch, loop and divide are only what they are because of what lies downstream. A room is
not a divide on its own; it is a divide because the paths beyond it do not reconverge.
These cannot be picked at location-generation time.

**The build order already supports this.** Step 4b writes the region's `Connections.mmd`
*before* 4c writes any location, so the graph exists when a location is drafted and the
node role can be read off it rather than invented. Nothing in `STEPS.md` needs to move.

What is missing is that `templates/Region_Connections.mmd` has no guidance on decision
shape at all — it specifies edge types (normal, hidden, one-way) and says nothing about
branching, looping or dividing. So the taxonomy belongs in `region/Scope.md` under
topology (D16), applied at 4b, and read as an input at 4c.

### F11 — an existing rule turns out to be doing decision-support work

`templates/Location.md` already requires that two exits never read identically — "position
is what keeps two exits of the same type distinguishable." That rule was written as an
anti-ambiguity measure for the referee.

It is actually what makes a **branch** a decision rather than a coin flip. A player
choosing between "a door" and "a door" is guessing; one choosing between "a low door,
scorched around the frame" and "a wide arch, the floor beyond worn smooth" is deciding.
The rule should be restated in that light in `dangerous/Dressing.md`, because its
justification is much stronger than the one currently given for it.

### Decomposition

| Element | File |
|---|---|
| Node role (empty / dead end / branch / loop / divide) | **read from the graph**, set at 4b |
| Whether something is concealed here, and at what rate | Features (via `Secrets.md`'s rate) |
| `empty dressing` — cobwebs, rat tunnels, a doll in a dingy crib, a slaughtered pig | Dressing |
| `special` — coloured pools, smashed statues, a magic mouth, waist-high mist | Dressing, unless it does something |
| Former purpose and whether it still holds | Dressing |
| Exit differentiation | Dressing — and it is load-bearing, per F11 |

**Result: decomposes cleanly, and F8 holds** — the three mandatory lines mean a LOW room
can never roll blank.

### Note on `special` — resolved by F12

Raised as a contradiction: "a stairwell down into a maze of unmappable corridors filled
with the skeletons of past visitors" *does something*, so by F1 it is Features — yet it
sits in a class supposedly holding no reactive element. Resolved by F12 below: a class is
defined by what it guarantees, not by what it permits. That entry can appear in a LOW room
without reclassifying it, because the room still *presents* as unremarkable.

## Case 3 — The trapped room, and what "obvious" means

**Source:** the `trap` table (29 entries in `hint; hint → effect` format) and `concealed
trap`, maintained as a **separate** table. **Stresses:** MEDIUM's mandatory challenge, the
required-tell rule, F12.

### F13 — the tell requirement follows from the class definition, and is not universal

The analysis found that `patterns/Traps.md` never requires a visible tell, while all 29
corpus traps state one. But the corpus also keeps `concealed trap` as its own table and
uses it specifically to guard treasure — so the corpus does not require tells universally
either. It requires them *by role*.

F12 explains why, and turns a rule I would otherwise have written flat into one that falls
out of the structure:

- **A trap that is a MEDIUM room's challenge must have a tell.** MEDIUM guarantees an
  obvious reactive element. A trap with no tell is not obvious, so a room built on one
  does not present as MEDIUM — it presents as LOW, and it should be classified LOW.
- **A concealed trap belongs in a LOW room, or guarding treasure.** It is part of why a
  room that looks empty is not always empty, which is exactly the work F12 gives LOW.
- **A treasure guard's tell is contextual, not physical.** The player does not need
  scratches on the flagstones to suspect a chest; the chest is the tell. The corpus's
  `fog chest` and `skunk chest` both state a *smell noticed on close examination* — a tell
  available only to someone already suspicious enough to look.

So the rule is not "every trap states a visible tell." It is: **a trap presented as the
room's challenge states a tell; a trap that is variance or a guard need not.** That is
one sentence in `dangerous/Features.md` and it is strictly better than the flat version.

### Decomposition

| Element | File |
|---|---|
| Whether this room's guaranteed challenge is a trap or a creature | Weight (the MEDIUM spec) |
| The mechanism — deadfall, darts, pendulum, walls closing in | Features |
| The tell — walls nicked and holes opposite; a raised floor segment | **Features** if it is the challenge; Dressing if it is variance |
| Resolution — save vs. breath, 2d6, TEST OF CONSTITUTION | **`setting/Procedures.md`** (D11) |
| Trap treasure at 33% | Features |
| What the room was for, and its ambiance | Dressing |

**Result: decomposes cleanly.** The one element that moves between files does so by role,
per F13, which is the same shape as F1's resolution — placement follows what a thing does,
not what it is.

### Note on the corpus's trap format

`**name**: hint; hint; hint → effect; effect` is worth adopting more or less verbatim as
the writing format in `dangerous/Features.md`. It is compact, it forces the tell to be
authored rather than assumed, and the arrow makes it obvious when a trap has been written
with no way to detect it. The corpus records the format in a comment; we should record it
as a requirement.

## Case 4 — The wilderness landmark

**Source:** `grass landmark` (21), `hills landmark` (20), `small landmark`, `calm clearing
feature`, `magic plant location`, `magic plant guardian`, `cave entrance`. **Stresses:**
wild/ all three files, position-within-region, D17.

### F14 — most corpus "landmarks" are our region terrain, not our WILD Landmarks

This is the sharpest sorting problem in the trial fit. `hills landmark` reads:

> The sandy slopes are heavily eroded by recent flooding.
> A small brook meanders between the hills here.
> Brilliant blossoming flowers coat the slopes like thick, wet paint.

None of that is a location. It is what the ground looks like, and in a point crawl it is
**connective terrain the referee narrates** — `region/Dressing.md`, feeding the Region
Overview's Terrain field. Our WILD Landmark is a different animal: a named destination
that can be revisited and connected to.

But the same table also holds:

> Atop a squat tor is a ring of crudely worked megaliths.
> A burned farmstead lies ahead, eerily silent in the whispering winds.
> Crumbling with age, the stony legs of an ancient aqueduct straddle the valleys.
> A foul-smelling den, barely concealed behind some stones.

Those are destinations.

**Sorting rule, for mining the corpus into `wild/Features.md`:** an entry is a Landmark if
it can be **named, revisited, and connected to**. If it cannot — if it is a quality of the
ground rather than a thing standing on it — it is region terrain texture. Roughly a
quarter of the corpus's landmark entries pass; the rest are `region/Dressing.md` material,
and they are *good* material, since F5 and F6 already established that our region fields
are the underspecified layer.

`magic plant location` (growing around a skeleton, along a creek, deep within a thorny
bush) sorts the same way: Foraging-field texture, not locations. Confirms the same
direction a third time.

### F15 — WILD depth is something the corpus cannot express

`calm clearing feature` is four entries, three pure dressing and one — "a spring of
frigid water that removes *fear*" — a standing effect, so Features by F1.

More interesting is what is absent. Every corpus landmark is **flat**: a hex holds a thing,
and the thing has no interior. There is no equivalent of a Landmark with a Hidden child,
or a Hidden location with a Secret below it. Its lairs (Case 5) are the nearest thing and
they are self-contained set-pieces, not landmarks with depth.

So D17 — that WILD prominence is expressed by *attaching children* rather than weighting a
location — describes a capability the corpus does not have. **We are not porting this from
the corpus; we are keeping something it lacks.** Worth stating plainly so Phase 3 does not
flatten WILD while mining corpus breadth into it.

### Decomposition

| Element | File |
|---|---|
| Landmark / Hidden / Secret; Site / Connection / Natural Feature | Classification |
| Whether this Landmark carries children, and how many | Classification (D17 — this *is* prominence) |
| `magic plant guardian` — treants, a hermit druid, trapdoor spiders | Features |
| The standing effect in the clearing | Features |
| Position within the region | Dressing |
| Terrain quality, erosion, flowers, brook | **`region/Dressing.md`** — not a location at all |
| `cave entrance` — dug into the ground; timber-shored former mine | Dressing, with the former purpose carrying it |

**Result: decomposes cleanly once F14's sorting rule is applied.** Without it, roughly
three quarters of the source material would have been miscategorised into `wild/`.

---

## Case 7 — The quest chain

**Source:** `alchemist job`, `alchemist quest` (11 stored objects), `treasure map`,
`patron plot hook`, `library mission`, `law and order jobs`, `magic plant guardian`,
`sharing agreement`. **Stresses:** D6 two-endedness, end to end.

### How the corpus actually does it

The quest economy runs on eleven objects — basilisk bile, chimera blood, griffon egg, hell
hound embers, hydra blood, medusa head, naga tongue, royal jelly, swamp crane feathers,
unicorn horn, winter wolf icicles — and the mechanism is inverted from what one would
expect:

**The target end is authored first, as a side effect of generating the target.** The giant
ant queen chamber ends with `[here store royal jelly as alchemist quest]`. The naga temple
stores naga tongue. Each location that *could* supply something registers that it can.
Only later does a settlement's alchemist pull `[nearby alchemist quest]` and the errand
come into being.

So it is not giver-then-target. It is **supply registered by targets, demand drawn from
the pool.**

### F16 — our build order already permits two-ended quests, and I had assumed it did not

The Quest design assumed a giver written at 4c could not name a real target, because the
target's file does not exist yet. That is wrong.

`STEPS.md` 4a creates the `Locations.md` gazetteer for **every** region before 4b creates
any connection graph, and 4b completes for every region before 4c writes any location
file. So when a quest giver is drafted at 4c, **every location in the setting already
exists as a stub** — name, weight or classification, and tags.

A giver in SAFE A.3 can therefore cite a real target in DANGEROUS C.14 by name at 4c. What
it cannot yet know is what C.14 *contains*, since that file is not written. Which is
exactly D14's container/data split doing its job: the Quest stub records giver, target and
a coined name; 4d writes what the object actually is, with both location files in view.

No new machinery, and no change to `STEPS.md`. The capability was already there.

### F17 — a quest needs a middle, not just two ends

`magic plant guardian` is eight entries and every one is an **obstacle standing between the
party and the object**: treants who hate anything living by thumb and fist; a hermit druid
with thirty wolves; a tomb of wights; a plant that only grows where owlbears have
fertilized it; a screaming mandrake that non-herbalists will always mistake for the real
thing.

That last one is the best of them, because the obstacle is *the giver's omission* — "*[same
human name]* is not about to tell you that." The complication is baked into the errand.

Neither `patterns/Keys.md` nor the Quest design as planned has a middle. A Key names what
it opens; a Quest was to name who wants what and where it is. Both describe endpoints. The
obstacle is what makes it an adventure instead of a delivery, and it is cheap to require:

**A Quest states three things — who wants it and why they will not go themselves, what
specifically and where, and what stands in the way.** The third is new and it is the one
that matters.

### F18 — the reward should be stated in the giver's voice

`sharing agreement` gives three named terms, each in first person: "I am generous: two
shares of the treasure found for me, the rest shared equally amongst the other survivors."
"I will provide all the expertise: five shares for me." "I'll be fair: half for me, half
amongst the other survivors."

The terms characterize the giver while stating the payment — the "generous" one is taking
a double share and the "fair" one is taking half. `patterns/Safe.md`'s Task bullet asks
"What's offered in return: coin, goods, information, standing?" and gets an abstract
answer. Asking for the offer **in the giver's own words** gets a concrete one and a piece
of characterization for free.

### Decomposition

| Element | File / artifact |
|---|---|
| That this location offers a quest at all | `safe/Kind.md` inclusion spec |
| Who wants it, and why they will not go | Features → Named Creature |
| What is wanted, and which location holds it | **`setting/Quests.md`** stub at 4c |
| What the object actually is | `setting/Quests.md` full entry at 4d |
| What stands in the way | Features at the *target* location; summarized in the Quest row |
| The terms, in the giver's voice | Features |
| The target location registering that it can supply something | Features at the target, at 4c |

**Result: decomposes cleanly, and D6 is confirmed** — with two additions (F17's obstacle,
F18's voiced terms) and one assumption corrected (F16).

## Findings

### F1 — Access: resolved, and the rule generalizes

*Superseded by the design pass.* The earlier reading — "existence is Features, description
is Dressing" — was too narrow. Both directions are legitimate:

- Features declares an egress → Dressing calls it a ladder.
- Features declares an empty room → Dressing puts a ladder there as dressing.

**The rule is: Features owns anything that changes what players can do; Dressing owns
everything else and may originate it freely.** The test is not which file mentions the
ladder — it is whether the ladder does anything. Folded into the plan's §2.

### F2 — Budget: resolved twice over

*Superseded.* The "compound site: 4-8" band assumed size drives budget; it does not. Then
the prominence framing was itself superseded by D15 and D17:

- **D15** makes budget emergent from the inclusion spec's percentages rather than stated
  as a range at all.
- **D17** closes the open question of whether SAFE and WILD need a prominence axis:
  **no.** In WILD every Landmark sits at a baseline and complexity is added by *attaching
  Hidden and Secret children*, not by weighting the Landmark heavier. In SAFE a baseline
  template covers almost everything and extra emphasis arrives as *additional optional
  locations*. Prominence is structural in both, so only DANGEROUS carries a per-location
  weight — because there, movement is room by room and each room must differ from its
  neighbour.

This also explains why the WILD classification is a discoverability axis and always was:
in WILD, depth *is* prominence.

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
| F6 | **Situation** field in the Region Overview | `templates/Region.md`, `region/Features.md` | folded in |
| F7 | LOW is the largest DANGEROUS class, and distribution scales with region size | `dangerous/Weight.md` | **new** |
| F8 | Every inclusion spec states at least one mandatory line | all three first-files | folded in |
| F9 | LOW is parameterized by node role; it carries decisions, not filler | `dangerous/Weight.md` | **new** |
| F10 | Branch/loop/divide are graph properties, set at 4b and read at 4c | `region/Scope.md`, `Region_Connections.mmd` | **new** |
| F11 | The distinguishable-exits rule is decision support, and should be justified as such | `dangerous/Dressing.md` | folded in |
| F12 | A class is defined by what it guarantees, not what it permits; weight is a presentation distinction | Plan §3, all three first-files | **new** |
| F13 | Tell requirement follows from class: a challenge trap states a tell, a variance or guard trap need not | `dangerous/Features.md` | folded in |
| F14 | Sorting rule — a Landmark can be named, revisited and connected to; everything else is region terrain | `wild/Features.md`, `region/Dressing.md` | **new** |
| F15 | WILD depth is a capability the corpus lacks; do not flatten it while mining breadth | `wild/Classification.md` | **new** |
| F16 | The build order already permits two-ended quests — every location stub exists before any location file | none needed | **new** |
| F17 | A Quest states three things: who wants it, what and where, **and what stands in the way** | `patterns/setting/Quests.md` | **new** |
| F18 | Reward terms are stated in the giver's own voice | `safe/Features.md` | **new** |

Still no amendment touches D1-D14. Three cases have moved numbers and added two Region
Overview fields; the structure itself has held.

**Note on F5 and F6 together:** both say the same thing from different directions — the
SAFE Region Overview is underspecified. It describes a place but not who is in it or what
is currently happening to it. That is the largest single gap the trial fit has surfaced so
far, and it is a `region/` problem, not a `safe/` one.

---

## Conclusion — Phase 2 closed

All seven planned cases decomposed, plus an eighth added to set the inclusion-spec
percentages from evidence.

**Against the acceptance criteria:**

1. **All cases decompose cleanly.** Two elements were genuinely contested (F1 access, F13
   trap tells) and both resolved into rules better than the flat versions they replaced.
   One category, `special`, looked like a contradiction and was dissolved by F12 rather
   than patched.
2. **The lair produced three legible outputs at three scales.** D5 confirmed; no lair tier.
3. **Breadth** is a Phase 3 authoring task, but F14 supplies the sorting rule that decides
   what corpus material feeds which file — without it about three quarters of the
   wilderness material would have landed in the wrong folder.
4. **The relaxation calls are backed.** F12 independently confirms D13: weight is a
   presentation distinction, so it cannot be validated by counting, and any mechanical
   budget check would be wrong in principle rather than merely strict.
5. **No guidance read identically across folders**, because the trap resolution mechanics
   moved to `Procedures.md` before the comparison could arise (D11).
6. **Counts re-derived, not assumed** (D9): the three DANGEROUS weights survived, the WILD
   classification survived and gained a justification it did not have (F15 — depth is
   prominence), and the class *distribution* moved substantially on evidence (F7).

**Nothing amended D1-D17.** Eighteen findings moved numbers, added two Region Overview
fields, added a decision-shape taxonomy, and corrected one assumption about the build
order. The structure itself held throughout.

**What Phase 2 changed about Phase 3's shape:**

- `templates/Region.md` is the largest single piece of work, not `patterns/`. F5, F6, D16
  and F14 all land on it, and it needs rebuilding per rating rather than patching.
- `patterns/setting/Quests.md` gains an obstacle clause (F17) that makes it materially
  different from `Keys.md` rather than a variant of it.
- The corpus is a source for `region/Dressing.md` at least as much as for the rating
  folders — the opposite of the expectation going in.

**Ready for Phase 3.**
