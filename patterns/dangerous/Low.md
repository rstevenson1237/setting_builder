# Dangerous - Low

## Provides
What a low-weight location guarantees, and what its node role requires of it.

## Read at
Step 4c, for a location its gazetteer stub marks low. Node role is taken from the region's
`Connections.mmd`, written at 4b.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Where a line names a file in parentheses,
that is the only other file this line requires.

```
DANGEROUS - LOW                        (parameterized by node role)
  1     Dressing, Secrets, and Naming, unconditional  (dangerous/Dressing.md,
                                                       dangerous/Secrets.md,
                                                       dangerous/Naming.md)
  1     Node role honoured, per the Patterns below    (this file)
  14%   Treasure - unguarded, cited from a table      (dangerous/Treasure.md)
  20%   A detail that rewards looking without demanding action
  10%   A detail that foreshadows a HIGH location elsewhere in the region
  10%   Key or Quest involvement                      (dangerous/Key.md, dangerous/Quest.md)
```

Low weight means the location presents as unremarkable. It does not mean the location is
empty: a low-weight room may hide a secret door, hold a corpse worth searching, or open
onto the region's worst decision. What makes it low is that **it looks like nothing**.

That is the whole value of the class. If a low-weight room could never repay attention,
players would learn to walk through them, and the region would lose the only thing that
makes attention a real cost.

## Design patterns

**What honouring a node role means** - the role is read off `Connections.mmd` at 4b, not
chosen here, and it changes the Exits line and, for some roles, the Secret. Per
`dangerous/Dressing.md`, every exit still gets its own type and position regardless of role.

- **Entryway** - one exit reads as the way in from outside the region rather than to
  another location: state what marks it from the outside (a specific approach, not "the
  entrance").
- **Simple connection** - one exit in, one out, no decision. Dressing still earns its
  baseline; a corridor is not exempt from having a purpose and a sensory fact.
- **Dead end** - exits stop at one. Per `dangerous/Secrets.md`'s 50% dead-end rate, roughly
  half of these hide a Secret whose Payload is a cache or a piece of lore, not a route -
  that is what keeps this role distinct from Appears as dead end below.
- **Appears as dead end** - presents with exactly one exit, same as Dead end, but carries a
  Secret whose Payload is specifically the hidden (-.-) route recorded at 4b. The Clue has
  to be findable before the room reads as a dead end at all, or the room is just a dead end
  that got lucky.
- **Branch** - two exits, both eventually reconverging elsewhere in the region. Per
  `dangerous/Dressing.md`, the two exits must be told apart by type and position, not just
  labeled - a real choice, not a coin flip.
- **Branch (many)** - three or more exits. The room's Purpose or Architecture should account
  for why this particular space has that many ways out - a junction, a collapsed chamber
  with several breaches, a room built to be passed through from any side.
- **Divide** - a choice that does not reconverge: each exit commits the party to a distinct
  wing of the region they cannot cross back between without retracing. State that
  consequence in the room, not just in the graph - per GENRE.md, a divide the players can't
  see coming makes their decision for them instead of letting them make it.
- **Loop leg** - one of a chain of three or more locations that returns to an
  already-visited node without reusing an edge - a circular route. A single loop leg's own
  entry does not need to announce the loop; the loop is a fact about the graph, discovered
  by walking it, not a line of text repeated at every leg.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
