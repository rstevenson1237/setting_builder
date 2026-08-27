---
id: region.engineer.connections
target: region
phase: engineer
writes: [Connections]
dependencies:
  - container:${CONTAINER_ID}
  - table:T-ARC
  - table:T-RUM
  - table:T-LOR
  - config
output_template: templates/region.md
schema_version: 1
---

Step 6. The Engineer settles the region-level containers, writes the region's
`sources`, and writes the Connections section that says what shape the region
is. It also opens `setting/regions/<region>/connections.md`, which is the source
of truth for every tier-3 and tier-4 edge.

The edges themselves cannot be written here, because a location-to-location edge
needs two locations and the locations are stubbed at step 9. What this step
decides is the frame those edges will be written into: how the region divides,
what a party is walking on between the divisions, and which table entries this
region has claimed as its own. Step 10 fills the table.

```
python tools/resolve_deps.py --pattern region.engineer.connections \
    --target R0n --var CONTAINER_ID=<setting-level-id>
python tools/mermaid_gen.py
```

## Patterns

**A container is a grouping and nothing else.** No file, no pattern, no phase,
no content. It exists so the diagram layer has a tier to draw, and a container
that starts acquiring lore is a location that has not been written yet. The
axis chosen at step 5 is confirmed or re-cut here, once, against what the region
actually turned out to be.

**Every container will hold locations, and a container holding one is a label.**
`validate.py` checks that every location names a declared container and that no
container stands empty, both from step 9 (M10). Judgement is the band: at a
region's weight, a container that will hold two locations is not a cut and a
container that will hold all of them is not either. Divide the weight roughly
evenly and expect one container to be the region's body.

**Write the Connections section as the region's shape, not as a list of edges.**
The edges live in `connections.md` and are drawn by `mermaid_gen.py`. What the
prose adds is what the graph cannot carry: which container is the spine, what a
party is walking on between two of them, and what makes crossing from one to the
next a decision. Four or five sentences, referee register.

**`sources` are `T` entry IDs and they are the region's claims.** A region cites
the recurring architecture it is built from, the rumours that point at it, and
the lore that explains what it was. `validate.py` fails on an `S` code at
location scale (M14) and on any ID that resolves to nothing (M16). At region
scale an `S` code is permitted and is still usually wrong: the S tables are the
setting's directing content, and a region that cites one directly has taken a
fact the T tables were carrying outward.

**A source is a claim, so two regions rarely cite the same row.** Where they do,
say what each takes from it, because a row two regions both own is a row neither
of them has read.

**More than one route reaches most places, inside a region as well as across the
setting.** The region graph written at step 10 is shaped by the containers cut
here. A region cut into a chain of three is a region where the third container
is gated on the second, whatever step 10 writes.

**Leave `connections.md` with its header row and no edges.** That is the correct
state at step 6, and `validate.py` defers its edge checks until step 10 for that
reason. An edge invented here names a location that does not exist and will be
rewritten by the step that does the work.

**Derive the diagrams after any container change.** `mermaid_gen.py` writes
every tier from these tables, and a renamed container leaves a tier-4 file
drawing a grouping that no longer exists. The regeneration removes it. M11 is
what catches it if the regeneration is skipped.

## Excluded patterns

- **Edges between locations.** Step 10. The locations do not exist yet, and a
  guessed edge becomes canon in a file the diagram layer reads.
- **A container that describes itself.** A name and an id. If it needs a
  sentence to justify it, the sentence belongs in the Connections section or in
  a location.
- **Difficulty, weight or type.** Set at step 5, and a number in two places is a
  number that will disagree with itself.
- **A hand-drawn diagram.** Every tier is derived, and the region file carries
  markers only (M13).
- **An `S` code in `sources`.** Permitted at this scale, refused at the next,
  and the reason it is refused is the boundary the S tables exist to hold.
- **Prose describing a location.** The region says what is between its places.
  What is at one of them is that location's, written at steps 9 to 12.

## Design questions

1. **Did the region turn out to be cut the way step 5 guessed?** State the axis
   again in one sentence. If it has changed, re-cut it now, because after step 9
   a re-cut moves every location's `container` field.
2. **Which container is the spine, and what is a party walking on between
   containers?** That answer is the Connections section.
3. **Roughly how does the region's weight divide across its containers?** Not a
   count, a share. Which one is the body?
4. **Which table rows does this region claim, and what does it take from each?**
   Name the claim, not just the ID.
5. **Where is the second route through the region?** A region cut into a chain
   gates each container on the last one, whatever step 10 draws.
6. **What does this region share with the one next door, and what does it
   refuse to share?** The container listing above names its neighbours. A border
   both sides describe the same way is a border neither has decided.
