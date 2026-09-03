# Setting - Outline

## Decides
The shape of the setting before any of its content exists: how many regions, of what
ratings, at what dice, and what altitude the party plays at.

## Read at
Step 2a, immediately after `GENRE.md` and before `setting/Setting.md`. Everything
downstream depends on it - most sharply `setting/Bestiary.md`, which cannot scale its
creatures without knowing the region dice.

## Spec

```
OUTLINE
  1     Region count, and the code range they occupy
  1     Rating mix - how many SAFE, WILD, DANGEROUS
  1     A die per region, d4 to d12
  1     Party altitude - what the characters are, and what they can expect to survive
  1     The shortest complete loop: one SAFE, one WILD, one DANGEROUS
  30%   A second SAFE region, where the setting is about somewhere being contested
```

**Region dice are the setting's difficulty spine**, and fixing them here is what lets every
later artifact scale against them. A Bestiary written without them will not cover its own
regions - which is a failure that only shows up at 4c, three steps too late to fix cheaply.

**The shortest complete loop is one of each rating.** A setting needs somewhere to
resupply, somewhere to cross, and somewhere to go - and the smallest version of that is
three regions. More is a choice; fewer is missing a leg.

## Patterns

**Rating mixes** - one of each, the default and the shape of a starting setting; two WILD
between one SAFE and one DANGEROUS, where getting there is the point; one SAFE and two
DANGEROUS, where the setting is about a choice between two ways down; two SAFE with one
WILD between them, where the setting is about a road and who controls it.

**Die by rating** - SAFE runs low, d4 to d6, and the die measures how much trouble the
place can generate rather than how lethal it is. WILD runs middling to high, d6 to d12,
scaled to how far from settlement it sits. DANGEROUS runs by depth and age, d6 to d12 -
older and deeper is higher, and a d12 DANGEROUS region should be somewhere a starting
party is expected to retreat from.

**Party altitude** - treasure hunters barely above commoners, per GENRE.md. State what
that means numerically here: what AD a party can handle head-on, what it must avoid, and
what it must be clever about. Everything the Bestiary and the region dice do is measured
against this line.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
