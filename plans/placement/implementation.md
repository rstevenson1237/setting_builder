# Implementation - placement

This is the task plan for `spec.md`. Commits cite tasks as `placement T1`. Each task ends with
`python3 tools/validate_setting.py` free of errors and both `--check` builds passing, and is
committed on its own.

| Task | Spec | What | Files |
|---|---|---|---|
| T1 | S6-S8 | `tools/space.py` dry fire, read-only, over today's fields: `east` and `north`, `footprint`, `bearing` and `distance`, `north` and `east`, sheet squares, and shared centres as a DANGEROUS block's place. Its first run is recorded. | `tools/space.py`, `dryfire-before.txt` |
| T2 | S1, S2, S4, S5, S13 | Values and fields in the schemas; `origin` in `BRIEF.md`, read by `tables.Brief`. G's rooms, its block, A and B's locations, `Sheets.md` and `Regions.md` are rewritten into `xyz` and `outline`, and every map is byte for byte the same. `space` reads only the new fields; the builders and `dungeon` place through it; the validator runs it. | `patterns/`, `BRIEF.md`, `tools/tables.py`, `tools/space.py`, `tools/maps.py`, `tools/dungeon.py`, `tools/validate_setting.py`, `setting/` |
| T3 | S3 | `against`: the contact sweep in plan and in z, over rect, circle (as a 64-sided polygon) and poly, with `xyz` as slide and gap; anchor problems. | `tools/space.py`, `tools/validate_setting.py` |
| T4 | S9-S12 | `place` writes regions' `outline` and `xyz`; settling, and `space.py settle`; `pack` writes `xyz` and `outline`, takes pins from absolute places, settles before and after, and moves an anchored room with its anchor. | `tools/maps.py`, `tools/space.py`, `tools/dungeon.py`, `tools/pack.py` |
| T5 | S14 | Templates, the STEPS wording, the README. | `templates/region/`, `STEPS.md`, `README.md` |
| T6 | | Dry fire The Buried City: pack C-F and H-L, settle every region, and resolve each problem in the content until the dry fire is clean; record it. | `setting/`, `dryfire-after.txt` |

## Risks

- **CI goes red on unfinished content.** An unplaced thing is a warning, and only a
  contradiction between two placed things is an error. T1's seven errors were fixed in T2 as the
  user decided (S16). Each level packed in T6 can raise new ones, such as S20.
- **Contact on curved and concave outlines.** The sweep is computed on polygon edges, and the
  result is rounded outward to whole feet. The rounded place is then checked again for overlap,
  so a touch never rounds into one.
- **The packer and anchors.** Moving an anchored room with its anchor is a change to the
  annealer. If it slows packing beyond use, an anchored room is placed after the rest are
  packed, and only the anchored rooms are repacked round it.
- **Levels too close for their rooms.** T6 will find rooms that reach into the level above (see
  `intake.md`). Each is fixed in the content, by a climb or a height; the check is never
  loosened.
- **B's two ways in.** Which of them moves, or whether B's layout changes, is a design choice.
  T6 puts that choice to the user and does not make it.
