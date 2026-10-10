# Dangerous - Block

## Provides
One block of a DANGEROUS region: what holds its rooms together as one quarter, and how it
meets the blocks around it. How many blocks a region holds, how many rooms each, and how
their rooms connect is the connection templates'; what one room holds is its weight's own
file.

## Spec

```
BLOCK
  1     Basis - what holds it together                                        {BASIS}
  1     Family - where purpose: the family its rooms serve; each room takes whichever
        use serves the family, never one answering another block's question  {FAMILY}
  1     Household - where household: whose home it is, an occupant from
        setting/Bestiary.md or setting/Factions.md, and the rooms any home of theirs
        needs: where they sleep, eat, keep their stores, stand guard, and put their dead
  1     Ways in - how it meets the blocks around it: which ways in it keeps, and who or
        what watches them
```

```
BASIS - exactly one
  purpose      - a functional quarter, whose rooms serve one purpose family
  household    - one occupant's home, whose rooms are where one group lives
```

```
FAMILY - exactly one, for a block or for a room
  keeping      - storing things
  working      - making or processing things
  living       - the daily life of whoever is here
  holding      - confining people or things
  meeting      - gathering, receiving, or ruling
  believing    - worship and rite
  dying        - death, and the dead
  moving       - bringing people or things through
```

## Constraints

- **Never two purpose blocks on one family, or two household blocks for one occupant.** A
  second block answering the same question means the region has one block too many, or
  one too few doing something else.
