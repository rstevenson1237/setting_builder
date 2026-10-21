# Seed of K Bugbear Den

```kdl
Seed K kind="single holding" comes="The Zurnaz's den in the dry fork off the east wall, paid by the Black Altar to keep the fork and collect the tithe. A party comes for the tithe store, and for the back stair." who="The Zurnaz, Bugbear, The Black Altar, Mort the Tithe-Taker" changing="The Zurnaz hold every tribe's tithe until it is carried up the stair."
Rung K if="a tithe is lost" then="They search the ravine."
Rung K if="a party finds the stair" then="The shrine is told within a turn."
Entry K name="the den mouth" from="the dry fork, 50 yards up its bed" stands="Bugbears hidden above the bed under an overhang, day and night."
Entry K name="the back stair" from="the shrine" stands="Nobody; a plastered door closes the den's end."
Conditions K material="stream bed, natural cave" height=10 width=6 light="none" sound="dies at once in the soft dust" footing="dry silt holding tracks" air="still" fire="shows from the ravine"
```
