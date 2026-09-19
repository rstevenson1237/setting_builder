# Safe - Lore

## Provides
What written record a settlement holds, who controls access to it, and what it costs to
read. Also drawn by `safe/Wealth.md`, where a cache's contents are lore rather than
treasure. Criteria are in `patterns/setting/Lore.md`.

## Spec

```
LORE
  1     Physical form - a kept document, not a found one
                                                (genre: lore-forms-settlement)
  1     Who holds it, and why they have it       (genre: lore-holders-settlement)
  1     What it takes to be allowed to read it   (genre: lore-access-price)
  1     Whose voice, and what they were wrong about   (genre: lore-voice)
  1     What it does to what the party already thinks (genre: lore-effects)
  30%   It is incomplete, and the holder knows where the rest went
```

## Constraints

- **Spoken word is not Lore.** What a person tells the party is a rumour, and belongs in
  `safe/Social.md` and `setting/Rumours.md`. Lore is an object.
