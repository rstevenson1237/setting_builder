---
id: setting.engineer.connections
target: setting
phase: engineer
writes: [Regions]
dependencies:
  - config
output_template: templates/setting.md
schema_version: 1
---

Step 2. The Engineer settles the setting-level containers, writes the region
roster into the Regions index, and writes `setting/connections.md`.

The roster comes before the connections because a region-to-region edge cannot
be written between two regions that have not been named. It comes before
Milestone 5 because step 5 stubs one `region.md` per region and needs to know
which ones. What this step does not decide is the dials: difficulty and weight
live in each region's own frontmatter, where they cannot drift from the region
they size.

## Patterns

**A container is a grouping and nothing else.** No file, no pattern, no phase,
no content. It exists so the diagram layer has a tier to draw, and a container
that starts acquiring lore is a region that has not been written yet. Pick one
axis and cut the whole setting on it: geography, depth, or who holds what.
Whatever the axis, a reader should be able to say which container a new region
belongs in without being told.

**Every region names exactly one container, and every container holds regions.**
`validate.py` checks the first (M10). The second is judgement: a container with
one region in it is a label, and a container with everything in it is not a cut.
Two to four regions each is the readable band.

**Size the roster from the cells, not from the map.** Nine cells exist and each
one is written to a different discipline. A roster that carries no `SAFE` region
never exercises three of them. Two regions of each type is the floor that puts
every cell in play. Beyond that, each further region is roughly
`region_weights.<weight>.locations_min` to `locations_max` more locations at
Milestone 6, and that is the cost to weigh.

**Type is placement and it is the primary classifier.** Region type selects the
cell file, decides which referee table the region carries, sets the units its
locations state, and constrains what they must declare. Assign it here,
deliberately, and expect it to be the field every later pattern reads first.

**Edges are binary at this tier.** `setting/connections.md` answers only whether
two regions connect. Quantity and type are drawn at tier 4 and nowhere else, and
a setting diagram carrying twelve typed edges between two regions is unreadable
(M12).

**More than one route reaches most places.** A roster shaped as a line makes
every region a gate on the next one, and a party that cannot pay at region three
has nowhere else to be. Leave at least one alternative into the interior, and
expect it to be longer, darker, or watched by something worse.

**Name the holdings now and make them factions at step 3.** Where the containers
cut the setting by who holds what, this step has decided the answer that `S-FAC`
writes up. State the holder in the container's name and let step 3 give it
something it wants and something it will trade.

**Every region name decomposes.** Same rule as the setting's own name, checked
the same way once step 5 stubs the regions (M18). Roots that do not exist yet
are proposed in this step's batch and recorded in `T-LNG` at step 3.

## Excluded patterns

- **Difficulty and weight in the roster.** They are dials and they live in
  `region.md`. A number in two places is a number that will disagree with
  itself.
- **A container that is a region.** If it has a character, a name people use, or
  anything happening in it, it is a region and it needs a `region.md`.
- **Typed or weighted edges.** Not at this tier. Not with a label, not with a
  count, not as a note in the cell.
- **A region with no way in.** Every region is reachable, and a region reachable
  only by crossing the hardest region in the setting is reachable only in
  theory.
- **Prose describing a region.** One line of placement. The region describes
  itself at steps 5 to 8.
- **Backfilling the roster from the tables.** The tables are step 3 and they are
  written to serve the roster, not the other way round.

## Design questions

1. **What divides this setting into containers?** Name the axis. What would a
   reader have to know to place a new region correctly?
2. **How many regions, and how are the three types distributed?** What does the
   roster's size cost at Milestone 6, in locations?
3. **Which region is the hardest, and which is the way in?** The hardest region
   carries the smallest difficulty die; the way in is usually `SAFE` and usually
   the largest.
4. **Which regions touch?** Draw the graph before writing the table. Where is
   the second route into the interior, and what does taking it cost?
5. **Which region names are new, and which roots do they need?** Every one of
   them decomposes, and the roots are recorded at step 3.
6. **Where the containers name a holder, what does that holder want?** Step 3
   writes it into `S-FAC`, and a holder that wants nothing is a place name.
