# Wild - Quest

## Provides
How a WILD location participates in a Quest. WILD **carries**: it is where quests are
travelled through, obstructed, and occasionally offered by somebody living rough.

A quest is the one hook that stays in registry rather than moving into the reward block
with lore and keys, because it is not an object and cannot be picked up. Criteria are in
`patterns/setting/Quests.md`; the registry is `setting/Quests.md`.

## Spec

```
QUEST - carrying end
  1     Its role {waypoint | obstacle | supply | giver}: a stop on the way, what
        stands in the way, something only found here, or somebody with an ask too
        small and personal for a settlement
  1     A stub row or an addition to an existing row in setting/Quests.md
  30%   Evidence of somebody else on the same errand, ahead or behind - a camp,
        a marker cut twice by different hands, or a party the group could meet,
        race, or join
```

**Obstacle is the role that matters.** A quest with two ends is a delivery; what stands in
the way is what makes it an adventure, and in a point crawl the way is WILD country. A
DANGEROUS target states the obstacle at the target; a WILD location states the obstacle
*en route* - the crossing that is out, the country that must be gone around, the thing
that holds the only path.

**Givers out here are unusual and need a reason to be out here.** A hermit, a trapper, a
survey party, an outlaw, somebody hiding, somebody who cannot go home. Their ask is
smaller than a settlement's and more personal, and they rarely have coin.

## Constraints
