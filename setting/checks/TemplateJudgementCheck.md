# Template Judgement Check - 2026-11-14, The Buried City after the block plans (8902787)

Every finding of the 2026-11-02 pass was fixed in 7f3d6cd. This pass reads the templates
changed since then (`templates/region/Design.md` new; `Connections.md`, `Location.md`,
`Locations.md` and `Tables.md` changed) and the check template that reads the designs.

Confirmed on every item: `templates/setting/*.md`, `templates/region/Region_Gazetteer.md`, `templates/region/Region.md`, `templates/region/Brief.md`, `templates/region/Locations.md`, `templates/region/Connections.md`, `templates/region/Tables.md`, `templates/region/Location.md`

## Findings
- templates/region/Design.md - No defaults: it leaves `fill`, `pad` and `width` to "the Design line's own settings", so every designed level states its own fill ("25-45%") in place of `BRIEF.md`'s `pack fill="35-55%"`. The rate belongs in `BRIEF.md`'s `design` line. - All ten levels carry their own fill.
- templates/region/Design.md - Consistent with STEPS.md and the other templates: it writes an `outline` "where the region's brief gives its block a shape", but the brief gives only a `footprint`, and nothing ties the two. - Every outline is wider than its footprint, and L (170 feet) is wider than K (140) where the setting has the pyramid narrowing.
- templates/region/Design.md - Genre drift guardrails: it does not ask that a room the seed places ("at its centre", "far") stands there in the design. - G.22, the sun chapel the seed puts at the centre, is south of centre.
- templates/checks/Map_Judgement_Check.md - Consistent with STEPS.md: "The level keeps its shape" reads the sequence from `BRIEF.md`'s footprints, which a design's outline now replaces. (Not a generation template; noted for the next edit.)

## Open Items
- Design.md: read `fill`, `pad` and `width` from `BRIEF.md`'s `design` line, and set the levels' rates there. Source: template; `BRIEF.md`.
- Design.md: an outline keeps to the brief's footprint (or replaces it, said once in `BRIEF.md`), so the levels widen then narrow as the brief says. Source: template.
- Design.md: a room the seed places (centre, far end) is placed so in the design. Source: template.
- Map_Judgement_Check.md: read the level's size from its `Design.md` outline. Source: template.
