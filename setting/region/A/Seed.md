# Seed of A The Drifted Streets

```kdl
Seed A terrain="desert" comes="Sand drifted to the rooftops of a gridded city, a stepped pyramid's tip standing from its centre ringed by three wind-worn statues, and a storm wall overhead. A party comes in out of the storm, for shelter first and then food and water." who="The Tomb Robbers, Hyena, Giant Scorpion, Giant Centipede, Giant Rat" changing="The tomb robbers' scouts work the rubble for a way past the tip's door, and their water is running out." crossing="1 watch" off="3 watches"
Rung A if="a day passes with no water found" then="Every character takes a Test of Constitution against thirst at dawn."
Rung A if="the tip's door is opened" then="The tomb robbers' scouts come to the statues within the watch."
Entry A name="the storm wall" from="the open dunes, in the storm" stands="Nobody; the storm hides the city until a party is in its streets." takes="A watch of blind travel, and the sand takes any track left behind."
Entry A name="the tip's door" from="the foot of the three statues" stands="Two of the tomb robbers' scouts by day, none by night; a bronze door stands half-open on the pyramid's first room." takes="A party must be willing to pass beneath three carved faces that watch the door." refused="A party turned from the door can try the dunes, and the storm."
Ruling A on="the cleared streets" buys="A watch covers 4 miles on a street the sand has not drifted over."
Ruling A on="over drifted sand" buys="A watch covers 2 miles; a party loses its tracks within a turn."
Ruling A on="deep dune" buys="A watch covers 1 mile and a Test of Constitution against thirst each watch."
Ruling A on="night and storm" buys="Sight is a few paces; a lit fire is seen from the tip."
```
