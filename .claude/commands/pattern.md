---
description: Change a pattern or cell file with the content tree held out of context
argument-hint: <request>
---

Change the pattern files under `patterns/` to satisfy `$ARGUMENTS`.

**Hold the `setting/` tree out of context for this workflow.** Do not read
`setting/setting.md`, any `region.md`, any location file or any table file
while deciding what a pattern should say. Existing generated content is
evidence about the last framework decision, and reading it while making the next
one biases the framework toward what has already been written.

The tools, `CLAUDE.md`, `SPEC.md`, `config/weights.yaml`, `MECHANICS.md` and the
pattern files themselves are all in scope. The content tree is not.

## Run

1. **Say which files change and why**, before changing them. A pattern edit is a
   change to how content is produced, and its cost is measured in the passes it
   invalidates.

2. **Make the change.** A pattern carries `id`, `target`, `phase`, `writes`,
   `dependencies` and `schema_version` in frontmatter, and a body of
   `## Patterns`, `## Excluded patterns` and `## Design questions`. `router.py`
   refuses to index one that does not.

3. **Regenerate the index.**

   ```
   python tools/router.py
   python tools/resolve_deps.py --check
   ```

   `DESIGN_PATTERNS.md` is generated from pattern frontmatter and is never
   hand-edited.

4. **Run the suite.**

   ```
   python -m unittest discover -s tests
   ```

   A new or changed mechanical check arrives with its negative case in
   `tests/test_validate.py`, and `test_every_check_has_a_case` fails if one is
   missing. A check with no case is indistinguishable from a check that no
   longer runs.

5. **Book the re-run, or say plainly that none is needed.** A pattern change
   that invalidates existing content is a step re-run, booked as its own pass.
   It is never a hand-patch of the affected files. Name the step and the scope.

## Where a decision goes

- **A ratified production rule** goes in the pattern or the cell file that
  enforces it.
- **A checked number** goes in `config/weights.yaml` and nowhere else. A number
  with two consumers lives there; a number only a writer reads stays inline in
  its pattern, and a config key with one named consumer is a bug.
- **A mechanical term** goes in `MECHANICS.md` and is cited in content as a
  token.
- **A dependency outside this repository** goes in `EXTERNAL.md`, which is the
  only backlog and is capped at one page.

## Rules

- **`GENRE.md` is frozen at the close of Milestone 2.** Editing it is a step
  re-run of everything downstream. Say so before touching it.
- **Cell files are the tuning surface and phase patterns are mechanism.** A rule
  that differs across the nine cells belongs in the cells. A rule true of every
  location belongs in the phase pattern, stated once.
- **Never write a checked count into a cell file.** Cite the `config` key by
  name, so one edit moves the whole system.
- **Rewrite, never annotate.** A pattern carries current state. It does not
  explain what it used to say.
- **No open-questions register and no decisions log.** Both accumulate, both
  grow a revision history in prose, and both become a parallel copy of the
  project that drifts.
