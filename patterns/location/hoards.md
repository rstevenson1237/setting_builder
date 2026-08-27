---
id: location.builder.hoards
target: location
phase: builder
writes: [Features]
dependencies:
  - region:${REGION_CODE}
  - cell:${CELL}
  - table:T-TR1
  - table:T-TR2
  - table:T-TR3
  - table:T-TR4
  - table:T-TR5
  - table:T-HRD
  - table:T-TRE
  - config
output_template: templates/location.md
schema_version: 1
---

Composing a hoard is a procedure, not a table. `T-HRD` holds the bespoke named
hoards, which are one collection because somebody made them one and are
therefore shared by construction. An ordinary hoard is assembled at the location
that holds it, by rolling the treasure tables, and the assembly happens here at
step 11.

`T-TRE` holds the named singletons: one of each, never restocked, each wanted
back by somebody still here. A location does not compose one of those either. It
places one, and placing one is a decision about the whole setting rather than
about a room.

This pattern is invoked from inside `location.builder.fields`. It writes no
heading of its own.

```
python tools/roll.py table T-TR2 --target R0n-L07 --count 3
```

## Patterns

**Roll it, do not choose it.** All randomness passes through `roll.py`, which
derives its seed from the setting seed and the target code, so the same location
composes the same hoard on a rebuild. A hand-picked hoard is a hoard picked to
suit the room, and every one of them ends up being what the party needed.

**Band by what the place was, not by how hard it was to reach.** `T-TR1` is
salvage stripped off what is left. `T-TR2` is goods somebody owned. `T-TR3` is
fine work and instruments. `T-TR4` is working devices. `T-TR5` is regalia the
Covenant made for its own offices. A store room holds goods however deep it is,
and a shaft head holds salvage however far a party walked to it.

**Three to six entries is a hoard. One entry is a find.** Most locations hold a
find or nothing. A location that holds a hoard has a reason it accumulated:
somebody was gathering, somebody stopped, somebody set it down, or the water put
it all in one place. State the reason in one clause, because a pile with no
reason is a prize rather than content.

**Every entry carries value, weight and quality, and the weight is the
content.** `{VALUE: n cn}`, `{WT: n}`, `{QUALITY: ...}`. A hundred coins is one
slot. What a party takes out of this location is what they cannot take out of
the next one, and that trade is the decision the weight exists to create. A
hoard written as a lump sum has deleted it.

**Say how it is held and in what order.** Stacked, sorted, scattered, sealed,
pegged, silted over, or lying where it fell in the order it fell. That sentence
is what a referee describes and it is what tells a party whether somebody has
been here.

**Say what cannot leave.** Almost every hoard has something in it that is not
portable without tools, not portable at all, or portable and recognised the
moment it is shown to anybody. Regalia is recognised on sight by anyone who
knows the Reach. A hold's door plate is missed by the people who kept the door.

**Where a `T-TRE` singleton is placed, place it against the whole setting.** It
is mentioned somewhere else in the corpus so that it can be sought rather than
stumbled on, and it is wanted back by somebody who is still here. Place at most
one per region, at a `HIGH` location, and write what the party carrying it is
now carrying.

**Where the location holds a `T-HRD` row, it holds the whole row.** A named
hoard is not partly present. Cite it as `(HOARDS, <name>)`, write how this
location holds it, and write what turns when something is taken from it.

**A `SAFE` region holds no hoard.** What is valuable in a lit place is owned,
priced and counted, and taking it is a transaction or a theft rather than an
extraction. Write the price instead.

**What comes out is not always an object.** A route, a name, a working device, a
way in, a measurement, a person willing to be led out. Where the extraction is
not a thing, it carries no tokens and it is still what the location is worth,
and the Referee Overview says what it is worth to somebody in a lit place.

## Excluded patterns

- **A hoard chosen to suit the room.** Roll it. The seed is what makes the file
  reproducible, and reproducibility is one of the four rules.
- **A lump sum.** Value, weight and quality, per entry, or it is not a hoard.
- **A hoard with no reason to have accumulated.** One clause. Somebody gathered
  it, or the water did.
- **Coin as the whole of it.** A hundred coins is one slot and a room of coin is
  a room with one decision in it.
- **A `T-TRE` singleton placed twice, or placed at a `MEDIUM`.** One of each,
  never restocked, and each is a landmark's content.
- **A hoard in a `SAFE` region.** Price it instead.
- **A guardian added because the hoard is good.** What holds territory is
  written because it holds territory. A hoard is not a difficulty setting.
- **An unowned hoard.** Somebody wants every one of these back, or knows it is
  gone, or is keeping a list. Name them, in a clause.

## Design questions

1. **What was this place, and which band does that put the hoard in?** The
   answer is what the room was for, not how deep it is.
2. **Why did it accumulate here, and why did that stop?** One clause, in the
   Referee Overview.
3. **How is it held, and in what order?** That sentence is what a referee reads
   out.
4. **What is the heaviest thing in it, and what does carrying that cost the
   party in the next location?** If the answer is nothing, the weights are
   wrong.
5. **What cannot leave, and who notices when it does?** Recognised, missed, or
   too heavy without tools.
6. **Is what comes out of this location actually an object?** A route or a name
   is an extraction and it is often the better one.
