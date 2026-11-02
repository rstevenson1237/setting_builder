# Seed of F Pyramid Level 4 - The Living Quarters

```kdl
Seed F kind="collection" comes="The fourth level's living quarters, cells and kitchens left as their cynidicean owners left them, with lairs of stronger monsters that came down from the sand and the tomb robbers' deepest camp. A party comes for the quarters' stores and the lairs' hoards." who="The Tomb Robbers, Giant Spider, Giant Scorpion, Ghoul, Zombie, Stirge, Hyena, Giant Rat, Kurumisa, Masked Dreamer" changing="The ghouls of the old family crypt have begun to hunt the quarters, and the Kurumisa captain who went after them has not come back."
Rung F if="the tomb robbers' camp is robbed" then="The camp hunts the thief through the quarters."
Rung F if="the captain's trail is followed" then="The ghouls come out of the crypt to meet whoever follows it."
Entry F name="the stair from above" from="the three halls" stands="Two Kurumisa soldiers, who stop all who go down." takes="A party must name its business." refused="A party turned back is walked up the stair by the two soldiers."
Conditions F material="plastered sandstone" height=12 width=6 light="torch only" sound="cloth hangings muffle sound" footing="dust over worn tile" air="stale, faintly rotten" fire="hangings burn; smoke fills the quarters"
```
