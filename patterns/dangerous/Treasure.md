# Dangerous - Treasure

## Provides
What a DANGEROUS location holds to be taken, what conceals it, and what stands between the
party and it. The tables are `setting/Treasure1.md`-`5.md`; the citation format is
`templates/region/Location.md`'s; a lock or quest target this room holds for somewhere else is its
weight file's registry.

## Spec

```
TREASURE
  1     Disposition                                                    {DISPOSITION}
  1     What - exactly one, drawn at these rates rather than freely chosen, since an
        unrated menu collapses to the table roll
        {table roll 55% | key 20% | lore 20% | unique treasure 5%}
                        (patterns/setting/Treasure.md,
                         dangerous/Key.md, dangerous/Lore.md,
                         patterns/setting/UniqueTreasures.md)
  1     Table - where a table roll: which of setting/Treasure1.md-5.md
  1     Unique - where a unique treasure: its setting/UniqueTreasures.md name
  1     Container - what it is in, under, or behind
  1     Material - what the container is made of
  1     Moves - whether the container can be moved                     {yes | no}
  1     Reach - the search or trigger that reaches it
  1     Seal                            {sealed | breached | reclosed | fused in place}
  1     Guard - where guarded: what guards it, and how it relates to what it guards,
        drawn as an Encounter or a Hazard   (dangerous/Encounter.md, dangerous/Hazard.md)
  25%   Lesser thing - something small living on or in the container, no match for the
        party, not knowing what it sits on, and a tell that nobody has been here
  25%   Set on - something set on the container itself, whatever the disposition, its
        clue the cache itself: mechanism fixed to trap
                                        (dangerous/Hazard.md, dangerous/Trap.md)
  30%   Tried - something already tried for it and failed
  20%   Left because - a reason it was left rather than taken
                        {too heavy | its owner never returned |
                         worthless to whoever holds this now}
```

```
DISPOSITION - exactly one
  guarded      - drawn on the Guarded line
  hidden       - in, under, or behind something, with a search or trigger that reaches it
  discarded    - in the open, unclaimed rather than unseen
```

## Constraints

- **A region's stated table-lean is a draw, not a claim.** A lean no room cashes out is a
  fact that reaches no player, and is settled at 5c.

- **Never write a lesser guard the party must fight.** The moment it is a threat it is the
  location's encounter, and the cache has two guards where the room was scoped for one.
