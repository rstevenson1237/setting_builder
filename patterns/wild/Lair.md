# Wild - Lair

## Provides
What an occupied Landmark is, and what its occupancy implies about the country around it.

## Read at
Step 4c, when a WILD classifier's Kind line draws Lair - `wild/Landmark.md`,
`wild/Hidden.md`, or `wild/Secret.md`, all three of which draw one kind per location.
A Lair is a place something currently lives, whether it built the place or
moved in.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate
at which a Feature carrying that content appears. This block is setting-neutral and
permanent - step 1b recompiles the Design patterns below it, never this.

```
KIND: LAIR
  1     What lives here, from setting/Bestiary.md
  1     The territory it claims, and how far that reaches
  1     A sign of it readable before the lair itself is reached
  1     What it eats, and where that comes from
  40%   Young, stores, or dependants - a reason it cannot simply leave
  30%   Absent when the party arrives, and elsewhere in the region
  30%   A child location: the den proper, the midden, the larder, the killing ground
  20%   What holds it is people, and they answer to one of the three factions
                                                              (wild/Faction.md)
```

**A Lair is the tier's natural place to carry depth.** Complexity comes from attaching
children rather than from writing the parent heavier - a lair decomposes into children more
readily than any other kind, because a thing that lives somewhere lives across several
spaces. **Territory is what makes a lair matter to the region**: a den nobody can find is a
room; a den whose owner ranges three landmarks in every direction is a fact about the whole
region.

## Design patterns

Compiled for this build, from this setting's chosen genre reference.

**Kinds of holding** - a cave or rock shelter; a burrow or dug warren; a hollow tree or
fallen trunk; a nest on a height, on a stack, or in a crown; a thicket beaten down from
inside; a dam, mound, or built structure of the occupant's own making; a taken-over ruin;
a place under water; a place under stone; a camp of somebody who moves seasonally.

**Signs readable first** - tracks, and how fresh; a kill, and how it was killed; scat,
pellets, or castings; a shed skin, feather, or antler; scrape marks, rubbing posts, or
scent marks; bones arranged rather than scattered; a silence where there should be birds;
a smell that arrives before the place does; prey behaving wrongly; something the occupant
has dragged and left.

**What it eats** - and this is the leverage a party gets. Livestock taken from a settled
region nearby. A specific animal it has reduced to nothing here. Carrion, and what
supplies it. Something it farms or tends. Travellers, and how often. Tribute, from people
who found that cheaper than fighting.

**Why it stays** - young too small to move; a store it has built up; water that exists
nowhere else nearby; something it guards that is not food; it was put here; it cannot
leave.

**Occupied by people** - a hunting camp; an outlaw band's holding; a hermit; a work party
too far out to return nightly; refugees; a household that has gone strange out here; a
picket belonging to a faction that has interests further in.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
