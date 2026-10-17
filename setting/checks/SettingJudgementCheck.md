# Setting Judgement Check - 2026-10-17, after review pass 1 (regions A to M complete, briefs written)

Recorded against the content as generated. Nothing below was fixed in this pass; each Needs Attention names its source and is carried to Open Items.

## Setting-level
- The brief was delivered: Needs Attention. Delivered: the outline, pressure and test (keep, wood, mere, ravine of six lairs and a maze, shrine; half a day out by the 12-mile trail, three watches); four History events, four Truths, four tongues, the eleven up-front Bestiary entries, eleven Factions with the Relations `BRIEF.md` names, twelve Rumours at T4 P3 F3 U2, five Quests, every registry used, all three procedure kinds, all seven SAFE, seven WILD and three DANGEROUS location types, a Test of Sanity at M.11 only, and Lethal Poison at F.5. Not delivered or short: (1) Rumours "one at each tribe" - none is about the bugbears; Rumour 7 and 8 reach them only through the tithe and the stones (source: `BRIEF.md` line, and Rumours template leaving coverage unchecked); (2) `dangerous target Reward.contents Keys="10%"` - 3 of 42 rewards, 7% (source: `BRIEF.md` target against a rate that gives a region at most two keys); (3) `target Hazard.damage Lethal="20%"` - 1 of 8 hazards, 12% (source: `BRIEF.md` Challenges rate, which yields too few hazards to hit a 40/40/20 split); (4) "No two tribes' creatures share both an AD and a Special" holds for Bestiary and Named Creatures.
- Genre held across levels: Confirmed with one note. Magic level: the Magic table and Treasure tables hold scrolls, potions and a few lasting items; the three Unique Treasures-class finds are one reliquary, one lamp and one tome, and a Named Creature (Veck) raises the dead. The Black Psalter teaches a PC to raise a Zombie daily - more than the "spell or two a day" the reference's casters hold, and the only item that hands a party Chaos's own tool (source: generator; `Setting_Schema` Magical Tomes `Teaches` is free text). Lethality: 1 Lethal hazard, Poison save-or-die at F.5, Hold effects on two Named Creatures. Reward: hoards 590 to 4,300 cn, all sold at A.7. Naming: tribes and the shrine carry coined names; every Named Creature is an epithet in the common tongue.
- The tests, hardest at the top: Confirmed. Setting.md, History.md, Truths.md and all thirteen seeds and briefs pass line by line; the one repeated phrase is "A party comes for ..." closing most Overviews, which is the seed field's shape.
- Discrete and discoverable, not vague: Confirmed. Each region's secrets in its Brief name a trigger and a tell; the shrine's secrets (hanging, niche, carved hand, bowl, runes, rime) are each findable.
- Every secret has its answer: Needs Attention. Rumours 8 (the stones answer) and 12 (the mere calls the drowned) are `U` and settle at "none"; `setting/Truths.md` holds no mystery or open gap to say they are held on purpose, and D.3's dead men and C.5's hum carry no cause in any entry (source: `Setting_Schema` - "U is the referee's by design" with no home in Truths; Truths template allows a mystery entry but does not require one).
- Nothing contradicts: Needs Attention. (1) The Kurzun: Bestiary "a pack holds a dozen", Faction "a dozen gnolls"; the rooms hold 3 at E.6, 3 at J.1, 2 at J.2, 6 at J.5 and Ruk, 15 (source: generator - no field ties a Faction's headcount to the sum of its Encounters). (2) The Zurnaz: "six to ten bugbears"; E.7 2, K.1 2, K.3 3, Mort 1 and C.5 3, 11 (same source). (3) The Gubak: "thirty or so"; the rooms hold 26. (4) The Burgnaz, Rokmok and Black Altar sums match their Resources lines. (5) The G.5 and H.5 secret passage is "west" from G.5 and "south" from H.5 (source: `Dangerous_Schema` - `orientation` is stated once per side with nothing checking the pair).
- Everything recurs, nothing is orphaned: Confirmed with notes. Every Bestiary entry, Faction, Named Creature, Lore, Key, Unique Treasure, Tome, Hoard and coined name is met in a location (checked by search; each is cited at least twice across the setting). Thin: Owlbear (E.10 only), The Carters' Guild and The Sellaca outside A, B, D; The Road Bounty's "black clay tally-disc" appears in no goblin room (source: Quests row against G rooms, generator).
- Vocabulary precise, not decorative: Confirmed. Terms in use (ossuary, refectory, censer, brazier, torc, sump, rime, psalter, antechamber, lintel, hasp) are applied to what they name; the validator's gloss tell reads 0. No misuse found.

## Region A
- Region reinforces the setting: Confirmed - Truth 4 and the Black Altar's agents are delivered at A.1, A.4, A.12.
- Locations reinforce this region: Confirmed.

## Region B
- Region reinforces the setting: Confirmed - the lost wagons and The Zhakuk's raids.
- Locations reinforce this region: Confirmed.

## Region C
- Region reinforces the setting: Confirmed - Zurnaz tithe path and the stones.
- Locations reinforce this region: Confirmed.

## Region D
- Region reinforces the setting: Confirmed - the makers' drowned shrine; the dead are unexplained (see Every secret has its answer).
- Locations reinforce this region: Confirmed.

## Region E
- Region reinforces the setting: Confirmed - six ledges, the tithe niche, History 1 and 4 marks.
- Locations reinforce this region: Confirmed.

## Region F
- Region reinforces the setting: Confirmed - tribute to the goblins, the first door.
- Locations reinforce this region: Confirmed.

## Region G
- Region reinforces the setting: Confirmed - the waybill and the secret passage (Truth 2).
- Locations reinforce this region: Confirmed.

## Region H
- Region reinforces the setting: Confirmed - the feud with the goblins, the passage, the captains' pressure.
- Locations reinforce this region: Needs Attention - H.3's tag "loud" is carried only by the notes; minor (source: Dressing has no field for sound, generator).

## Region I
- Region reinforces the setting: Confirmed - the Burgnaz's key and the grate (Truth 2).
- Locations reinforce this region: Needs Attention - I.4's tag "locked" is a barred door with no lock (source: `tag` is free text, `Dangerous_Schema` Location.tags).

## Region J
- Region reinforces the setting: Confirmed - captives, the buyer's tally, the heap (Truth 2).
- Locations reinforce this region: Confirmed.

## Region K
- Region reinforces the setting: Confirmed - tithe, back stair, sticks (Truth 3).
- Locations reinforce this region: Confirmed.

## Region L
- Region reinforces the setting: Confirmed - makers' passages, the keeper's charge, the vault key.
- Locations reinforce this region: Confirmed.

## Region M
- Region reinforces the setting: Confirmed - History 2 and 4, Truths 2, 3 and 4, and both Black Altar agents' letter.
- Locations reinforce this region: Needs Attention - M.14's tag "listening" has nothing in the room that listens (source: `tag`, as above).

## Room to Grow
- Rumours coverage of the bugbears, and a Rumour whose Settled at is K - the BRIEF line "one at each tribe" has no K row; Rumour 7 settles at K.2 but speaks of all tribes.
- Rumours 8 and 12 - the cause of the stones' hum and of the standing dead is not in any entry; hold on purpose in Truths, or settle at C.5/D.3.
- The Road Bounty - black clay tally-discs: no goblin room carries one (G.2, G.5, G.6, E.3 could).
- The Makers' Tongue - 18 roots recorded, one coinage (Thalosae); makers' names for the ravine's works, the sanctum or the keeper have not been coined. Candidate: the Vault Key's maker and the lamp.
- The Cant - one coinage (Sellaca), none in a person's or place's name.
- The Owlbear - E.10 only; its rim could carry a sign elsewhere on the east wall.
- J.2's nine captives - carried by Dressing and a Feature with no entry; Kerrin Torren and the four are the referee's.
- Coined-sounding words in prose: none found outside the recorded tongues.

## Open Items
- Fix Kurzun, Zurnaz and Gubak headcounts in the rooms (J.1, J.5; K or C.5; F) - source: generator; and consider a Faction headcount field or metric (`Setting_Schema`).
- Reconcile G.5/H.5 orientation, and check every paired orientation - source: `Dangerous_Schema` Connection.orientation.
- Write Truths entries for the stones and the drowned (open on purpose) or settle Rumours 8 and 12 - source: `Setting_Schema` Rumours `U` / Truths.
- Add a bugbear Rumour or relabel the BRIEF line - source: `BRIEF.md`.
- Raise Keys and Lethal shares or lower the targets - source: `BRIEF.md`.
- Carry the tally-disc in the goblin rooms - source: generator (5a).
- Retag I.4 and M.14 - source: generator (5a/5b).
- Decide on the Black Psalter - source: generator.
