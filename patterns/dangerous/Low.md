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

Low weight means the location **looks like nothing**. It does not mean it is empty, and
that is the whole value of the class: if a low-weight room could never repay attention,
players would learn to walk through them, and attention would stop being a real cost.

**A clue underground is the building disagreeing with itself**: a wall not matching its
neighbours in course, colour or wear; a floor worn toward a blank face; a draught where
there should be none; a seam; a fixture that has been moved; something too clean; a repair;
a sound carrying further than the room accounts for; an inscription one word short.

**A trigger here is worked, not spoken** - pressing, turning, lifting, prising, sliding,
weighting, digging, fitting, lighting. Per `GENRE.md` the act is the mechanic; no search
roll stands in for it.

**Treasure here is never guarded**, because a guard is a challenge and LOW has none.

## Constraints

- **Never let a room that simply ends pay out a route off the map.** A Payload that is a
  hidden way through belongs to a room whose secret edge the block diagram actually drew,
  at 100%. If the room should have the route, draw the edge at 4b and let the rate follow.

- **A LOW room whose concealed detail has no stated Clue is an empty room.** Every other
  class has a challenge or a reward carrying it; this one does not.
