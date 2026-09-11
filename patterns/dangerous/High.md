# Dangerous - High

## Provides
What a high-weight location guarantees.

## Read at
Step 4c, for a location its gazetteer stub marks high. Generate the region's high-weight
locations first, so medium and low can foreshadow what has already been decided.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Where a line names a file in parentheses,
that is the only other file this line requires.

```
DANGEROUS - HIGH
  1     Dressing, Secrets, and Naming, unconditional  (dangerous/Dressing.md,
                                                       dangerous/Secrets.md,
                                                       dangerous/Naming.md)
  1     Challenge            {creature | trap | mystery}
                                                      (dangerous/Creature.md,
                                                       dangerous/Trap.md,
                                                       dangerous/Mystery.md)
  50%   Secondary challenge  {creature | trap | mystery}   - not the same kind as the first
  30%   Mystery              - if not already taken as a challenge
                                                      (dangerous/Mystery.md)
  1     Architecture detail unique to this location  (dangerous/Dressing.md)
  50%   Ambiance detail unique to this location       (dangerous/Dressing.md)
  80%   Treasure             {hidden | trapped | discarded}   (dangerous/Treasure.md)
  40%   A Unique Treasure, in place of a table citation   (patterns/setting/Keys.md)
  30%   Lore, alongside the payload rather than instead of it   (dangerous/Lore.md)
  25%   A Named Creature, where the challenge is a creature   (dangerous/Creature.md)
  20%   Key or Quest involvement                         (dangerous/Key.md, dangerous/Quest.md)
```


High weight means the location **announces itself**. The architecture line is mandatory
because that is what does the announcing: before a party knows what is in the room, the
room has to look like somewhere that matters.


## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
