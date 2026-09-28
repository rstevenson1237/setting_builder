# Dangerous - Low

## Provides
One low-weight DANGEROUS location: a room that looks like nothing, and what its own exits
require of it.

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
          Clue    - the building disagreeing with itself, already visible in this
                    room's own Dressing and not itself the secret             {CLUE}
          Trigger - a stated act on the clue, worked by hand or by tool   {TRIGGER}
          Payload - the concealed route, where the block diagram drew one; otherwise
                    {a cache | a piece of Lore | a Key | a hazard understood before it
                     fires}

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
  30%   A second name, from a different mouth than the first
                                                (patterns/setting/Naming.md)
```

```
CLUE - exactly one
  mismatch     - a surface not matching its neighbours in course, colour or wear
  wear         - wear leading toward something that is not there
  draught      - air or sound moving where the room accounts for none
  seam         - a hinge, a groove or a seam
  moved        - a fixture that has been moved
  clean        - something cleaner than what is around it
  repair       - a repair
  stranded     - something built to be reached that no longer can be
  short        - an inscription or pattern broken off before its end
```

```
TRIGGER - exactly one
  worked       - a stated fixture pressed, turned, lifted, prised or slid
  weight       - weight applied or removed
  dug          - digging at a stated spot
  fitted       - an object carried in from elsewhere, fitted
  sequence     - things opened or moved in a stated order
  light        - a light lit or put out
```

## Constraints
