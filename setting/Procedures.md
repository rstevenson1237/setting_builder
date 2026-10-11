Procedures of [Setting Name]

## Tests and Consequences
A Test is one roll, called only where success and failure lead somewhere different. A
**Test of Constitution** is the saving throw that fits what threatens the body - poison,
paralysis, a breath, a blast - made against the character's own save. A **Test of Fate**
puts nothing of the character on the line: roll 1d20, and 11 or higher succeeds. There is
no Test of Sanity.

A failed Test of Constitution forces the Xd its hazard's tier allows. A failed Test of Fate
forces no Xd: it applies a Condition, or an Impact - ground given up or time spent before
whatever forced the Test stops mattering.

## Hazards
Every hazard is one of three tiers:

- **Nuisance** forces no Test. It costs what its Feature states - time, ground, noise, a
  torch burned early, a piece of gear spoiled.
- **Damaging** forces the Test its Feature names. A failed Test of Constitution costs 1d.
- **Lethal** forces the same Test at a harder cost: 2d or 3d.

A failed Test of Fate costs a Condition or an Impact at any tier, never Xd.

**Xd is a count of six-sided dice**, rolled and summed: 1d is 1d6, 3d is 3d6. It comes off
current hit points as damage of the Feature's stated Type - Piercing, Crushing, Poison,
Fire, Frost or Blast - and a hazard delivers only a Type its mechanism could produce. Xd
never runs past 3d; anything that forces more is a creature, not a hazard.

## Wounds and Madness
A character brought to 0 hit points is dead. Hit points come back with rest, 1d3 for each
full day of it. Nothing else lingers.

## Conditions
- **Paralysed** - no actions, and no resisting anything done to them, for 2d4 turns.
- **Held** - caught, tangled or pinned: no moving, and every attack against them hits,
  until freed.
- **Prone** - flat on the ground: crawling only, until an action is spent standing.
- **Blinded** - unable to see: no attacking what cannot be heard, and no reading, until
  sight returns.
- **Frightened** - unwilling to close with what caused it, for as long as it is in sight.

## Searching
Searching is never a Test. What a Feature states is found once it is looked for; what a
Secret hides is found by acting on its trigger, never by a roll. Going through a room, a
body or a container costs one action (see Time).

## Time
- **SAFE** - ordinary time. Nothing answers to a roll; the region's Events table moves on
  its own (see Region Dice).
- **WILD** - one action is four hours, and buys one of: a move between neighbouring
  Landmarks, a search of one Landmark, a forage, a tracking attempt, or making camp.
- **DANGEROUS** - one action is a ten-minute turn, and buys one of: a move between
  neighbouring rooms, a search, a fight, a door forced, a rest.

## Scaling
Three scales use dice, and none is read against another:

- **Creature Action Dice (AD)** - d6 only, 1 to 18: what a creature is. Fixed in
  `setting/Bestiary.md`.
- **Faction dice** - d6 only, meaningful only against another faction's. Fixed in
  `setting/Factions.md`.
- **The region die** - d4 to d12: how tense a region's Difficulty roll is. Fixed in
  `setting/region/Regions.md`. It says nothing about what lives there.

## Region Dice
Every WILD or DANGEROUS action rolls its region's die once - the **Difficulty roll** - and a
1 fails it:

- **WILD** - a failed roll triggers the region's d6 Encounter table.
- **DANGEROUS** - a failed roll ticks the region's d6 Danger table down one step, from 6.
  At 1, the place stops noticing and starts acting.
- **SAFE** - no Difficulty roll. The region's d6 Events table is rolled on arrival, and
  each week the party stays.
