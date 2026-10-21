# Seed of C The Dark Wood

```kdl
Seed C terrain="forest" comes="Old forest north of the keep, thick enough to hide a camp from a hundred yards, with the ravine at its far end. A party comes to reach the ravine, to hunt, or to find what the outlaws hide." who="The Wood Outlaws, Wolf, The Zhakuk, The Zurnaz, Ansel the Hermit" changing="The outlaws' trade has failed with the convoys, and they now stop any party on the trail for a toll. The Zhakuk's Wolves run the wood's edge, and the Zurnaz walk the trail by night to collect the tithe and take the last of any party camped on it." crossing="3 watches"
Rung C if="a party pays the outlaws' toll" then="It goes on untouched."
Rung C if="a party refuses the toll" then="Arrows come from the trees at the next bend."
Entry C name="the postern" from="the keep, on the south" stands="Nobody; the forest trail runs 12 miles north from it to the ravine."
Entry C name="the mere's north shore" from="the mere, on the west" stands="Nobody; a side path leaves the trail 2.5 miles out and runs west to it."
Entry C name="the ravine's mouth" from="the ravine, on the north" stands="Nobody; it is the trail's end."
Ruling C on="the trail" buys="A watch covers 4 miles."
Ruling C on="off the trail" buys="A watch covers 2 miles. Sight carries 30 yards, and a FAILURE on Navigate loses the party for a watch; fog or a storm adds Disadvantage."
Ruling C on="forage and hunt" buys="Succeeds on a 4 or more within a mile of the trail, and at Disadvantage deeper in."
Ruling C on="night" buys="Nothing is seen beyond a lit torch; a fire is seen at 200 yards, but the canopy hides its smoke."
```
