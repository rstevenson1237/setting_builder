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

**SAFE has no challenge block, and a gate instead.** A DANGEROUS location asks what opposes
the party; a settlement opposes nobody, and the thing actually standing between a party and
what they came for is a person with terms. That is the same slot, filled the way the rating
fills it, and why the gate line is mandatory here rather than restated per Kind.

**Transaction is SAFE's reward block**, and it is the pair of lines easiest to skip. *One
thing obtainable here and not at the last location* is what stops ten locations being ten
shops - it is the reason a party goes to this door rather than that one, and it has to be
nameable. *What this place cannot do, and where it sends them instead* is what turns a
settlement from a menu into a map: a smith with no steel until the barge comes has told the
party where to go next and given them a reason to care about the barge. Per `GENRE.md`,
both are handles; a SAFE location without them is a description of a building.

**The hooks are registry because of what they do, not how they are got.** A quest, a piece
of lore, a key and a faction all point the party at something that is not in this room -
which is the registry test. That a settlement hands them over through a person, rather than
leaving them to be found, is the gate's business and already stated one block up. This is
where SAFE parts from WILD, whose lore and keys are objects lying in open country and are
drawn in its reward block instead.

Prominence is decided here and recorded nowhere else - `Locations.md` carries name and tags
only for SAFE. Note it in the entry's own drafting and let the feature count carry it.

**Wealth is rarely a liner note.** A location whose whole premise is that something worth
protecting sits behind it has already earned working prominence at minimum - a liner-note
Wealth location is a contradiction unless the protection itself is the joke (a locked box
everyone knows is empty).

Per D17, extra weight in SAFE arrives as **more locations**, not heavier ones. A settlement
that matters gets a fuller list, not a longer entry per item.

**In a settlement a secret belongs to somebody, and that owner is the half that matters.**
A concealed cellar has a man who knows it is there; a false page in a ledger was written by
somebody still in the room. A dungeon's secret has nobody to notice it found - a
settlement's always does, which is why its Payload is not finished until it names who, how
soon, and what they do. That second half is usually worth more to the party than the
contents.

**Clues here are people and mismatches, not construction.** A room smaller inside than out;
a lock better than the door deserves; a stock that does not match the trade; an entry in a
ledger with no matching goods; a bricked opening; a key on a ring with nothing to open;
somebody's reaction to an ordinary question; a person never left alone with strangers.

## Constraints

- **Decide prominence first, and do not derive it from size.** A crossroads shrine may
  be central because the setting is about what is buried under it; a large market may be
  a liner note because the party is passing through and the market is only a market.
  **The variance is the point** - a settlement where every location is equally detailed
  reads as a gazetteer, not a place.

- **The gate is one line, here, and not one per Kind.** A question all the drawn classes
  share belongs to the class drawing them; what stays in a Kind file is the menu of
  answers that kind supplies. Several phrasings of the question every SAFE location
  answers is drift, not differentiation.

- **Never conceal something in a settlement that nobody living put there.** A concealed
  detail here has an owner, an heir, or a person who has been quietly maintaining it, and
  that person is what makes finding it a situation rather than a container. Ownerless
  concealment is a DANGEROUS device and reads as one the moment it is written here.
