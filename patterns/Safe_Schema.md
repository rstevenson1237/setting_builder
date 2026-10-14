# Safe Schema

A SAFE region's tables: every location reached from the region itself.

```kdl
enum Safe_Type Inn Merchant Bank Market Authority
enum Kind steading thorp village town seat hold   // a household; a few; trades; a market and authority;
                                                   // a greater power's seat; a garrison with folk under its walls

folder Safe type=Safe_Type {
  Locations Location
  Dressing Dressing
  seed {
    Kind Kind
    Overview text           // what a party sees arriving, and what it comes to do
    Approach text           // every way in: what stands at it, what passing takes, what befalls the turned away
    People text             // the roster BRIEF.md sizes: - Name, role - wants from a stranger; gives or sells
    Services text           // prices in Treasure I's coin; what it buys from a party; what cannot be had
    Law text                // what gets a stranger fined, locked up or put out; who enforces; what each costs
    Situation text          // who is behind it, and who is hurt
  }
  brief {
    Places text             // every location: what a party goes there for, who of People is found there
    Secrets text            // - the fact - who knows it; the entry that brings it out
    Leads text
    Tables text             // d6 Events, on arrival and each week; d6 people and trouble, for anywhere unkeyed
  }
}
```
