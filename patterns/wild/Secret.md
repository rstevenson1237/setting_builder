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
  20%   Concealed detail inside this location - a second triple, not the access one
        below:
          Clue kind   - {growth | ground | weather | wear}
          Clue        - in this location's own Dressing, never the parent's
          Trigger     - a stated act here
          Payload     - never another location
                        {a cache | a piece of Lore | a Key |
                         why this place was worth concealing}
          Payload row - where a cache, a piece of Lore or a Key: the treasure row it is,
                        its disposition hidden

  -- access: how the party comes to be standing here, its payload the hidden (-.-)
     edge the region's Connections.mmd already drew
  1     Parent - the parent location, by code
  1     Access clue - already visible in the parent's own Features, written into the
        parent's entry
  1     Access trigger - the specific action at the parent that reveals the way
  1     Concealed because - a reason it was worth concealing

  -- challenge: what opposes the party
  40%   Challenge   {creature | hazard | mystery}    (wild/Creature.md, wild/Hazard.md,
                                                      wild/Mystery.md)

  -- reward: what is here to take
  40%   Treasure                                                     (wild/Treasure.md)

  -- registry: what ties this place to somewhere else
  20%   Quest - this location's carrying role in a quest given elsewhere (wild/Quest.md)

  1     Naming, after everything above                (patterns/setting/Naming.md)
  20%   Second name - from a different mouth than the first
                                                       (patterns/setting/Naming.md)
```

## Constraints

- **Never write one triple where the other belongs.** The access triple's Clue sits in the
  parent and pays out this whole place; the inner one is wholly inside it. Swapped, the
  location is unreachable or reached twice.

- **A Secret location carries no child.** A clue at a parent that itself has to be found
  by acting on a clue is two triggers deep and will not be reached.
