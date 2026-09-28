# Safe - Settlement

## Provides
One SAFE location: which Kind of place it is, how much it matters, who stands between the
party and what it has, and what the party can get there. The settlement as a whole is its
Region Overview's.

## Spec

```
SETTLEMENT TYPE
  1     The settlement's type, from the Region Overview - never re-decided per location
```

```
PROMINENCE - decided per location, before anything is written
  liner note   - it does what everyone expects a place like this to do, and no more.
                 One or two features. Most locations in most settlements
  working      - it has a person, a want, or a wrinkle worth remembering. Three or four
  central      - the settlement is partly about this place. Five or more, and it is where
                 the region's Situation is most visible
```

```
SAFE - LOCATION                        (parameterized by prominence)

  -- substrate: what this place is
  1     Prominence                                                     {PROMINENCE}
  1     Dressing - what it is, and the signs of what happens in it   (safe/Dressing.md)
  1     Kind   {commerce | authority | social | people | wealth | garrison}
                        (safe/Commerce.md, safe/Authority.md, safe/Social.md,
                         safe/People.md, safe/Wealth.md, safe/Garrison.md)
  10%   A concealed detail, stated as:
          Clue    - {mismatch | behaviour}: the building or its stock disagreeing with
                    itself, or somebody acting wrongly around an ordinary question
          Trigger - as often social as physical
                    {asking | being trusted | being absent | buying | settling a debt |
                     handling}
          Payload - what is concealed, AND who finds out the party knows, how soon, and
                    what they do about it

  -- gate: who stands between the party and what this place has
  1     A person, drawn from the region's People roster - never invented here
                                                                     (safe/People.md)
  1     What it takes to get anything out of them, stated as terms rather than a mood
        (A Wealth location may instead be gated by its Protection, its owner absent,
         dead, or unaware the place is here)

  -- transaction: what the party can get here
  1     One thing obtainable here and not at the last location
                        {good | service | name | permission | place to stand}
  1     What this place cannot do, and where it sends them instead

  -- registry: what ties this place to the rest of the settlement and beyond
  liner note    nothing beyond the above. It does what a place like this does, and no more
  working       ONE hook   {quest | lore | key | faction}    (safe/Quest.md, safe/Lore.md,
                                                              safe/Key.md, safe/Faction.md)
  central       TWO hooks  {quest | lore | key | faction}, and this is the location where
                the region's Situation is most visible        (safe/Situation.md)
  40%   The region's Situation visible in passing, at any prominence
                                                              (safe/Situation.md)
  30%   A Named Creature, where the person will recur or be heard of first
                                                   (patterns/setting/NamedCreatures.md)

  1     Naming, after everything above                 (patterns/setting/Naming.md)
  20%   A second name, from a different mouth than the first
                                                       (patterns/setting/Naming.md)
```

## Constraints

- **Decide prominence first, and never derive it from size.** A crossroads shrine may be
  central because the setting is about what is buried under it; a large market may be a
  liner note. A settlement where every location is equally detailed reads as a gazetteer,
  not a place.

- **Never write a location heavier to make it matter.** A settlement that matters gets
  more locations, not longer ones; prominence is carried by the feature count and recorded
  nowhere else.

- **Never a liner-note Wealth location**, unless the protection itself is the joke. A
  place whose premise is that something worth protecting sits behind it is working at
  least.

- **Never conceal something in a settlement that nobody living put there.** A concealed
  detail here has an owner, an heir, or somebody quietly maintaining it; ownerless
  concealment is a DANGEROUS device.
