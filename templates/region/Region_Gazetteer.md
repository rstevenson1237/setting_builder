# Region_Gazetteer.md

## Purpose
An overview listing of all regions within the setting - the Regional Gazetteer.

## Context
Read first:
- `GENRE.md`, `STYLE.md` and `BRIEF.md`
- `setting/Setting.md`
- `setting/Language.md`

## Instructions
List the regions `BRIEF.md` names.

List an overview of all regions within the setting. This file is a Regional Gazetteer - further entries can be added by appending to or changing this file. Each region is rated SAFE, WILD, or DANGEROUS and given the die `BRIEF.md` sets (d4-d12), per `setting/Procedures.md`. A DANGEROUS region such as a dungeon may sit within a WILD region, and this should be noted in its overview. Each row names the regions it joins: those it borders, and the WILD region a DANGEROUS one opens from. A join is mutual, so each region lists every region that lists it, and none lists itself. Each row carries a tag line: one phrase defining the region one step past its name.

Codes follow a plain A-Z progression with no differentiation between types (A, B, C, ...). For a complex setting with more than 26 regions, continue with double letters (AA, AB, AC, ...).

A region's name follows `GENRE.md`'s Naming answer, a Place_Form
from `patterns/Common_Schema.md`. A tongue name is built from `setting/Language.md`'s roots, recorded
back into its "Coined here" list, and **glossed** in the Gloss column: what it means, in a
clause - a referee reads this gazetteer without opening Language.md mid-session. A common
name's Gloss is `none`.

## Template
```
Regional Gazetteer of [Setting Name]

| Code | Name | Form | Gloss | Rating | Die | Joins | Tag line |
|---|---|---|---|---|---|---|---|
| [A] | [Region Name] | [PLACE_FORM] | [what the name means, or `none` where it is plain] | [SAFE/WILD/DANGEROUS] | [d4-d12] | [codes of the regions it borders or opens onto, space-separated] | [one phrase, the region one step past its name] |
```
