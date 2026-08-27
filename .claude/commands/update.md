---
description: Regenerate one target from its pattern and write it back
argument-hint: <pattern-id> --target <code>
---

Regenerate the one target named in `$ARGUMENTS` and replace its file.

This is the single-target form of `/step`. It runs the same five actions on one
file, and it carries the same overwrite discipline: a file the Builder has
already touched is listed in `state/ledger.json` under `built`, and replacing it
is a booked step re-run rather than a hand-patch. A patched file cannot survive
its own regeneration, which is the failure the rule exists to prevent.

## Run

1. **Resolve dependencies.**

   ```
   python tools/resolve_deps.py --pattern <pattern-id> --target <code>
   ```

2. **Ask the design questions** from the pattern, as one batch. Wait for
   answers. Write nothing yet. The batch is smaller than a step's and it is not
   optional: this call is about to overwrite a finished file.

3. **Generate.** Pass the pattern, the bundle and the current target file to a
   subagent where the phase is `builder` or `decorator`. Three inputs, one
   output: the complete replacement content of the target file and nothing else.
   The subagent never reads the `setting/` tree.

4. **Write.** Replace the target file with what came back.

5. **Validate.**

   ```
   python tools/validate.py --target <code>
   ```

   Where the update touched an edge or a container, re-derive first with
   `python tools/mermaid_gen.py`.

## Rules

- **The ledger moves with the file.** `python tools/ledger.py built <code>` after
  a Builder pass, `decorated <code>` after a Decorator pass. A file whose record
  did not move is a file the next `/step` will try to write again.
- **Rewrite, never annotate.** The returned content replaces the file. It does
  not append to it, and it carries no note about what it supersedes. Git holds
  the history.
- **Every generated file is reproducible** from its pattern, its dependencies
  and its recorded seed. An update that only makes sense as a diff against what
  was there before has broken that.
- **An update that invalidates other content is a step re-run.** If changing this
  file makes its siblings wrong, book the pass rather than walking the region
  patching each one.
