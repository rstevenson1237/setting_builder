# Seed of D Pyramid Level 2 - The Halls of History

```kdl
Seed D kind="collection" comes="Four areas of halls and cells on the second level, where murals, carvings and the rooms between them tell the cynidiceans' history in order, joined by winding passages. A party comes down one of three hidden stairs to read it and to find the way on." who="The Tomb Robbers, Kurumisa, Ruhiahe, Sihuahet, Delver, Skeleton, Giant Rat, Zombie" changing="The tomb robbers have moved into the upper halls and the three branches' scouts have begun to come up from below."
Rung D if="a robber is killed" then="The robbers' camp sends six within the hour."
Rung D if="a mural is defaced" then="A scout from one branch comes to see who did it."
Entry D name="the trapdoor stair" from="the tile floor above" stands="Two soldiers of the Royal Guard patrol the arch beyond, and the robbers' watch sits behind a wooden door." takes="A coin or a name." refused="The watchers raise the camp."
Entry D name="the kings' stair" from="the mural wall above" stands="Nobody: a darted sill." takes="A touch on the sill sets off its darts."
Entry D name="the plinth stair" from="the plinth above" stands="Nobody: knee-deep dust over a hidden pit." takes="Wading the drift."
Conditions D material="carved sandstone" height=15 width=10 light="torch only" sound="stone carries a shout down every hall" footing="dust over smooth stone" air="dry, oil-scented" fire="smoke drifts up the stairs"
```
