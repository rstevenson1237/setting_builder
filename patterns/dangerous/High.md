# Dangerous - High

## Provides
One high-weight DANGEROUS location: a room that announces itself, holds a challenge, and
pays out.

## Spec

```
DANGEROUS - HIGH

  -- substrate: what this room is
  1     Dressing - what it is now, and what it was      (dangerous/Dressing.md)
  1     An architecture detail unique to this location - what makes it look like
        somewhere that matters before anyone knows what is in it
  50%   An ambiance detail unique to this location
  -- no concealed detail: what a HIGH room hides is already carried by a Treasure
     whose disposition is hidden, or by a Hazard's or a Mystery's own clue

  -- challenge: what opposes the party
  1     Challenge          {encounter | hazard | mystery}
                                                     (dangerous/Encounter.md,
                                                      dangerous/Hazard.md,
                                                      dangerous/Mystery.md)
  50%   Second challenge   {encounter | hazard | mystery} - not the kind already drawn
  30%   Mystery, where it was not already drawn as a challenge  (dangerous/Mystery.md)

  -- reward: what is here to take
  1     Treasure                                            (dangerous/Treasure.md)
  40%   Second treasure, of a different disposition         (dangerous/Treasure.md)

  -- registry: what elsewhere points at this room
  1     Any lock obligation recorded against this room       (dangerous/Key.md)
  20%   Something here that someone elsewhere would want, registered as supply
                                                     (dangerous/Quest.md)

  1     Naming, after everything above           (patterns/setting/Naming.md)
  30%   A second name, from a different mouth than the first
                                                 (patterns/setting/Naming.md)
```

## Constraints
