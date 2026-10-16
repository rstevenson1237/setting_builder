# Procedures.md

## Purpose
What the ruleset assumes a setting provides, once for the whole setting: how a hazard is
stated, the Wound and Madness tables, the Conditions, the coin and ordinary prices, time
and distance, weather, encounter distance, the Danger bands and carousing. It restates
none of the ruleset and holds nothing that belongs to one place; those are
`setting/LocalProcedures.md`'s. Seeded with working defaults, tailored once the setting is
written, and extended only if generated content turned out to need something the seed did
not cover.

## Context
Read first:
- `GENRE.md`, `STYLE.md` and `BRIEF.md`
- `patterns/Common_Schema.md` and `patterns/Setting_Schema.md`
- `setting/Setting.md` and `setting/Truths.md`, once written

## Instructions
Sections, in order: Ruleset, Forced Dangers, Wounds, Madness, Conditions, Coin and Prices,
Time and Distance, Weather, Encounters, Carousing.

- **Ruleset** - about eight lines: the vocabulary the rest assumes (the three Action Dice,
  the Difficulty die, a 1 is a FAILURE, a 2 or 3 a COMPLICATION, a 4 or more a SUCCESS).
- **Forced Dangers** - how a hazard states what it forces: a trigger, a Test, a count of
  Tests, a penalty. A Test of Constitution rolls the Combat die and a penalty is a Wound of
  a Type; a Test of Fate rolls the Skill die and a penalty is a named Condition; a Test of
  Sanity rolls the Magic die and a penalty is Madness. A hazard's `Damage_Type` sets its
  count: Nuisance 1, Damaging 2, Lethal 3. `GENRE.md`'s Lethality answer is a rule a hazard
  can cite: what one failed Test costs a first-level character.
- **Wounds** - one `### [Type]` table of six rows, `1` to `6`, for each Wound_Type
  `BRIEF.md`'s `Procedures wounds` lists: the mechanical effect of a Wound of that Type, plain
  enough to apply without looking anything up.
- **Madness** - present only where `BRIEF.md`'s `Procedures madness` is not 0: one table of
  six rows. A Test of Sanity is cited only where it exists.
- **Conditions** - each `- **Name** - effect; how long it lasts`. Every Condition a Test of
  Fate or a Wound row names is here.
- **Coin and Prices** - the common silver coin, cn, is the unit of every value in the
  setting; a hundred cn weigh 1 wt. Name each other coin the setting knows and its ratio to
  cn, the fee for changing one (3%) and for reselling goods (10-20%), and what copper pennies
  cover untracked. Then the ordinary goods and services a Purchase prices against, and a
  hireling's wage by the day, each in cn.
- **Time and Distance** - what each region type measures in, and the miles a watch covers on
  a road, off it and through the worst ground; how long a light lasts.
- **Weather** - a d6 table of six rows. A 1 is severe (travel impossible), 2 and 3 are poor,
  4 to 6 are calm; the setting writes what each is.
- **Encounters** - a d6 table of distance, 1 an instant surprise to 6 signs or tracks only,
  and the six Danger bands, 6 to 1, each in a line a region's Brief can instance. The party
  size numbers appearing are set for.
- **Carousing** - a d6 table of effects: 1 and 2 negative, 3 and 4 neutral, 5 and 6 positive.

## Template
```
Procedures of [Setting Name]

## Ruleset
[...]

## Forced Dangers
[...]

## Wounds
### [Wound_Type]
| d6 | Wound |
|---|---|
| 1 | [effect] |
| ... | ... |
| 6 | [effect] |

## Madness
| d6 | Madness |
|---|---|
| 1 | [effect] |
| ... | ... |
| 6 | [effect] |

## Conditions
- **[Name]** - [effect]; [duration]

## Coin and Prices
[...]

## Time and Distance
[...]

## Weather
| d6 | Weather |
|---|---|
| 1 | [severe weather] |
| ... | ... |
| 6 | [calm weather] |

## Encounters
[...]

## Carousing
| d6 | Effect |
|---|---|
| 1 | [negative effect] |
| ... | ... |
| 6 | [positive effect] |
```
