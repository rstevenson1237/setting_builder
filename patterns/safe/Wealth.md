# Safe - Wealth

## Provides
What a settlement's own cache of treasure, lore, or both actually holds, who it belongs to,
and what stands between a party and it. Alone among the five Kinds it may answer
`safe/Settlement.md`'s gate line with its Protection rather than with a person's terms.

## Spec

```
WEALTH
  1     Contents                   {Treasure | Lore | Both}
                        (patterns/setting/Treasure.md,
                         patterns/setting/UniqueTreasures.md, safe/Lore.md)
  1     What it holds, stated concretely             (genre: wealth-contents)
  1     Who it belongs to, or belonged to - and whether they know it is still here
                                                     (genre: wealth-owners)
  1     Protection, exactly one    {hidden | gated | guarded | trapped}
                                                     (genre: wealth-protection)
          hidden: guaranteed by this line, and states
            Clue    - legible in the building itself to somebody paying attention
            Trigger - a stated act on the clue
            Payload - the cache, and who notices it has been found
  30%   A second protection, of a different kind than the first
  20%   Somebody else wants it, and is closer to getting it than the party
```

**The Clue is what the building gets wrong about itself**, and per `GENRE.md` it is legible
before anyone knows there is anything to find.

## Constraints

- **A second protection compounds rather than repeats.** Hidden and trapped means finding
  it is not the same as surviving opening it; gated and guarded means knowing the phrase
  still leaves whatever is standing behind it.

- **A guard drawn from the region's standing problems is reframed, not duplicated.** What
  it supplies here is the reason nobody has cleared this out: dealing with it has always
  cost more than the wealth is worth.
