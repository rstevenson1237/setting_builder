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
```kdl
template scope="setting" writes="setting/Procedures.md"
read "setting/Setting.md" once="written"
read "setting/Truths.md" once="written"
format {
  line title pattern="Procedures of [Setting Name]"
  section Ruleset
  section "Forced Dangers"
  section Wounds out="table" head="Wound" each="BRIEF:Procedures.wounds"
  section Madness out="table" head="Madness" when="BRIEF:Procedures.madness"
  section Conditions out="bullets" item="**[Name]** - [effect]; [duration]"
  section "Coin and Prices"
  section "Time and Distance"
  section Weather out="table" head="Weather"
  section Encounters out="table" head="Distance"
  section Carousing out="table" head="Effect"
}
```

## Instructions
- **Ruleset** - about eight lines: the vocabulary the rest assumes (the three Action Dice,
  the Difficulty die, a 1 is a FAILURE, a 2 or 3 a COMPLICATION, a 4 or more a SUCCESS).
- **Forced Dangers** - how a hazard states what it forces: a trigger, a Test, a count of
  Tests, a penalty. A Test of Constitution rolls the Combat die and a penalty is a Wound of
  a Type; a Test of Fate rolls the Skill die and a penalty is a named Condition; a Test of
  Sanity rolls the Magic die and a penalty is Madness. A hazard's `Damage_Type` sets its
  count: Nuisance 1, Damaging 2, Lethal 3. `GENRE.md`'s Lethality answer is a rule a hazard
  can cite: what one failed Test costs a first-level character.
- **Wounds** - the mechanical effect of a Wound of each Type, plain enough to apply without
  looking anything up.
- **Madness** - a Test of Sanity is cited only where it exists.
- **Conditions** - every Condition a Test of Fate or a Wound row names.
- **Coin and Prices** - the common silver coin, cn, is the unit of every value in the
  setting; a hundred cn weigh 1 wt. Name each other coin the setting knows and its ratio to
  cn, the fee for changing one (3%) and for reselling goods (10-20%), and what copper pennies
  cover untracked. Then the ordinary goods and services a Purchase prices against, and a
  hireling's wage by the day, each in cn.
- **Time and Distance** - what each region type measures in, and the miles a watch covers on
  a road, off it and through the worst ground; how long a light lasts.
- **Weather** - a 1 is severe (travel impossible), 2 and 3 are poor, 4 to 6 are calm; the
  setting writes what each is.
- **Encounters** - distance, 1 an instant surprise to 6 signs or tracks only,
  and the six Danger bands, 6 to 1, each in a line a region's Brief can instance. The party
  size numbers appearing are set for.
- **Carousing** - 1 and 2 negative, 3 and 4 neutral, 5 and 6 positive.
