# Schema Judgement Check - 2026-10-17

Evidence: the Setting Judgement Check of the same date; its findings traced to a schema; the table files and write-ups of F (DANGEROUS, 5 rooms), E and C (WILD) and A (SAFE); and review pass 1's two framework items (the captives with no entry, the one-sided Secret).

Confirmed on every item: patterns/Common_Schema.md, patterns/Safe_Schema.md, patterns/Region_Schema.md.

## Across the schemas
- No overlap or contradiction: Needs Attention - `Wild_Schema` Mystery (`act`, `tell`) and `Dangerous_Schema` Mystery (`one-of Secret` with `trigger`, `tell`) hold the same fact in two shapes; and `Secret` means "the way into a Secret location" in Wild and "what sets off or opens the thing" in Dangerous, under one name.
- Nothing contradicts STYLE.md: Confirmed.
- Gaps: Needs Attention - (1) no DANGEROUS node produces a captive, hireling or prisoner, though a Quest's `Obstacle` may be `living`; (2) no field ties a Faction's stated strength to the Encounters that place it, so three headcounts drifted; (3) nothing checks that a connection's two `orientation` glosses agree.
- Unhoused content: Needs Attention - a `U` Rumour (referee's by design) has no schema home for its answer or for being held open on purpose.

## Findings by file
- patterns/Dangerous_Schema.md Connection.orientation - Specific: stated once per side, so a pair can disagree; G.5 reads "west" and H.5 "south".
- patterns/Dangerous_Schema.md Connection / Secret - Discoverable: a Secret is carried on one side only, so the far side's `Exits` reads as plain and the validator warns on all nine; the schema does not say the far side of a hidden way is open.
- patterns/Dangerous_Schema.md Encounter.left, far - Interactive: written for every encounter, carried by no write-up, brief or step; only the site's table pages show them.
- patterns/Dangerous_Schema.md Location.tags - Enforceable: three free tags are judged against the room by eye (I.4 "locked", M.14 "listening" have nothing under them).
- patterns/Dangerous_Schema.md - Gap: no node for people held in a room (J.2).
- patterns/Setting_Schema.md Factions - Enforceable: `Resources` states a roster in prose (Kurzun "a dozen", Zurnaz "six to ten"); no number field.
- patterns/Setting_Schema.md Factions AD and Relations dice, Tactics - Interactive: nothing in `setting/Procedures.md` sets factions against one another, so AD and the d12-d4 dice are read by no one, and the template's "Faction Turn" has no procedure.
- patterns/Setting_Schema.md Rumours `U` - Unhoused: no pairing with Truths.
- patterns/Setting_Schema.md Magical Tomes Teaches - Specific: free text allowed the Black Psalter, a daily Zombie, against GENRE.md's magic level.
- patterns/Wild_Schema.md Mystery.act - Specific: "what sets it off" is a gloss, where Dangerous uses a Secret the referee can run.

## Open Items
- Make `Mystery` one shape across ratings, and name the two senses of `Secret` - source: Wild_Schema, Dangerous_Schema.
- Add an optional DANGEROUS node or Encounter variant for held people, or say the Quest's object is the referee's - source: gap (Dangerous_Schema).
- Add a Faction `Strength` number (or a metric summing Encounter counts per Faction) - source: Setting_Schema Factions.
- Add an orientation-pair check, or state orientation once - source: Dangerous_Schema Connection.
- State that the far side of a Secret is open, or carry the Secret on both - source: Dangerous_Schema.
- Read `left` and `far` into the Location template or cut them - source: Dangerous_Schema Encounter.
- Give Factions AD and Relations dice a procedure, or cut them - source: Setting_Schema Factions, Procedures.
- Give a `U` Rumour a Truths pairing - source: Setting_Schema Rumours.
