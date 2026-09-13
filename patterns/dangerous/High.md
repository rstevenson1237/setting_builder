# Dangerous - High

## Provides
What a high-weight location guarantees.

## Read at
**Mode: entry.** Step 4c, for a location its gazetteer stub marks high. Generate the
region's high-weight locations first, so medium and low can foreshadow what has already
been decided.

## Spec

```
DANGEROUS - HIGH

  -- substrate: what this room is
  1     Dressing - what it is now, and what it was      (dangerous/Dressing.md)
  1     An architecture detail unique to this location
  50%   An ambiance detail unique to this location
  -- no concealed detail: what a HIGH room hides is already carried by a Treasure
     whose disposition is hidden, or by a Hazard's or a Mystery's own clue

  -- challenge: what opposes the party
  1     Challenge          {encounter | hazard | mystery}
                                                     (dangerous/Encounter.md,
                                                      dangerous/Hazard.md,
                                                      dangerous/Mystery.md)
  50%   Second challenge   {encounter | hazard | mystery} - not the kind already drawn
  30%   Mystery, where it was not already drawn as a challenge  (dangerous/Mystery.md)

  -- reward: what is here to take
  1     Treasure           {guarded | hidden | discarded}   (dangerous/Treasure.md)
  40%   Second treasure, of a different disposition         (dangerous/Treasure.md)

  -- registry: what elsewhere points at this room
  25%   A lock, and the key that opens it is elsewhere       (dangerous/Key.md)
  20%   The target of a quest given elsewhere                (dangerous/Quest.md)

  1     Naming, after everything above           (patterns/setting/Naming.md)
```

High weight means the location **announces itself**. The architecture line is mandatory
because that is what does the announcing: before a party knows what is in the room, the
room has to look like somewhere that matters. It is a question rather than an edge because
it is HIGH's own requirement - `dangerous/Dressing.md` supplies the baseline every location
gets, and MEDIUM and LOW do not demand this on top of it.

**Treasure is mandatory at HIGH.** A high-weight location the party clears and leaves
empty-handed has spent the region's scarcest slot on nothing.

## Constraints

- **Never add a discovery structure to a HIGH room.** What it hides is already carried by
  a Treasure whose disposition is hidden, or by a Hazard's or a Mystery's own clue. A
  separate one on top is a third thing to search in the region's most searched room.
