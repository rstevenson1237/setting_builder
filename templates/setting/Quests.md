# Quests.md

## Purpose
The registry of errands running between locations - who wants what, where it is, and what
stands in the way. Stubbed at 4c as each end is written, filled at 4d.

## Context
Read first:
- `GENRE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- `patterns/setting/Quests.md`
- At 4d: every location file the stub points to, both giver and target.

## Instructions
A Quest is **two-ended**: a giver location and a target location, both named by code. At
4c a stub row fills Name, Given at and Resolved at and leaves every other cell empty; at
4d write the rest, with both location files in view.

## Template
```
Quests of [Setting Name]

| Name | Given at | Resolved at | Ask | Giver | Reluctance | Object | Obstacle | Terms |
|---|---|---|---|---|---|---|---|---|
| [Quest Name] | [Code].[N] | [Code].[N] | [ASK] | [who wants it] | [why they will not go themselves] | [what specifically, and where in the target location] | [what stands in the way] | ["stated in the giver's own words"] |
```
