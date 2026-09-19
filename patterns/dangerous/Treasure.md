# Dangerous - Treasure

## Provides
What a DANGEROUS location holds to be taken - which registry or table it comes from, what
conceals it, and what stands between the party and it. The tables are `setting/Treasure1.md`
through `Treasure5.md`; the demand end - a lock or a quest target this room holds for
something elsewhere - is the weight file's registry lines.

## Spec

```
TREASURE
  1     Disposition   {guarded | hidden | discarded}
  1     What it is - exactly one, drawn at these rates rather than freely chosen
        {table roll 55% | key 20% | lore 20% | unique treasure 5%}
                        (patterns/setting/Treasure.md,
                         dangerous/Key.md, dangerous/Lore.md,
                         patterns/setting/UniqueTreasures.md)
  1     Which table, where the draw was a table roll  (genre: treasure-tables-underground)
  1     Container - what it is in, under, or behind   (genre: containers)
  1     Its condition, and the search or trigger that reaches it
                                                      (genre: container-condition)
  1     Hidden: what conceals it                      (genre: concealment)
  1     Guarded: what guards it, drawn as an Encounter or a Hazard
                        (dangerous/Encounter.md, dangerous/Hazard.md)
  25%   A lesser thing living on or in the container - small, no match for the party, and
        it does not know what it is sitting on         (dangerous/Creature.md)
  25%   Something set on the container itself, whatever the disposition - mechanism fixed
        to trap         (dangerous/Hazard.md, dangerous/Trap.md)
  30%   Something already tried for it and failed      (genre: treasure-claims)
  20%   A reason it was left rather than taken         (genre: treasure-survival)
```

**Never name or describe the contents of a table roll.** The cited roll decides them. This
does not apply to a unique treasure, a piece of lore, or a key: each is a stub row needing a
name.

**The rates exist because an unrated menu collapses to its first option.** Keys and Lore
reach a location only through this line, and a DANGEROUS region that finishes 4c having
drawn no key has skipped the draw.

**A lesser thing is not the guard.** Where the disposition is `guarded` the guard is still
drawn; what the lesser thing says is that nobody has been here.

## Constraints

- **One pull per citation.** A location wanting more takes a second citation elsewhere in
  its Features rather than multiplying one.

- **A region's stated table-lean is a draw, not a claim.** Treat it as a per-location draw
  and settle any that never got cited at 5c. A lean no room ever cashes out reaches no
  player.

- **Never write a lesser guard the party must fight.** The moment it is a real threat it is
  the location's encounter, and the cache has quietly been given two guards while the room
  was scoped for one.
