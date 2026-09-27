# Region - Dangerous

## Provides
One DANGEROUS Region Overview: the complex as a whole, which its blocks and rooms sit in.
How many locations it holds, in what weight mix, and how they connect is
`templates/Location_Gazetteer.md`'s and the connection templates'; what one block holds is
`dangerous/Block.md`'s, and what one room holds is its weight's own file.

## Spec

```
DANGEROUS REGION
  1     Kind - decided once, here, and stated first in Layout                 {KIND}
  1     Overview - three sentences: who built it, who took it and who holds it now; what
        a party comes for and what it costs; and the one thing true here and nowhere else
  1     Ambiance - sensory only, and true throughout: smell, sound carrying through the
        whole place, temperature, humidity
  1     Architecture - what it is built from and how well; one motif repeating through
        every room and tying them together as one work; the typical ceiling height and
        passage width every room defaults to
  1     Layout - its kind, its shape, its entrances, how deep it runs, and where its
        notable Features and Dangers sit; time runs on the Danger countdown, not hours
  1     Features - the facts that hold throughout: water, air, light, footing, what
        carries sound, what a fire does here
  1     Dangers - whether the place sleeps or is awake to intrusion, and what wakes it
  1     Creatures - who lives here, by setting/Bestiary.md name, and what living here
        takes: what they eat, where their water comes from, where their waste goes,
        where their young are, and what they guard, carry or know
  1     Factions - which of setting/Factions.md hold part of it as a position, and which
        sections, or `none`
  1     Secrets - what may be revealed about the setting's past, and what hidden ways
        exist, where
  1     Treasure - which of the five tables it leans on
  1     Tables - a d6 Danger table counting down from 6 with each failed Difficulty roll:
        entry 6 is the place noticing, entry 1 is the place acting
```

```
KIND - exactly one
  collection      - a worked complex of many parts, divided into blocks, whose size runs
                    with the region die
  single holding  - one occupant's home realized as a whole region, one block, whose
                    size is what the home actually contains
```

## Constraints

- **A single holding gets no tension from the countdown.** Its handful of rooms barely
  moves the Danger track, so its Overview names what supplies the pressure instead - a
  thing that cannot be fought, a way in that is not a way out, something that wakes.

- **Never a fact of the Overview restated in a room.** Ambiance, Architecture and
  Features are what every room shares, and a room states only what is its own.
