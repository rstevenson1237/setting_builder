# Tags.md

## Purpose
A flat, genre-derived pool of thematic tags, each with a one-line gloss - pure seed/color
material. Two instances exist per setting, same shape: `setting/Tags.md` (setting-wide,
~25 tags, generated at step 1b) and one `setting/region/[Code]/Tags.md` per region
(region-specific, ~25 more, generated alongside that region's Overview at step 3).
`Setting.md` and every Region Overview point to the matching pool with a single tag-line
instead of embedding tags inline, and a location's gazetteer stub draws exactly two tags -
one from the setting pool, one from its own region's - instead of inventing three fresh.

## Context
Read first:
- `GENRE.md` - the sole real input. Every tag traces back to the chosen reference's own
  concrete iconography, the same rule `patterns/setting/Genre.md` already uses for its own
  tag-building.
- At region level only: `setting/Tags.md` itself, to avoid duplicating its entries, and
  this region's own line in `setting/region/Regions.md` (rating, die, name) for texture.
- `patterns/setting/Tags.md`

## Instructions
Generate ~25 tags, each one or two words, each with a one-line gloss that constrains
rather than decorates - the same three-job test `patterns/setting/Genre.md` already uses
for its own tag bank: a tag represents a theme, acts as an index, and constrains the
material by ruling something out. Flat, not split by rating - a genre's texture applies
regardless of where a location sits; rating-specific content is the compiled tier-2
pattern files' job now, not the tag pool's. Draw every tag from the chosen reference's own
concrete iconography first, and only reach past it to fill a real gap.

At region level, add texture specific to this region - don't re-derive the setting-level
pool's own entries.

## Template
```
Tags of [Setting Name]

- **[Tag]** - [one-line gloss, specific and concrete, never decorative]
- **[Tag]** - [one-line gloss]
  ... (~25 total)
```

A region's own pool uses the same template, headed `Tags of [Region Code] [Region Name]`.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
