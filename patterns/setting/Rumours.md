# Setting - Rumours

## Provides
One lead a party can pick up: what it points at, how true it is, and where it is settled.
How many rumours the table holds and how they divide by truth is `templates/setting/Rumours.md`'s;
who repeats a rumour, and how, is the location's that delivers it.

## Spec

```
RUMOUR
  1     Points at                                                       {TARGET}
  1     Truth   {T | P | F | U}
  1     The substance, as it would be repeated - with no speaker and no framing
  1     Where P: which half is false - the false half is the interesting half
                                                                        {FALSEHOOD}
  1     Where the table calls for its sound to run against its truth: why {MISMATCH}
  1     Settled at - the location(s) holding what confirms, denies or corrects it, or
        `nowhere on this map` for a lead that points past the edge; where U, `the
        referee's`, and the place a party would go to try it
```

```
TARGET - exactly one
  region       - a region, by name
  location     - a specific place within one
  person       - someone, by name
  creature     - a creature, and what it does
  treasure     - a treasure, and where
  event        - an event from setting/History.md, misremembered
  truth        - a truth from setting/Truths.md, stated as superstition
  faction      - a faction, without naming it
  route        - what is passable, and when
  price        - a price, and why it moved
```

```
FALSEHOOD - exactly one
  elsewhere    - real, and somewhere else
  count        - real, and fewer or more than said
  taken        - real, and already taken
  person       - real, and it was a person, not a creature
  creature     - real, and it was a creature, not a person
  cause        - real, and the reason given is wrong
  age          - real, and it happened much longer ago
  survivor     - real, and the teller lied about their part
```

```
MISMATCH - exactly one
  plainest     - true, and the plainest statement of the setting's strangest truth
  number       - true, and a number too large to credit
  character    - true, and something a named person did out of character
  simplest     - true, and the simplest explanation where complicated ones are preferred
  too neat     - false, and a story that fits the setting's pattern too neatly
  plausible    - false, and a plausible cause for a real effect
  common       - false, and something everyone repeats, sourced to nobody
  stale        - false, and something that was true and stopped being
```

## Constraints

- **Never build a speaker into a rumour.** A rumour written with its teller inside it can
  only be delivered by that teller.

- **Never state what the players should do with it.** A rumour is a lead, not an
  instruction; so is its Settled-at line, which names where the truth sits and never what
  the party should conclude on finding it.

- **U is unverified by design, not undecided by accident.** The setting holds no answer
  to it and says so; the referee settles it when a party goes looking, and the place they
  would look is still named.

- **T/P/F/U and Settled at are the referee's, and never shared.** Mark against the truth of
  the substance, not of the framing.
