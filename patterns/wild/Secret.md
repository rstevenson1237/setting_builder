# Wild - Secret

## Provides
One Secret-tier WILD location, and the trigger at its parent that reveals it. It is the
end of a chain: its parent is the region's `Connections.mmd`'s, and it carries no child.

## Spec

```
WILD - SECRET

  -- substrate: what this place is
  1     Dressing - what it is, and what weather has done to it       (wild/Dressing.md)
  1     Kind   {ruin | lair | natural feature}      (wild/Ruin.md, wild/Lair.md,
                                                     wild/NaturalFeature.md)
  20%   A concealed detail inside this location - a second triple, not the access one
        below:
          Clue    - {growth | ground | weather | wear}, in this location's own Dressing,
                    never the parent's
          Trigger - a stated act here
          Payload - never another location
                    {a cache | a piece of Lore | a Key | why this place was worth concealing}

  -- access: how the party comes to be standing here
  1     Parent location, named
  1     Clue    - already visible in the parent's own Features
  1     Trigger - the specific action at the parent that reveals the way
  1     Payload - an Exit to this whole location, marked hidden (-.-) in the region's
        Connections.mmd
  1     A reason it was worth concealing

  -- challenge: what opposes the party
  40%   Challenge   {creature | hazard | mystery}    (wild/Creature.md, wild/Hazard.md,
                                                      wild/Mystery.md)

  -- reward: what is here to take
  40%   Treasure                                                     (wild/Treasure.md)

  -- registry: what ties this place to somewhere else
  20%   This location's carrying role in a quest given elsewhere     (wild/Quest.md)

  1     Naming, after everything above                (patterns/setting/Naming.md)
  20%   A second name, from a different mouth than the first
                                                       (patterns/setting/Naming.md)
```

## Constraints

- **Never write one triple where the other belongs.** The access triple's Clue sits in the
  parent and pays out this whole place; the inner one is wholly inside it. Swapped, the
  location is unreachable or reached twice.

- **A Secret location carries no child.** A clue at a parent that itself has to be found
  by acting on a clue is two triggers deep and will not be reached.
