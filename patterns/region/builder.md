---
id: region.builder.fields
target: region
phase: builder
writes: [Fields, Tables]
dependencies:
  - container:${CONTAINER_ID}
  - table:S-AMB
  - table:S-FAC
  - table:T-ARC
  - table:T-BES
  - table:T-CRE
  - table:T-HAZ
  - config
output_template: templates/region.md
schema_version: 1
---

Step 7. The Builder writes the region's Fields and its referee table, and the
Weather table where the region has outdoor extent.

These are the numbers every location inside the region will be written against.
A location states its distances in the units the region states, moves at a rate
the region set, and counts time in the region's unit. Getting the Fields wrong
is not a region-scale error: it is thirty locations measured against the wrong
ruler, and no later step catches it because every one of them will be
internally consistent.

## Patterns

**State the units the region's type requires, and state them as numbers.** A
`SAFE` region states feet indoors, yards outdoors, miles on safe roads, and time
in days. A `WILD` region states yards and miles, and time in watches, six to a
day. A `DANGEROUS` region states feet indoors, yards outside, and time in turns,
six to an hour. The unit is not a flavour choice; it is what makes two locations
in one region comparable.

**Every rate is a distance over a time unit, and the exceptions are stated.**
The rate on the region's easiest ground, the rate off it, and what recovers
neither. A party that cannot compute how long a crossing takes cannot decide
whether to make it, and a region that leaves them to guess has moved the
decision to the referee.

**Say what the difficulty die measures here, in this region's own terms.** The
type decides which of the three it is. The Fields say what it looks like on the
ground: which goods and services the settlement's size puts out of reach, which
ground the terrain makes expensive, or how readily this place's hazards find a
party.

**A field may be `None`, and `None` carries its reason.** `validate.py` refuses
a bare `None` (M22). "Firm ground off the road: None, and the reedcutters agree"
is a field. "Firm ground off the road: None" is an author who might have
forgotten.

**The referee table is six rows on a `d6` and its name follows the type.**
Events for `SAFE`, Encounters for `WILD`, Dangers for `DANGEROUS`.
`config` carries `region_tables.rows` and `region_tables.die`, and
`validate.py` checks the name, the count and the direction (M19).

**A Danger table counts down from 6 to 1**, each rung a step further into the
region. It carries no mandated curve, and this is the sane default: atmosphere,
then ominous signs, then hazards requiring a test, then traps and minor
guardians, then danger avoidable only by care, then a forced encounter.

**Every row is different in kind, not only in detail.** Six rows is the whole
table and a party will see all six in a long session. Before writing a row, say
what a referee does with it that they could not do with any other row here.

**Rows reach the shared substance through the tables and never around them.**
A creature is `(BESTIARY, <name>)` or `(NAMED CREATURES, <name>)`, terrain is
`T-ARC`, a hazard is `T-HAZ`, and the mark resolves or `validate.py` says so
(M16). A creature invented in a region table is a creature no other region can
use and no location can cite.

**Rows carry mechanics as tokens.** `MECHANICS.md` holds the vocabulary and
`validate.py` checks every token against it (M21) and reports a bare mechanical
value in prose (M24).

**Entry register.** A fragment, read aloud from the table at speed. What is
there and what it is doing, not what it means and not what a party should do
about it.

**A Weather table is six rows and each one changes something.** What the sky is
doing is the setup; what it does to sight, to sound and to the rate is the row.
Weather that only sets a mood is a row a referee skips.

**Strike the architect notes this step absorbs.** The Fields note and the table
notes go when their content lands.

## Excluded patterns

- **A row naming a specific location.** The region table fires anywhere in the
  region. Anything true of one place is that place's, and it is written there.
- **A row that is a category.** "A dangerous animal" is a category. "Reed-hounds
  working the shallows in threes, keeping pace a chain out" is a row.
- **A creature, hazard or terrain feature invented here.** It belongs in its
  table, where every region can reach it, and the row cites it.
- **A rate with no unit, or a unit the region's type does not use.** Both are
  the same error and both propagate into every location.
- **A discovery written as roll-gated.** Outside `T-PRC`, nothing says a thing
  is found on a roll. What a roll adjudicates is what the time costs.
- **Prose in the Overview.** Step 8. This step writes numbers and rows.
- **Padding a field to look complete.** State the nil and its reason.

## Design questions

1. **What does this region count in, and what is its easiest ground?** State the
   unit and the rate on it before anything else, because every location inherits
   both.
2. **What does leaving that ground cost, in the region's own time unit?** And
   what, if anything, recovers it?
3. **What does the difficulty die measure here, in this region's terms?** One
   sentence a referee can rule from.
4. **Which field is `None`, and why?** A region with no nil field has usually
   not been asked a hard enough question.
5. **What are the six rows, and what does each let a referee do that the others
   do not?** For a `DANGEROUS` region, what does each rung of the descent add?
6. **Which rows reach the shared tables, and which table does each reach?**
   A row that reaches none is content this region cannot share.
7. **Is this region open to the sky, and what does each weather row change?**
   Sight, sound, or the rate. A row that changes none of the three is atmosphere
   the Overview already carries.
