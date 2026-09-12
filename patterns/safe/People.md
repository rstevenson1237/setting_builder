# Safe - People

## Provides
Which individuals from the region's roster appear at this location, and what makes each
worth remembering.

## Read at
**Mode: kind, ingredient.** Step 4c, drawn twice by `safe/Settlement.md` and meaning two
different things: as a Kind, where the location *is* a household, and as the gate
block's mandatory person, which every SAFE location has whatever its Kind. Both draws
want the same fields, which is why there is one file. The roster itself is the Region
Overview's People field; this file turns a roster line into somebody at a location.
## Spec

```
PERSON
  1     Name, from the region roster - not invented here
  1     What they are doing when the party arrives
  1     One thing distinctive enough to be recalled a session later
  1     What they want, whether or not they are asking for it
  30%   A Named Creature row, where they will recur or be heard of first
  20%   An opinion about the region's Situation that is not the common one
```

**Recall beats description.** A party remembers one concrete thing - a scar, a habit, a
grudge, a way of speaking, a thing they carry - and forgets three sentences of appearance.
Write the one thing.

**Contract.** A People entry owes: a roster name (never invented here), what they're
doing, one distinctive, recallable thing, and what they want. Genre-neutral and
permanent. The personality flavor a "distinctive" thing draws on is not - the Personality
Examples below are this build's compile of it, from this setting's chosen genre
reference, standing in for what `GENRE.md` used to carry as its own People (personalities)
tag bank.

## Design patterns

**Personality flavor** - a one-word disposition a "distinctive" line can hang on, compiled
for this build: Treacherous, Fatalistic, Grasping, Superstitious, Proud, Servile,
Ruthless, World-Weary, Zealous, Craven, Calculating, Unbroken.

**What they are doing** - working, badly or well; eating; arguing with somebody who is not
present; counting; waiting for something specific; avoiding somebody; drinking earlier than
they should; teaching a child; repairing what they have repaired before; leaving.

**Distinctive** - a physical mark and the story it implies; a tic; a possession out of
keeping with their station; a phrase they reuse; a fear; a competence nobody expects; a
missing thing - a finger, a name, a tooth, a spouse; an animal that follows them; the way
they treat one particular other person.

**What they want** - out; in; a debt paid; a debt forgiven; somebody to be wrong; a child
safe; their old trade back; to be believed; to be left alone; to know what happened; more
than they have.

**When to make them a Named Creature** - they will appear at more than one location, or the
party will hear of them before meeting them, or they will be a problem later. Stat them per
`patterns/setting/Bestiary.md`, most often at 1-2 AD, and give them a motivation they act on
whether or not the party ever returns.

## Constraints

- **Draw from the roster; do not invent a cast.** The region's People field lists who is
  here. A location that invents its own people produces a settlement of strangers who
  never meet each other, which is the failure the roster exists to prevent. If somebody
  is needed who is not on the roster, add them to the roster.
