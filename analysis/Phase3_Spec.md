# Phase 3 Spec — file layout, organization format, template audit

Phase 2 is closed. This fixes what Phase 3 writes, in what shape, and what moves out of
`templates/` to make room.

---

## 1. Two places this layout beats the plan

**`region/` by rating, not by tier.** The plan had `region/` carrying Scope/Features/
Dressing. One file per rating is the right cut: F5, F6, D16 and F14 all established that
SAFE, WILD and DANGEROUS need *materially different* overviews, so splitting by tier would
have forced three-way branching inside every file — exactly the thing D3 exists to avoid.
One file per rating, each directing that rating's fields and their content.

**One `setting/` file per artifact.** The plan had a single catch-all `Artifacts.md`. One
file per table is better for the same reason the tiering is: each setting step loads
exactly the one pattern file it needs, instead of scanning a document mostly about other
artifacts. It also matches how `templates/` is already organized, so the pairing is
one-to-one and obvious.

---

## 2. Layout

```
patterns/
  setting/     Outline.md  Setting.md  History.md  Truths.md  Rumours.md
               Bestiary.md  Factions.md  Treasure.md
               Lore.md  Keys.md  NamedCreatures.md  UniqueTreasures.md  Quests.md
               Language.md  Procedures.md

  region/      Safe.md  Wild.md  Dangerous.md

  safe/        Settlement.md                                    (what kind, and how much)
               Commerce.md  Authority.md  Social.md  Situation.md
               Dressing.md  Secrets.md

  wild/        Landmark.md  Hidden.md  Secret.md                (classification)
               Ruin.md  Lair.md  NaturalFeature.md              (kind of place)
               Dressing.md  Secrets.md

  dangerous/   High.md  Medium.md  Low.md                       (weight)
               Trap.md  Mystery.md  Lore.md  Quest.md  Creature.md  Treasure.md
               Dressing.md  Secrets.md
```

**~43 files, each small and each loaded at exactly one point.** That is the point: a
generation step reads three or four short files rather than scanning one long one, which
is the same directing argument that produced the split in the first place.

Filenames stay TitleCase to match the existing repo convention (`Dressing.md`, `Safe.md`).

### Note on the two different Tier-2 axes

`wild/` organizes its middle tier by **kind of place** (Ruin, Lair, Natural Feature);
`dangerous/` organizes its by **kind of element** (Trap, Mystery, Lore, Quest, Creature,
Treasure). That is not an inconsistency — it follows what actually varies. In WILD the
question is *what sort of place is this*; in DANGEROUS the place is a room and the
question is *what is in it*. Worth stating in `CLAUDE.md` so it does not read as an
accident later.

---

## 3. Gaps and calls in the proposed layout

| # | Item | Call |
|---|---|---|
| 1 | **`dangerous/Treasure.md` was missing** | Added. Every inclusion spec cites treasure and nothing owned it. `setting/Treasure.md` governs the five tables; `dangerous/Treasure.md` governs which one fits, how it is concealed, and the guard relationship |
| 2 | **`Mystery.md` vs `Secrets.md`** | Different jobs, kept separate: `Mystery.md` is the *content* (what the strange thing is — a standing effect, a sealed door, a puzzle fixture); `Secrets.md` is the *discovery structure* (Clue / Trigger / Payload). A mystery may be plainly visible; a secret is by definition not. Puzzles fold into `Mystery.md` rather than getting their own file |
| 3 | **WILD loses "Connection"** | Correct for a point crawl — a road is procedural terrain, not a location. Bridges, fords, passes and gates are still covered: built ones are Ruins, natural ones are Natural Features. Stating it so nobody re-adds the kind later |
| 4 | **`safe/` Tier 1** | SAFE has no classification (D17: baseline template for almost everything, emphasis via extra locations). So Tier 1 is one file, `Settlement.md`, deciding settlement type *and* how much this one matters — which is where Case 1's "decide first how much this one matters" instruction lives |
| 5 | **`safe/` Tier 2** | The eleven `Safe.md` categories grouped four ways rather than eleven files: **Commerce** (hospitality, services, market), **Authority** (authority, notices, custom), **Social** (revelry, routine, task), **Situation** (tension, aftermath, and F6's ongoing situations) |
| 6 | **`setting/Outline.md`** | Keep it, keep it thin. It decides how many regions, what rating mix, and what altitude the party plays at — currently decided ad hoc at step 3a with nothing guiding it |
| 7 | **`dangerous/Lore.md` + `Quest.md` vs `setting/` versions** | Intended duplication per D3 — setting holds the *criteria*, dangerous holds *when to reach for one here*. This is the pair most likely to drift, so it is the first thing `PatternJudgementCheck` should look at |

---

## 4. Consistent organization format

Every pattern file, in every folder, uses this skeleton. It mirrors `templates/`'s
Purpose/Context/Instructions/Template so the two sets read as one system.

```markdown
# <Name>

## Decides
One line. What this file settles that no other file settles.

## Read at
Which step, and which files are read alongside it.

## Spec
The weighted inclusion spec, where this file has one.
`1` mandatory · `N%` at that rate · `{a | b | c}` pick-set · trailing clause constrains.

## Patterns
The match list. The bulk of the file in Tier 2; brief or absent elsewhere.

## Constraints
Starts empty. Entries arrive from testing, never from anticipation.
```

### On the Constraints section starting empty

This is the mechanism for "avoid negative patterns." A constraint has a home, so it does
not leak into the match lists as hedging — but it is empty until a generation actually
produces the failure it prevents.

The test for admitting one: **did we observe this failure, or are we imagining it?**
Phase 2's constraints pass, because each came from the corpus rather than from worry —
F8's mandatory line (the corpus's empty branch makes dressing mandatory), F13's tell
requirement (29 traps state one), F7's distribution (Moldvay, implemented exactly). A rule
with no observed failure behind it does not go in.

---

## 5. Template audit — what moves out of `templates/`

Every template is Purpose / Context / Instructions / Template, and **the Instructions
section is where pattern content has been hiding.** Twelve moves:

| From | Content | To |
|---|---|---|
| `Setting.md` | Nothing to move — it is thin, and *what makes a good premise* is absent entirely | `patterns/setting/Setting.md` is net-new |
| `History.md` | "an event is a fact of the past, not a ticking clock aimed at the party" | `setting/History.md` |
| `Truths.md` | "Truths should not directly exist as objects but can define a class of object… thematic ideas such as politics and religious ideology are also acceptable" | `setting/Truths.md` — substantive guidance, currently in a template |
| `Rumours.md` | "Do not assume who is providing the rumour or their intent… Do not state what the players should do" | `setting/Rumours.md` (T/P/F marking stays — that is format) |
| `Bestiary.md` | **The eleven Type definitions** — Man, Humanoid, Beast, Fantasy Creature, Undead, Construct, Horror, Wyrm, Fey, Fiend, Giant | `setting/Bestiary.md`. This is a match list living in a template |
| `Bestiary.md` | AD / +N / MA scaling math | `setting/Procedures.md` (D11 — mechanic, not format) |
| `Factions.md` | "A creature that is also a power carries both a Faction and a Bestiary entry"; "ignorance is its own relation" | `setting/Factions.md` |
| `Factions.md` | AD scaling | `setting/Procedures.md` |
| `Treasure.md` | **The distribution rules and quality percentages** — see §6 | `setting/Treasure.md` |
| `Region.md` | All thirteen field descriptions | `region/Safe.md` / `Wild.md` / `Dangerous.md`, rebuilt per rating |
| `Location.md` | The Secrets / Treasure / Creatures / Traps / Puzzles paragraphs under Features | split: citation *format* stays, selection guidance goes to each rating's Tier 2 |
| `Location_Gazetteer.md` | Weight definitions and the 3× rule | `dangerous/High.md` / `Medium.md` / `Low.md`, and the count becomes a Shape-set range (F3) |

**What stays in `templates/`:** Purpose, Context, the Template block itself, citation
syntax, the header/filename correspondence, the Exits line format, and the units rule
(feet indoors, yards outdoors, miles between regions) — which finally lives in exactly
one place.

---

## 6. `templates/Treasure.md` already contains an inclusion spec

Worth flagging as independent evidence that D15's format is right. The template currently
says, in prose:

> **Quality** — poor (~10%), normal (~50%), fine (~30%), masterwork (~3%), cursed (~5%).
> **Effect** — ~30% of fine items do, all masterwork items do (always positive), all
> cursed items do (always negative).

That is a weighted inclusion spec with mandatory lines, percentage lines, and a
conditional — written a year before we designed the notation. It should be rewritten in
the spec format:

```
TREASURE II - quality
  10%   poor
  50%   normal
  30%   fine        - 30% of these carry an effect
  3%    masterwork  - always carries a positive effect
  5%    cursed      - always carries a negative effect; presents as fine or masterwork
```

Two things follow. The mechanism is not novel to this restructure, it is a formalization
of something the framework already reached for. And the percentages sum to 98%, which the
framework has evidently tolerated — so the specs elsewhere need not sum exactly either.

The same file's result-position rules ("result 1 always significantly below average;
2 and 3 slightly below or double weight; 4-20 randomized so the roll cannot be read")
are a **table-shape** constraint rather than an inclusion spec, and stay as prose in
`setting/Treasure.md`.

---

## 7. Build order for Phase 3

1. `setting/Procedures.md` and `setting/Language.md` — seeded first, since steps 1b/1c
   now depend on them and everything downstream cites them.
2. The organization format applied to one file end to end — `dangerous/Low.md`, since
   Phase 2 specified it most completely — as the reference other files copy.
3. `region/Safe.md` / `Wild.md` / `Dangerous.md` — the largest lift, and everything at
   location level reads a Region Overview that these shape.
4. The three rating folders, Tier 1 → Tier 2 → Tier 3.
5. The `setting/` per-artifact files.
6. Template audit executed: move the twelve items, rewrite `Location.md`'s Context to walk
   the new folders, update `CLAUDE.md` and `STEPS.md`.
7. Validator adjusted to the D13 posture, plus the graph-shape diagnostic.
8. Generate from scratch, repeatedly. Constraints sections fill from what breaks.

**Proof criteria unchanged** from the plan's §10: multiple from-scratch generations, two
same-rating regions that do not converge, zero validator errors, all three judgement
checks re-run, and proper nouns traceable to `Language.md`.
