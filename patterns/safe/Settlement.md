# Safe - Settlement

## Provides
What kind of settled place this is, which locations it can plausibly hold, and - for each
one - how much it matters.

## Read at
Step 4c, before any other `safe/` file, for every SAFE location. Also read at 4a, which
takes its location list from here.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Where a line names a file in parentheses,
that is the only other file this line requires.

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
SAFE - INCLUSION                       (parameterized by prominence)
  1     Dressing and Secrets, unconditional          (safe/Dressing.md, safe/Secrets.md)
  1     Kind, exactly one   {Commerce | Authority | Social | People | Wealth}
          hospitality, trade, works   -> safe/Commerce.md
          office, posting place       -> safe/Authority.md
          gathering place             -> safe/Social.md
          household                   -> safe/People.md
          strongroom, hoard, vault    -> safe/Wealth.md
  1     A person, drawn from the region's People roster - never invented here (safe/People.md)
        (Wealth locations may instead draw an owner who is absent, dead, or does not know
        the location is here - see safe/Wealth.md)
  1     One thing obtainable here and not at the last location - a good, a service, a name,
        a permission, a place to stand
  1     What this place cannot do, and where it sends them instead

  liner note    nothing beyond the above. It does what a place like this does, and no more
  working       ONE hook   {Quest | Lore | Key | Faction}   (safe/Quest.md, safe/Lore.md,
                                                              safe/Key.md, safe/Faction.md)
  central       TWO hooks  {Quest | Lore | Key | Faction}, and this is the location where
                the region's Situation is most visible (safe/Situation.md)

  40%   The region's Situation visible in passing, at any prominence   (safe/Situation.md)
  30%   A Named Creature, where the person will recur or be heard of first
  10%   A Secret, per safe/Secrets.md - a settlement-wide rate, not a per-location one
```

**The two mandatory lines that are easiest to skip are the two that make a settlement
navigable.** *One thing obtainable here and not at the last location* is what stops ten
locations being ten shops - it is the reason a party goes to this door rather than that
one, and it has to be nameable. *What this place cannot do, and where it sends them
instead* is what turns a settlement from a menu into a map: a smith with no steel until the
barge comes has told the party where to go next and given them a reason to care about the
barge. Per `GENRE.md`, both are handles; a SAFE location without them is a description of a
building.

Prominence is decided here and recorded nowhere else - `Locations.md` carries name and tags
only for SAFE. Note it in the entry's own drafting and let the feature count carry it.

**Wealth is rarely a liner note.** A location whose whole premise is that something worth
protecting sits behind it has already earned working prominence at minimum - a liner-note
Wealth location is a contradiction unless the protection itself is the joke (a locked box
everyone knows is empty).

Per D17, extra weight in SAFE arrives as **more locations**, not heavier ones. A settlement
that matters gets a fuller list, not a longer entry per item.

## Constraints

- **Decide prominence first, and do not derive it from size.** A crossroads shrine may
  be central because the setting is about what is buried under it; a large market may be
  a liner note because the party is passing through and the market is only a market.
  **The variance is the point** - a settlement where every location is equally detailed
  reads as a gazetteer, not a place.
