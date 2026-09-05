# Bestiary.md

## Purpose
Reusable, system-neutral creature templates for the setting.

## Context
Consult when drafting:
- `GENRE.md` - low magic means most threats should be mundane, natural, or death-tainted rather than arcane.
- `patterns/setting/Bestiary.md` - the type mix, the AD spread, and the coverage the location patterns will ask for.
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md` - the material creatures should be drawn from or tied to.

## Instructions
Fix **party altitude** first - what the characters are and what they can expect to survive,
stated in dice (players run 1-6 dice of d4-d12, d6 average; per `GENRE.md`, "barely above
commoners" means a low count of ordinary dice). State it in a line at the top of this file.
The AD spread that follows is anchored to it and never to the region dice: a die is a
difficulty die and AD is a power count, and they are separate axes. A d8 region does not
want an 8 AD creature.

List reusable creature templates in a system-neutral rule set. Type mix, AD spread, and
what each entry must cover are in `patterns/setting/Bestiary.md`; AD, +/-N and MA scaling
are in `setting/Procedures.md`.

Every entry carries four lines. Description is prose; the other three are a clause each,
and they exist because the location patterns cite them rather than reinventing them per
location.

- **Range** - where it lives, how many the country supports, and what it eats.
- **Sign** - what a party finds before they find the creature.
- **Disposition** - what it does on being met, before anyone decides to fight.

Unique individuals go in `setting/NamedCreatures.md`, not here. One-off variants are
described inline at their location. The Bestiary holds only what recurs.

## Template
```
Bestiary of [Setting Name]

Party altitude: [what the characters are, in dice - what they can face, what they must avoid]

[Creature Name] (Type) - AD: Xd6 [+/-N] [MA: Y]
Description: [1-3 sentences of appearance and behaviour]
Range: [where it lives, how many, and what it eats]
Sign: [what a party finds before they find it]
Disposition: [what it does on being met, before anyone decides to fight]
```
