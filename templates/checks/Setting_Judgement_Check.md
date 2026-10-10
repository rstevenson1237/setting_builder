# Setting_Judgement_Check.md

## Purpose
A non-mechanical review pass over the generated `setting/` content - confirming, by human or model judgement, that the setting holds together thematically and structurally from location up through region up through the top-level setting, and that it's built from things a player can actually find rather than mood alone. Saved as `setting/checks/SettingJudgementCheck.md`. Unlike `templates/region/Location.md`'s deliberately narrow generation-time Context, this check is the one place a full read across levels is appropriate, since coherence between levels is exactly what's being judged.

## Context
Consult when running this check - deliberately broader than any single generation step, since cross-level coherence is the thing being judged:
- `GENRE.md` - the throughline every level should still be expressing.
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- `STYLE.md` - the tests judged against below.
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md` - what every region should be reinforcing.
- `setting/region/Regions.md` and each region's `setting/region/[Code].md` overview - what every location in that region should be reinforcing.
- each region's `setting/region/[Code]/Locations.md` and its location files.
- `setting/Bestiary.md`, `setting/Factions.md`, `setting/Lore.md`, `setting/Keys.md`, `setting/NamedCreatures.md`, `setting/UniqueTreasures.md` - recurring elements that should be tying levels together rather than sitting isolated.
- the output of `python3 tools/metrics.py` (its MIX section), `python3 tools/metrics.py --tells setting/`, and the region's table files, for any location whose draws are in question.

## Instructions
Run this once a region's locations are complete (or at the end of a full build). Record
each item as Confirmed or Needs Attention, with a note, in the order below; the Template
block lists the same items in the same order.

**Record against the content as generated, before anything is fixed.** This pass is a
diagnosis of the framework as much as of the setting: every Needs Attention names its
likely source - a pattern line, a template default, a `BRIEF.md` line, or the generator
alone - so a defect an edit later hides has already been traced to what produced it. Its
findings are the evidence `templates/checks/Pattern_Judgement_Check.md` starts from.

### Setting-level, once per pass

- **The brief was delivered** - take `BRIEF.md` line by line. For each request, name where the setting delivers it, or record that it does not. A count asked for is counted; a shape asked for (entrances per block, a gap left for the referee, a mix of peoples) is checked against the graph and the rooms, not the Region Overview's claim about them. Where a template default and the brief spoke to the same thing, record which one the content followed.
- **Genre held across levels** - take `GENRE.md`'s answers one by one and name where the setting delivers each: the Magic level answer in what the Treasure tables actually hold, the Lethality answer in what a hazard or creature can do, the Reward answer in what a party can carry home and sell, the Naming answer in the names on the map. Record any answer given differently at a lower level - a mechanic the reference does not have, a kind of creature it does not lean on, a history deeper than it wants - and any authored plot where a situation should be.
- **The tests, hardest at the top** - apply `STYLE.md`'s tests, as written there, to every sentence of the setting-level files and each Region Overview, line by line. They fail most often above the location level, because a location has to be run at a table and a Region Overview does not.
- **Discrete and discoverable, not vague** - is content built from concrete, specific, discoverable details (a named object, a specific trigger, a specific creature or faction presence) that a player can find and act on, rather than an atmospheric motif repeated without ever cashing out into something discoverable?
- **Every secret has its answer** - does every secret, mystery and undecided question in the setting-level files, the Region Overviews and the registries carry the fact the referee holds as true, or stand in `setting/Truths.md` as a mystery or an open gap held on purpose? A question the players may never answer is fine; one the referee cannot answer, and that nothing marks as deliberate, is a decision handed to whoever improvises first.
- **Nothing contradicts** - does any fact in one file disagree with another: a place said not to exist beside the location that is it, a building placed in two baileys, a person alive in one region and gone in another?
- **Everything recurs, nothing is orphaned** - is every Bestiary entry, faction, Named Creature, Lore, Key, Unique Treasure and coined name met in at least one location, and do the ones met in several stay consistent and build on each other? Is everything a Region Overview offers (a person, an occupant, a prize) somewhere a party can reach?
- **Vocabulary is precise, and precise is not decorative** - the one register audit nothing mechanical can perform, since `tools/validate_setting.py` can count a segment but cannot tell a term used correctly from one used approximately. Three failures, in rising order of cost. A **gloss** - a specialist term followed by its own definition, which pays for the same fact twice and is the tell that the writer did not trust the word (*Corbelled Ceiling: the ceiling steps inward in courses rather than arching*). A **decoration** - an archaic or elevated word that names no referent a party could be shown, which is mood wearing a scholar's coat and is already cut by `STYLE.md`'s first test. And the one that matters most, a **misuse** - a term applied to the wrong thing, which is worse than the plain word would have been, because a referee who half-knows it will describe the wrong thing to the players and the error reaches the table.

### Per region

- **Regions reinforce the setting** - does each Region Overview visibly connect back to `setting/Setting.md`/`History.md`/`Truths.md` (a named historical event, a faction's presence, a unique truth playing out), rather than feeling like an unrelated pocket bolted onto the setting?
- **Locations reinforce their region** - does each location's dressing and Features reflect the parent Region Overview's Conditions, Inhabitants and Places, rather than reading as a location that could belong to any region? Are its three tags recognisable in what it holds?
- **Rooms are distinct** - within the region, do two rooms share a Feature sentence, a room shape, or the same set of Features under different names? Where one occupant holds several blocks, does each block differ in more than its name? `tools/validate_setting.py` warns on a repeated Feature sentence; this item judges the near-repeats a string match cannot see.
- **Rates were rolled, not chosen** - do the region's tables sit near their types' rates? `python3 tools/validate_setting.py --pending` lists every room off its rate, and `python3 tools/metrics.py`'s MIX section counts connection and treasure kinds. A mix collapsed to one answer is recorded with the rate it should have held.
- **Entries written in one pass read as a form** - within one table, do the entries share a
  sentence shape, an opening word, or the same few glosses in rotation? A pass that sees
  every sibling exists to make them differ; a table that reads like a filled-in form has
  converged anyway.
- **Rooms read as one room** - does each location file read as one place, or as its entries
  laid side by side? A Feature that could not share the room with the others, or a Summary
  that names entries rather than a place, is the finding, traced to the entry that would not fit.
- **Said once** - does any location restate, near-verbatim, a sentence from its Region Overview, a Truth's Shows line, a Bestiary entry's Disposition, or another location? Per `STYLE.md` the higher level is the one that is wrong where a fact is merely repeated; where a room only transcribes the Bestiary, the room has said nothing of its own.
- **Tells, read** - for each of this region's hits in `python3 tools/metrics.py --tells setting/`, judge whether it is the failure its tell names: an absence claimed across time or space, a conclusion written for the players, a term glossed, a contrast doing a Feature's work.

### Room to Grow

- **Claims made upward are kept downward** - the one audit no mechanical check can do, and the only item on this list that reads *upward* rather than down. For every claim a setting-level file or a Region Overview makes, is there a location that delivers it? A truth's Handle names a real Location Code; a History event's Left line names a real Location Code; a treasure table a region says it leans on is actually cited by a room; a creature a region places somewhere is named in a room there; a motif a region says repeats throughout is present in the entries it applies to rather than a third of them. A claim with nothing under it yet is **not** cut - the claim already earned its place at the level that stated it; what's missing is only that no location has grown into it yet. Name it under Room to Grow instead, specific enough that the next location or revision can act on it.
- **Reinforcement candidates are named, not acted on** - which elements are thin enough on the ground that a later pass could thicken them? An element cited in one location that the setting leans on, a motif shown once where recognition would pay, a name met in a single place. Name them under Room to Grow with where they already appear. **This check authors nothing**: acting on a candidate is a decision made outside the numbered build, and naming one here is a recommendation rather than a task.
- **Coinage is tracked, not orphaned** - every proper noun `setting/Language.md` records as "coined here" is used somewhere in the setting, and every proper noun the setting actually coined is recorded there. A name invented once and never touched again is either placed (record it and cite it) or genuinely dropped - but a gap between the two is a Room to Grow item, not a silent loss.

### Bookkeeping, after the findings are recorded

Once every item above is recorded, fill what the build has earned: each `setting/Truths.md`
Handle, `setting/History.md` Left line and `setting/Rumours.md` Settled-at column that a
real location already delivers, per STEPS.md 5c. This is bookkeeping, not a fix; a claim
nothing delivers stays under Room to Grow.

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
- Rooms are distinct: [Confirmed / Needs Attention - note]
- Draws realized at their rates: [Confirmed / Needs Attention - rate asked, rate realized]
- Said once: [Confirmed / Needs Attention - note]
- Tells, read: [Confirmed / Needs Attention - note]

[repeat per region]

## Room to Grow
- [Claim, and where it's made] - [what's missing, specific enough to act on]
- [Element thin on the ground] - [where it already appears, and where it could be reinforced]
- [Coinage untracked or unused]

## Open Items
- [Anything flagged Needs Attention, carried forward as an action item, with its source:
  pattern, template default, brief, or generator]
```
