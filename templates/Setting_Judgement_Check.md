# Setting_Judgement_Check.md

## Purpose
A non-mechanical review pass over the generated `setting/` content - confirming, by human or model judgement, that the setting holds together thematically and structurally from location up through region up through the top-level setting, and that it's built from things a player can actually find rather than mood alone. Saved as `checks/SettingJudgementCheck.md`. Unlike `templates/Location.md`'s deliberately narrow generation-time Context, this check is the one place a full read across levels is appropriate, since coherence between levels is exactly what's being judged.

## Context
Consult when running this check - deliberately broader than any single generation step, since cross-level coherence is the thing being judged:
- `GENRE.md` - the throughline every level should still be expressing.
- `STYLE.md` - the three tests judged against below.
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md` - what every region should be reinforcing.
- `setting/region/Regions.md` and each region's `setting/region/[Code].md` overview - what every location in that region should be reinforcing.
- each region's `setting/region/[Code]/Locations.md` and its location files.
- `setting/Bestiary.md`, `setting/Factions.md`, `setting/Lore.md`, `setting/Keys.md`, `setting/NamedCreatures.md`, `setting/UniqueTreasures.md` - recurring elements that should be tying levels together rather than sitting isolated.
- `templates/Location.md` - the three tiers an entry displays information at, which the tiering item below is judged against.

## Instructions
Run this once a region's locations are complete (or at the end of a full build), region by region. Record each as Confirmed / Needs Attention, with a note.

- **Locations reinforce their region** - does each location's tags, dressing, Features, and Dangers actually reflect the parent Region Overview's Ambiance/Features/Dangers/Creatures, rather than reading as a location that could belong to any region? For a WILD region, does its landmark/hidden/secret split roughly track the guidance in `templates/Location_Gazetteer.md` (landmark the majority, hidden a third, secret the remainder), and does every hidden or secret location's connection actually trace back to a stated detail or Feature at its parent, rather than existing with no link back?
- **Regions reinforce the setting** - does each Region Overview visibly connect back to `setting/Setting.md`/`History.md`/`Truths.md` (a named historical event, a faction's presence, a unique truth playing out), rather than feeling like an unrelated pocket bolted onto the setting?
- **Discrete and discoverable, not vague** - is content built from concrete, specific, discoverable details (a named object, a specific trigger, a specific creature or faction presence) that a player can find and act on, rather than an atmospheric motif repeated without ever cashing out into something discoverable? Per each rating's `Dressing.md` Position guidance, this includes whether Features and Exits actually state where in the room they sit and, when spatially significant, their own dimension - a Referee shouldn't have to improvise where something is, or find two same-type exits in one room indistinguishable.
- **Information is tiered, and the chain holds** - per `templates/Location.md`'s three tiers, does each location present something at more than one of obvious / trigger / secret, and does every tier's way in actually sit in the tier above it? Three failures to look for, in rising order of cost: an entry whose Player Summary hands over everything, so nothing rewards acting on the room; an entry that reads empty because all of it sits behind a clue; and the one that matters most, a concealed detail whose Clue is stated nowhere in the obvious tier, which is content the referee knows and the players can never reach. Check the region as a whole too, since the secret tier is rationed rather than universal: a region where every room hides something teaches players to search every room, and one where no room does teaches them to stop - `patterns/dangerous/Low.md`'s split rates exist to hold that line, so a region that has drifted off them is the finding.
- **Recurring elements actually recur** - do Bestiary creatures, Factions, Lore, Keys, Named Creatures, and Unique Treasures referenced across multiple locations/regions stay consistent and build on each other, rather than each location inventing something new that never resurfaces?
- **Genre held across levels** - does the setting still read as Low Magic / Points of Light / Mythic Underworld at every level, or has drift crept in at the region or location level that the setting-level documents don't have (an implied central authority, commonplace magic, an authored plot rather than a situation)?
- **The three tests, hardest at the top** - open `STYLE.md` to **What a line has to earn** and apply its three tests, as written there, to every sentence of the setting-level files and each Region Overview, line by line. They fail most often above the location level, because a location has to be run at a table and a Region Overview does not.
- **Claims made upward are kept downward** - the one audit no mechanical check can do, and the only item on this list that reads *upward* rather than down. For every claim a setting-level file or a Region Overview makes, is there a location that delivers it? A truth's Handle names a real Location Code; a History event's Left line names a real Location Code; a treasure table a region says it leans on is actually cited by a room; a creature a region places somewhere is named in a room there; a motif a region says repeats throughout is present in the entries it applies to rather than a third of them. Fill in whatever Handle or Left line a real location already earns. A claim with nothing under it yet is **not** cut - the claim already earned its place at the level that stated it; what's missing is only that no location has grown into it yet. Name it under Room to Grow instead, specific enough that the next location or revision can act on it.
- **Reinforcement candidates are named, not acted on** - which elements are thin enough on the ground that a later pass could thicken them? An element cited in one location that the setting leans on, a motif shown once where recognition would pay, a name met in a single place. Name them under Room to Grow with where they already appear. **This check authors nothing**: acting on a candidate is a decision made outside the numbered build, and naming one here is a recommendation rather than a task.
- **Vocabulary is precise, and precise is not decorative** - the one register audit nothing mechanical can perform, since `tools/validate_setting.py` can count a segment but cannot tell a term used correctly from one used approximately. Three failures, in rising order of cost. A **gloss** - a specialist term followed by its own definition, which pays for the same fact twice and is the tell that the writer did not trust the word (*Corbelled Ceiling: the ceiling steps inward in courses rather than arching*). A **decoration** - an archaic or elevated word that names no referent a party could be shown, which is mood wearing a scholar's coat and is already cut by `STYLE.md`'s first test. And the one that matters most, a **misuse** - a term applied to the wrong thing, which is worse than the plain word would have been, because a referee who half-knows it will describe the wrong thing to the players and the error reaches the table. Check the per-rating `**Vocabulary.**` patterns in the `Dressing.md` and mechanism files are actually being drawn on, too: a rating whose entries never reach for its own compiled list has drifted to a general register, and the list is then either wrong for this build or unread.
- **Coinage is tracked, not orphaned** - every proper noun `setting/Language.md` records as "coined here" is used somewhere in the setting, and every proper noun the setting actually coined is recorded there. A name invented once and never touched again is either placed (record it and cite it) or genuinely dropped - but a gap between the two is a Room to Grow item, not a silent loss.

## Template
```
# Setting Judgement Check - [Date or revision note]

## Setting-level
- Discrete and discoverable, not vague: [Confirmed / Needs Attention - note]
- Genre held across levels: [Confirmed / Needs Attention - note]
- Recurring elements actually recur: [Confirmed / Needs Attention - note]
- Vocabulary precise, not decorative: [Confirmed / Needs Attention - note]

## Region [Code]
- Region reinforces the setting: [Confirmed / Needs Attention - note]
- Locations reinforce this region: [Confirmed / Needs Attention - note]
- Information tiered, and the chain holds: [Confirmed / Needs Attention - note]
- Secret tier rationed across the region: [Confirmed / Needs Attention - note]

[repeat per region]

## Room to Grow
[Claims made upward with no location under them yet, untracked coinage, and reinforcement
candidates - not defects, just named openings for the next location or revision to grow into]
- [Claim, and where it's made] - [what's missing, specific enough to act on]
- [Element thin on the ground] - [where it already appears, and where it could be reinforced]

## Open Items
- [Anything flagged Needs Attention, carried forward as an action item]
```
