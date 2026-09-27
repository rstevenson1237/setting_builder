# Tags.md

## Purpose
A flat, genre-derived pool of thematic tags, each with a one-line gloss - pure seed/color
material. Two instances exist per setting, same shape: `setting/Tags.md` (setting-wide,
~25 tags, generated at step 1a) and one `setting/region/[Code]/Tags.md` per region
(region-specific, ~25 more, generated alongside that region's Overview at step 3).
`Setting.md` and every Region Overview point to the matching pool with a single tag-line
instead of embedding tags inline, and a location's gazetteer stub draws exactly two tags -
one from the setting pool, one from its own region's - instead of inventing three fresh.

## Context
Read first:
- `GENRE.md` - the sole real input. Every tag traces back to its chosen reference's own
  concrete iconography or one of its answers.
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- At region level only: `setting/Tags.md` itself, to avoid duplicating its entries, and
  this region's own line in `setting/region/Regions.md` (rating, die, name) for texture.
- `patterns/setting/Tags.md`

## Instructions
Generate ~25 tags, each following `patterns/setting/Tags.md`'s Spec. The pool is flat, not
split by rating. Draw from the reference's own concrete iconography first, and reach past
it only to fill a real gap.

At region level, the pool is a corner of the setting-level one - what is true of this
region and not of the setting generally - and never re-derives the setting pool's entries.

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
