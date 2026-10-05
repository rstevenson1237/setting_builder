# NamedCreatures.md

## Purpose
A registry of specific, named creatures that may appear in multiple locations and act on their own motivation, distinct from the reusable templates in `setting/Bestiary.md`. Generated in two phases: stubbed empty at step 2h, a stub row added per entry when a region is allocated (step 4d) or a composition is written (step 4e), and the full entry written once every row placing it exists (step 4h).

## Context
Read first:
- Step 2h (stubbing the file): no context needed.
- Steps 4d and 4e (recording a stub): `GENRE.md`, `templates/region/Allocation.md`.
- Step 4h (writing the full entry): `GENRE.md`, `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`, `setting/Bestiary.md`, `setting/Factions.md`, `patterns/setting/NamedCreatures.md`, and every table row that places this creature.

## Instructions
- **2h**: create the file with only its title line.
- **4d, 4e**: append a stub record - its heading and Appears at only - when a table row names a Named Creature (or when this creature is stubbed again at a second location, add that location to its existing Appears at rather than duplicating it), and write its title into that row's cell.
- **4h**: fill each stub record's remaining fields per `patterns/setting/NamedCreatures.md`.

## Template
```
Named Creatures of [Setting Name]

### [Creature Name]
Type: [Type]
AD: [Xd6+N]
MA: [Y]
Appears at: [Location Code(s)]
Role: [ROLE]
Motivation: [the standing goal driving this creature]
Reaches by: [how it reaches a party before it is met]
Remembers: [something specific it remembers]
Wants: [something specific it wants]
Description: [1-3 sentences, same style as a Bestiary entry]
Special: [what it can do that its Action Dice do not already say, or `none`]
```
