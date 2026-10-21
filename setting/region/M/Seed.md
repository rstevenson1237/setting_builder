# Seed of M Thalosae

```kdl
Seed M kind="collection" comes="The makers' first shrine, cut into the cliff above the maze and reopened by the Black Altar five years ago, in four blocks: the stair-hall and outer shrine, the priests' cells and refectory, the crypts, and the sanctum and vault. A party comes for the sanctum's secrets and the vault." who="The Black Altar, Veck the Hollow, Zombie, The Zurnaz" changing="The Black Altar needs every tribe's tithe and every wagon day, and the Zurnaz visit to collect the tithe."
Rung M if="the tithe stops" then="The Zurnaz are sent into the ravine."
Rung M if="the sanctum is entered" then="The high priest knows by the time the party leaves it."
Entry M name="the stair" from="the ravine's head" stands="Acolytes; the stair-hall door is barred at night."
Entry M name="the makers' passage" from="the maze" stands="Nobody; it climbs from the maze's far end."
Entry M name="the back stair" from="the dry fork" stands="The Zurnaz, coming up from their den."
Conditions M material="cut makers' stone" height=14 width=10 light="black candles, sanctum fire" sound="chanting carries along the halls, hiding small noises" footing="smooth stone, stained black" air="thick with incense" fire="changes nothing"
```
