# Keys.md

## Purpose
A registry of physical objects that trigger something elsewhere - an actual key, a rod, a fitted gemstone, and the like. Generated in two phases: stubbed empty at step 2h, a stub row added per entry when a region is allocated (step 4d) or a composition is written (step 4e), and the full entry written once every row placing it exists (step 4h).

## Context
Read first:
- Step 2h (stubbing the file): no context needed.
- Steps 4d and 4e (recording a stub): `GENRE.md`, `templates/region/Allocation.md`.
- Step 4h (writing the full entry): `GENRE.md`, `setting/Setting.md`, `patterns/setting/Keys.md`, the table rows that place it - where the key lies, and the lock it opens.

## Instructions
- **2h**: create the file with only its title line.
- **4d, 4e**: append a stub row when a table row names a Key, and write its title into that row's cell. The row fills Name, Found at and Opens: **both locations**. The second is the obligation - the location it names draws the lock when it is generated, per `patterns/dangerous/Lock.md` - so it is written now, by code. Feature and the rest stay empty, because that feature does not exist yet.
- **4h**: fill each stub row's empty cells per `patterns/setting/Keys.md`.

## Template
```
Keys of [Setting Name]

| Name | Form | Found at | Opens | Feature | Apart | Connection |
|---|---|---|---|---|---|---|
| [Object Name] | [FORM] | [Location Code] | [Location Code] | [which Feature, and what it does] | [APART] | [CONNECTION] |
```
