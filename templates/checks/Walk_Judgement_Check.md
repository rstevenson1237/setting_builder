# Walk_Judgement_Check.md

## Purpose
The setting walked as a party walks it, for what no reading by file can see: where play stops,
or a referee must invent to keep it going. Saved as `setting/checks/WalkJudgementCheck.md`.

## Context
- `GENRE.md`, `STYLE.md` and `BRIEF.md` - its `test` line is the route, and its `walks` the
  number of times it is walked.
- at each location reached: its write-up's read-aloud, then each Feature a party would look at,
  then its Exits - nothing a party is not given.
- the maps, drawn by `python3 tools/maps.py draw --out _maps`, and `python3 tools/space.py from
  CODE to CODE` for where one place lies from another.
- the output of `python3 tools/validate_setting.py`.

## Instructions
Run this once the loop has exited, in a context that wrote none of the setting. Walk the `test`
line's route from where its party begins as many times as `walks` asks, each walk taking a
choice the others did not wherever the text offers one. Record findings only, each with the
location's code, its likely source - a table line, a write-up, a seed, a `BRIEF.md` line, a map
or a tool - and the step that owes it. A finding a tool could make - a count, an overlap, a missing citation - is also listed under Owed to a tool.

Read for:
- **A next step** - where the text gives a party no way on, or only one where the seed
  promises a choice.
- **What a party needs** - a fact it needs and cannot find: a way in, a price, who to ask,
  what a key opens.
- **One place** - where the map, the text and the brief disagree about what is there or which
  way it lies.
- **Nothing invented** - what a referee must make up to keep the walk going.

## Template
```
# Walk Judgement Check - [Date or revision note]

## Routes
1. [Location Code, Location Code, ...]
[one line per walk]

## Findings
- [Location Code] - [item]: [note] - [source] - [step]

## Owed to a tool
- [A finding a tool could make] - [tools/validate_setting.py, tools/metrics.py or tools/space.py]
```
