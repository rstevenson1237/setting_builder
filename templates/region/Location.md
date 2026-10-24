# Location.md

## Purpose
One location's write-up, `setting/region/[Region Code]/[Location Number].md`.

## Context
```kdl
template scope="[Region Code]" writes="setting/region/[Region Code]/[Location Number].md"
read "setting/Truths.md"
read "setting/Procedures.md" part="Forced Dangers, Conditions, Time and Distance"
read "setting/Language.md" part="roots for a coined name, and the coinages recorded"
read "setting/region/[Region Code]/Seed.md"
run "--location [Location Code]"
format {
  line header pattern="[Location Code] **[Location Name]** ([type]) - *[tags]*" hint="its three tags"
  line summary pattern="[Player Summary]" out="readaloud" hint="what a party sees on arriving, to be read aloud, with each Feature it names in **bold**"
  line notes pattern="*[Referee Notes]*" hint="size, shape, and what the referee needs to run the location"
  line feature pattern="**[Feature Name]:** [feature]" count="many" hint="the feature, where it sits, and any act on it with its effect; a hidden exit is written here, in the Feature that hides it"
  line exits pattern="**Exits:** [exits]" count="optional" hint="each exit as \"[make and condition], [position] -> [Location Code] [Location Name]\"; an exit off the map ends \"-> [where it leads]\" and comes last"
}
cite Bestiary form="([Demeanor], [Number appearing], Bestiary : [Entry Name])" example="(Wary, 6, Bestiary : Soldier)" note="Demeanor the item its reaction opens with; Number appearing its Creature count"
cite Roll form="([Table], d[N])" example="(Treasure I, d20)" note="Treasure I-V or Magic; N the table's rolls"
cite "Test of Constitution" form="(Test of Constitution, [X]d, [Type])" example="(Test of Constitution, 2d, Fire)" note="on every hazard Feature, from its Hazard, and every Mystery that asks a Test; X is the count of Tests"
cite "Test of Sanity" form="(Test of Sanity, [X]d)" example="(Test of Sanity, 1d)" note="only where setting/Procedures.md has a Madness table"
cite "Test of Fate" form="(Test of Fate, [Condition])" example="(Test of Fate, Exhausted)"
```

## Instructions
- Write every entry, and nothing without one. An entry naming this location from
  elsewhere is written as what a party meets of it here.
- Each thing a party can look at, act on, take, fight or open is its own Feature. An entry
  carries every Feature: Dressing carries what the room visibly holds, and anything a party
  can talk to, fight, take or open has an entry of its own, written before its Feature.
- A Dressing's `mark` is the faction's Identity, shown on something in the room.
- A Person is a Feature named for them: what they want and know come out in what they say
  and do, never as a list, and a `quest` they hold is cited there. A `member` is the
  referee's: the Feature shows only what the faction's Identity would show a party. A
  Garrison or a Faction's members are one Feature citing their Bestiary entry, where they have one. A Purchase is written
  with its `price` and `per` in the Feature that sells it, a menu or sale as the goods, a service as
  the act.
- A Stop is a Feature named for its `feature`, in the route's order, saying how far along the
  route it lies; one with a `to` says where its path leads, by that location's code.
- A key is cited at the location it lies and at each location whose Lock names it.
- A Local Procedure is the thing a party can start - the table, the game - cited from its
  Feature; its rules stay in the entry.
- Ground, height and slope are the `At` entry in `Ground.md`; a Feature never contradicts them.
- A location with no Connections entry has no Exits line.
