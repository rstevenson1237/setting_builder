# Setting - Tags

## Provides
The flat, genre-derived thematic pool every `Setting.md` and Region Overview points to
with a single tag-line instead of embedding tags inline, and the two-tag draw (one
setting-level, one region-level) every location gazetteer stub uses instead of inventing
three tags fresh.

## Read at
Step 1b, right after `GENRE.md` exists, to seed `setting/Tags.md`. Read again per region,
alongside its Region Overview at step 3c, to seed that region's own `Tags.md`.

## Spec

```
TAGS
  25    Tags, each one or two words, each with a one-line gloss
  1     Every tag traces to the chosen reference's own concrete iconography, or a Q2
        answer that mattered - the same intentionality test patterns/setting/Genre.md's
        own tag bank already uses
  1     Flat - no rating split. Rating-specific texture is the compiled tier-2 pattern
        files' job now (see patterns/setting/Genre.md's own Kind-related files), not the
        tag pool's
```

**This replaces `GENRE.md`'s old Safe/Wild/Dangerous/People/Creatures tag bank outright.**
That bank tried to do two jobs at once - flavor color and rating-specific structural
content - and lived at the wrong altitude for a value read at nearly every generation step
regardless of whether it was used. This file's pools stay pure color; the structural half
of that old job now belongs to the compiled tier-2 pattern files (demeanor and personality
examples in `dangerous/Creature.md`, `wild/Creature.md`, `safe/People.md`).

**What makes a good tag** - the same test `patterns/setting/Genre.md` already uses for its
own tag-building: it represents a theme (compresses something already true of the chosen
reference down to a word or two, rather than introducing a new idea of its own); it acts
as an index (scannable, findable again by a step that doesn't already know it's there); it
constrains the material (rules something out, per "Be specific, not generic" - a tag
generic enough to fit any setting in the reference's trope cluster was not worth writing).

**Where the gloss earns its place** - specific and mechanically or texturally concrete
("half-flooded, walkable only at low water"), never decorative ("watery," "mysterious").

**A region's own corner of the pool** - what's true of this region specifically that
isn't true of the setting generally: a local custom, a specific hazard, a texture of
speech or trade unique to this stretch of the map.

## Constraints

- **A tag is pure seed, never structural.** It never selects which pattern file governs
  a location - that is Kind's job - and it never carries its own inclusion math - that
  is a class file's Spec. Its only job is color: a one-line gloss the referee can read
  off a stub in passing, and an index a later step can scan for something that fits.

- **Region-level pools add, they don't restate.** A region's own 25 tags should feel
  like a corner of the setting-level 25 - narrower, textured to this specific place -
  not a second draw from the same well. Read the setting-level pool first specifically
  to avoid this.
