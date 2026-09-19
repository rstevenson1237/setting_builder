# Safe - Social

## Provides
Where people gather, what circulates there, and who a party can get something out of.

## Spec

```
SOCIAL
  1     Where people are gathered, and why here         (genre: social-places)
  1     Who is here, and what they are doing - not waiting to be talked to
                                                        (genre: social-people)
  1     What is circulating: a rumour, drawn from setting/Rumours.md where one fits
                                                        (genre: social-currency)
  1     What it takes to be talked to                   (genre: social-access)
  40%   A tension a stranger can be pulled into by doing nothing wrong
                                                        (genre: social-tensions)
  20%   Somebody who knows something and will not say it here
```

## Constraints

- **A Kind never draws a hook.** The hook layer is `safe/Settlement.md`'s registry block,
  and each hook file supplies its own holder. A Kind adding its own rate for a hook is a
  second, unaccounted path to an object whose cardinality the registry has already fixed.

- **A rumour is repeated, not delivered.** Whoever says it has their own reason for saying
  it, is probably wrong about part of it, and will not mark it true or false. Take the
  substance from `setting/Rumours.md`; the framing belongs to whoever is talking.
