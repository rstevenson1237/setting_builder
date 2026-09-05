# Pattern Judgement Check

Cleared. The 2026-09-04 pass's findings are resolved or superseded as of this commit:
`patterns/safe/Settlement.md`'s inclusion spec, and naming the Puzzle relationship (moot -
`templates/Location.md` no longer has a Puzzles bullet) were already fixed in an earlier
session. This commit closes the rest: the wild/Ruin.md cross-reference to a nonexistent
`patterns/dangerous/Faction.md` (the file now exists at `patterns/wild/Faction.md`), the
"a key that opens nothing is treasure" criterion restated four times (kept once, in
`patterns/setting/Keys.md`), and the three `Naming.md` files hardcoding a prior setting's
actual tongue names. The five-missing-SAFE-element-files item is treated as superseded by
redesign - `templates/Location.md` no longer asks SAFE for `Trap.md`/`Creature.md`/
`Treasure.md`/`Mystery.md`, folding those concerns into `Situation.md`/`People.md`/
`Commerce.md`/`Authority.md` instead - rather than reopened as missing files to write.
Several Constraints entries were added along the way, per the mechanism this file's own
prior pass flagged as sound but unused.

Per `STEPS.md` step 5b, this file is (re)created against every file in `patterns/`,
following `templates/Pattern_Judgement_Check.md`, including its inversion that two
restatements which read the same are a finding rather than a convenience.
</content>
