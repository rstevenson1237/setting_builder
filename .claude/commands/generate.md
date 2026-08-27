---
description: Sample a pattern's output without writing to the content tree
argument-hint: <pattern-id> [--target <code>]
---

Generate content in the pattern's format for `$ARGUMENTS` and print it to the
conversation. **Write nothing to `setting/`.**

This is how a pattern is sampled before the project commits to it. A pattern
that produces the wrong shape is cheaper to find here than at step 11 across
forty locations.

## Run

1. **Resolve the bundle.**

   ```
   python tools/resolve_deps.py --pattern <pattern-id> --target <code>
   ```

   A pattern targeting the setting takes no `--target`. Everything else needs
   one. `--stdout` prints the bundle instead of writing it, which is worth doing
   when the question is what the pattern is being given rather than what it
   produces.

2. **Dispatch, if the pattern's phase is `builder` or `decorator`.** Same
   contract as `/step`: the pattern file, the bundle, and the current target
   file if one exists. Output is the complete file content and nothing else. An
   `architect` or `engineer` pattern is run here in the main session.

3. **Print the result.** Say which pattern and which target it came from, and
   say plainly that nothing was written.

## Rules

- **Nothing is written to the content tree.** Not the target file, not
  `connections.md`, not `T-KEY`, not the ledger. A sample that lands in the tree
  is content nobody booked.
- **The bundle is written**, because it is a build artifact and `build/` is
  where those live.
- **Do not fix what the sample gets wrong by editing the sample.** The output is
  evidence about the pattern. If it is wrong, the pattern is wrong, and that is
  `/pattern`.
- **A target that does not exist yet is a legal question.** Resolve what can be
  resolved, say which selectors came back empty, and generate against that. What
  a pattern does with a thin bundle is worth knowing.
