---
id: table.names
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:T-LNG
  - table:S-FAC
  - table:S-HIS
  - config
output_template: templates/table.md
schema_version: 1
---

`T-NAM` holds names built from the recorded roots, with the decomposition stated
beside each one so a referee can coin more in the same register. It is the
worked examples of `T-LNG`.

**Columns:** `ID | Entry | Roots | Used for`.

## Patterns

**Every name shows its work.** The `Roots` column decomposes the name into the
registry, in order, and the `Used for` column says what kind of thing takes a
name of this shape. A row that cannot state its roots is a name that should not
exist yet, and the root goes into `T-LNG` first.

**Cover both layers.** Some rows are living-layer compounds of plain words, some
are older-layer names from the recorded vocabulary. Where a place carries one of
each, write both rows and let the `Used for` column say that the two disagree.
That disagreement is the most useful thing this table does.

**Name kinds, not just places.** A setting needs names for roads, waters,
buildings, people, and the things the fallen power made. A table of place names
only leaves a referee inventing a person's name at the table with no pattern to
follow.

**A name states what the namer thought.** The older layer is often wrong about
what the place is now, because the place changed and the name did not. Say so in
`Used for`: it is how a referee reads a name as evidence.

**Ten to twelve rows, and they are a generator rather than a list.** A referee
holding this table should be able to coin a name for something it does not
cover. If they cannot, the rows are too specific or the `Roots` column is doing
too little.

**Names already in use in the corpus are recorded here.** The setting's name,
the container names and the region roster all decompose, and this is where the
decomposition is written down.

## Excluded patterns

- **A name whose roots are not in `T-LNG`.** M18 will find it as soon as the
  name reaches a region or a location.
- **A name with an apostrophe standing in for a vowel, or a name that needs a
  pronunciation guide.** If it cannot be said aloud at the table at speed it
  will not be said.
- **A name that describes its own significance.** "The Doom Gate" has spent the
  discovery.
- **A person's full biography in `Used for`.** People are `T-CRE`.
- **A name for a specific location that already exists.** That location names
  itself; this table names the kind.

## Design questions

1. **Which names does the corpus already owe a decomposition?**
2. **What does a road's name look like here, and a water's, and a building's?**
3. **How does a person's name work, and does it carry where they are from?**
4. **Which name in the older layer is now wrong, and about what?**
5. **What is the fallen power's own word for itself, and who still uses it?**
6. **Which two names would a party assume are related, and are they?**
