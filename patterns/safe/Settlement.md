# Safe - Settlement

## Provides
What kind of settled place this is, which locations it can plausibly hold, and - for each
one - how much it matters.

## Read at
Step 4c, before any other `safe/` file, for every SAFE location. Also read at 4a, which
takes its location list from here.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Every line is either an edge - it names a
file in parentheses, the only other file that line requires - or a question the generator
answers here.

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
  1     Secrets - whether it conceals anything, at the settlement-wide rate its file
        sets                                                         (safe/Secrets.md)

  -- gate: who stands between the party and what this place has
  1     A person, drawn from the region's People roster - never invented here
                                                                     (safe/People.md)
  1     What it takes to get anything out of them, stated as terms rather than a mood
        (A Wealth location may instead be gated by its Protection, its owner absent,
         dead, or unaware the place is here - see safe/Wealth.md)

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

  1     Naming, after everything above                                (safe/Naming.md)
```

**SAFE has no challenge block, and a gate instead.** A DANGEROUS location asks what opposes
the party; a settlement opposes nobody, and the thing actually standing between a party and
what they came for is a person with terms. That is the same slot, filled the way the rating
fills it - which is why the gate line is mandatory here and the Kind files no longer each
ask their own version of it.

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

**Naming comes last because a place is named for what turned out to be in it**, the same as
every other rating.

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

- **The gate is one line, here, and not five in the Kind files.** `safe/Authority.md`
  asked what a stranger must do to get a hearing, `safe/Social.md` what it takes to be
  talked to rather than tolerated, and `safe/Commerce.md` for a condition on trade -
  three phrasings of the question every SAFE location answers. A question all the drawn
  classes share belongs to the class drawing them; what stays in a Kind file is the menu
  of answers that kind supplies.
