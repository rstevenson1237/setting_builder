# Setting - Lore

## Provides
One piece of lore: a made thing, whose voice it is in, and what it does. When a location
reaches for lore is its rating's own `Lore.md`; what a person says aloud is a rumour, not
lore.

## Spec

```
LORE ENTRY
  1     Form - a made thing                                    {written | cut | woven |
                                                                drawn | arranged}
  1     Whose voice, and how they are wrong or partial                    {WRONG}
  1     What it does                                                      {DOES}
  1     The one location that owns it - later locations may reference it
  1     Its length - enough to be read aloud in under a minute
```

```
WRONG - exactly one
  unknowing    - the author did not know what they were describing
  lying        - they were lying to a specific reader
  secondhand   - they were repeating what they were told
  late         - they wrote it long after
  interested   - they had a stake in one version
  unfinished   - they stopped partway, and why is findable
```

```
DOES - at least one
  purpose      - reveals part of a region's or the setting's purpose
  connection   - connects an event in setting/History.md to an entry in
                 setting/Truths.md, or two events, or two truths
  hook         - plants a lead a party may choose to chase
  naming       - names something the party has only seen the effects of
  dating       - dates something
  contradiction - contradicts a rumour they arrived with
```

## Constraints

- **Lore is an object, never spoken exposition.** It can be picked up, carried, lost,
  sold, and read by the wrong people.

- **Never an omniscient account.** Lore is written by somebody inside the setting with
  their own reasons; an account with no author has no place it could have come from.
