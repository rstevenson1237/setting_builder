---
id: location.builder.traps
target: location
phase: builder
writes: [Features]
dependencies:
  - region:${REGION_CODE}
  - cell:${CELL}
  - table:T-ARC
  - table:T-HAZ
  - table:T-PRC
  - config
output_template: templates/location.md
schema_version: 1
---

A trap is local content. It is invented at the point of use, by the Builder, at
step 11, and it is written into the feature that carries it. There is no trap
table and there is not going to be one: a trap's whole content is its
relationship to the room it is in, and a row drawn from a table has no
relationship to anything.

**A trap construction that genuinely recurs across a region is not a trap.** It
is recurring architecture, it belongs in `T-ARC`, and the locations that carry
it cite it. That is the test, and it is the only reason this file exists as a
pattern rather than as a paragraph in the builder.

This pattern is invoked from inside `location.builder.fields`. It writes no
heading of its own.

## Patterns

**Four parts, always all four: tell, trigger, cost, answer.** A trap missing any
one of them is not finished. The tell is physical and appears in what a party
can see before they commit. The trigger is a named action. The cost is what
happens, carried as tokens. The answer is what a party who read the tell does
instead, and it is priced.

**The tell is in the Player Overview.** Not a hint that something is wrong: the
physical fact that is true because the trap is there. Soot in every niche and
one clean. Wear running all the way to a wall and not slowing before it. A seam
that runs crooked for a pace and then straightens. Write the fact and never the
inference, and let the table do the reading.

**The trigger is a named action, not a location on the floor.** A party does not
step on a trap; they open the thing, lift the thing, put weight on the thing,
take the last one off the stack. Name the action, because a referee is going to
be asked whether what a player just described counts, and a trap keyed to a
square foot of floor cannot answer that.

**The cost is a token and never a number** (M21, M24). `{TEST: ...}`,
`{WOUND: ...}`, `{CONDITION: name / effect / duration}`. A condition carries all
three parts and the duration is stated in the region's time unit. What a trap
costs is written in the mechanical layer and the fiction beside it says what
physically happens.

**The answer is what the tell buys, and it is priced.** Not immunity: an
alternative with its own cost. Going round is longer. Going slow costs turns
against everything else that is burning. Wedging it costs the wedge, which is
something the party is carrying and will want later. A trap whose only answer is
noticing it is a tax with a saving throw attached.

**A trap is a mechanism and its state is readable.** A party can tell by looking
whether the thing is set, sprung, jammed or already spent. Somebody else has
been here, and half the traps in a `DANGEROUS` region should be in a state that
says so: sprung and not reset, disarmed by a hand that knew how, or set by
somebody who came after the builders.

**One trap per location at most, and most locations have none.** The Reach's
danger is construction and occupation rather than a corridor of devices. A
level where every third room is trapped teaches a party to move at a rate that
makes the region unplayable, and then the time pressure that is the real
mechanism stops working.

**A trap the fiction cannot explain does not go in.** Somebody built it, for a
reason, against somebody. Name who and against what, in one clause in the
Referee Overview. Empire work protects a hold or a shaft and is indifferent to
who is in front of it. Anything set more recently was set by somebody who is
still out there.

**Where the cost of springing it is a crossing rather than an injury, say so.**
A trap that floods a passage, drops a slab, puts a light out or makes a noise
that carries is worth two that do wounds, because it changes the map and the
map is what the session is played on.

## Excluded patterns

- **A trap with no tell.** The single most common failure and the one this file
  exists to prevent. A trap that exists only once it fires is a tax on a party
  for having walked forward.
- **A tell that is a conclusion.** "The floor looks unsafe" is the referee
  reading for the party. "The dust lies unbroken across the middle of the floor
  and is scuffed along both walls" is a tell.
- **A trap found on a roll.** Nothing in this corpus is found on a roll. What a
  roll adjudicates is what the time costs, and that is `T-PRC`.
- **A trap with no answer.** Two ways, both priced, and the text never names the
  mistake.
- **A save-or-die.** The Reach kills parties by distance, light and load. A
  device that removes a character for reading slowly is not this setting's
  danger.
- **A trap table.** Content is a table when it must be shared between locations
  or is created before it is placed. A trap is neither, and one that is both is
  `T-ARC`.
- **A number in the prose.** Every cost is a token.
- **A trap in a `SAFE` region.** Nothing in a `SAFE` region carries combat
  statistics or a wound. The cost of pushing there is standing, obligation or
  risk.

## Design questions

1. **What is physically true about this room because the trap is in it?** That
   fact is the tell and it goes in the Player Overview.
2. **What named action sets it off?** State it as a thing a player says they are
   doing.
3. **Who built it, against whom, and is it still in the state they left it in?**
   A sprung trap is content and a reset one is a question.
4. **What does a party who read the tell do instead, and what does that cost
   them?** In turns, in load, or in what they arrive without.
5. **Does this change the map or only the party?** The ones that change the map
   are worth more and there should be fewer of the others.
6. **Does this construction appear anywhere else in the region?** If it does, it
   is `T-ARC` and this location cites it.
