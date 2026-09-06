# Safe - Settlement

## Decides
What kind of settled place this is, which locations it can plausibly hold, and - for each
one - how much it matters, and what each Kind of location guarantees once chosen.

## Read at
Step 4c, before any other `safe/` file, for every SAFE location. Also read at 4a, which
takes its location list from here.

## Spec

```
SETTLEMENT TYPE
  {steading | thorp | village | town | seat}
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
  1     Kind, exactly one            {Commerce | Authority | Social | People | Wealth} -
        see the matching KIND block below for what each guarantees
  1     A person, drawn from the region's People roster - never invented here
        (Wealth locations may instead draw an owner who is absent, dead, or does not know
        the location is here)
  1     One thing obtainable here and not at the last location - a good, a service, a name,
        a permission, a place to stand
  1     What this place cannot do, and where it sends them instead
  1     Dressing, Secrets, Naming - unconditional, per those files

  liner note    nothing beyond the above. It does what a place like this does, and no more
  working       ONE hook   {Quest | Lore | Key | Faction}
  central       TWO hooks  {Quest | Lore | Key | Faction}, and this is the location where
                the region's Situation is most visible - see the SITUATION block below

  40%   The region's Situation visible in passing, at any prominence - see SITUATION below
  30%   A Named Creature, where the person will recur or be heard of first
  10%   A Secret, per safe/Secrets.md - a settlement-wide rate, not a per-location one
```

```
KIND: COMMERCE - hospitality, a trade, or works    (content in safe/Commerce.md)
  1     What it deals in, and who runs it - drawn from the region's People roster
  1     What is in stock, stated concretely
  1     What it cannot supply, and what it says to do instead
  1     Prices, in cn, for the two or three things a party will actually ask for
  40%   Something unusual in stock, and why it is here
  30%   A condition on trade - credit, membership, a grudge, a shortage
  20%   Something the proprietor wants that money will not buy
```

```
KIND: AUTHORITY - an office or a posting place     (content in safe/Authority.md)
  1     Who holds it here, and by what claim - elected, inherited, seized, granted, assumed
  1     What actually gets settled here, as opposed to what is claimed
  1     What a stranger must do to get a hearing
  1     The limit of the claim - where it stops being obeyed
  40%   A rival claim, and who backs it
  30%   Something posted, current, and specific
  20%   A custom a stranger will break without knowing
```

```
KIND: SOCIAL - a gathering place                   (content in safe/Social.md)
  1     Who is here, and what they are doing - not waiting to be talked to
  1     What is circulating: a rumour, drawn from setting/Rumours.md where one fits
  1     What it takes to be talked to rather than tolerated
  40%   A tension a stranger can be pulled into by doing nothing wrong
  30%   Somebody with a job to offer - see safe/Quest.md
  20%   Somebody who knows something and will not say it here
```

```
KIND: PEOPLE - a household                         (content in safe/People.md)
  1     Name, from the region roster - not invented here
  1     What they are doing when the party arrives
  1     One thing distinctive enough to be recalled a session later
  1     What they want, whether or not they are asking for it
  30%   A Named Creature row, where they will recur or be heard of first
  20%   An opinion about the region's Situation that is not the common one
```

```
KIND: WEALTH - a strongroom, hoard, shrine cache, or vault   (content in safe/Wealth.md)
  1     Contents                   {Treasure | Lore | Both}
  1     Who it belongs to, or belonged to - and whether they know it is still here
  1     Protection, exactly one    {hidden | gated | guarded | trapped}
  30%   A second protection, of a different kind than the first
  20%   Somebody else wants it, and is closer to getting it than the party
```

```
SITUATION, wherever it appears above                (content in safe/Situation.md)
  1     What is visibly different here because of it
  1     Who here is worse off, by name
  1     Which rung it is on, from the region's Situation field
  40%   Somebody here who benefits, and would rather it continued
  30%   What this location's people are doing about it, which is usually not enough
  20%   A way the party makes it worse by helping
```

**Decide prominence first, and do not derive it from size.** A crossroads shrine may be
central because the setting is about what is buried under it; a large market may be a liner
note because the party is passing through and the market is only a market. **The variance
is the point** - a settlement where every location is equally detailed reads as a
gazetteer, not a place.

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

**Commerce - the gap is more useful than the stock.** A party can assume a smith sells
nails; what changes their plans is that this smith has no steel until the barge comes, or
will not sell to them, or will trade but not for coin. State what is missing and where it
sends them - that is the line that turns a shop into a decision. **Prices are stated, not
implied** - two or three real numbers in cn. A location that makes the referee invent
prices at the table has left its job unfinished.

**Authority - Points of Light means no authority defaults to legitimacy.** Somebody is in
charge here because of a specific arrangement, and that arrangement has an edge past which
nobody is listening. State the edge - it is the most useful fact in the entry, and it is
where a party's leverage lives.

**Social - a rumour is repeated, not delivered.** Whoever says it has their own reason for
saying it, is probably wrong about part of it, and will not mark it true or false. Take the
substance from `setting/Rumours.md`; the framing belongs to whoever is talking. **Nobody is
waiting for the party** - everyone here has been having their evening since before the
party walked in, and the entry should say what that evening is.

**People - draw from the roster; do not invent a cast.** The region's People field lists
who is here. A location that invents its own people produces a settlement of strangers who
never meet each other, which is the failure the roster exists to prevent. If somebody is
needed who is not on the roster, add them to the roster. **Recall beats description** - a
party remembers one concrete thing (a scar, a habit, a grudge, a way of speaking, a thing
they carry) and forgets three sentences of appearance. Write the one thing.

**Wealth - Contents and Protection.** Treasure is cited from a table, per
`setting/Treasure1.md` through `Treasure5.md`, or stated as a Unique Treasure stub per
`patterns/setting/Keys.md`'s sibling registries. Lore follows `safe/Lore.md`'s fields -
physical form, whose voice, what it does - with one deliberate exception: `safe/Lore.md`
frames SAFE lore as *obtainable rather than discovered*, because its obstacle is normally a
living holder. A Wealth location's lore is the opposite case on purpose - nobody currently
holds it, or the holder does not know it is here - which is what makes it worth a
Protection line instead of an access clause.

Protection is exactly one, chosen for the Kind, not rolled. The four are not
interchangeable flavor text - each implies a different discovery structure:

- **hidden** reuses `safe/Secrets.md`'s Clue/Trigger/Payload structure directly, guaranteed
  by this spec line rather than by that file's own 10% settlement-wide roll. A Wealth
  location whose Protection is hidden has already spent its Secret; do not also roll
  `safe/Secrets.md`'s independent rate against it.
- **gated** means the cache's existence is known and unconcealed - access needs a stated,
  non-secret condition instead.
- **guarded** cites a creature already present in this region's Overview under Creatures,
  by name - per `patterns/region/Safe.md`, anything non-Man in a SAFE region is already
  working, penned, or a problem, and a guardian is the "working" case. Do not invent a new
  Bestiary entry here; if none fits, that is a signal to use a different Protection.
- **trapped** uses `setting/Procedures.md`'s impact tiers. A SAFE trap is usually
  somebody's work, not a dungeon mechanism: prefer an alarm, a marking dye, a lock that
  jams or maims, or a mechanism that ruins the goods rather than the person - a Lethal tier
  here should be rare and deliberate, reserved for a Wealth location the region's Situation
  already justifies treating that seriously. Write it in the same line format every Feature
  uses: `**Name:** tell; tell → effect; effect`.

**Nominal Authority does not stop at the wall.** Per `GENRE.md`, a settlement being SAFE
means it is safe from the wilderness, not that everything inside it is accounted for or
under anyone's real control - a Wealth location is where that gap becomes something a
party can act on.

**Situation - a condition, not a plot.** It is true whether or not the party engages, and
it moves on its own. Per `GENRE.md` the party are treasure hunters, not a resolution
mechanism, and the entry should read as something they walked into rather than something
waiting for them. **State the next rung** - the most useful line in a Situation entry is
what happens if nobody does anything, because that is what makes a party's inaction a
choice. A situation with no trajectory is scenery.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
