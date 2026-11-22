# Setting Judgement Check - 2026-11-22, the island build after #127, run before the step 4 loop exited

Run early, at the user's request: `--pending` shows 77 write-ups owed to 4b and 7 briefs owed to 4e. The findings below are on the content as it stands, and some stale write-ups may already be fixed when 4b is rerun.

Confirmed on every item: none in full. I read C, E, G and J by brief and a sample of write-ups, and recorded no finding of their own.

## Setting-level
- The brief was delivered: the step 4 loop has not exited. 77 write-ups are stale against their seeds (A, B, C, D, E, F, G, HA, HB and I.2) and 7 briefs are stale. Source: generator; the seeds changed in #127 and 4b and 4e were never rerun.
- The brief was delivered: `BRIEF.md` says dinosaurs are "met as a hazard to avoid as often as a fight", but every dinosaur is written as an Encounter, 7 of D's 9 reactions are Hostile, and no Hazard or Mystery involves a dinosaur. Source: brief line → `templates/region/Tables.md` (a beast offers no way to be written as a hazard).
- The brief was delivered: Rumours were asked to point at each faction. None points at the cult or at the bound men in the councils, which is the pressure's biggest secret; rumour 12 (the sinkhole) answers something nobody asked for. Source: generator at 4d.
- Genre held across levels: the Lethality answer (poison is save or die) holds. The Reference answer (an island explored a day's march at a time) is undercut because the WILD routes' Stops all sit within the first 2 miles of routes 8 to 24 miles long (B.1, D.1). Source: template (see TemplateJudgementCheck).
- Every secret has its answer: The Lost Hunters (Quest, obstacle `misdescribed`; Rumour 5) has no fact the referee holds about what took the hunters. D.10 holds only centipedes, and J.5's captives are cave men. Source: schema (Quests has no truth field) and generator.
- Nothing contradicts: the gate and its ridge. D.12 is "a high cleared ridge above the great wall" that "drops to the great gate", and Kunotewa "comes down the Wall Ridge at dusk" to A.1, yet `space.py` puts D.12 13 miles north of A.1 (Way A.1 → D.12, 13 miles). A's brief also says the gate stands "half a mile north" of the village, where A.2 → A.1 is 2.5 miles. Source: `tools/maps.py place` placed D.12 at D's way in, and the generator wrote the adjacency.
- Nothing contradicts: the serpent crown. HC's seed has the god sleeping "on a heap of old bones and the serpent crown", but Quests, Unique Treasures and HC.7 put the crown on the emperor's skull behind the locked bier gate, away from the god. Source: seed (3c) not brought in line at 4a.
- Nothing contradicts: the galleon's lock. The Captain's Key is "turning the lock on the bilge strongroom's hatch", while the Lock is on the wooden door I.4 → I.7. I.7 then also has a bolted iron hatch "opened from the hold above". That reads as two locks, or as one lock in two places. Source: schema (a Key opens a Connection, a hoard sits in a container) and generator.
- Nothing contradicts: HB.5's keepers are "three bound men ... (Bestiary : Snake Man)". Bound men are tribesmen everywhere else (HA.10, HB.2). Source: generator at 4b.
- Nothing contradicts: E.9's watch is "two snake men ... bound men beside them", where E's and HA's seeds say "two bound men and a snake man". Source: generator.
- Nothing contradicts: the shaft. HA's and HB's seeds say "no stair" and then "a party turned back is chased up the stair"; HB.1 has a chain where HA.10 has a rope. Source: template (mirrored Entry) and generator.
- Every faction can be dealt with: Tuuzesh's members in the councils (A.10, F.9) can be met, but nothing a party can do reveals one. The pass-phrase in the faction's Identity is never placed, and the scale-mark is shown only where it is already obvious (HA.10, HB.5, F.10). Source: template (Location.md, member Features).
- Vocabulary is precise: the misuse is "Bestiary : Snake Man" for bound men (HB.5). The 13 glosses `metrics --tells` lists (A.10 "The hearth -> a great flat hearthstone", D.3 "The bone heaps -> the bones of other dinosaurs", B.8, E.9 and the rest) restate their Feature names. Source: generator.
- Coinage: Kunotewa (the tyrant at the gate) and Kunotiwa (the A.10 elder) are one vowel apart, and a referee will swap them at the table. Source: generator at 4a; `setting/Language.md` records both.

## Region A
- Locations reinforce their region: A.a's map has no lagoon or beach, so A.2 "the beach" is drawn as a gatehouse in the stockade (see MapJudgementCheck). Source: tools/maps.py.
- Said once: the challenge-and-answer at A.1 ("Who keeps the wall?") is the only pass-phrase in the setting, while Tuuzesh's own is never used. Source: generator.
- Prices fit the list: the chiefs' word for 50 cn (A.10) and the council's seal for 30 cn (F.9) are near each other, and neither room says why. Source: generator.

## Region B
- Locations reinforce their region: B.9's captive "a woman with a scale-mark under her shirt" is bound while held for sale to the cult that binds people. Nothing says why. Source: generator; keep it if it is meant, and give it its answer.
- Entries match: B.1's Stops are out of order (0.8, 0.3, "at the way in", 1, 1.4). Source: template.

## Region D
- Distinct: D.12 and A.1 both open "a forty-foot reptile"; D.3 opens the same way. Source: generator.

## Region F
- Distinct: F.9 Vakomano copies A.10 Hatokali's lines (council's speaker, shirt laced to the throat, "knows what each ... fears"). Source: template.

## Region HB
- Entries match: HB.5's keepers carry the wrong Bestiary (see above). HB.8's Scale Seal lock is right, but the registry row reads "Opens HB.8". Source: schema.

## Region HC
- Regions reinforce the setting: the seed puts the crown with the god (see above).

## Region I
- One room: I.4 says "the tide floods it" and I's seed says the hold "floods to the second deck", but every deck sits at one height (z 0 to 8), so no deck stands above another. Source: tools/design.py and plan.py lay a ship out flat.

## Room to Grow
- Truth 1 (the two shores will not carry a stranger's word) - only A.4 and F.4 carry it; a Rung at A or F where carried word is refused would deliver it.
- The bound men in the councils (the pressure line) - only A.10 and F.9. A rumour, and a place where the pass-phrase can be overheard (F.10, the cellar where they meet), would make it discoverable.
- Named Creatures Nealvaol (I.4), Rank the Crested (J.7), Thazsheek (HB.11) and Zuuthtuuz (HC.6), and each Lore entry, each appear in one place. Thazsheek "knows which of the bound men sit in the councils", which is the natural hook to place him in a rumour.
- The lost hunters - J.5 or J.6 could hold the hunters' net-patterned gear, which would answer the quest and tie D.10 to J.
- Coinage untracked: none found beyond the Kunotewa/Kunotiwa collision.

## Open Items
- Finish the loop: rerun 4b on the 77 stale write-ups and 4e on the 7 stale briefs, then rerun 4c - generator.
- Settle the Wall Ridge: either move D.12 to within sight of A.1 (a `place` line or design for D.12 in `BRIEF.md`), or rewrite D.12, A.1 and Kunotewa as 13 miles apart; fix A's brief "half a mile" - brief, generator.
- Write the lost hunters' truth (what took them, and where their remains or survivors are) and place it at a location - schema, generator.
- Bring HC's seed in line with the crown at HC.7 - generator (3c).
- Make the galleon's lock one lock: the key opens the I.4 → I.7 door or the strongroom hatch, not both - generator, schema.
- HB.5 keepers: cite Tribesman, not Snake Man - generator.
- E.9 watch: two bound men and a snake man, as the seed says - generator.
- HA/HB shaft Entry: drop "up the stair" from `refused`; make the chain or the rope one thing - generator.
- Rename one of Kunotewa / Kunotiwa and record it in Language.md - generator.
- Add a rumour that points at the cult or the bound men, and place Tuuzesh's pass-phrase where a party can hear it - generator (4d), template.

## Owed to a tool
- Two location codes joined by a Way whose distance contradicts a "drops to" or "above" in either write-up - tools/space.py
- A Bestiary cite whose entry differs from the faction's first Field for a `member` (bound men as Snake Man) - tools/validate_setting.py
- Two coined names within one letter of each other - tools/validate_setting.py
- A Named Creature, Lore or Unique Treasure whose location's seed places it elsewhere - tools/validate_setting.py
- A Key whose Feature names a container in a location other than its Lock's `to` - tools/validate_setting.py

## Resolved since
- Dinosaurs stay Encounters: a hazard is triggered by an action, and a dinosaur's numbers make it one to avoid.
- The step 4 loop exited (Checked: trailers on the unchanged write-ups and briefs); the Wall Ridge text, the crown, the galleon's lock, HB.5, E.9, the shaft and the Kunotiwa name are fixed.
