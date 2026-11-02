# Map Judgement Check - 2026-11-02, The Buried City after step 4 (bab0daf)

Drawn with `python3 tools/maps.py draw --fit 1600x1600px`, and again at `--fit 110x150mm`
(G and F viewed at PDF size). `tools/space.py` reports 0 errors and 0 warnings, so stairs
meet stairs within its tolerance. Room traps (a hazard on a room, not a way) are never
marked; ways' traps are marked with a cross. Both points apply to every block and are not
repeated below.

## Block C.a
- Every way reads as itself: Confirmed - three stairs down in C.2, C.3 and C.4, a trapped sill at C.1, and the C.6 niche's trap marked.
- Floors read apart: Needs Attention - the C.4-C.3 stone passage runs beside C.2 behind a broken wall and reads as part of C.2. Source: `tools/dungeon.py` (a passage routed against a room's wall).
- Labels and marks read: Needs Attention - "Down to D.10" sits on C.4's door. Source: artgen label placement.
- Prose follows the map: Confirmed.
- The level keeps its shape: Confirmed - small rooms round one tiled hall.
- It plays: Confirmed - the C.2-C.3-C.4 loop and three choices of way down.

## Block D.a
- Every way reads as itself: Needs Attention - the D.5-D.6 archway, locked by The Sun-Disc Key, carries no lock mark. D.1-D.3 is drawn as two doors with floor between. Source: `tools/dungeon.py` (Lock not passed to artgen) / artgen.
- Floors read apart: Needs Attention - D.11 and D.12 are one L-shaped floor, and D.11 draws about 70 feet long against its 40. Source: `tools/dungeon.py` (an open way between touching rooms drawn as no wall).
- Labels and marks read: Needs Attention - "D.10" and "Up to C.4" run together. Source: artgen.
- Prose follows the map: Needs Attention - D.3's "winding passage" to D.4 is a gap in a shared wall. Source: `BRIEF.md` `pack passages="40%"` not met; `tools/dungeon.py`.
- The level keeps its shape: Needs Attention - the four areas group correctly (robbers west and south-west, scraped north-west, gallery east, founders south-east), but the brief's winding passages between them are absent; every room touches another. Source: `tools/dungeon.py` pack.
- It plays: Confirmed - the gallery has a locked front (D.5) and a trapped back way (D.12).

## Block E.a
- Every way reads as itself: Needs Attention - no trap mark on E.9 (darts and a spiked pit) or on the drum's rim, and no lock mark on the E.3-E.6 iron door. The two secret ways into E.14 are marked S. Source: `tools/dungeon.py` (hazards on a Connection not marked) / artgen.
- Floors read apart: Needs Attention - E.2, a 40-foot round drum in the tables, draws as an irregular floor merged with the mouths of its passages. The passage to E.3 and E.10 loops round the north and reads as a room. Source: `tools/dungeon.py` / artgen.
- Labels and marks read: Confirmed.
- Prose follows the map: Needs Attention - opposite rune pairs (hawk-eye: E.3-E.5; bell-falling stair: E.4-E.9) are not opposite on the map. The Three Claims' "Guard east, Priesthood north, Scholars west" disagrees with E.3 north-west, E.4 north-east and E.5 south-west. Source: table (no `wall` on E.2's ways) and `tools/dungeon.py`.
- The level keeps its shape: Needs Attention - eight arches round a drum is the level's idea, and it does not show. Source: as above.
- It plays: Confirmed - the drum gates every branch, and E.14 has two hidden ways in.

## Block F.a
- Every way reads as itself: Confirmed - F.7-F.18's trapped flag is marked; doors and openings read.
- Floors read apart: Needs Attention - F.1 and F.2 run together. A long passage loops across the north from F.17 to F.6 and F.20 and reads as a room with no name. Source: `tools/dungeon.py` (detour within `BRIEF.md`'s 150 feet per way, but chained).
- Labels and marks read: Needs Attention - "F.1" and "Up to E.9" overlap. Source: artgen.
- Prose follows the map: Needs Attention - F.7 "guards the way to the gallery stair", but F.13 opens off F.4. F.18's "winding" passage is straight. Source: write-up (F.7); `tools/dungeon.py` (F.18).
- The level keeps its shape: Confirmed.
- It plays: Confirmed - eight loops, and the robbers' camp reachable only through F.12's guards.

## Block G.a
- Every way reads as itself: Needs Attention - the secret G.21-G.14 stone is drawn as a plain door with no S. The G.7-G.10 iron door (King's Seal) and the G.19 arch (Queen's Ring) carry no lock mark. Source: `tools/dungeon.py` / artgen.
- Floors read apart: Needs Attention - G.2 runs into the passage west and north to G.4 and G.28. The G.18-G.5-G.13 passage loop reads as rooms. Source: `tools/dungeon.py`.
- Labels and marks read: Needs Attention - at PDF size "G.1" sits on its stair glyph, "Up to F.13" crosses a wall, "G.19" overlaps its stair, and "G.21" sits on a wall. Source: artgen.
- Prose follows the map: Confirmed - the G.19 stair is in the north wall; the side door is beside the lake doors.
- The level keeps its shape: Needs Attention - G.22, "at its centre" in the brief and "at the level's centre" in its write-up, is placed south-east (Dressing `xyz="60,-80"`). Source: `tools/dungeon.py` pack.
- It plays: Confirmed - a false tomb beside the true one, two keys, and a back way from the lake.

## Block H.a
- Every way reads as itself: Confirmed - both stairs up (G.19, B.10) sit in H.1, and the iron doors draw as bars.
- Floors read apart: Needs Attention - H.9, a 40 by 50 basalt hall with no `shape` in its Dressing, draws as a cave. Source: `tools/dungeon.py` / artgen.
- Labels and marks read: Needs Attention - "Up to B.10" sits on its stair glyph; "Down to I.1" crosses H.12's wall. Source: artgen.
- Prose follows the map: Needs Attention - H.1 shows a stair up to B.10 on the map, while its write-up says the way up is shut. Source: write-up.
- The level keeps its shape: Needs Attention - the brief lays it out "in the shape of level 4", and its plan shares nothing with F's. Source: `BRIEF.md` (nothing can carry it); `tools/dungeon.py`.
- It plays: Confirmed - five loops; the captives' pen reached by the drain or the pit.

## Block I.a
- Every way reads as itself: Needs Attention - the I.4-I.5 wooden door draws as three stacked bars, which read as steps. The I.9 gate's mask-lock carries no mark. Source: artgen / `tools/dungeon.py`.
- Floors read apart: Confirmed.
- Labels and marks read: Needs Attention - "Up to H.12" crosses I.1's wall. Source: artgen.
- Prose follows the map: Confirmed.
- The level keeps its shape: Confirmed.
- It plays: Confirmed - the gate can be reached through I.3 or I.13.

## Block J.a
- Every way reads as itself: Needs Attention - the J.5-J.6 iron door (Council Seal) carries no lock mark. J.1-J.8's trapped jamb is marked. Source: `tools/dungeon.py` / artgen.
- Floors read apart: Confirmed.
- Labels and marks read: Confirmed.
- Prose follows the map: Confirmed - J.6's gate and stair lie east.
- The level keeps its shape: Confirmed.
- It plays: Confirmed - J.8 lets a party bypass J.2 and reach Xothox.

## Block K.a
- Every way reads as itself: Confirmed.
- Floors read apart: Needs Attention - K.6 (20 feet square in its tables) draws as a large L that runs into K.2 and, down the west passage, into K.8. Source: `tools/dungeon.py`.
- Labels and marks read: Confirmed.
- Prose follows the map: Confirmed - K.3's gate and K.5's door lie east.
- The level keeps its shape: Confirmed.
- It plays: Confirmed.

## Block L.a
- Every way reads as itself: Confirmed.
- Floors read apart: Confirmed.
- Labels and marks read: Needs Attention - "L.1" and "Up to K.5" run together. Source: artgen.
- Prose follows the map: Confirmed - the floor slopes west to the pit.
- The level keeps its shape: Needs Attention - six rooms where the brief asks for "a single hall". Source: table.
- It plays: Confirmed.

## Open Items
- Mark Locks on ways: no locked way in any block shows a lock. Source: `tools/dungeon.py` (pass the Lock) or artgen (a lock symbol).
- Mark a trapped way when its Hazard sits on the Connection's far room (E.9). Source: `tools/dungeon.py`.
- Draw secrets as S in G (G.21-G.14), as E already does. Source: `tools/dungeon.py`.
- Keep an open way between touching rooms as a wall gap, never a missing wall (D.11-D.12, K.6-K.2, F.1-F.2). Source: `tools/dungeon.py`.
- Hold a round room's ways at fixed bearings, so E.2's opposite pairs are opposite, and give E.2's ways `wall`. Source: table; `tools/dungeon.py`.
- Meet `BRIEF.md`'s `passages="40%"` in D, or lower it. Source: `tools/dungeon.py` / `BRIEF.md`.
- Place G.22 central (a `place` or `xyz` hint the pack keeps). Source: `tools/dungeon.py` / table.
- Draw H.9 as a hall, not a cave. Source: `tools/dungeon.py` / artgen.
- Stair notes and labels overlap walls and glyphs at PDF size (C, D, F, G, H, I, L). Source: artgen - a report bundle (`artgen-maps.js report`) is the route.
- I.4-I.5's door glyph reads as steps. Source: artgen.
