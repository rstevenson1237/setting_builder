# Dangerous - Mystery

## Provides
What the strange thing is, how it is engaged, and what engaging it wrongly costs. Distinct
from `dangerous/Hazard.md`, which is the costly case, and from a concealed detail, which is
a discovery structure the weight file rates: a Mystery is content and may be in plain sight.

## Spec

```
MYSTERY
  1     Fixture, built or placed with purpose, never found debris
        {ward | water | altar | statue or effigy | illusion | machinery}
                                                        (genre: mystery-fixtures)
  2     Physical details it can be reasoned from - the floor, not the target: one detail is
        guessed at, three is reasoned out               (genre: mystery-properties)
  1     Trigger, stated explicitly                      (genre: mystery-triggers)
  1     What the correct trigger accomplishes
  1     What a genuinely wrong attempt costs
  40%   A third detail, where the trigger is more than one step
```

**Pick the fixture first and the details are already half-written.** Machinery is reasoned
from wear, travel and what it connects to; water from level, flow and what is in it; a
statue from pose and what is worn smooth; an altar from fittings, channels and stains; a
ward from what is kept clean and what stops short of it; an illusion from what disagrees.

**A Mystery left uninvestigated is neutral.** Inspection, theorising and a wrong guess that
stops short of a real attempt all cost nothing.

## Constraints

- **Ward and illusion are sorcery, and `GENRE.md` prices it.** Each has a maker traceable
  to an event in `setting/History.md`, and a region carries at most one of them - the same
  one a warded exit at `dangerous/Door.md` spends. A region that reaches for the two rare
  fixtures twice has made sorcery the ordinary case.

- **A fixture whose answer is elsewhere in the region is a lock.** It owes a
  `setting/Keys.md` row through `dangerous/Key.md`'s demand end, or the party arrives at a
  socket that nothing in the setting fills.

- **A fixture that costs on contact is a hazard.** Anything that acts on entry, on touch,
  or on presence is drawn at `dangerous/Hazard.md`.
