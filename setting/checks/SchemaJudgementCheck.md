# Schema Judgement Check - 2026-11-22, the island build after #127

Evidence: setting/checks/SettingJudgementCheck.md of 2026-11-22. I resolved A.1, A.10, A.12, B.1, B.5, B.9, C.4, C.9, D.1, D.10, D.12, E.9, F.9, F.10, HA.10, HB.1, HB.5, HB.8, HB.9, HB.13, HC.6, HC.7, I.4, I.7, J.1, J.7 and J.8.

Confirmed on every item: patterns/Common_Schema.md, patterns/Dangerous_Schema.md, patterns/Safe_Schema.md

## Across the schemas
- Gaps: no node writes a dinosaur, or any beast `BRIEF.md` says is "a hazard to avoid as often as a fight", as anything but an Encounter. A Hazard's types have no creature form, so the brief's line about beasts falls through. Files: patterns/Setting_Schema.md (Bestiary), patterns/Wild_Schema.md (Challenges).
- Gaps: nothing states how often an encounter comes. Procedures carries the distance table and the Danger bands but no check die or odds, so a WILD region's Encounter table cannot be rolled from the text. Files: patterns/Setting_Schema.md (Procedures), templates/setting/Procedures.md.
- Unhoused content: the pressure's bound men "wear a scale-mark hidden on the skin". A Faction's Identity holds the mark and a pass-phrase, but no field places a pass-phrase or a test where a party can use it, so it lands nowhere. Files: patterns/Setting_Schema.md (Factions), patterns/Common_Schema.md (Person `member`).

## Findings by file
- patterns/Setting_Schema.md Keys.Opens - Specific: `place from=Lock` names the Lock's `from` location, so each row names the room in front of the lock (Scale Seal "HB.8", Captain's Key "I.4", Serpent Ring "HC.6") rather than what it opens. Name the Connection ("HB.8 → HB.9") or the `to` side.
- patterns/Setting_Schema.md Quests.Obstacle - Enforceable / Discoverable: `misdescribed` (also `misplaced`) needs the truth beside it. The Lost Hunters has none, and nothing in the build says what took them.
- patterns/Setting_Schema.md Hoards / Keys - No overlap: a Key opens a Connection, while a Hoard sits in a room. When the prize is in a container inside the room (I.7's strongroom hatch), the writer adds a second lock. Say that a Lock on a Connection is the only lock its key opens, or give a Hoard an optional container lock.
- patterns/Region_Schema.md Entry - No overlap or contradiction: one Entry is copied into both joined regions' seeds, with one `stands` and one `refused`. The far side's text then describes the near side's ground (C's and D's great gate) or contradicts itself (HA's and HB's shaft "no stair" / "up the stair").
- patterns/Wild_Schema.md Stop.distance - Enforceable: a free distance with no tie to the Way's or the route's length. Stops cluster in the first 2 miles of routes 9.5 to 24 miles long (B.1, D.1). Hold the distances in order and within the route's length.

## Open Items
- Keys.Opens: name the locked Connection, or its `to` location - field.
- Quests: add a `Truth` text field, required when the Obstacle is `misdescribed` or `misplaced` - field.
- Factions / Person: a `member` Person shows one of the faction's Identity marks, a test or a phrase a party can catch - comment.
- Entry: write `stands`/`refused` from the side being entered, or split it into `near` and `far` - comment.
- Stop.distance: in order, and no greater than the route's length - range.
- Hoards / Lock: one lock per prize - comment.

## Owed to a tool
- Stops out of order, or beyond the route's length - tools/validate_setting.py
- A Key row whose Opens is the Lock's `from` side - tools/validate_setting.py (once the field is changed)
- A quest with obstacle `misdescribed` and no truth - tools/validate_setting.py

## Resolved since
- Encounter odds: decided not a gap. A WILD region's d6 Encounter table is rolled on a 1 of its Difficulty die, and Lost is the ruleset's own; `setting/Procedures.md` now says the first.
- Dinosaurs as hazards: decided against. A hazard is triggered by an action; a dinosaur attacks unprompted, and its numbers already make it one to avoid.
