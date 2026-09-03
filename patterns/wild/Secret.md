# Wild - Secret

## Decides
What a Secret-tier location guarantees, and the trigger that reveals it.

## Read at
Step 4c, last of the three tiers, after its parent Landmark or Hidden location exists.

## Spec

```
WILD - SECRET
  1     Parent location, named
  1     Clue    - already visible in the parent's own Features
  1     Trigger - the specific action at the parent that reveals the way
  1     Payload - the connection to this whole location
  1     A reason it was worth concealing
  70%   Creature, treasure, trap, or mystery - one, from the element files
  40%   Lore, Key, or Quest involvement
```

The Clue/Trigger/Payload here is the same shape as a feature-level Secret, scaled up: the
Payload is an Exit to an entire location rather than a detail inside one. Mark the edge
hidden (`-.-`) in the region's `Connections.mmd`.

Unlike a feature-level Secret, this is **mandatory, not rated** - a Secret-tier location
without a stated Clue at its parent is unreachable, and unreachable content is content
that does not exist.

## Patterns

**Why a Secret exists.** Pick one before writing it:

- **A reward** - a cache, hoard, or Unique Treasure reached no other way.
- **Knowledge** - a piece of Lore, a Rumour confirmed or overturned, a Truth made physical,
  a Named Creature's origin.
- **A route** - a way around a Landmark's danger, into a neighbouring region, or to a
  DANGEROUS region's entrance that bypasses its obvious approach.

**Who concealed it, and against what.** A Secret with no concealer is a coincidence.
Somebody hid this, or something grew over it, or the country closed on it - and whichever
it was leaves different marks. Deliberate concealment is tidier than it should be; natural
concealment is messier; abandonment is neither, just old.

**Clues that survive weather** - a worked stone in a natural face; a plant growing where
that plant does not grow; a path worn by animals to a place with no water; a mark cut
above the reach of a person standing on the ground now; a name in `setting/Language.md`'s
older tongue attached to a place with nothing on it.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
