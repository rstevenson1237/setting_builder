---
id: setting.decorator.prose
target: setting
phase: decorator
writes: [Overview, Style]
dependencies:
  - table:S-HIS
  - table:S-TRU
  - table:S-AMB
  - table:T-LNG
  - config
output_template: templates/setting.md
schema_version: 1
---

Step 4. The Decorator writes the setting's Overview and its Style section, and
raises the seven artifact tables to their finished register.

Two passes, one step. The Overview and Style pass runs once, against
`setting.md`. The artifact pass runs once per decorated table, against that
table's own pattern and its rows as the Builder left them, and it is the pass
that decides whether the tables are usable at the table or only readable at the
desk.

## Patterns

**The Overview is player register.** It shows and never concludes. It carries no
mechanical token (M24). It says what a person standing anywhere in this setting
sees, hears and is walking on, and it leaves what that implies to the table.
Three or four paragraphs.

**Every noun in the Overview is true in every region.** This is the same
least-common-denominator rule that binds `GENRE.md`, applied to a named setting
instead of an unnamed one. The test is mechanical: name a region on the roster
where the sentence is false. If one exists, the sentence belongs in that region.

**The Style section is referee register and it is a working page.** It states
what this setting counts in, how its two naming layers sound, and what its prose
refuses to state. A later writer reads it before writing anything, so it is
written for use rather than for atmosphere.

**Style is not genre restated.** `GENRE.md` says what kind of world this is and
enters every bundle already. The Style section says what this particular
setting's surface sounds like: its units, its names, its silences. Where the two
would say the same thing, the Style section says nothing.

**An artifact entry is the thing itself.** The lost journal's words, not the
fact that a journal is lost. The rumour as spoken, in the mouth it is spoken
from. The creature as described at the table, in the order a party meets it. A
row a referee has to paraphrase is a row that was not decorated (J9).

**Decorate the entry and leave the row's structure alone.** The Builder's
columns, IDs, mechanics and `draws_on` chain are settled. This pass rewrites the
Entry column and nothing else, because a citation that resolved at step 3 has to
resolve after step 4 (M16).

**Strike every architect note in a file this pass closes.** A note is struck
when its content is absorbed, and after this step `validate.py` reports any that
survive in a decorated file (M25). Record the closed targets with
`python tools/ledger.py decorated <codes>`.

**A parameter table is not touched.** Seventeen tables stop at Builder and their
Entry register is already their finished form. Decorating one adds words to a
row a referee reads at speed, which is the opposite of the job.

## Excluded patterns

- **A conclusion in the Overview.** "The silence is unsettling" states what a
  player is to feel. Write the silence.
- **A mechanical token anywhere in the Overview.** Referee-facing, and the
  Overview is not.
- **A named place, region or person in the Overview.** Anything true of one
  region is that region's, and the roster is a list rather than a description.
- **New rows, new IDs, or a reordered table.** Content arrives at step 3. This
  pass raises what is there.
- **An artifact entry that describes its own effect on the reader.** "A
  chilling account" is a review. Write the account.
- **A revision note.** The superseded line is rewritten and git holds the
  history.

## Design questions

1. **What does a person see, hear and stand on anywhere in this setting?** Three
   or four paragraphs' worth, and every noun survives the region test.
2. **What does this setting count in?** Distance, time, and the unit each region
   type is required to state. What does the prose measure and what does it
   refuse to measure?
3. **How do the two naming layers sound side by side?** What does the
   disagreement between them tell a referee?
4. **Which of the seven artifact tables is weakest as the Builder left it?**
   Decorate that one first, because it is the one a referee will notice.
5. **For each artifact table, what is the form the entry takes?** Spoken words,
   cut letters, a described figure, a creature met. State it before rewriting,
   so the rows in one table stay one kind of object.
6. **Which architect notes are still open?** A note whose content has not been
   absorbed is an open question and it is asked, not struck.
