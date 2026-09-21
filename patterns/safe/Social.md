# Safe - Social

## Provides
Where people gather, what circulates there, and who a party can get something out of.

## Spec

```
SOCIAL
  1     Who is here, and what they are doing - not waiting to be talked to, in
        whatever gathering place this settlement actually has: a taproom, a market
        day, a green or bridge where people stop, or wherever its people gather
  1     What is circulating: a rumour, drawn from setting/Rumours.md where one fits
  1     What it takes to be talked to rather than tolerated, this file's answer to
        `safe/Settlement.md`'s gate line - spending, an introduction, being
        recognised as useful, or answering for where you came from
  40%   A tension a stranger can be pulled into by doing nothing wrong - a feud, a
        debt, a grudge, or a fight the room wants and nobody here will start
  20%   Somebody who knows something and will not say it here
```

**Nobody is waiting for the party.** Everyone here has been having their evening since
before the party walked in, and the entry should say what that evening is.

**What it takes to be talked to rather than tolerated is `safe/Settlement.md`'s gate
line**, answered once per location whatever its Kind. This file states only what is true
of a gathering place: who is here, what is going round it, and what talking to somebody
here costs.

## Constraints

- **A Kind never draws a hook.** The hook layer is `safe/Settlement.md`'s registry
  block, and each hook file supplies its own holder. A Kind adding its own rate for a
  hook is a second, unaccounted path to an object whose cardinality the registry has
  already fixed. What stays here is what is true of a gathering place.

- **A rumour is repeated, not delivered.** Whoever says it has their own reason for
  saying it, is probably wrong about part of it, and will not mark it true or false.
  Take the substance from `setting/Rumours.md`; the framing belongs to whoever is
  talking.
