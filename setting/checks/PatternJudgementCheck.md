# Pattern Judgement Check - after the region-overview, tag and defaults rework

Run against `patterns/` at commit dc4bd44, with Greywatch (98 locations, through 4c) and
`tools/context.py 4c` resolutions of C.12, C.33, C.2, A.21, B.4, B.8 and C.48 as evidence.
The per-file blocks below cover only files with a finding; every other file was read
against the six per-file items and is Confirmed on all of them.

## Cross-pattern
- No overlap or contradiction: Confirmed - Hazard/Mystery, Trap/Environmental/Residual and
  wild Hazard (living)/Creature each state their boundary in Constraints.
- Three tiers supplied across the class files: Confirmed - HIGH's lack of a concealed
  detail is stated and deliberate.
- Concealment triples stated per class, and not converged: Needs Attention - the three WILD
  class files draw the same Clue set, `{growth | ground | weather | wear}`, and differ only
  in the qualifier after it (where it is legible from). The Payload sets differ; the Clue
  set has converged.
- Gaps in coverage: Needs Attention -
  - nothing specifies the space a DANGEROUS region's entrances open onto (a ravine floor,
    a cave mouth, a courtyard): `dangerous/Block.md` specifies a quarter, and every room is
    in one. Greywatch's ravine had no hub and two outside entrances;
  - no pattern produces a magic item of GENRE.md's ordinary kind (a potion, a scroll):
    `patterns/setting/Treasure.md`'s QUALITY carries an "effect" only on Table II, and
    nothing else reaches one;
  - `dangerous/Block.md`'s household line - "where they sleep, eat, keep their stores,
    stand guard, and put their dead" - is the same room list for every household; nothing
    varies it by occupant, and Greywatch's households came out with the same rooms.
- Unhoused user-requested content: Needs Attention - the reference's stock creatures by
  their stock names (orcs, kobolds, ogres) have no pattern line asking whether they are
  used; `patterns/setting/Bestiary.md` asks for a Type and a Description, and the Naming
  answer routes every non-human people through a coined name. Standing mysteries and
  referee-left gaps are now housed as Truth Kinds.
- Rates compound sensibly: Needs Attention -
  - `dangerous/Door.md`'s 40% gate is rolled per exit: a room with four exits is gated on
    at least one about 87% of the time, and C.12 resolves with three of four exits gated;
  - `dangerous/High.md` stacks a mandatory challenge, a 50% second, a 30% mystery, a
    mandatory treasure and a 40% second treasure: a typical HIGH room resolves to two
    challenges and two treasures, which is where Greywatch's 50-word Features came from;
  - `dangerous/Medium.md` gives treasure at 50% where the challenge is an encounter, but
    Greywatch's encounter rooms carried treasure in nearly every case - the rate was not
    the problem, the absence of a roll was.
- Nothing contradicts STYLE.md: Needs Attention - `dangerous/High.md`'s "Never leave a HIGH
  room empty-handed" forbids what STYLE.md's "Withholding is content" requires at least
  once per region: a genuinely rich-looking room with nothing in it.
- Neutral and permanent: Needs Attention - Sanity is written into
  `dangerous/Trap.md`'s DAMAGE, `dangerous/Residual.md`'s Damage line and
  `dangerous/Environmental.md`'s Constraints, and `patterns/setting/Procedures.md` requires
  "Wounds and madness". A reference without a sanity mechanic (B/X) still gets one.
- Spec notation: Needs Attention - `dangerous/Mystery.md` and `wild/Mystery.md` rate a line
  `2`, and `patterns/setting/Language.md` rates lines `3-6` and `15+`. `patterns/SPEC.md`
  allows `1` or a percentage; the validator and `tools/context.py` read the first as a
  continuation of the line above.

## patterns/dangerous/Block.md
- Tier coverage - obvious / trigger / secret: N/A - a block is a quarter, not a room.
- Specific: Needs Attention - the household room list is fixed across occupants.
- Discoverable: N/A
- Interactive: N/A
- Not overly generic: Needs Attention - as above; six Khughik warrens under one occupant
  passed the "never two household blocks for one occupant" constraint by name alone.
- Missing relevant features: Needs Attention - no line for how the block opens onto the
  region outside it.

## patterns/dangerous/Door.md
- Tier coverage: Confirmed.
- Specific: Confirmed.
- Discoverable: Confirmed.
- Interactive: Confirmed.
- Not overly generic: Confirmed.
- Missing relevant features: Needs Attention - the 40% gate is per exit with no cap per room.

## patterns/dangerous/High.md
- Tier coverage: Confirmed.
- Specific: Confirmed.
- Discoverable: Confirmed.
- Interactive: Confirmed.
- Not overly generic: Confirmed.
- Missing relevant features: Needs Attention - no room for a HIGH room that withholds.

## patterns/setting/Treasure.md
- Tier coverage: N/A
- Specific: Confirmed.
- Discoverable: N/A
- Interactive: N/A
- Not overly generic: Needs Attention - Greywatch's Table III is a generic gem list with no
  line reaching setting/History.md; the "what it is made of, or struck in" line is met by
  material alone.
- Missing relevant features: Needs Attention - no magic item of the ordinary kind.

## patterns/setting/Bestiary.md
- Tier coverage: N/A
- Specific: Confirmed.
- Discoverable: N/A
- Interactive: N/A
- Not overly generic: Confirmed.
- Missing relevant features: Needs Attention - no line asking whether an entry is one of
  the reference's stock creatures.

## Open Items
- A pattern for the space a DANGEROUS region's entrances open onto. (pattern gap)
- A slot for ordinary magic items. (pattern gap)
- Vary Block.md's household room list by occupant. (pattern)
- Cap Door.md's gate per room, or rate it per room rather than per exit. (pattern rate)
- Reconcile High.md's "never empty-handed" with STYLE.md's withholding. (pattern vs STYLE)
- Move Sanity out of the pattern files into a GENRE.md-answered option. (pattern neutrality)
- Differentiate the WILD Clue sets, or move the shared set to one file. (pattern)
- Bring `2`, `3-6`, `15+` rates into SPEC.md's notation, or SPEC.md to them. (notation)
- A Bestiary line for the reference's stock creatures. (unhoused)
