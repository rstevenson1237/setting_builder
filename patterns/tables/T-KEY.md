---
id: table.keys
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:T-ARC
  - table:T-PUZ
output_template: templates/table.md
schema_version: 1
---

`T-KEY` pairs every gate with the thing that opens it. It exists because a gate
and its key are two locations by definition, and that pairing is what makes them
checkable: `validate.py` asserts that both ends name a real location (M20).

**Columns:** `ID | Key | Found in | Opens | Notes`.

## Patterns

**The rows are written at step 10, not step 3.** Both ends name a location, and
locations are stubbed at step 9. Step 3 writes this file's guidance paragraph
and its columns; the Engineer fills the rows as gates are placed, and any row
written earlier names a location that does not exist and fails M20 outright.

**Both ends are location codes.** `Found in` is where the key is; `Opens` is
where the gate is. Prose beside the code is welcome and the code is what makes
the row a check rather than a note.

**A key is anything a party can carry, say, wear or do.** A rod, a tile, a
spoken name, a worn token, a bell clapper, a measurement. If it can be recorded
as found in one place and used in another, it is a key and it belongs here
rather than folded into `T-PUZ` or `T-ARC`, where neither end could be
validated.

**The two ends are never the same location.** A key found in the room it opens
is a delay, and the pairing has no distance to give it meaning.

**Every gate has an answer that is not the key, and the `Notes` column carries
it.** Not a second door: a longer road, a darker road, or a road watched by
something worse, and it is priced. Both branches are costed and the content
never says which is the mistake.

**The key's cost is stated.** Whether it is consumed, whether it stays in the
gate, whether taking it back closes the way again. A key that is free to use and
free to keep is a formality.

**A key may be a whole clue chain.** Where the key is a spoken name, the name
is in `T-LNG`, the record of it is in `T-LOR`, and the row here names the
location the record is found in. That is the pairing at its best.

## Excluded patterns

- **A row without a location code at either end.** M20 exists for this.
- **A row written before its locations exist.** It is a hard error, not a
  deferred one.
- **A key found in the same location as its gate.**
- **A gate with no alternative route.** Every gate has a priced answer that is
  not the gate (J3).
- **A key that only opens a door.** The best keys open a route, a machine, a
  conversation, or a place that was already open and is now safe to enter.
- **A masterwork lock with an ordinary key.** If the answer is a physical key
  and nothing else, the gate was a delay.

## Design questions

Asked at step 10, when the locations exist.

1. **Which gates in this region are opened by something carried from
   elsewhere?**
2. **For each: where is the key, and what does a party give up to use it?**
3. **What is the priced answer that is not the key?**
4. **Is the key consumed, held in place, or recoverable?**
5. **Which key is a spoken name or a piece of knowledge rather than an object,
   and where is it recorded?**
6. **Does any key open more than one gate, and does the party learn that
   before or after they spend it?**
