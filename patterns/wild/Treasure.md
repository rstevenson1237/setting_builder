# Wild - Treasure

## Provides
What a WILD location holds to be taken, why it is still out here, and what reaching it
costs. The tables are `setting/Treasure1.md`-`5.md`; a lock or a quest this place holds
for somewhere else is its classifier's registry.

## Spec

```
TREASURE
  1     What it is - exactly one, drawn at these rates rather than freely chosen, so the
        key the open country exists to separate is not lost to the cheapest option
        {table roll 45% | key 30% | lore 20% | unique treasure 5%}
                        (patterns/setting/Treasure.md,
                         wild/Key.md, wild/Lore.md,
                         patterns/setting/UniqueTreasures.md)
  1     Why it is still here after weathering
                           {buried | sealed | submerged | sheltered | recently left}
  1     What reaching it costs                  {climb | dig | wade | carry | wait}
  30%   Something that has a claim on it
                        {an animal nested in it | whoever buried it |
                         a faction that holds this country | whoever is coming back}
```

## Constraints

- **Never name or describe a table roll's contents.** The roll decides them. A key, a
  piece of lore or a unique treasure is named, because each is a registry row.

- **Never a pristine find in open country without a reason.** It has been rained on.
