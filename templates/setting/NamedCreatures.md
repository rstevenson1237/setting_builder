# NamedCreatures.md

## Purpose
A registry of specific, named creatures that may appear in multiple locations and act on their own motivation, distinct from the reusable templates in `setting/Bestiary.md`. Generated in two phases: stubbed empty at step 2h, a stub row added per entry during location generation (step 4c), and the full entry written afterward (step 4d).

## Context
Read first:
- Step 2h (stubbing the file): no context needed.
- Step 4c (recording a stub): `GENRE.md`, `templates/region/Location.md`.
- Step 4d (writing the full entry): `GENRE.md`, `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`, `setting/Bestiary.md`, `setting/Factions.md`, `patterns/setting/NamedCreatures.md`, and every location file that stubs this creature.

## Instructions
- **2h**: create the file with only its title line.
- **4c**: append a stub record - its heading and Appears at only - when a location's Feature calls for a Named Creature (or when this creature is stubbed again at a second location, add that location to its existing Appears at rather than duplicating it), and cite it in that Feature.
- **4d**: fill each stub record's remaining fields per `patterns/setting/NamedCreatures.md`.

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
