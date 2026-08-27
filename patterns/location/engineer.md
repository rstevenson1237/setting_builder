---
id: location.engineer.connections
target: location
phase: engineer
writes: [Exits]
dependencies:
  - region:${REGION_CODE}
  - siblings:location:${REGION_CODE}
  - container:${CONTAINER_ID}
  - table:T-ARC
  - table:T-KEY
  - table:T-PUZ
  - config
output_template: templates/location.md
schema_version: 1
---

Step 10. The Engineer closes the region's graph. It writes the edges into
`setting/regions/<region>/connections.md`, writes the matching Exits row into
every location at both ends, writes each location's `sources`, and writes a
`T-KEY` row for every gate it places.

The connections table is the source of truth and the Exits table is the
per-location view of the same edges. `validate.py` holds the two together from
both sides: M7 fails an exit with no row behind it, and M8 fails a row with no
exit in front of it. Neither is a formality. A graph that disagrees with the
files is a region a referee cannot run and a diagram layer drawing something
that is not there.

```
python tools/resolve_deps.py --pattern location.engineer.connections \
    --target R0n-L07 --var CONTAINER_ID=<region-level-id>
python tools/mermaid_gen.py
python tools/validate.py --scope R0n
```

## Patterns

**Write the whole region's table in one pass, then the Exits.** The edge is the
unit and it has two ends. Writing one location's Exits and moving on produces a
region where half the edges are one-way by accident, and `validate.py` reports
each of them separately at step 10 (M8), which is the expensive way to find out.

**Every edge is typed, and the type is what the crossing is made of.** Tier 4 is
the one tier that draws type, so this column is the whole of what the diagram
layer knows about how a region is traversed. `sunk span`, `stair`, `flooded
cut`, `pegged door`, `shaft`, `lane`: a noun a referee can picture. Not
`passage`, and not a compass bearing, which is a direction rather than a type.

**One-way is a physical fact and is written as one.** A drop, a slab that seats
behind, a climb that goes down and not up. Type an edge one-way only where the
far side states what makes it one-way, and expect to write that into the far
location's Features at step 11. Where One-way is `no`, both ends carry the exit
and `validate.py` checks it.

**More than one route reaches most places.** A region whose graph is a chain
gates every location on the one before it, and the party that fails the third
crossing has lost the region. Read the graph back when it is written: count the
locations with exactly one edge, and for each one say why the fiction refuses a
second. A landmark reachable one way only states the reason and states what the
one way costs in both directions.

**Every cue is sensory, stated from inside this location looking that way, and
carries a distance where there is one.** This is the requirement the
`DANGEROUS` type makes explicit and every type is better for. `East, low arch`
is a bearing. `East, low arch: the draught goes this way and takes a flame with
it` is a cue, and a referee reading only the Exits table can run the navigation.

**`sources` are `T` entry IDs and they are what this location is built from.**
An `S` code at location scale is refused outright (M14), because S content
reaches a player through a T table and never directly. Every ID resolves or
`validate.py` says so (M16). Cite what the location actually uses: the
architecture it is made of, the hazard its ground carries, the lore cut into
its wall, the creature standing in it. Four to six is the usual band, and a
location citing a dozen has usually cited the region's table rather than its
own content.

**Every `T` table is cited by at least one location before step 10 closes**
(M15). That is a whole-corpus check and it is this step's responsibility,
because nothing after it writes `sources`. Read the citation count across the
region roster and place the tables nothing has reached yet, at the locations
that have a reason for them.

**A gate and its key are two locations, and both ends go in `T-KEY`** (M20).
Write the row when the gate is placed, not afterwards. The row names the key's
location and the gate's location by code, and its `Notes` column carries the
answer that is not the key, priced. A gate whose row is missing is a gate whose
far end nobody has decided.

**Every gate has an answer that is not the gate, and both branches are edges.**
A longer road, a darker road, or a road watched by something worse. Both are in
`connections.md`, both are costed, and the text never says which is the
mistake. Where the bypass is cheaper in time, its cost is what the party arrives
without.

**Cross-region edges are written in the lower-numbered region's table.** One
row, one owner, and the location at the far end carries the reverse exit. The
tier-4 diagram draws only its own region's nodes, so the edge is correct in the
tables and simply not drawn on the far side, which is the intended behaviour and
not a gap.

**Derive the diagrams after any change to this table.** `mermaid_gen.py` writes
every tier from these rows, and M11 and M13 both fail against a stale
`build/diagrams/`.

## Excluded patterns

- **An exit with no row, or a row with no exit.** The two are one fact written
  twice, and the checks exist because they drift silently.
- **A compass bearing as a cue.** A bearing is where the exit is. A cue is what
  is noticed from here, and it is what navigation is played with.
- **A one-way edge for convenience.** One-way is a physical fact. Used to avoid
  writing the reverse exit, it makes a region that cannot be walked back out of.
- **A gate with one answer.** A gate with no answer is a wall, and a wall across
  a region is a region that cannot be played through.
- **An `S` code in `sources`.** Refused at this scale, and the refusal is the
  boundary the S tables exist to hold.
- **A `T-KEY` row written later.** Later is step 11, which is a Builder pass and
  does not write `sources` or edges. The pairing is placed here or it is not
  placed.
- **Prose.** This step writes a table, a field and a row. What the crossing is
  like is step 11's, and what it looks like is step 12's.

## Design questions

1. **What is the region's graph, drawn out?** Not a list of edges: the shape.
   Where is the second route, and which locations have exactly one edge?
2. **What is each crossing made of?** One noun per edge, and it is what tier 4
   will draw.
3. **Which edges are one-way, and what makes each one one-way from the far
   side?** That answer is content step 11 has to write.
4. **Where are this region's gates, and what is the answer to each?** Price both
   branches, and say what the cheaper one costs in what the party arrives
   without.
5. **Which `T` tables has this region not cited yet, and which location has a
   reason for each?** M15 is a corpus check and this is the last step that can
   answer it.
6. **What does each cue tell a party who cannot see the exit yet?** Read the
   Exits tables alone, as a referee would, and see whether the region can be
   navigated from them.
