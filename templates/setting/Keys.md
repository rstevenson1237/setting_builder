# Keys.md

## Purpose
A registry of physical objects that trigger something elsewhere - an actual key, a rod, a fitted gemstone, and the like. Generated in two phases: stubbed empty at step 2h, a stub row added per entry during location generation (step 4c), and the full entry written afterward (step 4d).

## Context
Read first:
- Step 2h (stubbing the file): no context needed.
- Step 4c (recording a stub): `GENRE.md`, `templates/region/Location.md`.
- Step 4d (writing the full entry): `GENRE.md`, `setting/Setting.md`, `patterns/setting/Keys.md`, the location file the stub points to, and (if it already exists) the location file it unlocks.

## Instructions
- **2h**: create the file with only its title line.
- **4c**: append a stub row when a location's Feature calls for a Key, and cite it in that Feature. The row fills Name, Found at and Opens: **both locations**. The second is the obligation - the location it names draws the lock when it is generated, per `patterns/dangerous/Lock.md` - so it is written now, by code. Feature and the rest stay empty, because that feature does not exist yet.
- **4d**: fill each stub row's empty cells per `patterns/setting/Keys.md`.

## Template
```
Keys of [Setting Name]

| Name | Form | Found at | Opens | Feature | Apart | Connection |
|---|---|---|---|---|---|---|
| [Object Name] | [FORM] | [Location Code] | [Location Code] | [which Feature, and what it does] | [APART] | [CONNECTION] |
```
