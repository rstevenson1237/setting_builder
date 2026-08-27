---
id: location.architect.headers
target: location
phase: architect
writes: [Player Overview, Referee Overview, Features, Exits]
dependencies:
  - region:${REGION_CODE}
  - siblings:location:${REGION_CODE}
  - config
output_template: templates/location.md
schema_version: 1
---

Step 9. The Architect writes the region's roster: one stub per location, each
carrying its name, its three tags, the container it sits in and the weight that
selects its cell. It writes no content. Every heading it creates is empty or
carries an architect note naming the step that fills it.

This is the step that spends the region's weight. Steps 5 to 8 sized the region
and said what it is made of; this step turns that into a list of files, and the
list is the largest single commitment in the project. `validate.py` checks two
numbers against `config` once this step closes (M6): the count sits in the
weight band, and the `HIGH` count meets the minimum.

```
python tools/resolve_deps.py --pattern location.architect.headers \
    --target R0n-L01 --var CELL=<TYPE>_<WEIGHT>
python tools/scaffold.py location --code R0n-L01 --name "<Name>" \
    --tags "<a>,<b>,<c>" --container <region-level-id> \
    --weight LOW|MEDIUM|HIGH [--pattern <shape>]
```

## Patterns

**Write the roster before writing any stub.** The whole list, in one pass: code,
name, container, weight. A roster built one location at a time drifts, because
the fifteenth location is chosen against the fourteenth rather than against the
region. Read the region's Overview and Fields back first: the sentences that
turned out to be about one place are locations the region has already ordered
(J1), and step 8 was told to hand that list forward.

**Weight is the cell and the cell is the discipline.** `HIGH` is what a party
travels to reach, `MEDIUM` is the working body, and `LOW` is the connective
ground that makes the other two legible. Count the `HIGH` locations first and
meet `region_weights.<weight>.high_min` deliberately rather than discovering at
step 11 that the region has no landmark. Then place the `MEDIUM` body. `LOW` is
what is left, and it is not filler: a `LOW` location still costs a party
something to cross, and a stretch that costs nothing is an edge in
`connections.md` and no file at all.

**The `MEDIUM` to `LOW` split is judgement and is never checked.** `config`
carries the count band and the `HIGH` floor and nothing else, because whether a
`LOW` room reads as empty or is empty is a decision a script cannot make. Do not
write a checked count into a cell file and do not invent a ratio here.

**Every location names exactly one declared container** (M10), and no container
stands empty. Step 6 cut the region on an axis a referee can apply to a location
they have not seen; apply it. A location that could sit in either container
means the axis was not a cut, and that is a step 6 problem rather than a reason
to guess here.

**The `cell` token is written by `scaffold.py` from the region's type and the
weight given.** It duplicates the parent's type on purpose, and a disagreement
between the two is a mis-tagged location, which is the error worth catching
(M5). Never hand-write it.

**Three tags, thematic, and they divide this location from its neighbours.**
Same rule as the region's, checked the same way (M3). The test is the sibling
list: if two locations in one container could swap tag sets without either
reading wrongly, neither set is doing work.

**Every name decomposes into roots recorded in `T-LNG`** (M18). A location whose
name needs a root the registry does not hold waits for the root. Propose it in
this step's opening question batch and write it into `T-LNG` before the stub is
written, never in passing. Both naming layers are available and the disagreement
between them is content: a living-layer name says what the place is now and a
Covenant-layer name is often wrong about it.

**`pattern` is a report-only field and it is worth filling.** It names the shape
the location takes, so a referee scanning a region can see its rhythm and a
later pass can find every location of one shape at once. `validate.py` never
fails on it.

**Number for the graph, not for the walk.** Codes are the primary key and they
never change once written, so a roster that numbers in walking order becomes
wrong the moment step 10 finds a second route. Number by container, in blocks,
and leave the order to `connections.md`.

**Leave the architect notes in.** Each stub carries `[[ ... ]]` naming the step
that fills it, and each is struck when its content is absorbed (M25).

## Excluded patterns

- **Prose in any heading.** The Features are step 11 and the Overviews are step
  12. A paragraph written here reads as finished, and the later step will not
  overwrite it.
- **Exits, sources or a container's edges.** Step 10. The sibling that an exit
  names may not be stubbed yet, and a guessed edge becomes canon in the file the
  diagram layer reads.
- **A roster built to hit the top of the band.** The band is a band. A region
  with fewer, better locations is a better region, and padding toward the
  maximum is how a level goes slack.
- **A `HIGH` location that is only the largest.** Scale is not content. A
  landmark is something a party carries away from, and the cell files say so
  three different ways.
- **A hand-written body.** `scaffold.py` fixes the shape and `validate.py`
  checks the same shape, so the two agree by construction.
- **A name coined against no root.** The registry is the constraint, and a name
  that needs a new root is a question rather than an invention.
- **A location for a thing that is really a feature.** If it has no exit worth a
  cue, nothing to notice and no reaction, it is a clause in its neighbour's
  Player Overview.

## Design questions

1. **Which locations did steps 7 and 8 already order?** Name each sentence in
   the region's Fields and Overview that turned out to be about one place, and
   name the location it becomes.
2. **What are the `HIGH` locations, and what does a party carry away from each?**
   Meet the floor in `config` deliberately. If the answer to "what comes out" is
   only "they are past it", it is not a landmark.
3. **How does the roster divide across the containers?** A share, not a count.
   Which container is the body, and does the axis from step 6 still cut?
4. **Which locations are `LOW`, and what does each cost to cross?** A stretch
   that costs nothing is an edge and no file.
5. **Which names are new, and which roots do they need?** Every name decomposes
   (M18). Propose the roots now, as a batch, and record them in `T-LNG` before
   any stub is written.
6. **What shape does each location take, and what does the region's rhythm look
   like written out?** The `pattern` field is the answer, and a region where
   every entry carries the same one has been written on a template.
