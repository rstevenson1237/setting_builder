# Brief

This build's design requests: what this one setting should hold, as distinct from
`GENRE.md`, which holds what any setting of its kind holds, and every count, mix and rate
it is built to - the templates and patterns set none of their own. It never overrides a
pattern's rules or `STYLE.md`.

The test case: a setting whose shape a reader recognises as *Keep on the Borderlands* -
built fresh by the framework, not transcribed from the module.

## Setting

- One frontier, small enough to cross on foot in a day or two: a keep at the end of the
  road from the realm, the wilderness around it, and a ravine of caves beyond.
- The pressure is Chaos gathering in the caves and the raids it sends out along the road,
  not an invasion or a war. Nobody at the keep knows how many are out there.
- History is shallow. What the land held before matters through what the caves' earlier
  occupants left behind, not through a chronicle of kingdoms. No events up front.
- No truths up front.

## Language

- Three tongues: a common tongue for the living, an older tongue for ruins and the dead,
  and one non-human tongue. Each has three to six affixes and at least fifteen roots.

## Bestiary

- Up front, only the entries named here; the rest are added as a region or location needs
  them. By the end of the build the AD spread runs from people and numbers at 1-3 to at
  least one entry at 13+, with no more than a third sharing one AD.
- Specials are rare below 4 AD, expected at 4 and above, and several at 8 and above.
- Men are the rank and file a faction fields, never one entry per human occupation.
- Humanoids are the heart of it: several distinct tribes of Chaos, each a different people,
  each able to hold a cave complex of its own - small and many, mid-sized and organised,
  large and brutal.
- Men: the keep's soldiery and whoever preys on the road.
- Beasts that make the wilderness and the caves dangerous without being anyone's servant.
- A few things that are neither people nor animals - something that dissolves, something
  that hunts in a labyrinth - and a small body of undead serving the evil at the ravine's
  head.
- Undead are a minority here, not the backbone.

## Factions

Three, each showing at least two identity marks. At least one pair does not know the other
exists, and at least one is a faction a party can plausibly work for:
- The keep: its commander, its garrison, and the realm's claim they stand for.
- The shrine at the head of the ravine: priests of Chaos drawing the tribes together, with
  a hidden agent inside the keep.
- The tribes: rivals to one another before they are allies of anyone, each out for its own
  share of the ravine.

## Treasure

- Table II quality: poor 10%, normal 50%, fine 30% (a third of them carrying an effect),
  masterwork 5%, cursed 5%.
- One result in five carries a provenance.
- In each table, result 1 sits well below the table's average value; results 2 and 3 are
  each slightly below it, or about double the average weight for their value.
- No result is worth more than a hundred times its table's average; anything greater is a
  Unique Treasure.

## Regions

- Every region's die is d8, unless a line below gives a reason to move it.
- The keep (SAFE), the borderland wilderness around it (WILD), the ravine (WILD), and one
  DANGEROUS region per cave complex: about ten of them, each opening off the ravine.
- The keep is a hold: an outer bailey of trade, lodging and worship open to travellers,
  and an inner bailey closed to them. About twelve locations, each one a place a party
  would stop or be turned away from, with the garrison's gate and walls folded into the
  locations they guard rather than counted apart. Its People roster names five to eight.
- The wilderness holds about six Landmarks off the road - a lair, a raiders' camp, a
  hermit, a mound in a fen - with one or two carrying a Hidden child and none a Secret.
- One of those Landmarks is left for the referee to stock: it is generated with its
  Dressing, its Kind, its reason to stop and its name, and every rated line comes out
  `none`. Its entry says it is unstocked, so the gap reads as a decision rather than a
  draw that never fired.
- The ravine is the walk between the caves: about ten Landmarks, one per cave mouth, plus
  a few Hidden children for what lies along the ledges and floor. No Secrets. Each cave
  mouth Landmark is the only way into its cave's region.
- Each cave is a household - one tribe, one lair, or one shrine - and a DANGEROUS region
  of between four and fifteen locations, sized to what that household needs rather than to
  a set count. A cave has one entrance, the ravine's Landmark for it.
- Caves connect to each other in only a few places, and those connections decide who can
  reach whom; the shrine's cave lies deepest.

## Rumours

- A d20 table: about a third true, a third partly true, a fifth false, and the rest
  unverified - the referee's to settle.
- At least three point at a region rather than a detail, at least two are true and sound
  false, and at least one is false and sounds unmistakably true.

## Targets

Shares the tables are placed and filled toward, in the forms `tools/tables.py` reads.

```kdl
target Location.type High="20%" Medium="50%" Low="30%" rating=Dangerous
target Hazard.damage Lethal="20%" Damaging="40%" Nuisance="40%"
target Reward.contents Keys="20%" Lore="20%" "Unique Treasures"="5%"
```
