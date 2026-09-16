# Dangerous - Low

## Provides
What a low-weight location guarantees, and what its own exits require of it.

## Spec

```
DANGEROUS - LOW                      (parameterized by this room's own exits)

  -- substrate: what this room is
  1     Dressing - what it is now, and what it was    (dangerous/Dressing.md)
  100%  A concealed detail, where this room has one mundane exit and a secret one -
        the concealed route IS the detail
  50%   A concealed detail, where this room has exactly one exit and it is mundane
  30%   A concealed detail, at every other exit count
        Each states:
          Clue    - already visible in this room's own Dressing, and not itself the secret
          Trigger - a stated act on the clue, worked by hand or by tool
          Payload - the concealed route, where the block diagram drew one; otherwise a
                    cache, a piece of Lore, a Key, or a hazard understood before it fires

  -- challenge: none. LOW presents as unremarkable, and a challenge here would
     make it a MEDIUM location. What LOW carries instead is its Secret.

  -- reward: what is here to take
  30%   Treasure - never guarded, and most often Table I   (dangerous/Treasure.md)

  -- registry: what ties this room to somewhere else
  10%   A detail that foreshadows a HIGH location elsewhere in the region
  1     Any lock obligation recorded against this room      (dangerous/Key.md)
  5%    Something here that someone elsewhere would want, registered as supply
                                                            (dangerous/Quest.md)

  1     Naming, after everything above          (patterns/setting/Naming.md)
```

Low weight means the location presents as unremarkable. It does not mean the location is
empty: a low-weight room may hide a secret door, hold a corpse worth searching, or open
onto the region's worst decision. What makes it low is that **it looks like nothing**.

That is the whole value of the class. If a low-weight room could never repay attention,
players would learn to walk through them, and the region would lose the only thing that
makes attention a real cost.

**Treasure here is never guarded**, because a guard is a challenge and LOW has none.
What LOW leaves lying is `dangerous/Treasure.md`'s Table I, Scavenged Loot - a detail that
rewards looking without demanding action.

**A clue underground is construction.** What gives concealment away down here is the
building disagreeing with itself: a wall not matching its neighbours in course, colour or
wear; a floor worn toward a blank face; a draught where there should be none; a hinge, a
groove, a seam; a fixture that has been moved; something too clean; a repair; a sound
carrying further than the room accounts for; a thing built to be reached that no longer
can be; an inscription one word short.

**A trigger here is worked, not spoken.** Pressing, turning, lifting, prising or sliding a
stated fixture; weight applied or removed; digging at a stated spot; fitting an object
carried in from elsewhere; opening in a stated order; lighting or putting out. What the
room hands a party is something to do with their hands, and per `GENRE.md` the act is the
mechanic - there is no search roll standing in for it.

**The Secret is LOW's whole load**, and it is the reason the DANGEROUS concealment rate lives
in the weight classes at all: no single rate could say what these three lines say.

**A room with one exit and a room with one exit plus a concealed route are different cases
precisely because of this rate.** A room that simply ends hides something only half the time
- if it never did, players would stop checking and the case dies; if it always did, it would
not be a secret, it would be a step. The other half of that question is the room whose
concealed route the block diagram already drew: that edge exists, so the detail revealing it
is not a rate but a certainty.

## Constraints

- **Never let a room that simply ends pay out a route off the map.** A Payload that is a
  hidden way through belongs to a room whose secret edge the block diagram actually drew,
  at 100%. Handing one to a room with no such edge turns a 50% room into a 100% one while
  the graph says otherwise - if the room should have the route, draw the edge at 4b and let
  the rate follow.

- **A LOW room whose concealed detail has no stated Clue is an empty room.** Every other
  class has a challenge or a reward carrying it; this one does not. An unstated clue here
  does not make the room subtle, it makes it the thing players learn to walk through, and
  it takes the class's only reason to exist with it.
