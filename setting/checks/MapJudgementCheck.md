# Map Judgement Check - 2026-11-22, the island build after #127

I drew the maps with `python3 tools/maps.py draw --fit 1600x1600px`. The Island sheet is not in that output, so I drew it separately with `maps.sheet_svg("Island")`. I read Island, A.a, HB.a, HC.a and I.a in full, and did not draw the 110x150mm pass.

Confirmed on every item: none in full. I drew HA.a, A.b, A.c, F.a and J.a and did not read them.

## Sheet Island
- Its edges keep the genre: nothing contradicts `GENRE.md`. But `draw` never writes the sheet, because `underlaid()` drops any sheet that a settlement uses as its underlay, and the master hex map is the one a party plays on. Source: tools/maps.py `draw`.
- Prose follows the map: D.12 "above the great wall" is drawn mid-island, 13 miles north of A.1. Source: tools/maps.py place, and the D.12 table line (see SettingJudgementCheck).
- It is what its seed says: F is "two villages at a river mouth". The sheet's only river runs out through G's ground to the north-west, and F's marks sit on dry grassland east of it. Source: BRIEF.md F `ground` (no river asked), tools/maps.py (no river on an island sheet).
- It is what its seed says: C.9 / I (the reef gap and the drowned galleon) are marked on C's sand, inland of the shore, not on the reef. Source: tools/maps.py place (half a square in from the coast for land regions).
- Labels and marks read: "E.9 HA" sits on the coastline at the island's east edge. In A, the labels for A.12, A.5, A.2, A.4, A.9, A.10 and A.11 overlap one another. F.7 and F.8 do not show at all. Source: artgen, tools/maps.py.

## Block A.a
- It is what its seed says: no lagoon, beach or shore is drawn. A.2 "the beach where boats land" is drawn as a gatehouse with two towers in the stockade's west side. A wide brown band crosses the village under A.10, and the text names nothing it could be. Source: tools/maps.py (A.2's Gate type drawn as a gatehouse), artgen settlement.

## Block HB.a
- Every way reads as itself: HB.1 → HA.10 is drawn as "Stairs up", where the text says the winch rope is the only way and there is "no stair". Source: tools/maps.py (a climb is drawn as a stair whatever its Connection type).
- Every way reads as itself: the locked banded door HB.8 → HB.9 is drawn the same as an unlocked door. Source: tools/maps.py or artgen (a Lock gets no mark).
- Floors read apart: HB.8's floor runs on without a wall into the passage to HB.13 and HB.14. Source: tools/plan.py.

## Block HC.a
- Labels and marks read: HC.7, the Emperor's Bier, carries a throne symbol, not a bier. Source: tools/maps.py, which picks the symbols.

## Block I.a
- It is what its seed says: the galleon is a column of rectangles cut into rock, not a hull, and the flooded hold I.4 has no water drawn. Source: tools/plan.py and artgen dungeon (no hull or water fill).
- The block keeps its shape: every deck sits on one level, so the stern deck, cabin, gun deck and holds lie end to end, where I's seed puts the hold "half in air and half in water" and floods "to the second deck". Source: tools/plan.py (one level per block).

## Open Items
- Make `maps.py draw` write every sheet, the underlay too - tools/maps.py.
- Fix D.12's place, or its text, so the Wall Ridge and the gate agree - BRIEF.md place or table line.
- Ask for a river at F's way in, or drop "river mouth" from F - BRIEF.md.
- Place C.9 / I on the reef, in the water - tools/maps.py place.
- Draw A.2 as a beach on a lagoon, not a gatehouse - tools/maps.py / artgen (report upstream with `artgen-maps.js report`).
- Draw a rope or winch Connection as a shaft, not a stair, and mark locked doors - tools/maps.py, artgen.
- Draw the galleon as a hull, with water in its flooded rooms, or split it into decks - tools/plan.py, artgen.
- Thin the overlapping location labels at A on the Island sheet - artgen.

## Owed to a tool
- A sheet in setting/*.json that `draw` writes no SVG for - tools/maps.py
- A location whose sheet mark lies on land where its region's ground is water or reef - tools/space.py
- A Connection drawn as a stair whose type is Rope - tools/validate_setting.py
