# Template Judgement Check - build 1, Roadsend, 2026-10-15

Confirmed on every item: templates/setting/Setting.md, Bestiary.md, Treasure.md, Magic.md, Language.md, Lore.md, Keys.md, NamedCreatures.md, UniqueTreasures.md, MagicalTomes.md, Hoards.md, Quests.md; templates/region/Region_Gazetteer.md, Connections.mmd, Tables.md, Brief.md; templates/dangerous/Connections.mmd and templates/wild/Connections.mmd.

## Findings
- templates/setting/Factions.md - no defaults: Purpose states "The 3 factions present"; `BRIEF.md` sets `Factions count=2`, and the build wrote 2.
- templates/setting/History.md and templates/setting/Truths.md - no defaults: Purpose says "1 or more"; `BRIEF.md` sets both to 0 and the Instructions then allow a header-only file. The Purpose contradicts the Instructions; the last build wrote both files as header lines.
- templates/setting/Factions.md - consistent with STEPS.md: Context reads `setting/Rumours.md`, written at 5d, three steps after 2e writes Factions; it did not exist when Factions was written.
- templates/setting/Rumours.md - no defaults: the Template block ends at row 20; `BRIEF.md` sets `Rumours die=6`. The Instructions say "numbered to the die".
- templates/setting/Procedures.md - consistent with the other templates: its Instructions list sections but not the three Tests (Constitution, Sanity, Fate) that `templates/region/Location.md` and the validator hard-code, so the last build defined them from the Location citation alone. The template asks for a Wounds and Madness section though the brief set no madness.
- templates/region/Location.md - format edge cases preserved: Citations offers `(Test of Sanity, Xd)`, which this build has no use for (no madness); a SAFE write-up has only Dressing entries, so "nothing without one" is not satisfiable for A (see the Schema check).
- templates/setting/Language.md - no context creep: Context has 5b read `patterns/Setting_Schema.md` whole (about 1,400 words) for one table of about 150, to record coinages.
- templates/setting/Procedures.md - genre drift guardrails: nothing in Instructions asks that Lethality (poison save or die) appear as a rule that a later hazard can cite; the last build's Lethal poison is defined and unused.

## Open Items
- Replace "3" with the brief's count (Factions) and "1 or more" with "the events/truths `BRIEF.md` asks for" (History, Truths) - template.
- Drop `setting/Rumours.md` from Factions' Context, or move the reading to the step that has it - template or STEPS.md.
- Cut the Rumours Template block's example to a placeholder row range - template.
- Name the Tests in Procedures' Instructions, or drop Sanity from Location's Citations - template.
- Name the Language table, not the whole Setting_Schema, in Language's Context - template.
