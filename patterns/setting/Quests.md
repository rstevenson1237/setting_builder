# Setting - Quests

## Provides
One quest: who asks, for what, at which location, what stands in the way, and on what
terms. A quest is asked before it is fulfilled, where a key is found before it is used; a
quest object that also opens something carries a Keys row as well. When a location gives
or holds a quest is its rating's own `Quest.md`.

## Spec

```
QUEST ENTRY
  1     The ask                                                             {ASK}
  1     Who wants it, and why they will not go themselves             {RELUCTANCE}
  1     What specifically, and which location holds it
  1     What stands in the way, stated at the target end              {OBSTACLE}
  1     The terms, in the giver's own words                               {TERMS}
  1     Both ends named by location code
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

- **A quest with one end is not a quest.** Both ends are real locations, named by code;
  two ends without an obstacle are a delivery.
