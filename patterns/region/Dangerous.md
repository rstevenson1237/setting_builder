# Region - Dangerous

## Provides
One DANGEROUS Region Overview: the complex as a referee runs an excursion into it without
opening a room - its ways in, what every room shares, who lives where and how they answer
an intruder, and where the prize lies. How many locations it holds, in what weight mix,
and how they connect is `templates/Location_Gazetteer.md`'s and the connection templates';
what one block holds is `dangerous/Block.md`'s, and what one room holds is its weight's
own file.

## Spec

```
DANGEROUS REGION
  1     Kind - decided once, here, and named in the Overview's first sentence   {KIND}
  1     Overview - what a party sees at the way in, and what it comes for
  1     Approach - every entrance: where it opens from, which block or room it leads
        into, and who or what watches it
  1     Conditions - what every room is unless its own entry says otherwise: what it is
        built or cut from, ceiling height and passage width, light, what carries sound
        and what deadens it, footing, air, and what a lit fire does
  1     Inhabitants - each occupant by setting/Bestiary.md or setting/Factions.md name:
        how many, which block or rooms, what they are doing now, what they want, and
        what they do on meeting a party
                      {fight | parley | flee | raise the alarm | ignore}
  1     Alarm - what raises it, who hears it first, and who comes - how many, from
        where, and how many turns later - in the order they arrive
  1     Places - for a collection, every block: its rooms by code, its occupant, its way
        in, what it holds worth the trip, and who it is at odds with; for a single
        holding, the same for its notable rooms
  1     Situation - what is changing inside, and the next two rungs: what each is, and
        what sets it off
  1     Loot - where the largest prize lies and what stands over it; what an ordinary
        find is and which treasure tables it draws on; and who outside will buy it, or
        want it back
  1     Secrets - each a fact the referee holds as true, and the act or place that
        brings it out
  1     Tables - a d6 Danger table counting down from 6 with each failed Difficulty
        roll, entry 6 the place noticing and entry 1 the place acting; and a d6 table of
        rooms for anywhere a party goes that no location keys - what the room is, and
        one thing in it
```

```
KIND - exactly one
  collection      - a worked complex of many parts, divided into blocks, whose size runs
                    with the region die
  single holding  - one occupant's home realized as a whole region, one block, whose
                    size is what the home actually contains
```

## Constraints

- **Every field sentence carries something usable at the table** - a name, a count, a
  room code, a distance, a ruling. A sentence about who built the place and why, or how
  it feels, is History's or nobody's, and is cut.

- **Never a secret without its answer.** The referee holds the truth even where the
  players never learn it.

- **A single holding gets no tension from the countdown.** Its handful of rooms barely
  moves the Danger track, so its Situation names what supplies the pressure instead - a
  thing that cannot be fought, a way in that is not a way out, something that wakes.

- **Never a fact of the Overview restated in a room.** Conditions are what every room
  shares, and a room states only what is its own; Places is an index, and what a room
  holds is its own entry's.
