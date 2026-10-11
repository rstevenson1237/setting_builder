# Wild - Treasure

## Provides
What a WILD location holds to be taken, why it is still out here, and what reaching it
costs. The tables are `setting/Treasure1.md`-`5.md`; a lock or a quest this place holds
for somewhere else is its classifier's registry.

## Spec

```
TREASURE
  1     What - exactly one, drawn at these rates rather than freely chosen, so the key
        the open country exists to separate is not lost to the cheapest option
        {table roll 45% | key 30% | lore 20% | unique treasure 5%}
                        (patterns/setting/Treasure.md,
                         wild/Key.md, wild/Lore.md,
                         patterns/setting/UniqueTreasures.md)
  1     Table - where a table roll: which of setting/Treasure1.md-5.md
  1     Unique - where a unique treasure: its setting/UniqueTreasures.md name
  1     Why here - why it is still here after weathering
                           {buried | sealed | submerged | sheltered | recently left}
  1     Reach - what reaching it costs          {climb | dig | wade | carry | wait}
  30%   Claim - something that has a claim on it
                        {an animal nested in it | whoever buried it |
                         a faction that holds this country | whoever is coming back}
```

## Constraints

- **Never a pristine find in open country without a reason.** It has been rained on.
