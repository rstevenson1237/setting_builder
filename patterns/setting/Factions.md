# Setting - Factions

## Provides
One power a party may treat with, oppose, or ignore, and how it is recognised before it is
named. How many factions the setting holds, and how they relate to each other, is
`templates/setting/Factions.md`'s; what a faction dice pool resolves is `setting/Procedures.md`'s.

## Spec

```
FACTION
  1     AD - in d6 only with no bonus - set against the other factions' dice and nothing
        else
  1     Want - concrete enough to be interfered with                          {WANT}
  1     Identity - repeated identically wherever it appears, so a party knows it two
        regions apart before anyone names it                              {IDENTITY}
  1     Resources - what it can actually spend
  1     Knowledge - what it knows that others do not, which is what makes it worth
        dealing with rather than only fighting
  1     Tactics - its characteristic move when contested, concrete enough to predict
        once it has been seen
  1     Reactions - what it does when interfered with: noticed, crossed, and injured
  1     Goals - what drives its turns now, each a standing condition it acts on
  1     Fields - what it fields in a fight: a setting/Bestiary.md entry by name, or `none`
```

```
WANT - exactly one
  route        - a way through, kept open or shut
  resource     - a supply, and exclusive access to it
  person       - one particular person
  cleared      - a place emptied of what is in it
  sealed       - a place kept shut
  legitimacy   - a claim acknowledged
  debt         - an obligation honoured
  rival        - a rival gone
  knowing      - something found out
  hiding       - something kept from being known
```

```
IDENTITY - at least two
  colour       - worn, hung or painted
  device       - an emblem put on what they own and carry
  habit        - a way of doing an ordinary task that only they do
  arms         - a weapon or armour tradition
  mark         - a sign left where they have been
  phrase       - a word or saying used among them
  tongue       - a tongue from setting/Language.md used among themselves
```

## Constraints

- **Faction dice are relative and nothing else.** Never pitch them against creature or
  party dice: a power that is weak in the world may still kill everyone in a room.

- **A goal is never a countdown to a climax.** It is a condition the faction acts on turn
  after turn, whether or not the party is present.
