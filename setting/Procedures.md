Procedures of Greywatch

## Tests and Consequences
A Test is a single roll, called only where success and failure would each lead somewhere
different. Every Test names what's on the line: **Constitution** (the body), **Sanity**
(the mind), or **Fate** (nothing about the character, pure chance). Roll 1d20. A Test of
Constitution or Sanity succeeds on a result equal to or under that attribute's score; a
Test of Fate has no score to roll under, and succeeds on 11 or higher.

A failed Test of Constitution or Sanity forces the Xd the hazard's tier allows - see
Hazards below for what Xd means and what each tier forces. A failed Test of Fate forces no
Xd at all: it applies a Condition (see Conditions) or an Impact instead - ground given up,
or time spent, before whatever forced the Test stops mattering.

## Hazards
Every hazard rolls one of three tiers, fixed by the rating's own pattern file - a rate that
varies by rating belongs there, not here:

- **nuisance** forces no Test. It costs whatever the Feature line states outright - time,
  ground, noise, a torch burned early, a piece of gear spoiled - and nothing beyond that.
- **damaging** forces the Test the Feature line names. A failed Test of Constitution or
  Sanity costs 1d. A failed Test of Fate costs a Condition or an Impact instead.
- **lethal** forces the same Tests, at a harder cost: a failed Test of Constitution or
  Sanity costs 2d or 3d. A failed Test of Fate still costs only a Condition or an Impact -
  Fate is never scaled by Xd, at any tier.

**Xd is a count, not a die size.** Every d is the same six-sided die, rolled and summed: 1d
is 1d6, 2d is 2d6, 3d is 3d6. A Test of Constitution's Xd comes off current HP as damage of
the Feature's stated Type - one of six: Piercing, Crushing, Poison, Fire, Frost, or Blast -
and a hazard only ever delivers a Type its own mechanism could plausibly produce. A Test of
Sanity's Xd comes off current Sanity the same way, and carries no Type. Xd never runs past
3d; anything that would force more belongs to a Creature, not a hazard.

## Wounds and Madness
A character brought to 0 HP by a **damaging** hazard doesn't die: they carry a **Wound**
instead, named plainly by the referee - a broken finger, a limp, a scar that pulls - and it
costs whatever that injury would plainly cost until it's treated. A character brought to 0
HP by a **lethal** hazard dies outright, with no Wound to carry it - a first blow at low
level can already be the one that ends the character.

Wounds pile up. A character already carrying three dies the next time anything brings them
to 0, whichever tier does it.

Sanity works the same, one level up. A character brought to 0 Sanity carries a **Madness** -
a fixation, a compulsion, a fear - named plainly and played out whenever it applies, until
it's treated. A character already carrying three is lost to play the moment a fourth would
apply: the referee keeps the character, and the player brings someone new to the table.

Rest refills HP and Sanity. Neither refills a Wound or a Madness - only time, a healer, or
the one thing that would plausibly mend that specific one does.

## Conditions
- **Poisoned** - every Test rolls at a -2 penalty while the toxin runs its course, until
  treated or a full day passes.
- **Bleeding** - 1 HP is lost at the start of every turn spent moving or fighting, until the
  wound is bound.
- **Prone** - flat on the ground: an easy target, and able only to crawl until an action is
  spent standing back up.
- **Held** - caught, tangled, or pinned: unable to move, and acting at disadvantage until
  freed.
- **Blinded** - unable to see: everything is treated as unseen, and every action is at
  disadvantage until sight returns.
- **Frightened** - unable to willingly close with whatever caused this, and at disadvantage
  while it's in sight, until the fear passes or is faced down.
- **Exhausted** - whatever the character can carry or force their body through is halved,
  until a full rest is taken.
- **Paralyzed** - no actions, and no resisting anything done to them, for as long as the
  Feature or Creature that caused it states.

## Searching
Searching is never a Test. Whatever a Feature or a room's own Dressing already states is
found once looked for - the chance that mattered was already spent writing it down. What a
search costs is time: a glance folds into whatever the character is already doing, but
going through a container, a body, or a room's dressing costs one action (see Time), and
turns up nothing beyond what that space's own Feature or Dressing already names.

## Time
Each rating runs on the grain it actually needs:

- **SAFE** - ordinary time. A scene runs as long as it runs, and nothing here answers to a
  roll. What moves on its own clock is the keep's Situation and its own Events table (see
  Region Dice).
- **WILD** - the action. One action spends four hours and buys exactly one of: a move
  between neighbouring Landmarks, a search of one Landmark, a forage, a tracking attempt,
  or making camp. Every action rolls one Difficulty roll (see Region Dice).
- **DANGEROUS** - the Danger countdown, not the clock. Each meaningful action - a room
  searched, a fight finished, a door forced - rolls one Difficulty roll (see Region Dice),
  and the Danger track is what it counts down.

## Scaling
Three scales use dice, and none of them reads against the others:

- **Creature Action Dice (AD)** - d6 only, 1 to 18, a flat measure of what a creature *is*.
  Fixed in `setting/Bestiary.md`.
- **Faction dice** - d6 only, no bonus, and meaningful only set against another faction's
  own dice. Fixed in `setting/Factions.md`.
- **The region die** - d4 to d12, a difficulty die fixed per region in
  `setting/region/Regions.md`, sized to how tense that region's own Difficulty roll should
  feel. It says nothing about what lives there.

A d12 region isn't more dangerous than a d4 one, a 3-die faction isn't a 3 AD creature, and
a region's die says nothing about the creatures inside it - reading one scale against
another is always a mistake.

## Region Dice
Every region carries one die, d4 to d12, fixed at 3a per Scaling above. Every WILD or
DANGEROUS action rolls that die once - the **Difficulty roll** - and a result of 1 fails it:

- **WILD** - a failed Difficulty roll triggers the region's own d6 Encounter table.
- **DANGEROUS** - a failed Difficulty roll ticks the region's own d6 Danger table down one
  step, counting from 6. Reaching 1 means whatever the block holds stops merely noticing and
  starts hunting.
- **SAFE** - carries no Difficulty roll. Its own d6 Events table is rolled once on arrival,
  and again each week the party stays.

A region's die size sets how many locations it holds, not how tough they are: about as many
WILD Landmarks as the die has faces, and about 3x the die in a DANGEROUS collection's
location count, both fixed at the region level per `patterns/region/Wild.md` and
`patterns/region/Dangerous.md`. This file states only the roll both of them depend on.
