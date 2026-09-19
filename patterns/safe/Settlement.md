# Safe - Settlement

## Provides
What kind of settled place this is, which locations it can plausibly hold, and - for each
one - how much it matters.

## Spec

```
SETTLEMENT TYPE
  {steading | thorp | village | town | seat} - read from the Region Overview's Layout
  field, stated once for the whole region. Do not re-decide it per location.
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
  1     Dressing - what it is, and the signs of what happens in it   (safe/Dressing.md)
  1     Kind, exactly one   {commerce | authority | social | people | wealth}
          hospitality, trade, works   -> safe/Commerce.md
          office, posting place       -> safe/Authority.md
          gathering place             -> safe/Social.md
          household                   -> safe/People.md
          strongroom, hoard, vault    -> safe/Wealth.md
  10%   A concealed detail, stated as:
          Clue    - a mismatch, or somebody's behaviour around an ordinary question
          Trigger - as often social as physical: asking the right person, being trusted,
                    being absent, buying what nobody buys, settling a debt
          Payload - what is concealed, AND who finds out the party knows, how soon, and
                    what they do about it

  -- gate: who stands between the party and what this place has
  1     A person, drawn from the region's People roster - never invented here
                                                                     (safe/People.md)
  1     What it takes to get anything out of them, stated as terms rather than a mood
        (A Wealth location may instead be gated by its Protection, its owner absent,
         dead, or unaware the place is here)

  -- transaction: what the party can get here
  1     One thing obtainable here and not at the last location - a good, a service, a
        name, a permission, a place to stand
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
```

**SAFE has no challenge block, and a gate instead.** A settlement opposes nobody, and what
stands between a party and what they came for is a person with terms - which is why the gate
line is mandatory here rather than restated per Kind.

**Transaction is SAFE's reward block**, and its pair of lines is the easiest to skip. *One
thing obtainable here and not at the last location* is what stops ten locations being ten
shops, and it has to be nameable; *what this place cannot do, and where it sends them
instead* is what turns a settlement from a menu into a map. Per `GENRE.md`, both are handles.

**The hooks are registry because of what they do**: a quest, a piece of lore, a key and a
faction all point the party at something not in this room. That a settlement hands them over
through a person is the gate's business, one block up - which is where SAFE parts from WILD,
whose lore and keys lie in open country and are drawn in its reward block.

Prominence is recorded nowhere else; `Locations.md` carries name and tags only for SAFE.
Per D17, extra weight in SAFE arrives as **more locations**, not heavier ones.

**Clues here are people and mismatches, not construction**: a room smaller inside than out;
a lock better than the door deserves; a stock that does not match the trade; a ledger entry
with no matching goods; a key on a ring with nothing to open; somebody's reaction to an
ordinary question.

## Constraints

- **Decide prominence first, and do not derive it from size.** A crossroads shrine may be
  central because the setting is about what is buried under it; a large market may be a
  liner note because the market is only a market. The variance is the point - a settlement
  where every location is equally detailed reads as a gazetteer, not a place.

- **Wealth is rarely a liner note.** A location whose whole premise is that something worth
  protecting sits behind it has earned working prominence at minimum.

- **The gate is one line, here, and not one per Kind.** A question all the drawn classes
  share belongs to the class drawing them; what stays in a Kind file is the menu of answers
  that kind supplies.

- **Never conceal something in a settlement that nobody living put there.** A concealed
  detail here has an owner, an heir, or somebody quietly maintaining it, and that person is
  what makes finding it a situation rather than a container. Its Payload is not finished
  until it names who notices, how soon, and what they do.
