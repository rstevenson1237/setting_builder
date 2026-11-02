# Template Judgement Check - 2026-11-02, The Buried City after step 4 (bab0daf)

Confirmed on every item: `templates/setting/Setting.md`, `templates/setting/History.md`, `templates/setting/Lore.md`, `templates/setting/Keys.md`, `templates/setting/Hoards.md`, `templates/setting/UniqueTreasures.md`, `templates/setting/MagicalTomes.md`, `templates/setting/NamedCreatures.md`, `templates/setting/Magic.md`, `templates/setting/Treasure.md`, `templates/setting/LocalProcedures.md`, `templates/region/Region_Gazetteer.md`, `templates/region/Locations.md`, `templates/region/Connections.md`

## Findings
- `templates/region/Brief.md` - Consistent with STEPS.md and the other templates: it never says the Danger table runs 6 to 1, as `setting/Procedures.md` and the schema do. All ten DANGEROUS briefs run 1 to 6, so every roll reads backwards.
- `templates/region/Brief.md` - Every field is used: it does not say to omit a list field that holds nothing. D to L print an empty "Entrances:" heading.
- `templates/region/Brief.md` - No context creep: Conditions are re-read from the seed and rewritten as prose. H's brief drifted to "8 wide" against the seed's width=10.
- `templates/region/Region.md` - Consistent with the other templates: nothing asks that an Entry from a joined region match that region's Entry for the same way. Seed H puts B.10's bronze door at the G.19 stair and calls the way up shut; seed B makes the same stair H's exit up. B.10 and H.1 then disagree.
- `templates/region/Region.md` - No context creep: it reads all of `setting/Bestiary.md` and `setting/Factions.md` for `who`, which takes their titles only; its own `field "Seed.who"` line is the fix.
- `templates/region/Region.md` - Consistent: "state only what this region changes" covers Conditions and View but not `Ruling`. Seeds A and B restated `setting/Procedures.md`'s 4/2/1 miles a watch in regions under a mile across.
- `templates/region/Tables.md` - No context creep: it reads all of Bestiary, Factions, History and Language besides its `field` lines (Bestiary 2,074 words, Factions 945).
- `templates/region/Tables.md` - One context, no step instructions: "An entry that will not fit its room is a finding for 5c" names a step. The rule stands without it ("is a finding, never moved or dropped").
- `templates/region/Location.md` - Format edge cases preserved: the cite list has no form for a faction's members, though the Instructions say they cite "their Bestiary entry, where they have one". The build cites `(Wary, 2, Faction : Kurumisa)` in seventeen Features and `Bestiary : Delver` for the same faction elsewhere (D.3 against F.10). `metrics.py` then reports Acolyte, Adept and Soldier as met nowhere.
- `templates/region/Location.md` - Format edge cases preserved: `**[Feature Name]:** [feature]` does not say the body leaves the name unrepeated. Thirty-five Features open by restating their label ("**The Chest:** A tool chest ..."), which `metrics.py` counts as glosses.
- `templates/region/Location.md` - Format edge cases preserved: the read-aloud `summary` names no voice. G.1, G.17 and K.3 address the players as "you", and the other 155 do not.
- `templates/region/Location.md` - Genre drift guardrails: nothing pushes against a Feature that is lasting magic. G.22's font heals a Wound per drinker every day, against `GENRE.md`'s "present but scarce".
- `templates/setting/Language.md` - Format edge cases: it does not say that every root, affix and coinage keeps to its tongue's own consonants, vowels and syllable. Both coined tongues break theirs (Cynidicean "mehe", "anuk"; Black Speech "ghul", "krul", "zhok").
- `templates/setting/Factions.md` - Every field is used: it does not ask for a common name for a tongue-named faction. `BRIEF.md`'s "the Royal Guard", "the Priesthood" and "the Scholars" leaked into briefs, rumours and quests beside the coinages, with no line joining them.
- `templates/setting/Quests.md` - Consistent with the schemas: "set in that Person's `quest`, in the region's `People.md`" holds only for SAFE. The B giver is unplaced. "Written from what that location holds" was not kept: Quest 1's clean water points at A.3's brackish sump, and Quest 4's heron mask is not at H.4.
- `templates/setting/Rumours.md` - Consistent with the schema: it never says what U means. Rumour 11 is marked U though L.4 settles it.
- `templates/setting/Truths.md` - Every field is used: a standing mystery "may be listed". Nothing makes it the home of an answer two files give differently, and four answers to what feeds the demon stand unreconciled.
- `templates/setting/Bestiary.md` - Genre drift guardrails / Every field is used: it does not say that Sight describes every creature of the kind. The Wraith's king's robe binds every wraith.
- `templates/setting/Procedures.md` - No defaults: it sets the exchange fee (3%), the resale fee (10-20%), the weather spread (1 severe, 2-3 poor, 4-6 calm), the carousing spread and "about eight lines". Each belongs in `BRIEF.md`'s `files` node.
- `templates/setting/Bestiary.md` - No defaults: "two or three sentences" for Description is a count the brief does not set.

## Open Items
- Brief.md: state that the Danger table's first row is band 6, that an empty list field is omitted, and draw Conditions from the seed instead of rewriting them. Source: template.
- Region.md: require an Entry from a joined region to match that region's Entry for the same way; replace the whole Bestiary and Factions reads with the `who` field line; extend "state only what this region changes" to Rulings. Source: template.
- Tables.md: trim reads to `field` lines; drop the "5c" reference. Source: template.
- Location.md: add a Faction cite form, or say members cite their `Fields` Bestiary entry; say a Feature's body does not repeat its name; name the read-aloud voice; add a guardrail against lasting magic in a Feature. Source: template.
- Language.md: every root, affix and coinage keeps to its tongue's inventory and syllable. Source: template; validator.
- Factions.md: a common name for a tongue-named faction (after the schema adds `gloss`). Source: template.
- Quests.md: where a giver stands outside SAFE; check the object against the location. Source: template.
- Rumours.md: define U. Source: template.
- Truths.md: an answer two files give differently is written here. Source: template.
- Bestiary.md: Sight is the kind's, never one creature's; move "two or three sentences" to `BRIEF.md`. Source: template.
- Procedures.md: move fees, the weather spread and the carousing spread to `BRIEF.md`. Source: template.
