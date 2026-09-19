# Wild - Natural Feature

## Provides
What an unbuilt, unoccupied Landmark is, and why it is worth four hours to visit.

## Spec

```
KIND: NATURAL FEATURE
  1     What it physically is, and its scale in yards   (genre: natural-features)
  1     Why a party would stop - shelter, water, vantage, materials, or a crossing
  1     One way it is not like the country around it
  30%   Something mysterious about it, priced or dangerous to use, per GENRE.md
                                                        (genre: natural-strangeness)
  30%   A resource findable here, tied to the region's Foraging field
  20%   A hazard that is simply part of the place
  15%   The resource is worked by one of the three factions, whose claim reaches
        past this place                                        (wild/Faction.md)
```

## Constraints

- **It has no builder and no occupant, so it earns its slot on what it does.** A Natural
  Feature that offers nothing - no shelter, no water, no vantage, no materials, no way
  through - is terrain, and terrain belongs in the Region Overview's Terrain field.

- **Strangeness here is rare, never routine, and never free.** Per `GENRE.md`'s Low Magic a
  feature may carry something strange, but the cost is stated on the same line.
