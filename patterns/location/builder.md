---
id: location.builder.fields
target: location
phase: builder
writes: [Referee Overview, Features, Exits]
dependencies:
  - region:${REGION_CODE}
  - container:${CONTAINER_ID}
  - cell:${CELL}
  - siblings:location:${REGION_CODE}
  - table:T-ARC
  - table:T-HAZ
  - table:T-KEY
  - table:T-PUZ
  - table:T-PRC
  - table:T-BES
  - table:T-CRE
  - table:T-LOR
  - table:T-NAM
  - config
output_template: templates/location.md
schema_version: 1
---

Step 11. The Builder writes the fields the region's type requires and the
Features the location is made of. This is where the content actually arrives,
and it is the largest step in the project by a wide margin.

**The step runs in three passes: `HIGH`, then `MEDIUM`, then `LOW`.** Landmarks
are written first because the thinner cells are written against them. A `LOW`
location written before its region's landmarks exist has nothing to be thin in
contrast to, and it comes out either padded or arbitrary. Set the pass with
`python tools/ledger.py pass HIGH` and record every target as it lands.

**One cell file reaches this bundle and eight do not.** The cell is the
discipline: it states what belongs in this location, where the boundary to the
next cell falls, the form it takes and what it excludes. This pattern is the
mechanism the nine cells are hung on and it does not repeat them. Where the two
disagree about form, the cell file wins, because it is the tuning surface and
this file is not.

```
python tools/ledger.py pass HIGH
python tools/resolve_deps.py --pattern location.builder.fields --target R0n-L07
python tools/ledger.py done 11 R0n-L07 && python tools/ledger.py built R0n-L07
```

## Patterns

**Open the cell file first and write to its form.** The sentence bands, the
feature counts and the tables each cell leans on are stated there and they are
not the same across the nine. A `DANGEROUS_LOW` room written to the
`WILD_HIGH` form is a corridor with an approach passage on it.

**The required fields are the region's type, and they are not optional.**
`SAFE` declares a Service, a Cost and a Refusal. `WILD` declares an Approach
and Terrain. `DANGEROUS` declares Reactions and a Gate. `validate.py` checks
that every one is present and that none is a bare `None` (M22). A field may be
`None` and the nil carries its reason, which is a decision written down rather
than a gap.

**State every measurement in the region's own units, and take them from the
region's Fields.** Feet indoors, yards outdoors and miles on safe roads in a
`SAFE` region; yards and miles in a `WILD` one; feet indoors and yards outside
in a `DANGEROUS` one. Time in days, in watches six to a day, or in turns six to
an hour, by type. A location measured against the wrong ruler is internally
consistent and wrong, and no later step catches it.

**Every rate in this location is the region's rate or a stated departure from
it.** Say which. A location that quietly halves the region's rate has moved a
decision the party was supposed to be able to compute.

**Features are `### Name` subsections and each opens with what the thing is.**
Then what it does, then what a named physical action reaches inside it. A
referee reading only the first line of each feature can still run the location,
and that is the test the format is written to pass.

**The three layers are written as three layers.** The landmark layer is what
arriving and looking gives, and it is step 12's Player Overview. The hidden
layer is a feature's name and its opening line, reached by asking about a thing
named above or by spending time. The secret layer is inside that same feature
and is gated on a named physical action: standing somewhere, clearing
something, opening something, speaking a name, looking back.

**Every secret carries at least one clue** (J2). Proximate, in this location, or
distributed, reached through the tables. A `T-LOR` entry reinforcing an `S-HIS`
item is a clue and it is how S content reaches a player at all. A secret with
no clue is a die roll wearing a costume.

**No secret and no clue resolves on a roll.** What a roll adjudicates is what
the time costs, and the one place a die may gate a result is `T-PRC`, where the
entry states all three outcomes. Cite the procedure rather than writing a new
one.

**Reach the shared substance through the tables and never around it.** A
creature is `(BESTIARY, <name>)` or `(NAMED CREATURES, <name>)`, terrain and
construction are `T-ARC`, a hazard is `T-HAZ`, a legible thing is `T-LOR`, a
gate's key is `T-KEY`, and the mark resolves or `validate.py` says so (M16). A
creature invented in a location is a creature no other location can use.

**Traps and ordinary hoards are local and are written here.** Both have their
own pattern in this directory: `traps.md` for a trap's tell, trigger, cost and
answer, and `hoards.md` for composing a hoard from the treasure tables at the
point of use. Neither is a table, and the reasoning is in SPEC.md section 4.8.

**Mechanics are tokens and prose states no mechanical value.** `MECHANICS.md`
holds the vocabulary, `validate.py` checks every token against it (M21) and
reports a bare value in prose (M24). A token sits beside the sentence it belongs
to, referee-facing, and never in a Player Overview.

**Treasure carries value, weight and quality, and the weight is real.** What a
party takes out of this location changes what they can do in the next one, and
that is the decision the weight exists to create. A hoard written as a lump sum
has removed it.

**The connection pointer lives inside a feature and nowhere else** (M23). It is
what the diagram derivation reads, so any other use of `->` corrupts the graph.
The feature that carries the route out is where it goes, in the sentence that
says where the route goes.

**Thin is not failure.** A field may be empty and a `LOW` location may hold one
feature or none. State the nil and its reason. A region where everything is
interesting has no landmarks, and padding a location to match its neighbour is
how that happens.

**Each deliberate defiance names the straight instances funding it, by code, in
the Referee Overview** (J8). Content that subverts constantly teaches a party
that nothing means what it looks like, and then every clue placed anywhere goes
unread.

**Strike the architect notes this step absorbs**, and record the target with
`python tools/ledger.py done 11 <code>` and `built <code>` after every file,
never only at the end of the pass.

## Excluded patterns

- **A feature that is really a location.** If it has its own exits, its own
  approach and something a party travels to reach, it is a file and it waits
  for a booked step 9 re-run rather than being smuggled in here.
- **A trap with no tell.** Every trap has a physical tell in what a party can
  see before it fires. A trap that exists only once it fires is a tax.
- **A discovery written as roll-gated.** Outside `T-PRC`, nothing in the corpus
  says a thing is found on a roll.
- **A creature, hazard or construction invented here.** It belongs in its table,
  where every location can reach it, and this location cites it.
- **A measurement in the wrong unit.** The region's type sets the units and the
  region's Fields state them. Both are in this bundle.
- **A statistic written as a number.** Everything mechanical is a token.
- **Prose in the Player Overview.** Step 12. This step writes fields, features
  and what is true.
- **Reading the `setting/` tree.** A subagent receives the pattern, the bundle
  and the target file. If it needs more, the dependency selector was wrong and
  the pattern changes.

## Design questions

1. **Which cell is this, and what does its form say?** Sentence band, feature
   count, and the tables it leans on. Answer before writing a line.
2. **What are this location's required fields, and which one is `None`?** A
   location with no nil field has usually not been asked a hard enough question.
3. **What is the secret here, if there is one, and what physical action gates
   it?** Then: what is the clue, and is it proximate or distributed?
4. **What comes out of this location, what does it weigh, and what is it worth
   to somebody in a lit place?** For a `LOW` location the honest answer is
   usually nothing, and that is stated.
5. **Which table does each feature reach, and does the mark resolve?** A feature
   that reaches none is content this location cannot share.
6. **What does this location cost in the region's time unit?** To cross, to
   work, and to undo.
7. **What is this location thin in contrast to?** Name the landmark. If the
   pass order has been kept, it is already written.
