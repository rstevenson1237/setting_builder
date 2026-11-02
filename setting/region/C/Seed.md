# Seed of C Pyramid Level 1 - The Trapped Rooms

```kdl
Seed C kind="collection" comes="A tight complex of small trapped rooms round a hall tiled in coloured squares, at the foot of the pyramid's tip, its walls carved with the cynidiceans' story. A party comes in out of the sand to shelter, and stays to find a way down." who="Gargoyle, Skeleton, Giant Centipede" changing="The three ways down are hidden and trapped, and each opens only by something done in the rooms."
Rung C if="the plinth is touched" then="The skeletons along the wall step out and the gargoyle drops from its perch."
Rung C if="a way down is opened wrongly" then="Its trap fires, and the tiles of the hall click and shift for a turn."
Entry C name="the tip's door" from="the statues above" stands="A gargoyle crouches over the lintel and a trapped tile lies on the threshold." takes="Passing the threshold sets off its tiles." refused="Those outside have only the storm."
Conditions C material="carved sandstone" height=20 width=10 light="sun-shafts by day" sound="hard walls carry every sound" footing="trapped tiled floor" air="dry and still" fire="smoke rises up the tip's shaft"
```
