---
id: table.hoards
target: table
phase: decorator
writes: [Entries]
dependencies:
  - table:S-FAC
  - table:T-TR4
  - table:T-TR5
  - table:T-TRE
output_template: templates/table.md
schema_version: 1
---

`T-HRD` holds the bespoke named hoards: the accumulations that are shared by
construction because somebody in this setting put them together on purpose. It
is an artifact table — rows at step 3, and a Decorator pass at step 4.

**Columns:** `ID | Entry | Mechanics`. `decorate: true`.

## Patterns

**A hoard is here because it was assembled, not because it is large.** Composing
an ordinary hoard is a procedure: a location rolls the treasure tables at the
point of use, and that is `patterns/location/hoards.md`. A row in this table is
a specific collection with a reason for being one collection.

**Say who gathered it and why they stopped.** That is the row's content. A pile
with no gatherer is a random draw and it belongs in the procedure.

**A hoard is a place before it is a value.** How it is held, what it is in, what
order it is in, and what condition. A hoard sorted by size tells a party
something. One thrown down a shaft tells them something else.

**Name what is in it in kinds, and name the one piece that is specific.** The
bulk can cite the treasure bands. One item is named, and it is usually the
reason the hoard exists.

**Not all of it can leave.** Weight, bulk, fixture, or a piece that is owed to
somebody still here. The interesting decision in a hoard is what a party leaves
behind, and a hoard that fits in the packs has no decision in it.

**Six rows.** These are set pieces and each one is a location's whole reason for
existing. Six is enough for a setting of six regions, and the rest of the
setting's treasure comes out of the procedure.

## Excluded patterns

- **A random pile.** Use the procedure.
- **A total value with no itemisation.** A number is not a hoard.
- **A hoard with no owner, past or present.**
- **A hoard that is entirely portable.**
- **A dragon's hoard as a genre object.** If something is sitting on it, that
  thing is `T-CRE` and it wants something.
- **A hoard placed in a named location.** Placement is step 10 and step 11.
  These are composed before they are placed, which is why they are a table.

## Design questions

1. **Who in this setting gathers things, and what do they gather?**
2. **For each hoard: why did the gathering stop?**
3. **What is it held in, and in what order?**
4. **What is the one named piece, and which table is it from?**
5. **What cannot leave, and why?**
6. **Who else knows this hoard exists?**
