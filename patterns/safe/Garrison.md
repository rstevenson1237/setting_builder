# Safe - Garrison

## Provides
Where a settlement keeps its defence: who stands watch, against what, and what that watch
lets through. The authority the soldiers answer to is `safe/Authority.md`'s where it sits
in the same place.

## Spec

```
GARRISON
  1     What it defends and from where                                     {POST}
  1     Who stands watch, drawn from the region's People roster, and how many
  1     What they watch for, and what they do on seeing it - the order they follow
  1     What they let through, and on what terms - this file's answer to
        safe/Settlement.md's gate line      {name | toll | arms given up | sponsor | none}
  1     What they are short of              {men | arms | pay | rest | faith in the order}
  30%   Something they take that is not theirs to take, and look away from for a price
  20%   Somebody posted here as punishment
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
