# Setting - Treasure

## Provides
One result on a treasure table: what it is, what it is worth, and what it costs to carry.
How many tables there are, what each holds, and how value spreads within one is
`templates/Treasure.md`'s; what holds a find, and what it takes to reach, is the
location's.

## Spec

```
TREASURE RESULT
  1     What it is - named as the thing itself, with no word on where it is stored,
        found or carried
  1     Value, in the coins named at the head of Table I
  1     Weight - what it actually takes to move, however large that gets        {WT}
  1     Density - at about 100 coins' worth per wt, or an order of magnitude denser
        for a small valuable, or far below it for mundane bulk
  1     Quality, on Table II only                                           {QUALITY}
  1     What it is made of, or struck in - from setting/History.md and
        setting/Truths.md: who made or minted it, and whether it is still accepted
  20%   A provenance a party could trace, worth more to the right buyer and dangerous to
        sell to the wrong one                     {a device | a maker | an owner}
```

```
WT - exactly one
  0            - pocketed and forgotten about, no call on anyone's hands
  1            - one hand, or about 100 coins
  2            - both hands
  3+           - more than one person to carry, and more still the higher it goes
```

```
QUALITY - at these rates
  poor         - 10%
  normal       - 50%
  fine         - 30%, and 30% of these carry an effect
  masterwork   - 5%, always carrying a positive effect
  cursed       - 5%, always carrying a negative effect, presenting as fine or
                 masterwork, and valued and described as what it presents as
```

## Constraints

- **Never decide the container.** A result is reusable everywhere and tied to no place.

- **Never shrink a weight to keep a number tidy.** A hoard is heavy because it is worth
  something, and the wt it costs is the decision the find exists to force.

- **Nothing past two orders of magnitude over the average is a table result.** It is a
  `setting/UniqueTreasures.md` entry.
