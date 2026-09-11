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
                                                       dangerous/Trap.md, see MYSTERY below)
  50%   Secondary challenge  {creature | trap | mystery}   - not the same kind as the first
  30%   Mystery              - if not already taken as a challenge   (see MYSTERY below)
  1     Architecture detail unique to this location  (dangerous/Dressing.md)
  50%   Ambiance detail unique to this location       (dangerous/Dressing.md)
  80%   Treasure             {hidden | trapped | discarded}   (dangerous/Treasure.md)
  40%   A Unique Treasure, in place of a table citation   (patterns/setting/Keys.md)
  30%   Lore, alongside the payload rather than instead of it   (dangerous/Lore.md)
  25%   A Named Creature, where the challenge is a creature   (dangerous/Creature.md)
  20%   Key or Quest involvement                         (dangerous/Key.md, dangerous/Quest.md)
```

```
MYSTERY, wherever one appears above              (content in dangerous/Mystery.md)
  1     Fixture - something built or placed with purpose, not found debris
  2     Physical details it can be reasoned from - the floor, not the target: one detail is
        guessed at, three is reasoned out
  1     Trigger, stated explicitly
  1     What the correct trigger accomplishes
  1     What a genuinely wrong attempt costs
  40%   A third detail, where the trigger is more than one step
```

High weight means the location **announces itself**. The architecture line is mandatory
because that is what does the announcing: before a party knows what is in the room, the
room has to look like somewhere that matters.

**A Mystery left uninvestigated is neutral.** Inspection, theorising, and a wrong guess
that stops short of a real attempt all cost nothing - this is what separates a Mystery from
a Trap: a trap fires on contact or presence, a mystery fires only on a failed attempt to
use it.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
