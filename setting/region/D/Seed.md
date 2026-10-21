# Seed of D The Black Mere

```kdl
Seed D terrain="swamp" comes="Reed marsh north of the road and west of the wood, three miles across by the causeway. A party comes to cross to the wood, to look for what the drowned shrine holds, or to turn the Sellaca against the outlaws." who="The Sellaca, Zombie, The Wood Outlaws" changing="The Sellaca, from their stilt village, are closing the mere to every stranger. The makers' drowned shrine lies under its eastern flats, and the dead in it do not stay down. The outlaws are testing the causeway's edge." crossing="1 watch"
Rung D if="a party leaves the causeway" then="The Sellaca close in boats within a watch."
Rung D if="the outlaws and the Sellaca clash" then="The causeway closes to everyone."
Entry D name="the causeway" from="the road, 5 miles from the keep" stands="The Sellaca, watching from the reeds." takes="Keeping to it." refused="Boats from the reeds within a watch."
Entry D name="the north shore" from="the wood's side path" stands="Nobody; the reeds come to the path's end."
Ruling D on="the causeway" buys="A watch covers 8 miles; by pole boat 4, and wading through the worst ground 2."
Ruling D on="off the causeway" buys="A FAILURE on Maneuver sinks a party to the waist and holds it until freed, a Test of Constitution each Round."
Ruling D on="fog and night" buys="Fog hides the causeway's edges, and a party that leaves it by night is lost until dawn."
Ruling D on="a fire" buys="A fire on the flats draws the drowned dead."
```
