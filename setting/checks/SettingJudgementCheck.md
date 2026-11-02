# Setting Judgement Check - 2026-11-02, The Buried City after step 4 (bab0daf)

Run against the build as it stands. The validator reports 0 errors and 0 warnings, but
`--pending` still owes 39 stale write-ups (all of A and B, and some in F to L) and the
briefs of A and B, so the step 4 loop has not fully exited. Findings below are against
that text.

## Setting-level
- The brief was delivered: Needs Attention -
  - `test` "every location type, procedure kind and registry the framework has is used at least once": not delivered. No region is SAFE, so the Inn, Merchant, Bank, Market, Authority and Gate types, People, Purchases and Garrisons are never used. Registries and the three procedure kinds are all used. Source: `BRIEF.md` (its regions ask for no SAFE rating while its test asks for every type).
  - `outline`, `history`, `truth`, `tongue`, `bestiary`, `bestiary-note`, `relations`, `rumours`: delivered. The levels widen and then narrow by location count (6, 12, 15, 20, 29, then 20, 14, 9, 8, 6), and every rumour subject is covered.
  - `pressure`: food, water and respite delivered (A.3, A.9, A.7's skins, A.2, Joining a faction). Source of the gap below: `BRIEF.md`.
  - `procedures` "a party that has none loses Wounds to thirst and exposure": no Wound type carries it. A's Rung asks a Test of Constitution against thirst with no type, and drowning and suffocation are written as Crushing (G.26, K.6). Source: `BRIEF.md`'s `wounds` line names four types, none for thirst, exposure or air.
  - `faction` the Priesthood, "the former female-led clergy": thin. Only G.3 and E.11 show priestesses; the Acolyte entry is "a man or woman" and Factions never says who leads. Source: generator.
  - `quest` "water for a party's first camp": written inverted, as water *for* the Guard, and pointed at A.3's sump, which A.3, Rumour 6 and the foraging table all say is brackish. Source: generator; `templates/setting/Quests.md` asks for the object to be written from what the location holds.
  - `quest` "a mask-seller's request": the giver stands in B.9, a loft that holds only rats. The heron mask the object wears is not in H.4. Source: schema (no Person outside SAFE), generator.
  - Region C: its gazetteer tag says "One room" and its seed kind is "single holding" ("one occupant's home"), while the brief and the build have a six-room trap complex. Source: generator; `Dangerous_Kind` comment.
  - Region D "four areas joined by winding passages": the areas are delivered (robbers D.1/D.3/D.7, founders D.2/D.8/D.9, scraped D.4/D.10/D.11, gallery D.5/D.6/D.12), but the map has no passages; every room shares a wall. Source: `tools/dungeon.py` pack.
  - Region E "eight passages on opposite sides": the runes pair E.3 with E.5 as opposite arches, but the map puts them north-west and south-west. Source: `tools/dungeon.py` pack, which has no way to hold a round room's arches opposite.
  - Region F "strange cynidicean encounters" and "stronger monsters": not delivered. F holds no cynidicean encounter besides Kurumisa sentries, and its sand-borne lairs (hyena AD 1d6, spider, scorpion) are no stronger than level 1's. Source: generator.
  - Region G "at its centre a great chapel": G.22 is placed south-east of centre. Source: `tools/dungeon.py` pack.
  - Region H "laid out in the shape of level 4": the write-ups echo F (H.7 "the old feast hall" like F.7), but the map does not. Source: unhoused - nothing in the schema or packer can copy a level's plan.
  - Region H "the way up is behind a party": written as "a stair that has no way back up", which contradicts H.1's own exit up to B.10. Source: generator (`templates/region/Region.md`).
  - Region L "a single hall": six rooms. Source: generator.
- Genre held across levels: Needs Attention -
  - Reference, Authority, Allegiance, Population, Decay, Reward: held.
  - Lethality: held - Giant Scorpion is save-or-die, and each DANGEROUS level has a Lethal hazard except J and K. Thirst has no rule that kills (see above).
  - Magic level: mostly held. Magic items are found, never bought. But G.22's font heals one Wound per drinker every day for as long as the bowl is lit, a standing healing source the reference does not have. And the fungus, "the one thing sold that works like magic", has no written effect: B.3 and Trading for the fungus say the stallholder "names what it does", and nothing names it. Source: generator.
  - Naming: the places the party names are common. But the pyramid's levels, which `GENRE.md` gives coined names, are all common ("Pyramid Level 2 - The Halls of History"). The faction coinages are the only names the files use for the factions, while every brief, rumour and quest says "the Royal Guard", "the Priesthood" and "the Scholars". Source: generator; schema (no common name for a faction).
- The tests, hardest at the top: Needs Attention - seeds K and L's `comes` tell the party why it comes ("to prepare for the last hall", "to end it"). Seed H's `refused` ("None; the way back is the way in"), and K and L's "None.", carry nothing a referee can run. Seed I's Entry comes "from the first level" (it is the sixth). Seed B's terrain is "desert" for a lake cavern.
- Discrete and discoverable, not vague: Needs Attention - mostly concrete. "Costs the mind" (H.9, K.5) and "unleashes the mind's dread" (H.11) name no effect beyond the Test they cite.
- Every secret has its answer: Needs Attention -
  - What feeds the demon has four answers, and no Truth picks one: the cynidiceans' dead (seed L, L.3, Ghulox's Wants), what was left in the tombs (Lore: The Demon's Breath), the blood of the unmade (Lore: The Making of the Chosen, I.8), and living captives (H.7, Rumour 4 marked T, The Cult's Ledger). Quest 5's `misdescribed` obstacle needs the true answer written somewhere.
  - What the king's keys open for the cult. Voxkroth wants them "to open what the demon wants opened", and The Demon's Breath says they "wake it". In the build they open only G.10 and the G.19 arch, and nothing below level 5 needs them.
  - The word at E.1 ("a word in the cynidicean speech") and the lieutenants' word at J.1 are never written. Xothox knows the second.
  - The captain's fate, and "the thing at the foot of the stair" that eats the Guard's scouts (seed F, Lore: The Captain's Last Orders). No location holds either.
  - What shuts the stair behind a party at H.1, and at F.1 ("or find the stair shut").
  - A.6's sealed door onto solid rock, its sun-disc chiselled out: no answer, and not marked as an open question in Truths.
- Nothing contradicts: Needs Attention -
  - H: seed and H.1 say the way up is shut, but H.1 exits up a stair to B.10. Seed H puts "a bronze door unbarred from below" at the head of the G.19 stair; that door is B.10's, and G.19 is an arch with a bone lock-plate.
  - B.10 stands at z -63 in `space.py`, 50 feet above the lake-city floor and above level 4. It is "behind the granary wall" (B.5) with no climb on that way. `space.py` does not flag it.
  - B.5 puts the carved face in the east wall; B's brief puts it in the west. B.9 adds a second pressable mask.
  - A.5's wall is "twice a man's height" and "50 feet high at its tallest point".
  - A.8 runs "a mile and a half", but its stops end at 110 yards. Its head is "20 yards east of the way in" on a canal said to run west.
  - A.2 opens A.9 by pulling the hearth's back plate; A.9 is reached "under a lifted flagstone".
  - C.1 lies "15 feet below the statues", and its stair up "is 20 feet".
  - C.3 has faces scraped on the last six panels; its Lore says panels five to eleven are too worn to read.
  - D.6 says "each king's face blacked out"; The Gallery of the Fall blacks out only the guest's.
  - E.3: "forty soldiers", "six sixes" and a count of 6, beside 36 berths in E.10.
  - The Three Claims puts the Guard east, the Priesthood north and the Scholars west. The map has E.3 north-west, E.4 north-east and E.5 south-west.
  - F.7's spiders "guard the way to the gallery stair", but F.7 does not adjoin F.13. F.10 has "barricades across two doors" and one door.
  - G.6 has "four tomb doors" in its summary and five in its Feature.
  - G.8's wraith is the queen's, while the Wraith's Sight is "a figure in a king's robe ... under its crown", as are I.5's unmade chosen and every other wraith.
  - H's brief gives "14 feet high and 8 wide"; the seed's Conditions say width=10.
  - K.2 and K.3 call the air "thin" and "airless"; the seed and K.3's own Feature call it "thick and hard to breathe".
  - Rumour 11 is marked U ("a party would look at L.4"), yet L.4 holds the Binding Chain that does what it says. It is T.
  - Cultist's Range is "below the sixth level"; the cult holds the sixth.
  - The Queen's Last Rite says the king "went down to the veiled guest of his own will", while G.7 entombs him. If the K.1 wraith in a king's robe is meant to be him, nothing says so.
  - All ten DANGEROUS briefs order their Danger table 1 quiet to 6 acting. `setting/Procedures.md`'s bands and the schema run 6 (warnings) down to 1 (forced encounter), so every roll reads backwards. Source: `templates/region/Brief.md`; the schema comment alone did not hold it.
- Everything recurs, nothing is orphaned: Needs Attention - every registry entry is placed. Acolyte, Adept and Soldier show as orphaned in `metrics.py` only because write-ups cite their faction (`Faction : Ruhiahe`) instead of the Bestiary entry `templates/region/Location.md` asks for. Seed B's `who` omits the Masked Dreamer, who holds the city. Seed F offers the lost captain and no location places him.
- Vocabulary precise, not decorative: Needs Attention - "thin air" is a misuse in K, as above. A "reliquary" (E.2) holding "a casket of offerings" is a misuse; it holds relics. "Carved carvers" (D.12) is a stumble. The 35 `gloss` tells are not glosses: they are Feature labels repeated in the body ("**The Chest:** A tool chest ..."), which is the "said once" failure. No archaic decoration found.

## Region A
- Region reinforces the setting: Confirmed - the gridded streets, the statues and the robbers all trace to History and Factions.
- Locations reinforce this region: Confirmed.
- Entries match: Needs Attention - all nine write-ups are stale (`--pending`); their Ground `At` and Block entries changed since. Source: step 4b owed.
- Prices fit the list: Confirmed - no Purchases.
- One room: Confirmed.
- Distinct: Needs Attention - "A rope coil and notches" is A.1's Mark, A.7's Mark and C.4's Mark in the same frame. Source: generator.
- Said once: Needs Attention - A.5, A.8 and A.2/A.9 contradict themselves (see above).
- The tests, at the location: Confirmed.

## Region B
- Region reinforces the setting: Confirmed - Truth 3 is visible in B.2, B.4 and B.6.
- Locations reinforce this region: Confirmed.
- Entries match: Needs Attention - all ten write-ups and the brief are stale. Source: steps 4b and 4e owed.
- Prices fit the list: Needs Attention - the fungus is 10 cn a dose in the local procedure and absent from Coin and Prices, which is allowed; but nothing says what a dose buys. Source: generator.
- One room: Confirmed.
- Distinct: Confirmed.
- Said once: Needs Attention - B.10's bar ("unbarred from below", "barred from the lake city's side", "the dreamers bar it from above") is said three ways in one write-up.
- The tests, at the location: Needs Attention - B.9's "the sellers say" names sellers who are not there.

## Region C
- Region reinforces the setting: Confirmed.
- Locations reinforce this region: Confirmed - every room is a puzzle, a trap or a clue.
- Entries match: Confirmed.
- Prices fit the list: Confirmed - no Purchases.
- One room: Confirmed.
- Distinct: Confirmed.
- Said once: Confirmed.
- The tests, at the location: Needs Attention - C.4's "The Scholars know which way": no Scholar is reachable on level 1, so a party cannot act on it here. Source: generator.

## Region D
- Region reinforces the setting: Confirmed - the strongest level for History.
- Locations reinforce this region: Confirmed.
- Entries match: Confirmed.
- Prices fit the list: Confirmed.
- One room: Confirmed.
- Distinct: Needs Attention - D.8, D.11 and D.12 each end on who knows the trick ("The tomb robbers step over it", "... know the trick", "the Scholars know it"), as do C.3, C.4, C.5, E.9, F.17, G.24 and G.28. Source: the generator writes `knows` as a closing sentence.
- Said once: Confirmed.
- The tests, at the location: Needs Attention - D.3's "a winding passage leads off" describes a passage the map does not draw.

## Region E
- Region reinforces the setting: Confirmed - Truth 2 is plain in E.3 to E.5.
- Locations reinforce this region: Needs Attention - E.3's Hostile skeletons stand guard at the Guard's own banner, and E.6's at the Guard's own armoury, with no reason given. Source: generator.
- Entries match: Confirmed.
- Prices fit the list: Confirmed.
- One room: Confirmed.
- Distinct: Confirmed.
- Said once: Needs Attention - E.3's soldier counts (see above).
- The tests, at the location: Confirmed.

## Region F
- Region reinforces the setting: Confirmed.
- Locations reinforce this region: Needs Attention - no strange cynidicean encounter (brief).
- Entries match: Needs Attention - F.2, F.4, F.11, F.12 and F.13 are stale.
- Prices fit the list: Confirmed.
- One room: Confirmed.
- Distinct: Confirmed.
- Said once: Needs Attention - F.3 says its ovens line the wall twice in the read-aloud. F.4's "Passage" Feature restates its exits.
- The tests, at the location: Needs Attention - F.9's "The Kurumisa captain's trail leads here" and F.11's "his men moved after him" assert a trail no Feature shows.

## Region G
- Region reinforces the setting: Confirmed.
- Locations reinforce this region: Confirmed.
- Entries match: Needs Attention - G.1 and G.19 are stale.
- Prices fit the list: Confirmed.
- One room: Confirmed.
- Distinct: Confirmed.
- Said once: Needs Attention - the side door is described in G.14, G.20 and G.21, and the brief's Entrance puts it at G.14's top.
- The tests, at the location: Needs Attention - G.1 and G.17 are written in the second person ("Your breath", "as you enter"); every other write-up is in the third. G.6's "Touching the first turns them all toward the true tomb" hands over the false-tomb puzzle with no cost.

## Region H
- Region reinforces the setting: Confirmed.
- Locations reinforce this region: Confirmed.
- Entries match: Needs Attention - H.1, H.5, H.11 and H.12 are stale. H.4 cites `Faction : Voxkroth` for the captives, who are not the cult.
- Prices fit the list: Confirmed.
- One room: Confirmed.
- Distinct: Confirmed.
- Said once: Confirmed.
- The tests, at the location: Needs Attention - H.1 (see Nothing contradicts).

## Region I
- Region reinforces the setting: Confirmed.
- Locations reinforce this region: Confirmed.
- Entries match: Needs Attention - I.2, I.4 and I.8 are stale. I.1 carries I.14's dart trap.
- Prices fit the list: Confirmed.
- One room: Confirmed.
- Distinct: Needs Attention - "the unmade" are zombies in I.3 and wraiths in I.5.
- Said once: Confirmed.
- The tests, at the location: Confirmed.

## Region J
- Region reinforces the setting: Confirmed.
- Locations reinforce this region: Confirmed - three lieutenants who can be played against each other, and J.8 lets a party overhear them.
- Entries match: Needs Attention - J.6 is stale.
- Prices fit the list: Confirmed.
- One room: Confirmed.
- Distinct: Confirmed.
- Said once: Confirmed.
- The tests, at the location: Needs Attention - the lieutenants' word (see secrets).

## Region K
- Region reinforces the setting: Confirmed.
- Locations reinforce this region: Confirmed.
- Entries match: Needs Attention - K.1 and K.5 are stale.
- Prices fit the list: Confirmed.
- One room: Confirmed.
- Distinct: Confirmed.
- Said once: Confirmed.
- The tests, at the location: Needs Attention - K.3 is in the second person ("your own heartbeat"), and K.2/K.3 use "thin air".

## Region L
- Region reinforces the setting: Confirmed.
- Locations reinforce this region: Needs Attention - six rooms where the brief asks for one hall.
- Entries match: Needs Attention - L.4 is stale.
- Prices fit the list: Confirmed.
- One room: Confirmed.
- Distinct: Confirmed.
- Said once: Confirmed.
- The tests, at the location: Confirmed.

## Room to Grow
- Truth 4's Handle, "cut off what feeds it", is backed only by L's Rung. No location shows a feeding line a party could break: no channel, cart or chute from H.7 or I.8 that is named as reaching L.
- The Ruhiahe Goal "Find the ritual lost with the last queen" - G.8 holds the queen's Lore and L.3 the sealing words, but nothing ties either to the Priesthood's ask. A Ruhiahe person or Lore line at G.8 could carry it.
- The tomb robbers trade with the cult for the keys (Voxkroth's Tactics), but no robber appears below level 4. A go-between at H.10 or a note at F.10 would show it.
- The masked captives (H.4, H.19) and the Kinsman quest: the heron mask could be placed at H.4 or H.19.
- Named Creatures are met only in their own rooms. Krulox, Xothox and Zhurjul could each be heard of above level 8 (I.2's guards, The Cult's Ledger).
- Coinage: the Cynidicean Speech is declared CVCV with vowels a, i, u, aa, yet its roots include "mehe", "ahet" and "anuk", and Ruhiahe has an e. The Black Speech's consonants omit l and k, yet its roots include "ghul", "krul" and "zhok". The validator checks that coinages are recorded, not that they obey their tongue.

## Open Items
- Finish step 4: 39 stale write-ups and briefs A and B (`--pending`). Source: generator (4b, 4e owed).
- Write one answer to what feeds the demon, as a Truth or a Lore line, and bring L, I.8, H.7, Ghulox and Rumour 4 into line. Source: generator; `templates/setting/Truths.md`.
- Reconcile H.1, seed H, seed B and B.10: one bronze door, on the B side, with the G.19 stair as a plain way down. Source: generator; `templates/region/Region.md`.
- Reverse the Danger tables in all ten DANGEROUS briefs to run 6 to 1. Source: `templates/region/Brief.md`.
- Write the E.1 and J.1 words, the captain's fate, the fungus's effects and what shuts the H.1 stair. Source: generator.
- Fix the factual contradictions listed under Nothing contradicts. Source: generator.
- Re-mark Rumour 11 as T, and point Quest 1 at clean water. Source: generator; `templates/setting/Rumours.md`.
- Give thirst, exposure and air a Wound type or a rule. Source: `BRIEF.md`; schema.
- Place the mask-seller and the heron mask, and give F a cynidicean encounter. Source: schema; generator.
- Ask for a SAFE region or drop the "every location type" test line. Source: `BRIEF.md`.
