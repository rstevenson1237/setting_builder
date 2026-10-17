# Template Judgement Check - 2026-10-17

Confirmed on every item: templates/setting/Bestiary.md, templates/setting/Hoards.md, templates/setting/Keys.md, templates/setting/MagicalTomes.md, templates/setting/UniqueTreasures.md, templates/setting/LocalProcedures.md, templates/setting/NamedCreatures.md, templates/setting/Quests.md, templates/setting/Setting.md, templates/region/Region_Gazetteer.md, templates/region/Connections.mmd, templates/safe/Connections.mmd, templates/wild/Connections.mmd, templates/dangerous/Connections.mmd.

## Findings
- templates/setting/Magic.md - Consistent with STEPS.md and the other templates: Purpose says "a reusable d6 table" while `BRIEF.md` sets `Magic rolls=12` and `setting/Magic.md` holds 12 rows.
- templates/setting/Procedures.md - No defaults: states "the fee for changing one (3%) and for reselling goods (10-20%)", "about eight lines" and a hundred cn to the wt; each belongs in `BRIEF.md`. The last build wrote 3%, 10-20% and the 80% resale as written.
- templates/setting/Factions.md - Every field is used: Tactics is "how they typically act on a Faction Turn", but `setting/Procedures.md` has no Faction Turn, and AD and the Relations dice are read by no step or table.
- templates/region/Tables.md - One context, no step instructions: Instructions are organised by step (4a, 4c, 5a, 5d). Also holds "a stub that will not fit its room is a finding for 5c", which is STEPS.md's.
- templates/region/Location.md - One context, no step instructions: "When entries change for a location already written, rewrite only the lines they touch" is step 5b's.
- templates/region/Location.md - Format edge cases preserved: (1) a Faction's members are cited by Bestiary entry, but The Black Altar's acolytes have none (Fields: Zombie only), so M.1, M.3, M.11 cite nothing; (2) a Mystery that asks a Test (M.11) has no citation form - the page used `(Test of Sanity, 1d)`; (3) a Lock's key is not said to be cited, and the validator demanded `(Keys: ...)` on L.1, M.10 and M.11.
- templates/region/Location.md - Entries match: J.2's captives are a Feature carried only by Dressing `obvious`; nothing in the template says a Feature may exist without an entry of its own.
- templates/region/Brief.md - One context, no step instructions: "A fact no entry holds is a placement for step 5d" names a step.
- templates/setting/Rumours.md - No defaults: "numbered to the die `BRIEF.md` sets" is fine, but nothing asks that every tribe `BRIEF.md` names be covered; the last build has no bugbear rumour.
- templates/setting/Truths.md - Genre drift guardrails: allows "a standing mystery or a gap left for the referee" but does not require one for each `U` Rumour; Rumours 8 and 12 have none.
- templates/setting/Lore.md, templates/setting/History.md - Consistent with STEPS.md: STEPS.md 5d says "fill the Handles and Left lines", while both templates ask for Codes; the last build filled Codes (a Handle names no code).
- templates/setting/Treasure.md - No context creep: reads `setting/Bestiary.md`; the tables do not use it.
- templates/setting/Language.md - Every field is used: only 1 of 18 Makers' Tongue roots and 1 Cant root are used in a coinage; the template asks for 15-20 roots a tongue regardless.
- templates/checks/Setting_Judgement_Check.md (observation; reviewed by being run) - names "a truth's Handle names a real Location Code" and "a History Left line names a real Location Code", where the codes sit in Codes; and lists neither Quests, Rumours, Hoards, Tomes nor Local Procedures in Context although "Everything recurs" covers them.

## Open Items
- Change Magic.md's "d6" to the brief's rolls - source: templates/setting/Magic.md.
- Move Procedures' 3%, 10-20% and line counts to `BRIEF.md` - source: templates/setting/Procedures.md.
- Define a Faction Turn in `setting/Procedures.md` or cut it from Factions.md; decide AD and dice use - source: templates/setting/Factions.md.
- Move step headings out of Tables.md, the 5b rewrite line out of Location.md, and the 5d line out of Brief.md into STEPS.md - source: Tables.md, Location.md, Brief.md.
- Add Location.md rules for member Features with no Bestiary entry, a Mystery's Test, and a Lock's key citation - source: templates/region/Location.md.
- Say whether a Feature may stand on Dressing alone - source: templates/region/Location.md.
- Ask Rumours to cover every tribe and Truths to hold every `U` answer - source: templates/setting/Rumours.md, Truths.md.
- Change STEPS.md 5d "Handles and Left lines" to name Codes - source: STEPS.md.
- Drop Bestiary from Treasure.md's Context; cut or justify the 15-20 roots floor - source: Treasure.md, Language.md.
- Correct the Setting check's Handle/Left wording and Context list - source: templates/checks/Setting_Judgement_Check.md.
