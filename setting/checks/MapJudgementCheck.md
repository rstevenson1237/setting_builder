# Map Judgement Check - 2026-11-14, The Buried City after the block plans (8902787)

Drawn with `python3 tools/maps.py draw --fit 1600x1600px`, and again at `--fit 110x150mm`
(H and I viewed at PDF size). Every locked way is drawn as a barred door. `maps.py draw` reports two notes it could not place on the site
sheet: the room labels `F.1` and `G.1`. Every level now has an approved design (3e), so "the
level keeps its shape" is read against `Design.md`'s outline, and the brief's `footprint` beside it.

Confirmed on every item: block C.a.

## Block D.a
- Floors read apart: an unlabelled floor runs between D.2, D.9, D.10 and D.3, and D.3 runs into D.4 with no wall between. Source: the D plan (rooms set against a shared floor) / `tools/plan.py`.
- The level keeps its shape: the design's outline is 160 feet; the brief's footprint is 120. Source: `Design.md` / `BRIEF.md`.

## Block E.a
- Floors read apart: the E.15 passage meets the turning hall with no wall arc, and the passage from E.2 breaks E.4's rounded end. Source: artgen (a passage meeting a curved wall).
- The level keeps its shape: eight passages off a central round hall, as the brief says, but in a 220-foot outline against a 140-foot footprint. Source: `Design.md` / `BRIEF.md`.

## Block F.a
- Floors read apart: F.6 opens into F.3 along most of a wall. Source: the F design.
- Labels and marks read: the F.1 label is not placed at site size; "Up to E.9" sits on F.1's wall. Source: artgen label placement.
- The level keeps its shape: 240-foot outline against a 180-foot footprint. Source: `Design.md` / `BRIEF.md`.

## Block G.a
- Floors read apart: G.15's drum sits on G.20's north wall; G.13 runs on into the passage to G.12; G.11 and G.24 read as passage. Source: the G plan / `tools/plan.py`.
- Labels and marks read: the G.1 label is not placed at site size. Source: artgen label placement.
- Prose follows the map: G.16 gives the way to G.15 "on its west side"; it leaves the gallery's north end. Source: generator (4b, write-up not redone after the re-plan).
- The level keeps its shape: the seed and brief put the sun chapel (G.22) "at its centre"; it lies south of centre. Last pass's finding, still open. Source: the G plan.

## Block H.a
- Floors read apart: H.2 and H.13 read as passages, and H.4 opens east into the passage to H.15 with no wall. Source: the H plan.
- Labels and marks read: at PDF size "Up to G.19" and "Up to B.10" lie on H.1's stair and wall, and "Down to I.1" is split across H.4 and H.12. Source: artgen label placement.
- The level keeps its shape: 240×230-foot outline against a 210-foot footprint. Source: `Design.md` / `BRIEF.md`.

## Block I.a
- Labels and marks read: at PDF size I.1's stair glyph sits on I.5's wall and its note "Up to H.12" lies inside I.2. Source: the I plan (I.1 is 10 feet wide) / artgen.
- The level keeps its shape: 180×190-foot outline against 160. Source: `Design.md` / `BRIEF.md`.

## Block J.a
- The level keeps its shape: 160-foot outline against 140. Source: `Design.md` / `BRIEF.md`.

## Block K.a
- The level keeps its shape: 140×160-foot outline against 130. Source: `Design.md` / `BRIEF.md`.

## Block L.a
- Floors read apart: L.2 runs into the passage to L.1 with no wall. Source: the L design.
- The level keeps its shape: its 170×160-foot outline is wider than K's 140, but the setting says the pyramid narrows for its last five levels. Source: `Design.md`.

## Open Items
- Make each level's outline and the brief's footprint agree: shrink L below K, or say in `BRIEF.md` that a design's outline replaces the footprint and drop the footprints. Source: `Design.md` / `BRIEF.md`.
- Put G.22 at the level's centre, or change the seed and brief. Source: the G plan.
- Give rooms that run into passages a wall and a gap (D.3-D.4, D's middle floor, F.6-F.3, G.13, H.4, L.2). Source: plans / `tools/plan.py`.
- Stair notes and labels still collide at PDF size (H.1, H.4/H.12, I.1) and two labels go unplaced (F.1, G.1). Source: artgen - a report bundle (`artgen-maps.js report`).
- A passage meeting a curved wall leaves a gap in the curve (E.2/E.15, E.4). Source: artgen.
- Rewrite G.16's exits to match the map. Source: generator (4b).
