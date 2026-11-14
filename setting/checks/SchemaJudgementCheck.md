# Schema Judgement Check - 2026-11-14, The Buried City after the block plans (8902787)

Evidence: `setting/checks/SettingJudgementCheck.md` of the same date. Its findings traced to a
schema are the level sizes (D to L) and G.22's place. Every finding of the 2026-11-02 pass was
fixed in 7f3d6cd.

Confirmed on every item: `patterns/Setting_Schema.md`, `patterns/Common_Schema.md`, `patterns/Safe_Schema.md`, `patterns/Wild_Schema.md`, `patterns/Dangerous_Schema.md`

## Across the schemas
- No overlap or contradiction: Needs Attention - a block's size is set twice: `Design` `outline` in `patterns/Region_Schema.md` and `BRIEF.md`'s `pack` `footprint`. The schema says an unset `fill` falls back to the brief, but says nothing of `outline` against `footprint`, and the validator lets them differ.

## Findings by file
- patterns/Region_Schema.md `Design` `outline` - Enforceable: nothing checks a designed level's outline against the brief's footprint, or the sequence of levels (widening, then narrowing) that the brief and `setting/Setting.md` describe.
- patterns/Region_Schema.md `Design` - Gaps: no field holds a room's required place in the block (centre, far end), so a seed's "at its centre" cannot be checked against the solved design.

## Open Items
- Say which sets a designed block's size, its `outline` or `BRIEF.md`'s `footprint`, and have `tools/validate_setting.py` warn where they disagree. Source: comment; validator.
- Add a way for a `Room` or `Bind` to name its place in the block (`at="centre"`), checked after `solve`. Source: field; gap.
