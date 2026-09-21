# Safe - Quest

## Provides
How a SAFE location gives a quest: who asks, what they want, what they offer, and what
they leave out.

SAFE **gives** - this is the giver end. Criteria are in `patterns/setting/Quests.md`;
the registry is `setting/Quests.md`.

## Spec

```
QUEST - giver end
  1     Who asks, drawn from the region's People roster
  1     Why they will not go themselves - and it must be a real reason: a
        limitation, a watcher, a standing need here, or a past attempt they
        cannot admit to
  1     What specifically - retrieved, found, delivered, destroyed, verified, or
        collected - and which location holds it, by code and name
  1     The terms, stated in the giver's own words
  1     A stub row or an addition to an existing row in setting/Quests.md
  40%   Something they have not mentioned, and know they have not - a previous
        attempt, a rival want, a right they do not have, or a payment that is not
        really theirs to give
  30%   A deadline, and what happens after it
  20%   Somebody else has been asked already
```

**Name a real target.** Every location in the setting exists as a gazetteer stub before any
location file is written, so a giver can name a specific location by code and name at 4c.
A quest pointed at an invented place is the failure this registry exists to prevent - and
what the object actually *is* gets written at 4d, with both ends in view.

**Terms in the giver's own words.** Not "they offer coin" but the offer, spoken. It states
the payment and characterises the payer in one line - the *generous* one is taking a double
share, the *fair* one is taking half - and it costs nothing to write it that way instead.

**What they leave out is the quest.** Two ends make a delivery; an omission makes an
adventure. The giver who does not mention that the last two people did not come back is
more useful than any amount of description.

**A deadline is what makes a party choose between two hooks**, which is the point of
having more than one - so state what happens after it passes, not only the date.

## Constraints
