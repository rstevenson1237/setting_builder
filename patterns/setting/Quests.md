# Setting - Quests

## Provides
One quest: a lead with a reward - who wants what, on what terms, and what stands in the
way. It points one way, at where its object lies, or at nothing on this map; a quest
object that also opens something carries a Keys row as well.

## Spec

```
QUEST ENTRY
  1     Ask                                                                 {ASK}
  1     Giver - who wants it, and how a party comes to hear of it
  1     Reluctance - why they will not go themselves                  {RELUCTANCE}
  1     Object - what specifically
  1     Obstacle - what stands in the way                             {OBSTACLE}
  1     Terms - in the giver's own words                                  {TERMS}
  1     Points to - the location code or setting entry holding the object, or
        nowhere on this map
```

```
ASK - exactly one
  retrieve     - bring something back
  find         - find someone or something, or confirm it dead
  deliver      - take something where the giver cannot go
  destroy      - end something
  verify       - learn whether something is still so
  take         - take something from a person
  collect      - collect a debt
  recover      - bring a body back
  message      - carry word to someone who will not receive the giver
```

```
RELUCTANCE - exactly one
  unable       - something about them bars them from going
  burned       - it nearly killed them
  shamed       - going would admit something
  needed       - they are needed here
  turned back  - they went, turned back, and cannot say so
```

```
OBSTACLE - exactly one
  living       - it is inside something living
  guarded      - something that will not negotiate holds it
  fragile      - taking it breaks it
  watched      - taking it is noticed
  contested    - somebody else is already there for it
  misplaced    - it is not where the giver said
  misdescribed - the giver's description is wrong in a way that matters, and they know
```

```
TERMS - exactly one
  fee          - coin, half up front or not
  share        - a stated share of what is found
  favour       - goods, standing, or a debt forgiven
  loan         - the use of something the giver owns
  bait         - generous, because the giver expects not to pay
```

## Constraints

- **Points to is said, never left blank.** A quest pointing off the map says so, so a
  deliberate lead beyond the edge reads differently from one nobody finished.
