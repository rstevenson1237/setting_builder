# Template Judgement Check - 2026-11-22, the island build after #127, run before the step 4 loop exited

Confirmed on every item: templates/region/Region_Gazetteer.md, templates/region/Locations.md, templates/region/Design.md, templates/setting/Setting.md, templates/setting/History.md, templates/setting/Truths.md, templates/setting/Bestiary.md, templates/setting/Factions.md, templates/setting/Treasure.md, templates/setting/Magic.md, templates/setting/Language.md, templates/setting/Lore.md, templates/setting/UniqueTreasures.md, templates/setting/MagicalTomes.md, templates/setting/Hoards.md, templates/setting/LocalProcedures.md, templates/setting/NamedCreatures.md, templates/setting/Rumours.md

## Findings
- templates/region/Brief.md - No defaults: the Tables field takes no row count from the die or from `BRIEF.md`, and the `--skeleton 4e` shape it points to (tools/templates.py) prints 6 rows under a "[die, if rolled]" heading. The writer heads each table with the region's die and writes 6 rows - the build shows "d10 Encounter" in D.md and "d8 Encounter" in B.md, C.md and E.md, each with 6 rows, so rolls of 7 to 10 land on nothing.
- templates/setting/Procedures.md - Every field is used: its Encounters item asks for distance and the Danger bands but never for how often an encounter comes. `setting/Procedures.md` says "a party rolls an encounter check each watch" and gives no die or chance, so no WILD table can be rolled from the text.
- templates/region/Region.md - Consistent with the other templates: a Ruling may restate a procedure in its own terms. B's Ruling has Lost checked "each watch"; `setting/Procedures.md` and D.1 have it "at the start of each day".
- templates/region/Region.md - Every field is used: an Entry joining two regions is copied word for word into both seeds, so its `refused` fits only one side. HA's and HB's shaft Entry reads "chased up the stair" beside "no stair", and C's and D's great-gate Entries describe A's tower, not the ground a party reaches on their side.
- templates/region/Location.md - Entries match: "A `member` is the referee's" says what the Feature hides, but not what a party can read off a member. Both councils' bound men (A.10 Hatokali, F.9 Vakomano) fall back on the same invented tell ("keeps the shirt laced to the throat ... knows what each chief/elder fears"). Neither shows Tuuzesh's second Identity mark, the pass-phrase "The sleeper turns".
- templates/region/Location.md - Format edge cases preserved: "A Stop ... in the route's order, saying how far along" is not held to the route's length. B.1 lists its stops at 0.8, 0.3, "at the way in", 1 and 1.4 miles on a 9.5-mile way, and D.1 ends its stops at 2 miles on a two-day crossing.
- templates/setting/Quests.md - Every field is used: a quest's Obstacle `misdescribed` has no line for what is true, so The Lost Hunters points at D.10 and nothing in the setting says what took the hunters.
- templates/setting/Keys.md - The right schemas: it writes `Opens` from the Lock's `from` location, so all three keys name the room before the lock, not the room it opens (Scale Seal "HB.8" for the HB.9 treasury, Captain's Key "I.4" for the I.7 strongroom, Serpent Ring "HC.6" for the HC.7 bier).

## Open Items
- Brief.md and tools/templates.py: give the Tables field a row count, either one row per face of the stated die or a fixed d6 with the heading "d6". Rewrite B.md, C.md, D.md and E.md to match - template.
- Region.md: say that a Ruling cites a Procedures rule rather than restating it, and that a mirrored Entry's `stands` and `refused` are written from the side being entered - template.
- Location.md: say a faction member's Feature shows one of the faction's Identity marks, and never the same invented tell twice - template.
- Quests.md: when the Obstacle is `misdescribed`, require the truth to be written in the Object or under Truths - template, schema (see SchemaJudgementCheck).

## Owed to a tool
- A brief table whose heading die differs from its row count - tools/validate_setting.py
- Stops out of distance order, or a last Stop far short of the route's length - tools/validate_setting.py
- A Feature sentence frame repeated across regions for faction members (same verb phrase on two Persons) - tools/metrics.py
- An Entry `refused` that names a feature (a stair) its own `stands` denies - tools/validate_setting.py

## Resolved since
- Brief tables are d6: the skeleton heads them d6, Brief.md says a WILD Encounter table is rolled on a 1 of the Difficulty die and a row may offer several encounters, and the validator rejects any other die. B, C, D and E rewritten to match.
- Encounter odds and Lost: decided not template gaps; Procedures.md's Encounters item names the Difficulty-die trigger.
