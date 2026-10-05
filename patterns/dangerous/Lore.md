# Dangerous - Lore

## Provides
A DANGEROUS location's find when it is written rather than valuable, and what form it
takes. What earns a Lore row is `patterns/setting/Lore.md`'s.

## Spec

```
LORE
  1     Form - an object written, marked or recorded by hand, its own condition part of
        what it tells
  1     Survived - why it survived where it did
  1     Voice - whose voice it is in: most useful from someone who did not know what
        they were describing
  1     Wrong about - what that voice was wrong about
  1     Does - the one thing it does                                          {DOES}
  1     Lore row - a stub row in setting/Lore.md, name and this location only; the
        content is the registry entry's
  50%   Detail - a detail that only makes sense once another location is seen
  1     Seen at - where a detail was drawn: that other location, by code
```

```
DOES - exactly one
  place        - names a place the party has not found
  misread      - explains a feature they have already seen and misread
  connection   - connects an event in setting/History.md to something physical here
  contradiction - contradicts a rumour they arrived with
  naming       - gives a name to an effect they have only seen
```

## Constraints

- **Never a document that knows everything.** That is a briefing, not a find.
