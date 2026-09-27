# Bestiary.md

## Purpose
Reusable, system-neutral creature templates for the setting.

## Context
Read first:
- `GENRE.md`
- `patterns/setting/Bestiary.md`
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`

## Instructions
Build about 20 entries, each one following `patterns/setting/Bestiary.md`'s Spec for a
single entry. The collection as a whole must hold this shape:

```
TYPE MIX - about 20 entries, drawn only from patterns/setting/Bestiary.md's TYPES list
  30%   Beast + Men          - specialized combatants that reinforce this setting specifically
  30%   Humanoid + Fantasy   - non-human peoples and setting-flavor creatures, for diversity
  30%   Undead               - what a DANGEROUS region is built around; some of these
                               entries should be built as a guardian (holds one thing,
                               does nothing else) or a hazard (a recurring danger, not
                               one room's trap) - both are roles any Type can carry, per
                               patterns/setting/Bestiary.md's Constraints
  10%   Everything else      - whatever remains of Construct, Horror, Wyrm, Fey, Fiend,
                               Giant, each a unique challenge in its own right. Rarely
                               more than two of these types in one setting
```

```
AD SPREAD - anchored to what GENRE.md's lethality establishes the party can survive,
NOT to the region dice
  1     At least six entries at 1-3 AD    - people, numbers, the things underfoot
  1     At least six entries at 4-8 AD    - the working middle of the setting
  1     At least two entries at 9-12 AD
  1     At least one entry at 13+
  1     At least one entry the party is NOT meant to beat
  1     No more than a third of entries sharing a single AD value
```

**Coverage the collection needs**, spread across the roughly 20 entries: something that
ranges rather than lairs, so a WILD region can meet the same thing twice; something that
lairs and cannot leave - young, stores, or a thing it guards; something a party can talk
to; something that will not fight and is a problem anyway; something small enough to be a
nuisance in numbers; something that eats what a settlement produces, so a SAFE region has a
standing grievance; something death-tainted that is a fact of the underworld rather than a
villain; something that was made rather than born.

Every entry states its modifier and its MA - both are written on every line, because both
carry their meaning in how far they sit from their average (one third of AD and one quarter
of AD respectively, each rounded up), and an omitted field says nothing at all.

## Template
```
Bestiary of [Setting Name]

[Creature Name] (Type) - AD: Xd6+N [MA: Y]
Description: [1-3 sentences - whichever of appearance, behaviour, range, sign, or
disposition this entry actually needs; none of these is mandatory on every entry]
Special: [what it can do that its Action Dice do not already say, or `none`]
```
