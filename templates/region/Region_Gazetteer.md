# Region_Gazetteer.md

## Purpose
An overview of all regions within the setting - the Regional Gazetteer.

## Context
```kdl
template scope="setting" writes="setting/region/Regions.md" shape="gazetteer"
read "setting/Setting.md"
read "setting/Language.md"
field "Region.name" from="Language.Coined here"
```

## Instructions
Write a `Region` node for each region `BRIEF.md` names; further regions are appended.

Each region is rated and given the die `BRIEF.md` sets, per `setting/Procedures.md`. A DANGEROUS
region such as a dungeon may sit within a WILD region, and its `joins` names that region. A
region's name follows `GENRE.md`'s Naming answer. A tongue name is built from
`setting/Language.md`'s roots, recorded back into its "Coined here" list, and glossed: a referee
reads this gazetteer without opening Language.md mid-session.
