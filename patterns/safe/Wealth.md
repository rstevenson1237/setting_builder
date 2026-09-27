# Safe - Wealth

## Provides
What a settlement's own cache of treasure, lore, or both holds, who it belongs to, and
what stands between a party and it. Alone among the Kinds it may answer
`safe/Settlement.md`'s gate line with its Protection rather than a person's terms.

## Spec

```
WEALTH
  1     Contents                   {Treasure | Lore | Both}
                        (patterns/setting/Treasure.md,
                         patterns/setting/UniqueTreasures.md, safe/Lore.md)
  1     Who it belongs to, or belonged to, and whether they know it is still here
                        {an authority's reserve | a household's | a temple's |
                         a guild's common fund | the settlement's own}
  1     Protection, chosen for the cache rather than rolled                {PROTECTION}
  30%   A second protection, of a different kind - compounding rather than repeating
  20%   Somebody else wants it, and is closer to getting it than the party
```

```
PROTECTION - exactly one
  hidden       - concealed, stating its Clue (what the building gets wrong about
                 itself), Trigger (a stated act on the clue) and Payload (the cache, and
                 who notices it has been found)
  gated        - known and unconcealed, opened by a stated condition that is not secret
  guarded      - watched by a creature the Region Overview already has working, cited
                 by name
  trapped      - set with a trap: 5% lethal, else 35% damaging, else nuisance; somebody's
                 work, which marks, jams, or ruins the goods more often than it kills
```

## Constraints

- **A hidden Protection has spent its concealed detail.** Never roll
  `safe/Settlement.md`'s concealed-detail rate against it as well.

- **Never invent a Bestiary entry to guard it.** Where the Region Overview has no creature
  working that fits, the Protection is a different one.

- **A lethal trap here is rare and deliberate** - reserved for a cache the region's
  Situation already justifies treating that seriously. A trap is written as one Feature,
  per `templates/Location.md`.

- **Its lore has no living holder.** Unlike `safe/Lore.md`'s kept records, nobody holds a
  cache's documents or the holder does not know they are here, so its Protection stands
  where an access clause would.
