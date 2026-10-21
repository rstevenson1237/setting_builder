# Setting_Judgement_Check.md

## Purpose
A non-mechanical review pass over the generated `setting/` content - confirming, by human or model judgement, that the setting holds together thematically and structurally from location up through region up through the top-level setting, and that it's built from things a player can actually find rather than mood alone. Saved as `setting/checks/SettingJudgementCheck.md`. Unlike `templates/region/Location.md`'s deliberately narrow generation-time Context, this check is the one place a full read across levels is appropriate, since coherence between levels is exactly what's being judged.

## Context
Consult when running this check - deliberately broader than any single generation step, since cross-level coherence is the thing being judged:
- `GENRE.md` - the throughline every level should still be expressing.
- `BRIEF.md`
- `STYLE.md` - the tests judged against below.
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md` - what every region should be reinforcing.
- `setting/region/Regions.md` and each region's seed, `setting/region/[Code]/Seed.md`, and brief, `setting/region/[Code].md` - what every location in that region should be reinforcing.
- each region's `setting/region/[Code]/Locations.md`, its table files and its location files, each write-up with its entries from `python3 tools/validate_setting.py --location [Location Code]`.
- `setting/Bestiary.md`, `setting/Factions.md`, `setting/Lore.md`, `setting/Keys.md`, `setting/NamedCreatures.md`, `setting/UniqueTreasures.md`, `setting/MagicalTomes.md`, `setting/Hoards.md`, `setting/LocalProcedures.md`, `setting/Rumours.md`, `setting/Quests.md` - recurring elements that should be tying levels together rather than sitting isolated.
- the output of `python3 tools/validate_setting.py`, `python3 tools/metrics.py` and `python3 tools/metrics.py --tells setting/`.

## Instructions
Run this once the loop has exited and the briefs are written, in a context that wrote none
of the content. This check reads across levels, location up. Record
each item as Confirmed or Needs Attention, with a note, in the order below; the Template
block lists the same items in the same order.

**Record against the content as generated, before anything is fixed.** This pass is a
diagnosis of the framework as much as of the setting: every Needs Attention names its
likely source - a schema line, a template line, a `BRIEF.md` line, or the generator
alone - so a defect an edit later hides has already been traced to what produced it. Its
findings are the evidence `templates/checks/Schema_Judgement_Check.md` starts from.

### Setting-level, once per pass

- **The brief was delivered** - take `BRIEF.md` line by line. For each request, name where the setting delivers it, or record that it does not. A count asked for is counted; a shape asked for (entrances per block, a gap left for the referee, a mix of peoples) is checked against the graph and the rooms, not the brief's claim about them.
- **Genre held across levels** - take `GENRE.md`'s answers one by one and name where the setting delivers each: the Magic level answer in what the Treasure tables actually hold, the Lethality answer in what a hazard or creature can do, the Reward answer in what a party can carry home and sell, the Naming answer in the names on the map. Record any answer given differently at a lower level - a mechanic the reference does not have, a kind of creature it does not lean on, a history deeper than it wants - and any authored plot where a situation should be.
- **The tests, hardest at the top** - apply `STYLE.md`'s tests, as written there, to every sentence of the setting-level files and each region's seed and brief, line by line. They fail most often above the location level, because a location has to be run at a table and a seed does not.
- **Discrete and discoverable, not vague** - is content built from concrete, specific, discoverable details (a named object, a specific trigger, a specific creature or faction presence) that a player can find and act on, rather than an atmospheric motif repeated without ever cashing out into something discoverable?
- **Every secret has its answer** - does every secret, mystery and undecided question in the setting-level files, the seeds and briefs, and the registries carry the fact the referee holds as true, or stand in `setting/Truths.md` as a mystery or an open gap held on purpose? A question the players may never answer is fine; one the referee cannot answer, and that nothing marks as deliberate, is a decision handed to whoever improvises first.
- **Nothing contradicts** - does any fact in one file disagree with another: a place said not to exist beside the location that is it, a building placed in two baileys, a person alive in one region and gone in another?
- **Everything recurs, nothing is orphaned** - is every Bestiary entry, faction, Named Creature, Lore, Key, Unique Treasure and coined name met in at least one location, and do the ones met in several stay consistent and build on each other? Is everything a seed or brief offers (a person, an occupant, a prize) somewhere a party can reach?
- **Vocabulary is precise, and precise is not decorative** - the one register audit nothing mechanical can perform, since `tools/validate_setting.py` can count a segment but cannot tell a term used correctly from one used approximately. Three failures, in rising order of cost. A **gloss** - a specialist term followed by its own definition, which pays for the same fact twice and is the tell that the writer did not trust the word (*Corbelled Ceiling: the ceiling steps inward in courses rather than arching*). A **decoration** - an archaic or elevated word that names no referent a party could be shown, which is mood wearing a scholar's coat and is already cut by `STYLE.md`'s first test. And the one that matters most, a **misuse** - a term applied to the wrong thing, which is worse than the plain word would have been, because a referee who half-knows it will describe the wrong thing to the players and the error reaches the table.

### Per region

- **Regions reinforce the setting** - does each region's seed visibly connect back to `setting/Setting.md`/`History.md`/`Truths.md` (a named historical event, a faction's presence, a unique truth playing out), rather than feeling like an unrelated pocket bolted onto the setting?
- **Locations reinforce their region** - does each location's dressing and Features reflect its region's seed and brief, rather than reading as a location that could belong to any region? Are its three tags recognisable in what it holds?
- **Entries match** - does every write-up carry every entry its location holds, and nothing written without one? `python3 tools/metrics.py --carry` lists the table words each write-up drops, a prompt to look and not a verdict.
- **Prices fit the list** - does each coin `price` of a Purchase sit near what `setting/Procedures.md`'s Coin and Prices lists for the same or a like good, and where it differs, does its room say why?
- **One room** - does each write-up read as one place, not its entries side by side?
- **Distinct** - does any write-up share a Feature, shape or sentence frame with its block, or any table's entries a sentence shape, opening word or rotation of the same few glosses?
- **Said once** - is anything in a write-up restated from the seed, a setting entry or another room?
- **The tests, at the location** - does each write-up line pass `STYLE.md`, and is each tell `metrics.py --tells` lists read for whether it is the failure the tell names?

### Room to Grow

- **Claims made upward are kept downward** - the one audit no mechanical check can do, and the only item on this list that reads *upward* rather than down. For every claim a setting-level file or a seed makes, is there a location that delivers it? Each Code on a truth names a location whose write-up delivers its Handle; each Code on a History event names a room whose write-up shows its Left mark (the validator checks the `left` pointers, not what the write-up shows); a treasure table a region says it leans on is actually cited by a room; a creature a region places somewhere is named in a room there; a motif a region says repeats throughout is present in the entries it applies to rather than a third of them. A claim with nothing under it yet is **not** cut - the claim already earned its place at the level that stated it; what's missing is only that no location has grown into it yet. Name it under Room to Grow instead, specific enough that the next location or revision can act on it.
- **Reinforcement candidates are named, not acted on** - which elements are thin enough on the ground that a later pass could thicken them? An element cited in one location that the setting leans on, a motif shown once where recognition would pay, a name met in a single place. Name them under Room to Grow with where they already appear. **This check authors nothing**: acting on a candidate is a decision made outside the numbered build, and naming one here is a recommendation rather than a task.
- **Coinage is tracked, not orphaned** - the validator checks that every name whose form is `tongue` or `family` is recorded in `setting/Language.md` and every recorded coinage is used by one. What it cannot see is a coined-sounding word set in prose or in a name declared `common`: name any, and whether the tongues' reach matches `GENRE.md`'s Naming.

## Template
```
# Setting Judgement Check - [Date or revision note]

## Setting-level
- The brief was delivered: [Confirmed / Needs Attention - per line, and its source]
- Genre held across levels: [Confirmed / Needs Attention - per answer, and its source]
- The tests, hardest at the top: [Confirmed / Needs Attention - note]
- Discrete and discoverable, not vague: [Confirmed / Needs Attention - note]
- Every secret has its answer: [Confirmed / Needs Attention - note]
- Nothing contradicts: [Confirmed / Needs Attention - note]
- Everything recurs, nothing is orphaned: [Confirmed / Needs Attention - note]
- Vocabulary precise, not decorative: [Confirmed / Needs Attention - note]

## Region [Code]
- Region reinforces the setting: [Confirmed / Needs Attention - note]
- Locations reinforce this region: [Confirmed / Needs Attention - note]
- Entries match: [Confirmed / Needs Attention - location, and its source]
- Prices fit the list: [Confirmed / Needs Attention - location, and its source]
- One room: [Confirmed / Needs Attention - location, and its source]
- Distinct: [Confirmed / Needs Attention - locations, and its source]
- Said once: [Confirmed / Needs Attention - locations, and its source]
- The tests, at the location: [Confirmed / Needs Attention - locations, and its source]

[repeat per region]

## Room to Grow
- [Claim, and where it's made] - [what's missing, specific enough to act on]
- [Element thin on the ground] - [where it already appears, and where it could be reinforced]
- [Coinage untracked or unused]

## Open Items
- [Anything flagged Needs Attention, carried forward as an action item, with its source:
  schema, template, brief, or generator]
```
