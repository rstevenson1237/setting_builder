# Dangerous - Key

## Provides
A key lying in a DANGEROUS location: the object, how it is held, and the lock elsewhere it
answers. The lock end is `dangerous/Lock.md`'s; what earns a Keys row is
`patterns/setting/Keys.md`'s.

## Spec

```
KEY - a key lying here
  1     Object - what it physically is: shaped, cut, or marked to fit one specific lock
        and nothing else
  1     Held - how it is held here           {carried | fitted | buried | mounted | owed}
  1     Keys row - a stub row in setting/Keys.md naming this location and the location
        it opens, never one already written; its Unlocks line is written later
  1     Opens - the location it opens, which owes the lock
  40%   Connection - a clue connecting object to lock, where the connection is not
        obvious: shared in the making, never stated outright
  20%   Used - evidence it has been used before
```

## Constraints

- **Nothing is owed at the close of allocation.** A Keys row whose far location draws no
  lock is a dangling thread.
