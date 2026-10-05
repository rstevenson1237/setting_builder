# Bestiary.md

## Purpose
Reusable, system-neutral creature templates for the setting.

## Context
Read first:
- `GENRE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- `patterns/setting/Bestiary.md`
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`

## Instructions
Each entry is one record following `patterns/setting/Bestiary.md`'s Spec for a single entry.

By default the Bestiary is barebones: only the entries `BRIEF.md` or the user's prompt
names, and it grows as the build needs it - a location or Region Overview that needs a
creature the Bestiary lacks adds its entry here first, then cites it. The collection
shape below applies only where `BRIEF.md` or the prompt asks for a full Bestiary, and
wherever the brief states its own mix, the brief's mix replaces this one.

```
TYPE MIX - about 20 entries
  30%   Beast + Men          - specialized combatants that reinforce this setting specifically
  30%   Humanoid + Fantasy   - non-human peoples and setting-flavor creatures, for diversity
  30%   Anchors              - unique creatures a DANGEROUS region can be built around: the
                               undead, a guardian of a place, a creature that is itself a
                               hazard. Undead is one Type among these, never the whole share
  10%   Everything else      - Construct, Horror, Wyrm, Fey, Fiend, Giant, each a unique
                               challenge in its own right. Rarely more than two of these
                               types in one setting
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
  1     Modifiers and MAs spread above and below their averages - a collection sitting
        on its averages has thrown both fields away
```

**Coverage a full collection needs**, spread across the roughly 20 entries: something that
ranges rather than lairs, so a WILD region can meet the same thing twice; something that
lairs and cannot leave - young, stores, or a thing it guards; something a party can talk
to; something that will not fight and is a problem anyway; something small enough to be a
nuisance in numbers; something that eats what a settlement produces, so a SAFE region has a
standing grievance; something death-tainted that is a fact of the underworld rather than a
villain; something that was made rather than born.

Cut any field that does not fit the template block below, and any entry the collection
shape above does not call for.

## Template
```
Bestiary of [Setting Name]

### [Creature Name]
Type: [Type]
AD: [Xd6+N]
MA: [Y]
Description: [...]
Range: [...]
Sign: [...]
Disposition: [...]
Special: [... or `none` - one Special line per ability]
```
