# Seed of HA The Pyramid's Upper Temple

```kdl
Seed HA kind="collection" comes="Terraces of dressed stone climbing a stepped pyramid out of the jungle, a stair on each face, and a shrine on the top under the open sky. A party climbs the stair for the crown, or a way down." who="Tuuzesh, Snake Man, Tribesman" changing="Bound men carry captives up the stair at dusk, and each sacrifice makes the cult bolder."
Rung HA if="a captive is carried up the stair" then="Blood runs down the stair's channel to the shaft, and the torches on the terraces burn lower."
Rung HA if="the shrine's fire is put out" then="The cult's watch comes up the stair within the turn."
Entry HA name="the pyramid's foot" from="the eastern jungle" stands="Two bound men and a snake man on the first terrace by day, a patrol by night" takes="A hundred feet of open stair, in sight of the jungle" refused="A party turned back is followed by patrols to the jungle's edge"
Entry HA name="the shaft" from="the pyramid's halls" stands="A rope-and-pulley winch worked by bound men, and no stair" takes="A hundred feet down in the dark, past the cult's watch" refused="A party turned back is chased up the stair"
Conditions HA material="mossy dressed limestone" height=15 width=10 light="sun, then torches" sound="wind carries every voice down the stair" footing="worn wet steps" air="warm, humid and open" fire="smoke rises and shows from the jungle"
```
