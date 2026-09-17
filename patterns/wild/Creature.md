# Wild - Creature

## Provides
What lives in or ranges through a WILD location, and how it meets a party.

Scaling is in `patterns/setting/Bestiary.md`. Distinct from `wild/Faction.md`, which is
what a place is held or worked by rather than what the party meets in it, and from
`wild/Hazard.md`'s living mechanisms, which have nowhere else to be and nothing they
want.

## Spec

```
CREATURE
  1     Bestiary entry, or an inline description where none fits
  1     Number - how many the country supports, from the entry's Range
  1     Scale - pitched against party altitude, not the region die. Usually something a
        party can handle or avoid; occasionally something they cannot, and must read
  1     What it is doing, and whether it has noticed the party first
  1     Reaction - most things met in the open would rather not fight, and a party
        that assumes otherwise should be able to be wrong
  1     Its limit - the ground, depth, light, or distance it will not cross
  40%   Range - it is not only here, and the party may meet it elsewhere in the region
  30%   Absent, with signs of it, and elsewhere in the region right now
```

**A WILD creature is usually avoidable, and that is the point.** In a dungeon a creature
in the room is a problem to solve; in open country it is a fact to be navigated. State the
limit and stop: where a thing will not go is a fact about the thing, and what going around
costs is the party's to find out. Per `GENRE.md`, a line saying the way around is free,
or worth taking, has made their decision for them.

## Design patterns

**Demeanor flavor** - a one-word behavior for how something met here carries itself
before a fight starts or doesn't, compiled for this build: Predatory, Territorial,
Cunning, Ravenous, Skulking, Frenzied, Wary, Ancient, Venomous, Relentless.

**Personality flavor, for the People pattern below** - a one-word disposition for a
traveler or patrol met here, compiled for this build: Treacherous, Fatalistic, Grasping,
Superstitious, Proud, Servile, Ruthless, World-Weary, Zealous, Craven.

**How it meets the party** - it is seen first, at distance; it sees them first and they do
not know; both at once, badly; it is heard and not seen; it is following, and has been for
a while; it is fleeing something else; it is feeding and will defend the kill; it is
between the party and where they were going.

**Territorial signalling** - a boundary it marks and will not cross; a warning it gives
before committing; a display; a call answered from somewhere else; a thing it does that
looks like aggression and is not.

**Populations, not individuals** - a WILD region holds a *population* with a range, a
season, and a food supply. State how many the region supports and where they go when they
are not here. A single creature written as though it were the only one of its kind belongs
in a lair, not a landmark.

**People** - travellers, a hunting party, a work crew, outlaws, pilgrims, a survey party,
somebody lost, somebody who does not want to be found, a faction's patrol working the
country between its positions.

## Constraints
