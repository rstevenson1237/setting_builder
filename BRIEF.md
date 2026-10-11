# Brief

This build's design requests: what this one setting should hold, as distinct from
`GENRE.md`, which holds what any setting of its kind holds, and every count, mix and rate
it is built to - the templates and patterns set none of their own. It never overrides a
pattern's rules or `STYLE.md`.

The test case: the thinnest setting that runs every step once - a keep, the ravine beyond
it, and one cave - whose shape a reader recognises as *Keep on the Borderlands*, built
fresh by the framework, not transcribed from the module.

## Setting

- One frontier, crossed on foot in half a day: a keep at the end of the road from the
  realm, a ravine beyond it, and one cave opening off the ravine.
- The pressure is a goblin tribe in the cave raiding the road, not an invasion or a war.
  Nobody at the keep knows how many goblins there are.
- History is shallow: what the land held before matters through what the cave's earlier
  diggers left behind. No events up front.
- No truths up front.

## Procedures

- B/X's own shape: hit points and saving throws stand behind every Test, and there is no
  madness track - Wounds and Madness covers wounds only.

## Language

- Three tongues: the common tongue of the keep and the realm; the goblins' tongue; and the
  dead tongue of the diggers, met only cut into the cave. Each has three to five affixes
  and fifteen to twenty roots.

## Bestiary

- Up front: goblin; wolf; the keep's soldier. The rest are added as a region or location
  needs them.
- Men are the rank and file a faction fields, never one entry per human occupation.
- Specials are rare below 4 AD, and expected at 4 and above.

## Factions

Two, each showing at least two identity marks:
- The keep: its commander, its garrison, and the realm's claim they stand for.
- The goblin tribe of the cave, out for what the road carries.

## Treasure

- Table II quality: poor 10%, normal 50%, fine 30% (a third of them carrying an effect),
  masterwork 5%, cursed 5%.
- One result in five carries a provenance.
- In each table, result 1 sits well below the table's average value; results 2 and 3 are
  each slightly below it, or about double the average weight for their value.
- No result is worth more than a hundred times its table's average; anything greater is a
  Unique Treasure.

## Regions

Three, in this order:
- The keep (SAFE, d8): a hold at the road's end. Four locations - its gate, an inn, a
  trader, and the commander's hall. Its People roster names four.
- The ravine (WILD, d8): the walk from the keep to the cave. Three Landmarks, one of them
  the cave mouth, which is the only way into the cave.
- The cave (DANGEROUS, d4): a single holding - the goblin tribe's home in an old dig. Six
  locations, one entrance.

## Rumours

- A d6 table: two true, two partly true, one false, one unverified - the referee's to
  settle.
- At least one points at the cave, and one is true and sounds false.

## Quests

- One quest, given at the keep.

## Targets

Shares the tables are placed and filled toward, in the forms `tools/tables.py` reads.

```kdl
target Location.type High="17%" Medium="50%" Low="33%" rating=Dangerous
target Reward.contents Keys="20%" Lore="20%"
```
