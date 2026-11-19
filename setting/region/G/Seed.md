# Seed of G The Northern Headlands

```kdl
Seed G terrain="coast" comes="Windward headlands of scrub and grass above sea cliffs, the rim of an old volcanic crater, and a tented camp above a shingle landing. A party comes for the treasure hunters' second camp, the bird cliffs or the crater." who="The Treasure Hunters, Treasure Hunter, Pterodactyl, Caveman" changing="The treasure hunters are fortifying their second landing, and a band of cave men is raiding the cliffs for eggs." crossing="3 watches" off="6 watches"
Rung G if="a party camps on the crater rim" then="Pterodactyls roost on the rim and stoop on any fire."
Rung G if="the hunters learn a party holds a map" then="Their sentries follow the party's boat from the landing."
Entry G name="the crater trail" from="the hill jungle" stands="A treasure hunters' sentry at the crater's lip by day, none at night" takes="A day's climb to the crater rim in sight of the sentry" refused="A party turned back from the rim is followed down the trail"
Entry G name="the shore track" from="the northern villages" stands="Fish-drying racks and a boat watch at each end of the track" takes="A day's walk along the north shore, below cliffs and above a surf-beaten beach" refused="A party turned back at the headland is not followed"
Entry G name="the crater landing" from="the sea" stands="A treasure hunters' sentry on the cliff and a boat drawn up on the shingle" takes="A boat through the surf; in a storm none lands" refused="A boat refused the landing is followed along the coast"
Ruling G on="cliff edge in wind" buys="A gale makes the edge a Test of Constitution each watch, a Wound of Crushing on a failure at the foot."
Ruling G on="the crater rim" buys="The rim is open scrub, 2 miles a watch, with every fire and lantern seen from the sea."
```
