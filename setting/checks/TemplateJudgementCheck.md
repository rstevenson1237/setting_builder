# Template Judgement Check - after the region-overview, tag and defaults rework

Run against `templates/` at commit dc4bd44, with Greywatch (98 locations, through 4c) as the
last build. Items marked N/A do not apply to the file's artifact.

## templates/Setting.md
- Correct patterns, correct order: Confirmed - names `patterns/setting/Setting.md` only.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: N/A
- Format edge cases preserved: Confirmed - the tag line sits between name and outline; the site reads the first non-italic line as it.
- Genre drift guardrails: Confirmed - the pattern's "something a generic setting of its genre does not have" line carries it.
- Defaults yield to the brief: N/A - no counts.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed - name, tag line and outline all render on the site's index.
- Consistency across templates: Confirmed.

## templates/Procedures.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: N/A
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Needs Fix - the section list is fixed (Tests and Consequences, Hazards, Wounds and Madness, ...) whatever GENRE.md's Reference is. Greywatch's B/X build carries Tests of Sanity and a Madness track the reference does not have; nothing here says a section the reference lacks is dropped. Source: template default.
- Defaults yield to the brief: Needs Fix - the section list is not framed as a default.
- Defaults are neutral: Needs Fix - "Wounds and Madness" is one genre's mechanic.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/Language.md
- Correct patterns, correct order: Confirmed.
- No context creep: Needs Fix - "At 4d: every location, region and registry file" is the whole setting; the step only needs the coined names, which `tools/metrics.py` or a grep can list.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: N/A
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed - three tongues default, stated as a default.
- Defaults yield to the brief: Confirmed.
- Defaults are neutral: Needs Fix - "an older tongue for ruins and the dead" presumes a setting with ruins built by a departed people; in Greywatch it helped push a 900-year Old Tongue history against the brief's "history is shallow". Source: template default.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/History.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: Confirmed - Left lines carry `[pending 4d]`.
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed - "at least one still resolving" keeps it a situation.
- Defaults yield to the brief: Confirmed - now empty unless asked.
- Defaults are neutral: Needs Fix - "at least one outside living memory, whose evidence is physical only" and "three occupancies" presume deep time; a shallow-history brief still gets them once a history is asked for.
- Every field is used: Confirmed.
- Consistency across templates: Needs Fix - the Template block shows `[pending 4d]` but STEPS.md fills Left lines at 5c.

## templates/Truths.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: Needs Fix - Handle `[pending 4d]` in the Template block, filled at 5c per STEPS.md.
- Format edge cases preserved: Needs Fix - the Template block shows only the rule and Handle; Greywatch's truths also carry Costs, Learned and Shows lines, which the pattern asks for and the Template block omits.
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Confirmed.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Needs Fix - as above.

## templates/Rumours.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: Confirmed - Settled at `[pending 5c]`.
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Needs Fix - "A referee-facing table of 20 rumours" in Purpose is a fixed count, not a default.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/Bestiary.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: N/A
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Confirmed - reworked this session; Greywatch's bestiary predates it and followed the old 30% Undead default against the brief. Source: template default.
- Defaults are neutral: Needs Fix - "At least one entry the party is NOT meant to beat" and "at least one at 13+" are one genre's shape; Greywatch's Bound Depth (14d6) exists to satisfy them in a starter-dungeon setting.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/Factions.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: N/A
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Needs Fix - "List 3 factions" is a fixed count. The brief named the tribes, plural, as a faction group; Greywatch made one tribe a faction and left Hukkgur and the Khughik without Faction entries.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/Treasure.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: N/A
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Needs Fix - no table has a slot for GENRE.md's Magic level answer. B/X's "a potion, a scroll or a weapon a little better than it should be" has nowhere to land except Table II's fine/masterwork effects, and Greywatch's five tables carry no potion or scroll at all. Source: template default.
- Defaults yield to the brief: Confirmed.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/Lore.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: Confirmed.
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Needs Fix - `BRIEF.md` is missing from Context.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Needs Fix - same omission in Keys, NamedCreatures and UniqueTreasures.

## templates/Keys.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: Confirmed.
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Needs Fix - `BRIEF.md` missing from Context.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Needs Fix - see Lore.

## templates/Quests.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: Confirmed.
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Confirmed.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/NamedCreatures.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: Confirmed.
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Needs Fix - `BRIEF.md` missing from Context.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Needs Fix - see Lore.

## templates/UniqueTreasures.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: Confirmed.
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed - "a setting supports very few of these".
- Defaults yield to the brief: Needs Fix - `BRIEF.md` missing from Context.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Needs Fix - see Lore.

## templates/Region_Gazetteer.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: N/A
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Confirmed - "start every region at d8, move off it only for a reason".
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/Connections.mmd
- All items: Confirmed; N/A for registries and defaults.

## templates/Region.md
- Correct patterns, correct order: Confirmed.
- No context creep: Needs Fix - reads all of Rumours, Bestiary and Factions whole; the overview's Inhabitants needs the names and dispositions, not every field.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: N/A
- Format edge cases preserved: Confirmed - validator checks the field set and two d6 tables.
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Confirmed.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed - new this session; every field is a run-sheet field.
- Consistency across templates: Needs Fix - `templates/Location_Gazetteer.md`'s DANGEROUS default of "1-2 entrances at about 12 locations" and Region.md's Approach ("every entrance") agree, but nothing in either lets an entrance open onto a region-level space; see Block_Connections.

## templates/Region_Connections.mmd
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: N/A
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: N/A
- Defaults yield to the brief: Confirmed.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/Location_Gazetteer.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: Confirmed - stubs carry weight and tags, no Pattern.
- Two-phase registries respected: N/A
- Format edge cases preserved: Confirmed - three tags, validator checks header against stub.
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Needs Fix - the SAFE count default ("about as many as the die") was overridden by the brief's thirty; the result was thirty thin liner notes. The default was right and nothing here says a count far past the die should become Features instead of locations. Source: brief.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/Block_Connections.mmd
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A
- Two-phase registries respected: N/A
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: N/A
- Defaults yield to the brief: Needs Fix - "Every location reachable from an entrance" with "locations connect only to locations" gives an entrance nothing to open onto but another region's location. The brief's ten entrances onto the ravine could not be drawn; two were. Source: template.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/Location.md
- Correct patterns, correct order: Confirmed - names only the class file; the rest is reached by Spec edges.
- No context creep: Confirmed - and `tools/context.py 4c` now assembles it. The stream adds `STYLE.md` and drops sibling rooms, which Location.md's list does not mention either way.
- Pattern chosen at generation time, not earlier: Confirmed.
- Two-phase registries respected: Confirmed.
- Format edge cases preserved: Confirmed - the Feature grammar is unchanged; it is still the construction that funnels contrasts into "rather than" (73 of 192 Features).
- Genre drift guardrails: Confirmed.
- Defaults yield to the brief: Confirmed.
- Defaults are neutral: Confirmed.
- Every field is used: Confirmed.
- Consistency across templates: Confirmed.

## templates/Template_Judgement_Check.md, Pattern_Judgement_Check.md, Setting_Judgement_Check.md
- Reviewed separately, below; this check does not audit itself line by line.

## Open Items
- Procedures.md: frame its section list as a default the reference can drop from. (template default)
- Language.md: narrow the 4d read set; stop defaulting to an older tongue of the dead. (template default)
- History.md, Truths.md: pending markers say 4d where STEPS.md fills at 5c; Truths' Template block omits Costs/Learned/Shows. (template)
- Rumours.md, Factions.md: counts stated as fixed rather than as defaults. (template default)
- Bestiary.md: the unbeatable and 13+ requirements are one genre's shape. (template default)
- Treasure.md: no slot for GENRE.md's Magic level answer. (template default)
- Lore, Keys, NamedCreatures, UniqueTreasures: add `BRIEF.md` to Context. (template)
- Region.md: read names and dispositions, not whole setting files. (template)
- Location_Gazetteer.md: say what happens to a SAFE count far past the die. (template)
- Block_Connections.mmd: give an entrance something to open onto. (template)
