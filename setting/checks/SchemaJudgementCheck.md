# Schema Judgement Check - 2026-11-02, The Buried City after step 4 (bab0daf)

Evidence: `setting/checks/SettingJudgementCheck.md` of the same date, and its findings traced
to a schema. Tables were read for A and B (WILD) and C to L (DANGEROUS). No SAFE region
exists, so `patterns/Safe_Schema.md` is judged from its text alone.

Confirmed on every item: `patterns/Safe_Schema.md`, judged from its text alone (no SAFE region was built)

## Across the schemas
- Gaps: Needs Attention -
  - `patterns/Region_Schema.md` `enum Terrain` has no underground ground. The lake cavern (B) was given `desert`, and its Rulings then copied the surface's "4 miles a watch" onto a 600-yard cavern.
  - `patterns/Wild_Schema.md` and `patterns/Dangerous_Schema.md` have no Person. A quest giver who is one named person outside a SAFE region has nowhere to stand: B's mask-seller is named by Quest 4 and absent from B.9. `templates/setting/Quests.md` assumes a `People.md` that only SAFE has.
  - `patterns/Common_Schema.md` `enum Wound_Type` has no type for thirst, exposure, drowning or suffocation, the killers `GENRE.md`'s Lethality names first. G.26 (drowning) and K.6 (breath pulled out) are written as Crushing.
- Unhoused content: Needs Attention -
  - `BRIEF.md` region H: "laid out in the shape of level 4". Neither a Block field nor the packer can take another block's plan.
  - The passwords at E.1 and J.1 sit in an Entry's free-text `takes`. `enum Key_Form` already has `word`, but an Entry cannot hold a Lock, so the validator never asks where the word is found. Both words went unwritten.
  - The fungus's effects (`GENRE.md`: "the one thing sold that works like magic") have no field. A Local Procedure's Results can name an outcome but not what a dose does, and WILD has no Purchase.
  - `BRIEF.md` B asks for "a city" that by Truth 3 has no authority. SAFE needs `Law="1+"`, so it became WILD, which is why the build has no SAFE region and misses the brief's `test`.
- No overlap or contradiction: Needs Attention - `patterns/Region_Schema.md` has every brief restate the seed's Conditions as prose (`field "Conditions" from="Conditions"`). H's restatement drifted (width 8 against the seed's 10). Conditions could be `drawn` like Inhabitants, and never written.
- Nothing contradicts STYLE.md: Confirmed.

## Findings by file
- `patterns/Region_Schema.md` `region Dangerous` `brief.Tables` - Enforceable: its comment "Danger, 6 noticing to 1 acting" was misread in all ten DANGEROUS briefs, which run 1 to 6. An order the validator can check is a rule not yet written: the first row of a Danger table is band 6.
- `patterns/Region_Schema.md` `brief.Entrances` (`holds=entrance`) - Specific: a region whose ways in all come from another DANGEROUS region holds no `entrance` location. D to L print an empty "Entrances:" heading. Say that an empty list field is not written.
- `patterns/Region_Schema.md` `enum Dangerous_Kind` - Specific: "single holding" (one occupant's home) was used for C, a six-room trap complex, and then fed a gazetteer tag of "One room". Its comment should say what it is not.
- `patterns/Setting_Schema.md` `table Factions` `Form` - Gap: a `tongue` faction has no common name, unlike `Region`'s `gloss`. The build names each branch only by its coinage, while every brief, rumour and quest calls them "the Royal Guard", "the Priesthood" and "the Scholars". A `gloss` field, shown wherever the faction is cited, closes it.
- `patterns/Setting_Schema.md` `table Bestiary` `Sight` - Specific: a per-kind field written for one creature binds every one. The Wraith's "king's robe ... crown" makes the queen's wraith (G.8) and the cult's unmade chosen (I.5) kings. Either Sight stays generic to the kind, or an Encounter carries a look of its own.
- `patterns/Setting_Schema.md` `table Rumours` `Truth_Mark` U - Enforceable: "U is the referee's by design" does not say a U is something the build does not settle. Rumour 11 is marked U and is settled at L.4. Write U as "nothing in the build confirms or denies it", and the validator can refuse a U whose "where a party would look" location holds a cited entry that answers it.
- `patterns/Setting_Schema.md` `table Language` `Syllable`, `Consonants`, `Vowels` - Enforceable: the build's roots break their own tongue's inventory (Cynidicean "mehe", "anuk"; Black Speech "ghul", "zhok"). The inventory is a closed set, so each root and each coinage can be checked against it.
- `patterns/Setting_Schema.md` `table Truths` - Gap: nothing makes two files' answers to one question meet. What feeds the demon has four answers (L's seed, Lore: The Demon's Breath, Lore: The Making of the Chosen, H.7 with Rumour 4), and Truths holds none. A Truth row, or a Lore entry flagged as the referee's answer, is where it belongs.
- `patterns/Wild_Schema.md` `node Seed` `terrain` - Specific: it feeds `Ruling`, which then restated `setting/Procedures.md`'s watch rates unchanged in a region a watch's walk could cross many times. A Ruling should state only what this ground changes.
- `patterns/Dangerous_Schema.md` `node Encounter` `Faction` - Enforceable: E.3's Faction node says `present=6` while its write-up says forty soldiers in sixes. A faction's total belongs to its `Resources`, and the Encounter's prose should not restate it.
- `patterns/Common_Schema.md` `enum Wound_Type` - Gap: as above; thirst and air.

## Open Items
- Add an underground value to `enum Terrain`, or a WILD `kind` for a cavern. Source: enum.
- Add a Person node, or allow `Person` in WILD and DANGEROUS, so a quest giver can be placed outside SAFE. Source: gap.
- Add Wound types (or a Procedures rule) for thirst, exposure and air. Source: enum, gap.
- Let an Entry hold a Lock, so a password is a Key with `form=word` and a Found at. Source: gap.
- Make `brief.Conditions` drawn, not written. Source: field.
- Write the Danger order as a rule the validator checks: first row band 6. Source: comment; range.
- Say that an empty list field (Entrances) is not written. Source: comment.
- Tighten the `Dangerous_Kind` comment: "single holding" is one occupant's home, never a complex. Source: comment.
- Add `gloss` to Factions for a tongue-named faction. Source: field.
- Keep Bestiary `Sight` to the kind, or give an Encounter a look of its own. Source: comment, field.
- Define Rumour U as unsettled by the build, and have the validator check it. Source: comment; validator.
- Check roots and coinages against their tongue's inventory in `tools/validate_setting.py`. Source: range; validator.
- Give a question two files answer differently a home in Truths. Source: gap.
- Decide where a level's plan copied from another goes (BRIEF H), or drop it from the brief. Source: gap.
- A lawless city: let SAFE take `Law` as none, or say in the brief that such a city is WILD. Source: gap.
