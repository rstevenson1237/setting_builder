Procedures of Kordath

## Tests and Consequences
A Test is a single roll, made only where success and failure would each change what happens
next. Every Test names the attribute at stake: **Constitution** (the body), **Sanity** (the
mind), or **Fate** (nothing about the character, pure chance). Roll 1d20. A Test of
Constitution or Sanity succeeds on a result equal to or under that attribute's score; a Test
of Fate has no score to roll under, and succeeds on 11 or higher.

A failed Test of Constitution or Sanity forces the Xd the hazard states - see Hazards below
for what Xd means and what each tier allows. A failed Test of Fate forces no Xd at all: it
applies a Condition (see Conditions) or an Impact - ground the character has to reach, or
time they have to spend, before whatever is forcing the Test stops applying to them.

## Hazards
Every hazard rolls one of three tiers, fixed by the rating's own pattern file (a rate that
varies by rating belongs there, not here):

- **nuisance** forces no Test. It costs something stated outright - time spent, ground
  given up, noise made, position lost, or a piece of gear spoiled - and nothing more.
- **damaging** forces the Test its Feature line names. A failed Test of Constitution or
  Sanity costs 1d. A failed Test of Fate costs a Condition or an Impact instead.
- **lethal** forces the same Tests, at a higher cost: a failed Test of Constitution or
  Sanity costs 2d or 3d. A failed Test of Fate still costs only a Condition or an Impact -
  Fate is never scaled by Xd, whatever the tier.

**Xd is a count, not a die size.** Every d is the same six-sided die, rolled and summed: 1d
is 1d6, 2d is 2d6, 3d is 3d6. A Test of Constitution's Xd is lost as damage of the Feature's
stated Type, taken straight off current HP; the Type is one of six - Piercing, Crushing,
Poison, Fire, Frost, Blast - and a hazard draws only the one its own mechanism could actually
produce. A Test of Sanity's Xd is lost off current Sanity the same way, and carries no Type.
Xd never exceeds 3d; anything that would force more is an encounter, not a hazard, and
belongs in a Creature file instead.

## Wounds and Madness
A character reduced to 0 HP by a **damaging** hazard does not die: they carry a **Wound**
instead. The referee names it concretely - a scar, a limp, a broken finger - and it imposes
whatever penalty that injury would plainly cause until treated. A character reduced to 0 HP
by a **lethal** hazard dies outright; there is no Wound to carry.

Wounds accumulate. A character already carrying three dies the next time anything reduces
them to 0, whatever tier caused it.

Sanity works the same way, one level up. A character reduced to 0 Sanity carries a
**Madness** instead of losing the character: a compulsion, a fixation, or a fear, named
concretely and acted on whenever it applies, until treated. A character already carrying
three Madnesses is lost to play the moment a fourth would apply - the referee takes the
character from here, and the player brings someone new to the table.

HP and Sanity refill with rest and treatment. Wounds and Madnesses do not: only time, a
healer, or the specific thing that would plausibly mend that one removes it.

## Conditions
- **Poisoned** - every Test rolls at a -2 penalty while a toxin works through the body,
  until treated or a full day passes.
- **Bleeding** - 1 HP is lost at the start of every turn spent moving or fighting, until the
  wound is bound.
- **Prone** - the character is on the ground: an easy target, and can only crawl until an
  action is spent standing up.
- **Restrained** - held, tangled, or pinned: the character cannot move, and acts at
  disadvantage until freed.
- **Blinded** - the character cannot see, treats everything as unseen, and acts at
  disadvantage until sight returns.
- **Frightened** - the character cannot willingly approach whatever caused this, and acts at
  disadvantage while it is in sight, until the fear passes or is faced down.
- **Exhausted** - what the character can carry or force their body through is halved, until
  a full rest is taken.
- **Stunned** - the character takes no actions and cannot resist being acted on, usually for
  one round.

## Searching
Searching is never a Test. A stated detail, once investigated, is found; whatever chance
mattered was already resolved when the Feature was written. What a search costs is time: a
glance folds into whatever the character is already doing, but going through a container, a
body, or a room's own dressing costs one action (see Time) and finds only what that space's
own Feature or Dressing already states.

## Time
Each rating is tracked at the grain it actually needs:

- **SAFE** - ordinary time. A scene runs as long as it runs; nothing here is gated by a
  roll. What moves on its own clock is the settlement's Situation and its Events table (see
  Region Dice).
- **WILD** - the action. One action is four hours and buys exactly one of: a move between
  neighbouring Landmarks, a search of one Landmark, a forage, a tracking attempt, or making
  camp. Every action rolls one Difficulty roll (see Region Dice).
- **DANGEROUS** - the Danger countdown, not hours. Each meaningful action - a room searched,
  a fight finished, a door forced - rolls one Difficulty roll (see Region Dice), and the
  Danger track is what counts it down.

## Scaling
Three scales use dice, and none of them is the others:

- **Creature Action Dice (AD)** - d6 only, 1 to 18, an absolute measure of what a creature
  *is*. Fixed in `setting/Bestiary.md`.
- **Faction dice** - d6 only, no bonus, meaningful only measured against the other two
  factions' own dice. Fixed in `setting/Factions.md`.
- **The region die** - d4 to d12, a difficulty die fixed per region in
  `setting/region/Regions.md`, sized to how tense that region's own Difficulty roll should
  feel. It says nothing about what lives there.

Never read one scale against another: a d12 region is not weaker than a d4 one, a 3-die
faction is not a 3 AD creature, and a region's die says nothing about the creatures inside
it.

## Region Dice
Every region carries one die, d4 to d12, fixed at 3a per Scaling above. Every WILD or
DANGEROUS action rolls that die once - the **Difficulty roll** - and a result of 1 fails it:

- **WILD** - a failed Difficulty roll triggers the region's own d6 Encounter table.
- **DANGEROUS** - a failed Difficulty roll ticks the region's own d6 Danger table down one
  step, counting down from 6. Reaching 1 means the place is no longer merely noticing - it
  is acting.
- **SAFE** - carries no Difficulty roll. Its d6 Events table is rolled once on arrival and
  again each week the party stays.

A region's die size sets how many locations it holds, not how tough they are: about as many
WILD Landmarks as the die has faces, and about 3x the die in a DANGEROUS collection's
location count, both fixed at the region level per `patterns/region/Wild.md` and
`patterns/region/Dangerous.md`. This file states only the roll both of them depend on.
