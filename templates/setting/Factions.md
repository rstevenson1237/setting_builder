# Factions.md

## Purpose
The factions present in the setting - the powers a party may treat with, oppose, or ignore.

## Context
```kdl
template scope="setting" writes="setting/Factions.md" shape="Factions"
read "setting/Setting.md"
read "setting/History.md"
read "setting/Truths.md"
read "setting/Bestiary.md"
format {
  table head="Level, Relation, Die, Stance" {
    row "5" "Friendly" "d12" "Will look to advance the causes of their allies."
    row "4" "Tolerated" "d10" "Will look for equal gain between parties."
    row "3" "Neutral (or Ambivalence)" "d8" "Will only cooperate with some advantage to themselves."
    row "2" "Antipathy" "d6" "Will only cooperate with great advantage to themselves."
    row "1" "Hatred (or Fear)" "d4" "Will only cooperate under duress, may take an opportunity to disadvantage one of their opponents, otherwise Hostility or Escape are preferred."
  }
}
```

## Instructions
List the factions `BRIEF.md` names, each following its fields in `patterns/Setting_Schema.md`.

The file opens with its format's Relations table, copied as written. Each entry's Relations
lists every other faction once, by the Relation it holds toward that faction; where
`BRIEF.md` names one, that is the Relation. A parenthetical in the table is a second name
the line may add: `- The Zhakuk - Hatred (fear)`.
