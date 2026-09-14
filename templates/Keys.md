# Keys.md

## Purpose
A registry of physical objects that trigger something elsewhere - an actual key, a rod, a fitted gemstone, and the like. Generated in two phases: stubbed empty at step 2h, a stub row added per entry during location generation (step 4c), and the full entry written afterward (step 4d).

## Context
Read first:
- Step 2h (stubbing the file): no context needed.
- Step 4c (recording a stub): `GENRE.md`, `templates/Location.md`.
- Step 4d (writing the full entry): `GENRE.md`, `setting/Setting.md`, `patterns/setting/Keys.md`, the location file the stub points to, and (if it already exists) the location file it unlocks.

## Instructions
- **2h**: create the file with only its title line.
- **4c**: append a stub row when a location's Feature calls for a Key, and cite it in that Feature. The row names **both locations**: where the key is found, and the location it opens. The second is the obligation - the location it names draws the lock at rate `1` when it is generated, per `patterns/dangerous/Key.md` - so it is written now, by code. Which **feature** the lock sits on is not, because that feature does not exist yet.
- **4d**: replace each stub row with its full entry per `patterns/setting/Keys.md`.

## Template
```
Keys of [Setting Name]

[Object Name] (*form - key, rod, gemstone, seal, token, etc.*) - found at [Location Code] [Location Name]
Unlocks: [Location Code] [Location Name] - [which Feature, and what it does, written in step 4d]
```
