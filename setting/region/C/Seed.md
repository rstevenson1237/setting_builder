# Seed of C The Wreck Coast

```kdl
Seed C terrain="coast" comes="Beaches, sea cliffs and caves along a reef awash with broken hulls, a cove with a ship at anchor, and a tent camp on the sand. A party comes for the reef's wrecks, the mer people's trade or the pirates' anchorage." who="Nealeu, Merman, The Cove Pirates, Pirate, The Treasure Hunters, Treasure Hunter, Giant Crab" changing="The pirates and the mer people are at war over the cove's water, and the treasure hunters are surveying the beach for a way to the pyramid." crossing="3 watches" off="8 watches"
Rung C if="the pirates' anchorage is cleared" then="The mer people open the reef's passages to a party and name a wreck to dive."
Rung C if="a boat crosses the reef without a pilot" then="The reef holes it, and the mer people claim what floats off."
Entry C name="the great gate" from="Puluni's wall, by the gate" stands="A gate-tower in the wall's only gap, a warden and a watch of spearmen day and night, and food set at its foot at dusk" takes="The chiefs' word to open it, and a search of what is carried through" refused="A party turned back is shut outside the wall for the night, where the night's visitor comes"
Entry C name="the western ridge trail" from="the hill jungle" stands="Red hand-prints on the rocks at the trail's head, and a cave men's watch on the ridge at dusk" takes="A day's steep climb along a ridge in sight of the caves" refused="A party driven back down the ridge is hooted off it"
Entry C name="the reef gap" from="the drowned galleon" stands="The galleon's stern wedged across the gap, and a mer people's guard in the water" takes="A boat with a pilot, or a swim through the surf at low water" refused="A boat refused the gap is holed on the reef"
Entry C name="the surf landing" from="the sea" stands="A pirate lookout on the cliff above the cove, and a treasure hunters' sentry on the beach" takes="A boat through the reef's passages with a pilot; one without is holed" refused="A boat that fails the passages is wrecked on the reef"
Ruling C on="beach at low tide" buys="A party walks 4 miles a watch on the hard sand; at high tide the beach is under water and the cliff path takes 2."
Ruling C on="reef at low water" buys="Wading it is the worst ground, and a Test of Constitution each watch against the coral's cuts, a Wound of Piercing on a failure."
Ruling C on="storm" buys="The surf breaks over the whole reef, no boat puts out, and the wrecks are under water."
```
