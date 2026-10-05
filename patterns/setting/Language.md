# Setting - Language

## Provides
One tongue - who speaks it, its sounds, and the roots names are built from - and the two
rules every artifact keeps when it coins or reuses a proper noun. How many tongues the
setting holds is `templates/setting/Language.md`'s; what a location is called, and in whose mouth,
is `patterns/setting/Naming.md`'s.

## Spec

```
TONGUE
  1     Who speaks it, and whether any of them are alive                 {SPEAKERS}
  1     A consonant inventory and a vowel inventory, audibly unlike every other
        tongue's in the setting
  1     A syllable shape, open or closed unlike the others'
  3-6   Affixes, each marking one thing                                    {AFFIX}
  15+   Roots, each a morpheme with a gloss, together covering every item   {ROOTS}
```

```
SPEAKERS - exactly one
  present      - the people living here now
  departed     - a people who were here, and are not
  arrived      - a people never here, whose tongue came by trade or conquest
  side         - everyone of one allegiance, whatever their people
  non-people   - something that is not a people
  jargon       - a trade's working tongue
  liturgy      - a register nobody speaks conversationally
```

```
AFFIX - each exactly one
  place        - a place, holding or settlement
  water        - water, and what kind
  diminutive   - smallness
  plural       - a plural or a collective
  possession   - belonging
  age          - old, first, or former
  direction    - direction or position
  negation     - negation
  title        - a title
```

```
ROOTS - every item
  ground       - ground and stone
  water        - water
  growth       - growing things
  weather      - weather and temperature
  colour       - colour
  body         - the body and its parts
  making       - making and breaking
  exchange     - taking and giving
  light        - light and dark
  dead         - the dead
  number       - number
  direction    - direction
```

```
REGISTER - whenever any step coins a proper noun
  1     Recorded under "Coined here", decomposed into its roots
  1     A name that cannot be decomposed is either wrong, or a loan word and marked as one
  1     Roots are added, never replaced
```

```
REUSE - whenever any artifact reuses a proper noun coined elsewhere
  1     Glossed where it appears - what it means, or who it was - so the referee is
        never sent to this file mid-session
  1     Coining happens at the setting and region level only. Nothing below coins; a
        location, a creature entry or a treasure entry reuses what already exists, or
        is named in the common tongue instead
```

## Constraints

- **Never two tongues on one inventory.** Two tongues sharing their sounds are one tongue
  with two names, and a party can no longer hear which culture a name came from.

- **Never a root list weighted toward abstractions.** It cannot name a hill.

- **Never coin without registering, never reuse without glossing.** A coinage left out of
  this file is stranded; a reuse with no gloss hands the referee a word it cannot
  translate.
