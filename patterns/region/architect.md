---
id: region.architect.headers
target: region
phase: architect
writes: [Overview, Fields, Tables, Connections, Diagram]
dependencies:
  - config
output_template: templates/region.md
schema_version: 1
---

Step 5. The Architect stubs one `region.md` per region on the roster, sets its
three tags, its difficulty die and its weight, and names the region-level
containers the diagram layer will draw. It writes no content: every heading it
creates is empty or carries an architect note naming the step that fills it.

Almost all of this step is `scaffold.py`, which is the point. Which referee
table a region carries, how many rows it has, which direction it counts in and
where the diagram markers sit are all decided by the type, so they belong in
code. What is left here is four dials and a list, each of which every later step
reads and none of which may change afterwards.

```
python tools/scaffold.py region --code R0n --name "<Name>" \
    --tags "<a>,<b>,<c>" --type SAFE|WILD|DANGEROUS --difficulty d4..d12 \
    --weight low|medium|high --container <setting-level-id> \
    --sub <id>=<Name> [--sub ...] [--weather]
```

## Patterns

**Type, name and placement are already decided and are transcribed, not
chosen.** Step 2 wrote the roster into `setting.md` and it is canon. A region
whose type reads wrong at step 5 is a step 2 re-run, booked as its own pass, and
never a quiet change here that leaves `setting.md` saying something else.

**Difficulty is a dial and it is set against the whole roster, not against the
region.** A larger die is easier and `d8` is average, so the question is not
"how hard is this place" but "where does this place sit between the way in and
the hardest region in the setting". Set the extremes first, then fill the middle.
`config` carries `difficulty.dice` and `difficulty.average` and `validate.py`
checks the value against the list (M4).

**What the die measures changes with the type and it is stated in the region's
own Fields.** In a `SAFE` region it measures the size of the settlement and what
can be got there. In a `WILD` region it measures the treacherousness of the
terrain and what leaving the road costs. In a `DANGEROUS` region it measures the
evil of the place and how readily its traps and hazards find a party. Two
regions of different types carrying `d6` are not the same difficulty and never
read as though they are.

**Weight is a location count and it is the bill for Milestone 6.** `config`
carries `region_weights.<weight>.locations_min`, `locations_max` and `high_min`,
and `validate.py` checks both numbers once step 9 has run (M6). A `high` region
is forty to sixty locations written one at a time. Set it from what the region
has to hold, and know what has been ordered.

**Three tags, thematic rather than descriptive.** Same rule as the setting's,
checked the same way (M3). A region's tags divide it from its neighbours: if two
regions in one container could swap tag sets without either reading wrongly,
neither set is doing work.

**Containers may be stubbed here and are settled at step 6.** The scaffold needs
at least one, because it writes a tier-4 marker for each. Cut the region on one
axis a referee can apply without being told: the road and what stands off it,
the surface and what is under it, the part that is kept and the part that is not.
Two or three containers is the readable band at region scale.

**Say whether the region has outdoor extent.** `--weather` adds the six-row
Weather table, and a region open to the sky carries one (M19). An entirely
interior region does not, and adding one there is six rows nobody rolls.

**Leave the architect notes in.** Each stub carries `[[ ... ]]` naming the step
that fills it, and each is struck when its content is absorbed (M25).

## Excluded patterns

- **Prose in any heading.** The Overview is step 8 and the Fields are step 7. A
  paragraph written here reads as finished and the later step will not overwrite
  it.
- **Location names, location counts, or anything about what is inside.** The
  roster of locations is step 9, and the weight set here is what sizes it.
- **A difficulty set to make one region feel exciting.** The die is a position on
  a curve that spans the setting. It is read against the roster or it is noise.
- **A hand-written body.** `scaffold.py` fixes the shape and `validate.py`
  checks the same shape, so the two agree by construction.
- **A container that is a place.** If it has a character, a name people use, or
  anything happening in it, it is a location and it waits for step 9.
- **A mermaid block.** Every diagram is derived. The scaffold writes markers and
  `mermaid_gen.py` writes the files they name (M13).

## Design questions

1. **Where does each region sit on the difficulty curve?** Name the way in and
   the hardest region first, then place the rest between them. What does the die
   measure in each, given its type?
2. **What weight does each region carry, and what does that cost?** Sum the
   bands across the roster. That total is the number of locations Milestone 6
   writes.
3. **What three tags divide each region from its neighbours?** Name the region
   each tag set would be wrong for.
4. **What is each region's container axis?** State it in a sentence a referee
   could apply to a location they have not seen yet.
5. **Which regions are open to the sky?** Those carry a Weather table and the
   rest do not.
6. **Which region names are new since step 2, and which roots do they need?**
   Every name decomposes (M18), and a new root is recorded in `T-LNG` rather
   than coined here.
