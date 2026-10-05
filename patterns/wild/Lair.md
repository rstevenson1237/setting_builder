# Wild - Lair

## Provides
What an occupied Landmark is - a place something currently lives, whether it built the
place or moved in - and what its occupancy implies about the country around it.

## Spec

```
KIND: LAIR
  1     Lives - what lives here, from setting/Bestiary.md
  1     Holding - the holding it has made          {dug | built | taken over | occupied}
  1     Territory - the territory it claims, and how far that reaches
  1     Sign - a sign of it readable before the lair itself is reached
  1     Eats - what it eats, and where that comes from: the party's leverage
  1     Child - where the region's graph gives it a child, what the child is
                                    {the den proper | the midden | the larder |
                                     the killing ground}
  40%   Dependants - young, stores, or dependants: a reason it cannot simply leave
  30%   Absent - absent when the party arrives, and elsewhere in the region
  20%   People - what holds it is people, answering to a faction from
        setting/Factions.md     {a camp | a band | a hermit | a picket}  (wild/Faction.md)
```

## Constraints

- **A den nobody could find is a room.** A Lair matters to its region through its
  territory; one whose owner ranges nowhere has not been written as a lair.
