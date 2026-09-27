# Safe - Lore

## Provides
What written record a settlement holds, who controls access to it, and what it costs to
read. What earns a Lore row is `patterns/setting/Lore.md`'s.

## Spec

```
LORE
  1     Physical form - a kept document, made or kept for an administrative reason
                        {ledger | register | charter | correspondence | survey}
  1     Who holds it, and why they have it                                  {HOLDER}
  1     What it takes to be allowed to read it
                        {a fee | a vouching | a service | reading it under watch}
  1     Whose voice, and what they were wrong about
  1     The one thing it does                                                 {DOES}
  30%   It is incomplete, and the holder knows where the rest went
```

```
HOLDER - exactly one
  institution  - an institution's own record
  claimant     - an heirloom proving somebody's claim
  wrong hands  - somebody who should not have it
```

```
DOES - exactly one
  older name   - names a place by an older name
  payment      - records a payment that should not have needed paying
  ownership    - establishes who owned what before the current claim
  dating       - dates an event in setting/History.md
  contradiction - contradicts what the settlement says about itself
```

## Constraints

- **Spoken word is not Lore.** What a person tells the party is a rumour, and belongs in
  `safe/Social.md` and `setting/Rumours.md`.
