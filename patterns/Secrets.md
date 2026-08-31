# Secret Patterns

Formalizes something this framework already does informally - a hidden Feature nested inside an obvious one - so hidden content stays reliably discoverable instead of ad hoc. Unlike `Treasure.md`, `Creatures.md`, `Traps.md`, and `Puzzles.md`, a Secret isn't tied to one chosen pattern bullet; it's a layer that can sit on top of any Feature a location already has, decided independently at generation time.

## Inclusion
A Secret's presence is a rate, not a mandate - decide against these odds at generation time, based on the region's rating and (for DANGEROUS) the location's weight:
- SAFE: >10% of locations.
- WILD: >20% of locations.
- DANGEROUS, low weight: >30% of locations.
- DANGEROUS, medium weight: >40% of locations.
- DANGEROUS, high weight: no fixed rate - include one only when it genuinely fits alongside the location's other Features; high weight already carries its own density of content.

## Structure
Every Secret has three parts, all stated:
- **Clue** - an obvious detail already visible or discoverable through ordinary observation, not itself the secret, but noticeable enough to invite a closer look.
- **Trigger** - the specific action that acts on the clue to reveal or unlock the secret (examining, pressing, aligning, speaking, removing).
- **Payload** - what the trigger produces: a secret door or exit, a neutralized effect (a trap disarmed, a hazard bypassed), a puzzle solved, a hidden trap revealed before it's sprung, or treasure uncovered.

A Secret without a stated Clue isn't discoverable - it's just a fact the referee knows and the players can never find. All three parts are required, even stated briefly.
