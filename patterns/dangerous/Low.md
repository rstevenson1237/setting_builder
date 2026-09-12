# Dangerous - Low

## Provides
What a low-weight location guarantees, and what its node role requires of it.

## Read at
**Mode: entry.** Step 4c, for a location its gazetteer stub marks low. Node role is
taken from the region's `Connections.mmd`, written at 4b.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Every line is either an edge - it names a
file in parentheses, the only other file that line requires - or a question the generator
answers here.

```
DANGEROUS - LOW                        (parameterized by node role)

  -- substrate: what this room is
  1     Dressing - what it is now, and what it was    (dangerous/Dressing.md)
  1     Node role honoured, per the node-role spec below
  100%  Secrets, where the node role is "appears as dead end" - the hidden route
        IS the role                                   (dangerous/Secrets.md)
  50%   Secrets, where the node role is an honest dead end
                                                      (dangerous/Secrets.md)
  30%   Secrets, at every other node role              (dangerous/Secrets.md)

  -- challenge: none. LOW presents as unremarkable, and a challenge here would
     make it a MEDIUM location. What LOW carries instead is its Secret.

  -- reward: what is here to take
  30%   Treasure - never guarded, and most often Table I   (dangerous/Treasure.md)

  -- registry: what ties this room to somewhere else
  10%   A detail that foreshadows a HIGH location elsewhere in the region
  5%    A lock, and the key that opens it is elsewhere      (dangerous/Key.md)
  5%    The target of a quest given elsewhere               (dangerous/Quest.md)

  1     Naming, after everything above                      (dangerous/Naming.md)
```

Low weight means the location presents as unremarkable. It does not mean the location is
empty: a low-weight room may hide a secret door, hold a corpse worth searching, or open
onto the region's worst decision. What makes it low is that **it looks like nothing**.

That is the whole value of the class. If a low-weight room could never repay attention,
players would learn to walk through them, and the region would lose the only thing that
makes attention a real cost.

**The treasure line is the old pair merged.** LOW used to draw unguarded treasure at 14%
and "a detail that rewards looking without demanding action" at 20% - which is
word-for-word what `dangerous/Treasure.md` already calls Table I, Scavenged Loot. They were
one thing written twice, and the merged rate is what the two came to independently. Never
guarded, because a guard is a challenge and LOW has none.

**The Secret is LOW's whole load**, and the three rates above are the only place node role
feeds content rather than just the Exits line. LOW is also the reason the DANGEROUS
concealment rate lives in the weight classes at all: a single rate in
`dangerous/Secrets.md` could not say what these three lines say.

**Dead end and appears as dead end are different roles precisely because of this rate.** A
plain dead end hides something only half the time - if it never did, players would stop
checking and the role dies; if it always did, it would not be a secret, it would be a step.
Appears as dead end exists for the other half of that question: a location assigned that
role at 4b is committing, at the graph level, to the hidden route always being there.

**What honouring a node role means** - the role is read off `Connections.mmd` at 4b, not
chosen here, and it changes the Exits line and, for some roles, the Secret. Per
`dangerous/Dressing.md`, every exit still gets its own type and position regardless of role.

- **Entryway** - one exit reads as the way in from outside the region rather than to
  another location: state what marks it from the outside (a specific approach, not "the
  entrance").
- **Simple connection** - one exit in, one out, no decision. Dressing still earns its
  baseline; a corridor is not exempt from having a purpose and a sensory fact.
- **Dead end** - exits stop at one. Per the 50% dead-end rate above, roughly
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

- **Never let an honest dead end's Secret pay out a route off the map.** A Payload that
  is a hidden way through is what the "appears as dead end" role commits to at the graph
  level, at 100%. Handing one to a plain dead end quietly turns a 50%-rate room into a
  100%-rate one without the graph saying so - if the room should have the route, relabel
  its node role at 4b and let the rate follow.
