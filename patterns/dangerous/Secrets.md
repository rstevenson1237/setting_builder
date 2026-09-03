# Dangerous - Secrets

## Decides
Whether a DANGEROUS location hides something, and the three parts that make it findable.

## Read at
Step 4c, for every DANGEROUS location - consulted unconditionally to decide whether there
is a secret at all. A Secret is a discovery structure and may sit on top of any feature the
location already has; it is not drawn by a spec line. Distinct from
`dangerous/Mystery.md`, which is content and may be in plain sight.

## Spec

```
SECRET
  1     Clue    - already visible through ordinary observation, and not itself the secret
  1     Trigger - the specific action that acts on the clue
  1     Payload - what the trigger produces
```

Rate, by weight and node role:

```
INCLUSION
  low weight, dead end     50%   - this is the role's entire question
  low weight, other        30%
  medium weight            40%
  high weight              by fit only - high weight already carries its own density
```

The dead-end rate is the one that matters. If a dead end never hides anything, players
stop checking and the role dies. If it always does, it is not a secret - it is a step.
Half is the number that keeps the question live.

**A Secret without a stated Clue is not discoverable.** It is a fact the referee knows and
the players can never find, and it is the most common way this structure fails. The clue
has to already be legible to a player paying attention, before they know there is anything
to find.

## Patterns

**Clues** - a draft where there should be none; a wall that does not match its neighbours
in course, colour, or wear; a floor worn toward a blank face; a fixture that has been
moved; a sound that carries further than the room accounts for; a hinge, a groove, or a
seam; something too clean; a repair; a thing built to be reached that no longer can be;
an inscription that is one word short.

**Triggers** - pressing, turning, lifting, or sliding a stated fixture; placing or removing
weight; fitting an object carried from elsewhere; speaking something recorded elsewhere in
the region; opening in a stated order; flooding, draining, lighting, or extinguishing;
breaking something on purpose.

**Payloads** - a way through, on or off the region's map; a cache, cited from a table; a
hazard neutralised before it fires; a trap revealed before it is sprung; a mystery answered
in one step instead of several; a piece of lore; a shortcut back to somewhere already
cleared; a sight of somewhere the party has not reached yet.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
