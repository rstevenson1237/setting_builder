# Intake - visual design: blocks designed before they are written

## The request, verbatim

> Read the below plan [image_tools `docs/DUNGEON-DESIGN.md`, commit `86e957d`], clarify and then
> write out instructions for sonnet to execute.
>
> **Item 1.** Observation: we are currently not basing our setting generation around a generated
> visual design. Instead we are generating location and region meta data with sufficient detail to
> generate an image and then using a routing algorithm to connect everything together with limited
> attention being paid to an interesting and correct visual design as a first party to the setting.
> Proposal: Add a new step or sub step prior to the generation of Locations.md and Connections.md
> where visual region and location blocks are generated from detail in the brief and then the
> location and connection writeups are written based on the approved visuals. The setting checker
> would ensure that these are concurrent. Visuals can be optional, based on the brief. When absent
> the current process would take precedence.
>
> **Item 2.** Observation: a dungeon design markdown files with observations from setting builder
> and recommendations on extending our design capabilities. Proposal: read the proposal, verify its
> claims, integrate into a plan within this repository or optionally, push some of the work back
> into the image_tools repo to be completed there.
>
> **Item 3.** artgen has been updated to v0.13 with fixes for discovered bugs.
>
> **Item 4.** create an artgen themed settings that are ideal to this project.
>
> **Item 5.** investigate layouts, coordinated with a skill. Layouts are design motifs that
> describe a collection of rooms and how they connect. By generating layouts and not just
> individual rooms we can create more engaging and interesting visual design. I am open to locking
> 1 layout to 1 block, or simply including as a design tool to build blocks.
>
> **Item 6.** investigate expanding blocks. A block is always represented by a point but also may
> be bounded by a shape. A block bounded by a shape should try to fill its shape. A block without a
> shape should build from the point, expanding outward as the design recommends. Configuration may
> adjust these behaviors (for example encouraging a certain corridor length between locations or
> how much we are encouraging to fill the block). Explicit voids (areas that should not have rooms
> written into them) within the block are allowed. Every location is addressable within the block
> and every block is addressable within its region which are addressable within the setting which
> means that every location can be expressed in relation to another in 3d space.

## Questions put, and the answers

| Asked | Answer |
|---|---|
| Item 4: a house map style, Claude Code settings for artgen work, or both? | Both. |
| Item 2: where the layout engine work is built | Prototype here (Python, feeding the existing `dungeon layout`), and write an artgen report so image_tools can take the engine half later. |
| Item 5: layouts per block | Several per block, chained by sockets; one per block is the simplest case. |
| Item 1: the source of truth once a design is approved | A committed design file per block. The tables are written from it, the validator fails when they disagree, and drawn maps are still built from the tables. |

## Second follow-up, verbatim

> confirming that we are building everything here, feedback from the process and our prototype
> will identify what makes sense to port back to artgen and write that into the report. Once user
> is satisfied then artgen can be upgraded and our work here reintegrated?
>
> Two letter steps seem overboard. Just change the steps.
>
> Yes we can pick the default, give me options. This should be tweakable in brief.md

Read as: everything is built here; the report is written from what the work shows and sent when
the user is satisfied; a later plan moves the framework onto the artgen release (spec S14). The
design step is a new 3d and the steps after it are renumbered (spec S1). The look is a `maps`
lever in `BRIEF.md`, at a default the user picks from the options in spec S11 and `looks/`.

The user's pick of default look: *(not yet given; T3 asks)*.

## How it is read

| Asked | Read as |
|---|---|
| Visual region and location blocks | Regions are already placed visually on their sheets at step 3b. What is new is the block: a DANGEROUS level or a SAFE/WILD settlement, designed as a picture before its locations are written. |
| Generated from detail in the brief | From the region's `BRIEF.md` node (outline, location count, type targets, footprint) and its seed (entries, conditions). |
| Approved visuals | The user picks one of a few rendered candidates. Only the user approves. |
| Write-ups based on the visuals | Steps 3d and 3e write `Locations.md`, `Connections.md` and `Blocks.md` to agree with the approved design. |
| Concurrent | The validator compares the design and the tables: same locations, same places and shapes, same ways, same voids. |
| Optional, based on the brief | A region whose `BRIEF.md` node has a `design` line is designed; any other region is built as today. |
| Layouts | Named motifs (a cell row, a ring hub, a suite) with roles, parts, ways and sockets, that expand to rooms and ways. |
| A block is a point, maybe bounded | A block has an `xyz`; with an `outline`, the design fills it; without one, it grows from the point and its outline is drawn from what it holds. |
| Voids | Areas inside a block that no location takes: DANGEROUS has `Rock` already; SAFE and WILD gain the same. |
| Every location in relation to another in 3D | Already true: `tools/space.py` resolves all 190 places to one frame with 0 problems (run on `7f3d6cd`). The plan keeps it true for designs and adds a command that states one place from another. |
| artgen themed settings | (a) one map look for the build, set once and applied to every dungeon, settlement and terrain map; (b) `.claude/settings.json` tuned for this repo's artgen and tools work. |
