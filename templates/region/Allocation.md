# Allocation.md

## Purpose
Every table a region's locations are written from, created with its columns, and every row
the class files decide created as a stub with its tags settled. It is the row-level
counterpart of the gazetteer's guarantee: after this, every unit any location will hold
exists before any of it is written. This file is also the format every region table file
takes.

## Context
Read first:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- this region's Overview, `setting/region/[Region Code].md` - its Inhabitants and Loot are what the stubs are counted against
- this region's `Locations.md` and its connection diagrams
- the class file each row's Weight names - `patterns/safe/Settlement.md`; `patterns/wild/Landmark.md`, `patterns/wild/Hidden.md`, `patterns/wild/Secret.md`; `patterns/dangerous/High.md`, `patterns/dangerous/Medium.md`, `patterns/dangerous/Low.md` - and the pattern files they draw, for their draws
- the rating's file templates in `templates/safe/`, `templates/wild/` or `templates/dangerous/`, for which tables each file holds

## Instructions

### The table format
Every region table file - `Locations.md`, `Exits.md`, `Challenges.md`, `Treasures.md`,
`Links.md` - takes this shape. Which tables a file holds is its rating template's; which
columns a table has is its pattern's, per `patterns/SPEC.md`'s **How a Spec becomes
tables**.

- A table is a `## [Pattern name]` heading over a pipe table. Its columns, in order: the
  key; `Location` (on an exit, `From` and `To`); one column per Spec line, by its label, in
  Spec order; and `Realized`, last, on every table whose rows a location file shows as its
  own Feature or Exit - every table outside `Locations.md` except a kind table, and in
  `Locations.md` the class tables.
- The key is `Code` in `Locations.md`. Elsewhere it is `ID`, the table's prefix and a
  number, unique in the region and never reused. A kind table - one its classifier's Kind
  or Mechanism picks - keys its rows by the classifier row's ID and holds no `Location`.

```
PREFIXES
  EX  Exit, Door        EN  Encounter         CR  Creature         FA  Faction
  HZ  Hazard            MY  Mystery           TR  Treasure         LK  Lock
  QU  Quest             LO  Lore              KY  Key              SI  Situation
```

- A cell holds a tag (a draw's item, one or two words), a gloss (at most six words), an
  id, or a code - never a sentence. A rated line not taken is `none`. An empty cell is
  owed: a stub, which `python3 tools/validate_setting.py --pending` lists by step. `|` never
  appears in a cell.
- A line rated `2` takes numbered columns; a draw of "at least one" takes a comma-separated
  list in one cell.
- Every column exists from the table's creation. A later pass fills cells and never adds a
  column.

### Allocating
1. Create every file the rating's templates name, each table with its header row.
2. **Allocation decides every tag; the table passes write every gloss.** Walk each
   location's class file and every file it draws. Decide each rated line and each draw
   across the whole region at once, so the region's totals hold the rates: a rated line
   taken leaves its cells for the pass, one not taken writes `none`, and a draw writes its
   item.
3. A line that draws a unit creates that unit's row in its table, as a stub carrying its
   key, its `Location`, and every tag decided for it. A kind draw creates the row in the
   kind table it picked. A drawing line that names the row by id (a Guard, a Who, a Payload
   row) gets that id now.
4. One `Exits.md` row per edge of the region's diagrams, its Kind read off the edge and its
   gate decided once for the edge, and one per way off the map the Overview's Approach
   names, its `To` in plain terms. A cross-region edge's row lives in the region of its
   `From` location.
5. Where a row names a registry entry - a Keys, Lore or Quests row, a Named Creature, a
   Unique Treasure - append its stub to the setting file now, per that file's template, and
   write its title in the row's cell. A Keys stub names the location the key opens, which
   owes a lock: write that location's lock row now.
6. Before closing, count: the region's creature rows against the Overview's Inhabitants,
   and each rated line's share across the region against its rate. Correct by deciding
   again, never by leaving the count unmade.

## Template
```
# [File name] of [Region Code] [Region Name]

## [Pattern name]
| ID | Location | [Spec label] | [Spec label] | Realized |
|---|---|---|---|---|
| [XX1] | [Location Code] | [tag] | | |
```
