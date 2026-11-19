# Intake - judgement checks: reviews that find what a checklist cannot

## The request, verbatim

> We can design 8.

## How it is read

Review item 8. `spec.md` numbers each proposal for approval; none is built.

## What the history holds

| Commit | What it decided or found | Here |
|---|---|---|
| efc0626, 7e23680 | Step 5 began as three checks, each a checklist filled per item. | The shape J1 changes. |
| 6924638 (#64) | "Make the judgement checks look for what the last build got wrong": each finding "traced to its source", and the checklist gained "the checks a Greywatch read-through needed and none of the three templates asked for". | How the checklist has grown before: from a read-through of a finished build. J5 does it again. |
| 778ff41 (#82) | "5c is mechanical", and four of a check's findings became `metrics.py` readings: CARRY, HEADCOUNT, RECURRENCE, FRAMES. | J4 is this, made the rule. |
| f4469bd, `fixtures/control/COMPARISON.md` | One fixed map, three arms, judged item by item. The validator "caught eleven genuine errors" and one warning fired "on every secret edge ... so it carries no signal at all". | A check that always says the same thing is noise: the case for J1. |
| 5780bd9 | The introspective plan listed "no playtest intake" among the workflow's gaps. That plan was reverted at b288649. | J2 is the smallest form of it: a walk, read, by the model. |

## What the checks returned last time

`setting/checks/SettingJudgementCheck.md` holds 104 item lines: 8 for the setting and 8 for each of 12 regions.
91 read "Confirmed". The 13 findings are real and small: stale write-ups, a repeated phrase, a chapel off centre.

The same pass, and the map check beside it, did not report:

- that the Black Stair's head lies inside pyramid level 4, and the lake cavern's floor cuts level 6;
- that the three branches a party is meant to bargain with have nobody to bargain with by name;
- that the buried city's map shows no city, and has forest and a river at its edge;
- that no map draws what a room holds.

None of these is an item on a checklist. Each shows the moment someone walks the place in order.

## Out of scope

What the validator and `metrics.py` can count: a finding a tool can make is the tool's.
