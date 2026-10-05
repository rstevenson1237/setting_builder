# Wild - Natural Feature

## Provides
What an unbuilt, unoccupied Landmark is, and why it is worth an action to visit. With no
builder and no occupant, it earns its slot on what it does.

## Spec

```
KIND: NATURAL FEATURE
  1     Is - what it physically is
  1     Scale - its scale in yards
  1     Matter          {stone | water | growth | ground | a weather effect outlasting
                         its cause}
  1     Stop for - why a party would stop
                                  {shelter | water | vantage | materials | a crossing}
  1     Unlike - one way it is not like the country around it
  30%   Mysterious - something mysterious about it, held to GENRE.md's Magic level
  30%   Resource - a resource findable here, tied to the region's Loot field
  20%   Hazard - a hazard that is simply part of the place
  15%   Faction - the resource is worked by a faction from setting/Factions.md, whose
        claim reaches past this place                             (wild/Faction.md)
```

## Constraints
