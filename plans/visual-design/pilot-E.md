# Pilot - region E

Region E (pyramid level 3, fifteen locations) designed at step 3d, then its tables and its two
neighbours written to agree.

## What it changed

- `BRIEF.md`: a `design` line for E (`spacing="10-30 feet"`).
- `setting/region/E/Design.md`: one block, `E.a`, in a `rect 140 140`. A `spine-ring-hub` (the Turning Hall
  with the Corridor of Darts as its spine), three `cell-row`s with one cell a side (the Guard, the
  Priesthood and the Scholars) and four fill rooms, each hub socket joined to one room. Solved
  unpinned over sixty seeds; seed 1 (score 94) accepted and approved by the user.
- E's `Dressing.md` places, sizes and shapes and the hub's `wall` on each archway; types, ways and
  Blocks.md did not change.
- D and F were packed again around E's stairs (D.6 over E.1, F.1 under E.9): every room of both moved.
- Nine write-up sentences, each only a size (E.3, E.4, E.5, E.8, E.10, D.5, D.12, F.4, F.6).
- Library: `cell-row` takes one to four cells a side, a hall of 30 to 60 by 10 to 30 and cells of 10 to 30;
  `spine-ring-hub` a spine of 40 to 120 and a ring of 20 to 40.

## What it showed

- **A designed level is pinned by the levels beside it.** A stair room stands over the room it
  meets, so E.1 and E.9 were fixed by D and F as they were packed. Solved pinned, passages crossed and
  several seeds failed; solved unpinned (`--free`), all seeds routed. The level to design first is
  free, and each next one is pinned to the last: design a stair's two ends together, or in order.
- **Prose states constraints the design cannot.** E.2's write-up says its eight arches pair up on
  opposite sides. A design that only joins sockets can break that, and did once; a layout or a design
  needs a way to say which sockets are opposites.
- **The solver's bearings are soft.** `hub-n` to E.3 gave E.3 to the south on one seed. Every candidate
  needs its bearings checked, or the engine must hold them (report R2).
- **Scoring needs what artgen allows.** Passages leaving one room may cross or run together by artgen's
  rules, which read as no spoke at all. `solve` now charges for them and for artgen's own `check` findings.
- **Rooms lie on the 10 ft lattice at whole-foot places**, so layouts size rooms in 10 ft steps, and a
  room of shape `hall` must be one passage wide (10 ft here), so the hall of a `cell-row` is a room.
- **The tables hold places and ways, not routes.** The map redraws each passage, so it reads as the
  design in its rooms and not in its passage shapes.
- **A checked write-up stays flagged.** Staleness is git time, so a write-up that needs no change (F.20,
  and the three briefs) stays on `--pending` until something touches it.
