# Dangerous - Lock

## Provides
The lock in a DANGEROUS location that a key lying elsewhere opens, and the feature it sits
on. The key end is `dangerous/Key.md`'s; what earns a Keys row is
`patterns/setting/Keys.md`'s.

## Spec

```
LOCK - an obligation a Keys row names against this room
  1     On - the feature it sits on: an exit whose gate is fitted, or a mystery whose
        answer lies elsewhere, matching the setting/Keys.md row that named this room
  1     Lock - what it physically is
  1     Keys row - the setting/Keys.md row that named it
  20%   Forced - evidence it has been forced at, and held
```

## Constraints

- **A lock with no Keys row is a wall.** Every lock answers a row whose key lies at
  another location.
