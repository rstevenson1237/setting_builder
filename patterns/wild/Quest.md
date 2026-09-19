# Wild - Quest

## Provides
How a WILD location participates in a Quest. WILD **carries**: it is where quests are
travelled through, obstructed, and occasionally offered by somebody living rough. Criteria
are in `patterns/setting/Quests.md`; the registry is `setting/Quests.md`.

## Spec

```
QUEST - carrying end
  1     Its role   {waypoint | obstacle | supply | giver}
                                                (genre: quest-roles-outdoors)
  1     A stub row or an addition to an existing row in setting/Quests.md
  30%   Evidence of somebody else on the same errand, ahead or behind
                                                (genre: quest-prior-attempt)
```

**Obstacle is the role that matters.** A quest with two ends is a delivery; what stands in
the way is what makes it an adventure. A DANGEROUS target states the obstacle at the target;
a WILD location states it *en route*.

**A quest stays in registry rather than moving into the reward block** with lore and keys,
because it is not an object and cannot be picked up.

## Constraints

- **Givers out here need a reason to be out here** - a hermit, a trapper, a survey party, an
  outlaw, somebody who cannot go home. Their ask is smaller than a settlement's and more
  personal, and they rarely have coin.
