# Seed of E The Eastern Jungle

```kdl
Seed E terrain="jungle" comes="Low jungle under a closed canopy, the vine-choked stone of the snake people's towns, a slow brown river, and a stepped pyramid standing over the trees. A party comes past the serpent posts for the pyramid's gold, or is driven here." who="Tuuzesh, Snake Man, Tribesman, Giant Python, Giant Centipede" changing="Patrols and bound men walk the serpent roads each night leading captives to the pyramid, and the boundary posts at the jungle's edge are being re-carved." crossing="4 watches" off="10 watches"
Rung E if="a party passes the serpent posts" then="Cult patrols come onto the road behind it within the watch, and any village that learns of the crossing withdraws its standing."
Rung E if="a captive is led into the pyramid" then="A tremor runs through the stair and the jungle birds go silent for a watch."
Entry E name="the serpent posts" from="the hill jungle" stands="Posts carved with coiled serpents at the jungle's edge, and no guide past them" takes="Crossing the posts unguided; a villager who goes is cast out" refused="A guide turns back at the posts and goes no further"
Entry E name="the pyramid's foot" from="the pyramid's upper temple" stands="Two bound men and a snake man on the first terrace by day, a patrol by night" takes="A hundred feet of open stair, in sight of the jungle" refused="A party turned back is followed by patrols to the jungle's edge"
Ruling E on="the serpent roads" buys="Worn stone under the vines is a road: 4 miles a watch, and every patrol uses it."
Ruling E on="the closed canopy" buys="Light is dim at noon and dark by the second watch, a fire is seen through the leaves, and a party off the roads is Lost on a failed Test of Fate."
Ruling E on="the slow river" buys="A raft goes down it at 2 miles a watch, in sight of both banks and every crocodile."
```
