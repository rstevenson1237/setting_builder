---
id: setting.architect.headers
target: setting
phase: architect
writes: [Overview, Style, Tables, Regions]
dependencies:
  - config
output_template: templates/setting.md
schema_version: 1
---

Step 1. The Architect names the setting, fixes its three tags and its seed, and
stubs `setting.md` and all twenty-four tables. It writes no content: every
heading it creates is empty or carries an architect note naming the step that
fills it.

Almost all of this step is `scaffold.py`, and that is the point. The shape of a
setting file is deterministic and belongs in code, so the judgement left here is
small and load-bearing: a name, three tags and a seed, each of which every later
step reads and none of which may change afterwards.

```
python tools/scaffold.py setting --name "<Name>" --tags "<a>,<b>,<c>" \
    --seed <n> --container <id>=<Name> [--container ...]
python tools/scaffold.py tables
```

## Patterns

**The name decomposes.** Every proper name in the setting decomposes into roots
recorded in `T-LNG`, and the setting's own name is the first one held to that
rule (M18). `T-LNG` is written at step 3, so the roots the name needs are
proposed in this step's question batch and written down when the registry is.
Two or three words. A name that has to be explained is a name that will be
explained in every bundle for the rest of the build.

**Three tags, and they are thematic rather than descriptive.** `config`
carries `tags.count` and `validate.py` checks it (M3). A tag names something the
setting is made of, not something it is like: `drowned` is a tag, `atmospheric`
is a preference. The three together should be able to reject a draft.

**The seed is recorded once and never changed.** `roll.py` derives every dice
result and every table draw from the setting seed and the target code, so the
same target rolls the same result on a rebuild. Changing the seed after step 1
silently invalidates every recorded roll in the corpus.

**Containers may be stubbed here and are settled at step 2.** The scaffold needs
at least one to write the tier-2 markers. Name the ones already implied by the
genre brief, and expect the Engineer to add, rename or re-cut them once the
region roster exists.

**Stub every table, including the ones nothing will cite for months.** The
catalogue is fixed at twenty-four (SPEC.md section 4.7) and the scaffold writes
all of them. A table stubbed late is a table whose `draws_on` chain was
guessed at rather than resolved.

**Leave the architect notes in.** Each stub carries `[[ ... ]]` naming the step
that fills it. They are struck when their content is absorbed, and `validate.py`
reports any that survive a Decorator pass (M25).

## Excluded patterns

- **Prose in any heading.** The Overview and the Style section are step 4. An
  Architect that writes a paragraph has decided at step 1 something step 4
  exists to decide, and the Decorator will not overwrite it because it reads as
  finished.
- **Region names, region counts, or anything about the map.** The roster is
  step 2 and the regions themselves are Milestone 5.
- **Table rows.** Step 3, and every row goes through the table's own pattern.
- **A fourth tag, or a tag that is a synonym of another.** Three, and they
  divide the space rather than converging on one corner of it.
- **Hand-writing what `scaffold.py` writes.** The scaffold fixes the body shape
  and `validate.py` checks the same shape, so the two agree by construction.
  A hand-written stub is where that agreement breaks.

## Design questions

1. **What is the setting called?** Two or three words. Which roots does it
   decompose into, and are any of them new? A new root is proposed here and
   recorded in `T-LNG` at step 3.
2. **What three tags?** Each names something the setting is made of. Name a
   draft each tag would reject; a tag that rejects nothing is decoration.
3. **What is the seed?** Any integer. It is recorded in `setting.md` and in the
   ledger, and it never changes again.
4. **What are the first containers?** Name the groupings the genre brief already
   implies, knowing step 2 settles them against the region roster. What divides
   the setting: geography, depth, or who holds what?
5. **Does the catalogue fit this setting?** Twenty-four tables is the fixed
   shape. Is there a table here that will hold nothing, and if so, what will be
   put in it instead of leaving it empty?
