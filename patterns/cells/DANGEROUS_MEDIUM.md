# DANGEROUS_MEDIUM

> The working body of a level.

A `DANGEROUS_MEDIUM` location is a room with something to do in it. It holds a
mechanism, a hazard, a territory, a piece of a puzzle, a hoard to compose or a
door that will not simply open. It is where the level's difficulty is actually
paid, and it is written so that a party that reads it carefully spends less than
a party that does not.

## What belongs here

- **Reactions branching on named player actions.** The type requires them and
  this cell is where they earn their keep. Name the action — the lid is lifted,
  the water is entered, the name is spoken, the light is put out, the thing is
  addressed — and state what follows. Two or three branches, each one line. A
  room that reacts only to being attacked has one branch and is a smaller room
  than it thinks.

- **One job for the level.** Every room in this cell does something for the
  whole: it gates a direction, it supplies a thing needed elsewhere, it warns
  about what is deeper, it is the answer to a gate somewhere else, or it is the
  cost of a shortcut. State the job in one line in the Referee Overview. A room
  that does no job for the level is a `LOW` room with furniture.

- **A hazard, a mechanism or a territory — usually one.** A hazard has a tell, a
  trigger and a cost, and it carries its tokens. A mechanism has a state, a way
  to read the state, and a way to change it that is physical. A territory has an
  occupant, a range, and what it does about an intruder before it does anything
  else. Two of the three in one room is close to the `HIGH` boundary.

- **A gate with a priced answer, where there is a gate.** Not a second door: a
  longer road, a darker one, or one watched by something worse. Both branches
  costed, and the text never names the mistake. Where the gate opens to a key,
  both ends are recorded in `T-KEY`.

- **Something worth carrying out, sometimes.** Where there is treasure, it
  carries value, weight and quality, and the weight is real: what a party takes
  from this room changes what they can do in the next one. An ordinary hoard is
  composed at the point of use by rolling the treasure tables.

- **A secret, where the room has a reason for one.** Gated on a named physical
  action, carrying at least one clue, proximate or distributed. Not every room,
  and never one per room as a rule.

- **The cost in turns.** Six to an hour. Say what the room costs to cross, to
  work and to undo. Time is the level's real currency and this cell is where it
  is spent.

## Where the boundary falls

- **Down to `DANGEROUS_LOW`** when the only thing to do here is notice
  something. Passing is `LOW`. Doing is `MEDIUM`.

- **Up to `DANGEROUS_HIGH`** when the room is the reason somebody would come to
  this level, when it holds the level's answer, or when more than one route has
  to reach it for the level to work. Consequence for the room is `MEDIUM`.
  Consequence for the region is `HIGH`.

- **Not a location at all** when the mechanism is really a mechanism plus a
  corridor plus a store. Split it. Rooms in a `DANGEROUS` region are cheap and
  clarity is not.

## Form

- **Player Overview:** five to nine sentences. Dimensions and material first,
  then what is in it, then the state it is currently in. Bold two or three nouns
  and give each a feature.
- **Features:** two to four. Each opens with what the thing is, then what it
  does, then what is inside it that a named action reaches.
- **Referee Overview:** the job for the level, the reactions and their branches,
  what is true that the Overview withholds, the gate and both prices, and the
  cost in turns.
- **Exits:** every one with a sensory cue. Where the room gates a direction, say
  what the gate looks like from both sides.
- **Tokens:** beside the feature that carries them. A test, a wound, a
  condition, a value, a weight, a quality. Referee-facing and never in the
  Player Overview.
- **Tables it leans on:** `T-HAZ`, `T-KEY`, `T-PUZ`, `T-ARC` for what recurs,
  `T-BES` for what holds territory, `T-TR1` to `T-TR5` for composing a hoard,
  `T-PRC` for what working the mechanism costs.

## Worked example

An illustration of the shape and the register. Nothing in it is canon, and the
codes are stand-ins.

**Player Overview.** Thirty feet square, and the ceiling is a barrel vault
running north to south. Down the middle of the floor is **a channel**, a foot
wide and a foot deep, cut level and dry. At the north end the channel ends at
**a plug** of the same stone, seated flush and cut with a slot across its face.
The vault is dressed on the north half and rough on the south, and the joint
between the two is a straight line across the ceiling. There is a smell of cold
iron that gets stronger toward the plug.

**Referee Overview.** *Job for the level:* this is the answer to the flooded
stair two rooms east. Pulling the plug drains that stair over four turns.
*Cost:* one turn to cross, two to read the channel, three to work the plug with
a bar. *Reactions:* if the plug is turned with the slot, it seats a quarter turn
and stops, and the stop is deliberate. If it is levered, it comes out whole and
cannot be put back. If the channel is entered, the party is standing in the
thing that will carry the water. *What is true:* the water that drains has been
standing since the level was cut, and it goes somewhere lower that nobody has
been to yet {TEST: Constitution} {WOUND: Poison}. *Gate and answer:* the flooded
stair is the short way down. The long way is the rough south half, which is a
worked face rather than a passage, and which comes out two levels lower having
cost the party the light they were saving. Neither is the mistake. *Clue:* the
slot in the plug is cut to the same width as the bar racked in the room the
party has already passed (ARCHITECTURE AND TERRAIN, T-ARC-07).

## Excluded patterns

- **A puzzle whose answer is a roll.** No secret and no clue resolves on a die.
  What a roll adjudicates is what time costs, and that is `T-PRC`.
- **A mechanism with no readable state.** A party must be able to tell what
  position the thing is in by looking at it, and to change it by doing something
  physical.
- **A trap with no tell.** Every trap in this cell has a physical tell in the
  Player Overview and a stated trigger. A trap that only exists once it fires is
  a tax.
- **A room that reacts only to violence.** Name three things a party might do
  and answer them.
- **A hoard listed as a lump sum.** Value, weight and quality, and the weight is
  what makes carrying it a decision.
- **Statistics written as numbers.** Everything mechanical is a token, and the
  vocabulary is `MECHANICS.md`.
- **A room that explains the level.** What is deeper is warned about physically:
  a smell, a temperature, a mark, a thing carried up and abandoned. Never a
  note left by a previous expedition summarising the plot.
