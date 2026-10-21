# Seed of B The Wagon Road

```kdl
Seed B terrain="plains" comes="Open grass either side of the realm's road, which runs west from the keep's main gate 12 miles to the map's edge and on to the realm. A party comes to ride with the wagon, to see where the last ones were lost, or to turn off toward the mere." who="The Carters' Guild, The Keep, The Wood Outlaws, The Zhakuk" changing="Wagons are taken in the last miles before the keep by raiders working from the wood's edge, where the wood and the mere come close to the road. The Carters' Guild runs a convoy on the keep's wagon days, and the Keep's Soldiers patrol the first stretch in sixes." crossing="2 watches" off="3 watches"
Rung B if="the next convoy arrives whole" then="The Carters' Guild adds a second wagon."
Rung B if="the next convoy is lost" then="The Guild stops running and posts a bounty at the keep's market."
Entry B name="the keep's main gate" from="the road's east end" stands="The Keep's Soldiers, patrolling the first stretch in sixes."
Entry B name="the realm" from="the road's west end, off the map" stands="Nobody; the convoy comes this way on wagon days."
Entry B name="the causeway" from="the road, 5 miles out" stands="Nobody on the road; it leaves for the mere."
Ruling B on="the road" buys="A watch covers 8 miles. Sight carries 3 miles by day, so a party on the road is seen from the wood's edge long before it sees anyone there."
Ruling B on="off the road" buys="A watch covers 4 miles through tall grass. A FAILURE on Navigate loses the party for a watch, a COMPLICATION for half of one."
Ruling B on="night" buys="A fire shows 5 miles, and travel off the road is at Disadvantage."
Ruling B on="rain" buys="The verge turns to mud, and the pace off the road halves."
```
