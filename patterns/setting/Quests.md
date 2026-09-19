# Setting - Quests

## Provides
What earns a row in `setting/Quests.md`, and what a finished entry must state.

The per-rating decision of when to reach for a quest is in each folder's own `Quest.md`.

## Spec

```
QUEST ENTRY
  1     Who wants it, and why they will not go themselves
  1     What specifically, and which location holds it
  1     What stands in the way
  1     The terms, in the giver's own words
  1     Both ends named by location code - a quest with one end is not a quest
```

**A quest is two-ended, and both ends must exist.** Every location exists as a gazetteer
stub before any location file is written, so both ends can be named at 4c and resolved at 4d
with both files in view.

**Supply is registered by targets, not requested by givers.** A location holding something
somebody would want records a stub when it is written, whether or not a giver exists yet.
Givers are drafted from what has been registered.

**Distinguishing a Quest from a Key.** Same shape, opposite ends: a Quest is asked first and
fulfilled later; a Key is found first and used later. A quest object that also opens
something carries both rows.

## Constraints

- **A quest needs a middle.** Two ends make a delivery. What stands in the way is what makes
  it an adventure, and it is stated at the target end, where it lives.
