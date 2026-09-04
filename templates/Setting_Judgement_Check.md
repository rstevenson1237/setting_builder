# Setting_Judgement_Check.md

## Purpose
A non-mechanical review pass over the generated `setting/` content - confirming, by human or model judgement, that the setting holds together thematically and structurally from location up through region up through the top-level setting, and that it's built from things a player can actually find rather than mood alone. Saved as `checks/SettingJudgementCheck.md`. Unlike `templates/Location.md`'s deliberately narrow generation-time Context, this check is the one place a full read across levels is appropriate, since coherence between levels is exactly what's being judged.

## Context
Consult when running this check - deliberately broader than any single generation step, since cross-level coherence is the thing being judged:
- `GENRE.md` - the throughline every level should still be expressing.
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md` - what every region should be reinforcing.
- `setting/region/Regions.md` and each region's `setting/region/[Code].md` overview - what every location in that region should be reinforcing.
- each region's `setting/region/[Code]/Locations.md` and its location files.
- `setting/Bestiary.md`, `setting/Factions.md`, `setting/Lore.md`, `setting/Keys.md`, `setting/NamedCreatures.md`, `setting/UniqueTreasures.md` - recurring elements that should be tying levels together rather than sitting isolated.

## Instructions
Run this once a region's locations are complete (or at the end of a full build), region by region. Record each as Confirmed / Needs Attention, with a note.

- **Locations reinforce their region** - does each location's tags, dressing, Features, and Dangers actually reflect the parent Region Overview's Ambiance/Features/Dangers/Creatures, rather than reading as a location that could belong to any region? For a WILD region, does its landmark/hidden/secret split roughly track the guidance in `templates/Location_Gazetteer.md` (landmark the majority, hidden a third, secret the remainder), and does every hidden or secret location's connection actually trace back to a stated detail or Feature at its parent, rather than existing with no link back?
- **Regions reinforce the setting** - does each Region Overview visibly connect back to `setting/Setting.md`/`History.md`/`Truths.md` (a named historical event, a faction's presence, a unique truth playing out), rather than feeling like an unrelated pocket bolted onto the setting?
- **Discrete and discoverable, not vague** - is content built from concrete, specific, discoverable details (a named object, a specific trigger, a specific creature or faction presence) that a player can find and act on, rather than an atmospheric motif repeated without ever cashing out into something discoverable? Per each rating's `Dressing.md` Position guidance, this includes whether Features and Exits actually state where in the room they sit and, when spatially significant, their own dimension - a Referee shouldn't have to improvise where something is, or find two same-type exits in one room indistinguishable.
- **Recurring elements actually recur** - do Bestiary creatures, Factions, Lore, Keys, Named Creatures, and Unique Treasures referenced across multiple locations/regions stay consistent and build on each other, rather than each location inventing something new that never resurfaces?
- **Genre held across levels** - does the setting still read as Low Magic / Points of Light / Mythic Underworld at every level, or has drift crept in at the region or location level that the setting-level documents don't have (an implied central authority, commonplace magic, an authored plot rather than a situation)?
- **The three tests, hardest at the top** - per `GENRE.md`'s **What a line has to earn**, read the setting-level files and each Region Overview line by line and ask three things of every sentence. *Did it survive translation* - does something reach the players from it, or does it only tell the referee how to feel about the place? *Does it name a handle* - an object, a person, a place, a number a party can act on? *Does it state a situation rather than a conclusion* - has the entry written down what the party will realise, what the encounter is really about, or what the correct play is? These fail most often above the location level, because a location has to be run at a table and a Region Overview does not.
- **Claims made upward are kept downward** - this is step 4e's audit and it is the one no mechanical check can do. For every claim a setting-level file or a Region Overview makes, is there a location that delivers it? A truth's Handle names a real Location Code; a History event's Left line names a real Location Code; a treasure table a region says it leans on is actually cited by a room; a creature a region places somewhere is named in a room there; a motif a region says repeats throughout is present in the entries it applies to rather than a third of them. A claim with nothing under it is cut from the file that made it, not defended.

## Template
```
# Setting Judgement Check - [Date or revision note]

## Setting-level
- Discrete and discoverable, not vague: [Confirmed / Needs Attention - note]
- Genre held across levels: [Confirmed / Needs Attention - note]
- Recurring elements actually recur: [Confirmed / Needs Attention - note]

## Region [Code]
- Region reinforces the setting: [Confirmed / Needs Attention - note]
- Locations reinforce this region: [Confirmed / Needs Attention - note]

[repeat per region]

## Open Items
- [Anything flagged Needs Attention, carried forward as an action item]
```
