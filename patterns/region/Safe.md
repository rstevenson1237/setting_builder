# Region - Safe

## Provides
What a SAFE Region Overview says, how many locations it holds, and what shape its
connection graph takes.

## Spec

```
LOCATION COUNT
  About as many as the die type. A d8 region holds about eight.
```

```
TOPOLOGY - a shallow hub
  1     Every location reachable from the settlement itself, independently
  1     No location gated behind another
  20%   One location outside the walls or the edge of settlement
```

**SAFE is the one rating where the region file carries more than its locations do.** The
Overview describes the place; the locations are the interesting entry points for player
interactivity, not a survey of every house and person. So SAFE locations do not
interconnect - they all hang off the settlement, and the settlement is described here.

**The die is how eventful the place is.** SAFE's table is rolled on entry and each week
after, not per location, so the die measures how often the settlement generates trouble on
its own rather than traverse pressure. d8 is baseline; d6 is a place with something wrong
with it, d10 a place where little happens.

The Region Overview's fields, for a SAFE region.

```
FIELDS
  1     Overview   - what this settlement is for, why it is here rather than a mile away,
                     and what it lives on. What it trades away to exist is worth stating
  1     Ambiance   - what it looks, sounds and smells like, and the architectural style and
                     materials that make it read as one place
  1     People     - and this field carries the roster. The trades present, the trades
                     conspicuously absent, and who holds standing. Absence is the
                     interesting half. Locations draw their cast from this list
  1     Situation  - what is happening right now: a standing state affecting every location,
                     not a random event. Who is responsible, who is affected, which rung it
                     is on, and what the next rung looks like
  1     Layout     - the settlement's type first, per safe/Settlement.md, then its shape,
                     approaches, defences, and where the locations sit relative to each
                     other. State that SAFE is not time-bound
  1     Features   - what the settlement offers that is not a location: its law such as it
                     is, its prices relative to elsewhere, what it will not trade for, its
                     gate hours, where outsiders are allowed
  1     Dangers    - a SAFE region is safe from the wilderness, not from its own people:
                     debt, law, feud, faction interest, being noticed, being remembered
  1     Creatures  - Man, overwhelmingly, and going about business. Anything else is
                     working, penned, or a problem
  1     Factions   - whether any of the three hold ground here, and how much. Usually
                     influence over a trade, gate or office rather than territory; none
                     where the settlement is genuinely unclaimed
  1     Secrets    - what the settlement is not saying, and who knows it
  1     Treasure   - what is for sale or in stock rather than found; which tables the local
                     trade draws on, and what money looks like here
  1     Tables     - a d6 Events table, rolled on entry and each week thereafter. Events
                     happen to the settlement, distinct from the Situation already underway
```

## Constraints
