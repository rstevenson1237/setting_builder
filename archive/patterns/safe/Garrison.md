# Safe - Garrison

## Provides
Where a settlement keeps its defence: who stands watch, against what, and what that watch
lets through. The authority the soldiers answer to is `safe/Authority.md`'s where it sits
in the same place.

## Spec

```
GARRISON
  1     Post - what it defends and from where                              {POST}
  1     Watch - who stands watch, drawn from the region's People roster
  1     Count - how many
  1     Watches for - what they watch for
  1     Order - what they do on seeing it: the order they follow
  1     Lets through - what they let through, and on what terms: this Kind's answer to
        safe/Settlement.md's gate           {name | toll | arms given up | sponsor | none}
  1     Short of                            {men | arms | pay | rest | faith in the order}
  30%   Graft - something they take that is not theirs to take, and look away from for
        a price
  20%   Punished - somebody posted here as punishment
```

```
POST - exactly one
  gate         - a way in, and who comes through it
  wall         - a stretch of defence, and what lies beyond it
  tower        - a raised post, and what can be seen from it
  quarters     - where the soldiers sleep, eat and keep their gear
  armoury      - where the arms and stores for a defence are kept
  mounts       - where the riders' animals are kept and worked
```

## Constraints

- **A garrison watches outward.** What it does to the settlement's own people is
  `safe/Authority.md`'s; a garrison turned inward on the settlement is its Situation.
