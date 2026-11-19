# Proof - content schema (C6)

Region A, The Drifted Streets (WILD, 9 locations), built twice from the same brief: as committed, and with
`wild` rated `Lair Rewards="0-1" Purchases="0-2"` and `Ruin Natural Hidden Secret Rewards="0-1"`.
The second build added, at steps 4a and 4b:

```kdl
Reward A.7 container="a sand-scoured strongbox" contents="Treasure I"
Reward A.9 container="jars, seals unbroken" contents="Treasure IV"
Purchase A.7 type="sale" item="hemp rope, iron spikes and lamp oil" price="listed" limit="paid in water"
Purchase A.7 type="service" item="a scout to guide past the first room" price="30 cn" per="a day" limit="one scout, door open"
```

and three Features: A.7's Strongbox and Spare Gear, A.9's Jars, with A.7's Scouts given the guide's price.

## Measured

| Reading | Without | With |
|---|---|---|
| Validator errors, warnings | 0, 0 | 0, 0 |
| Words, A | 1,757 | 1,827 |
| Words a location, A | 195 | 203 |
| Features, setting | 407 | 410 |
| Words a Feature, mean and max | 18.0, 70 | 18.0, 70 |
| Write-up against table, A | 5.6x | 5.4x |
| Table words dropped, A | 22 of 191 (11%) | 22 of 210 (10%) |
| Tells: rather than, absence, conclusion, gloss | 0, 1, 1, 5 | 0, 1, 1, 5 |
| Rewards, A | none | Treasure I, Treasure IV |

Every word the new entries added was carried into its write-up. Nothing measured got worse; the words a
location rose by what the new Features hold.

## Setting Judgement Check

- **The brief was delivered**: A.7 is the robbers' camp that "trade what they take" and now sells; the
  Coin and Prices line "nothing here is sold above the pyramid's tip except what the tomb robbers will trade"
  now has a place that does.
- **Prices fit the list**: the rope, spikes and oil are `listed`; the guide's 30 cn a day is the list's Guide wage.
- **Genre held**: GENRE.md's Reward ("water, food and a place to rest") is the price of the sale, paid in water.
- **Entries match, one room, said once, the tests**: no Feature restates another; none tells the party what to do.

The setting is left as committed: the rates stay 0 in `BRIEF.md` until a build asks for them, and the entries
above are what region A gets when it does.
