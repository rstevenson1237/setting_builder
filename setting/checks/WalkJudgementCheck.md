# Walk Judgement Check - 2026-11-22, the island build after #127, walked before the step 4 loop exited

## Routes
1. A.2, A.7, A.10, A.1, D.12, D.11, E.1, E.9, HA.1, HA.10, HB.1, HB.4, HB.5, HB.8, HB.13, HC.1, HC.2, HC.6, HC.7
2. A.2, A.4, A.3, B.1, B.9, B.5, D.1, D.10, F.1, F.9, F.10
3. A.2, A.1, C.1, C.4, C.9, I.1, I.4, I.7, C.10, D.2, D.6, J.1, J.4, J.7

## Findings
- A.1 - One place: the gate's exit "an uphill trail -> D.12" lands on a ridge "above the great wall" that is 13 miles away, so a party at the ridge cannot see the gate it was told it overlooks - map, table line - 3b/4a
- A.1 - A next step: a party turned back at night "is shut outside, where Kunotewa comes", but nothing says what happens when it meets a 10d6+2 creature at the bowls, whether it can hide or give food - write-up - 4b
- D.11 - What a party needs: the guide turns back and the party goes on alone. Nothing at D.11 or E.1 says how a party without a guide finds the road (a Lost test applies, but E's Ruling counts it only "off the roads") - seed - 3c
- HB.1 - One place: the map draws stairs up where the text says the rope is the only way. A party fleeing up "the stair" (the shaft Entry's `refused`) has none - map, seed - 3c/3e
- HB.5 - Nothing invented: the keepers are "bound men" cited as Snake Man, so the referee must decide whether to run men or snake men - table line - 4a
- HC.7 - One place: the crown lies behind the bier gate, while HC's seed has it under the god in HC.6. A referee reading the seed first places it wrongly - seed - 3c
- D.10 - A next step: the lost hunters' camp holds centipedes and a snapped bow. Nothing says what took the hunters or where to go next, so the quest and Rumour 5 stop here - Quests, table line - 4a/4d
- F.9 - What a party needs: Tiwahato wants "proof of what the cult feeds its god", but nothing says what counts as proof (a captive brought home, the Priests' Codex at HB.11, the frieze at HA.8) - Quests - 4d
- B.1 - A next step: the Stops run 0.8, 0.3, "at the way in", 1, 1.4 miles on a 9.5-mile way, so the walk from A.3 has no stop for its last 8 miles - table line - 3f/4a
- B.5 - A next step: the Egg Hummock has no Exits. A party carrying the egg-stone in reaches it by the region map alone, and the brief's Ways do not name the path - Connections - 3f
- I.4 - What a party needs: the key's lock is on the I.4 → I.7 door, while I.7 has a second bolted hatch "opened from the hold above". It is unclear whether the party needs the key twice or can open the hatch only from I.4 - table line - 4a
- I.4 - One place: the hold "floods to the second deck", but the map has no decks above it - map - 3e
- C.9 - One place: the island sheet marks the reef gap on dry sand inland - map - 3b
- J.7 - Nothing invented: Rank sells "a captive's ransom for 50 cn, each", but J.5 holds only cave men, so a referee must invent whose ransom the party is buying - table line - 4a

## Owed to a tool
- A Way between two locations whose distance contradicts "above" or "drops to" in either write-up - tools/space.py
- A WILD location with no Exits and no Stop naming it - tools/validate_setting.py
- A Quest with ask `verify` whose Object names no Feature a party can carry or show - tools/validate_setting.py
