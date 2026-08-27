---
id: table.factions
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-HIS
  - table:S-TRU
output_template: templates/table.md
schema_version: 1
---

`S-FAC` is who wants what, and what they will trade for it. Referee-facing, and
the one table in the corpus whose rows are entities rather than results.

**Columns:** `ID | Faction | Wants | Trades`. Where the setting-level containers
name a holder, this table is where that holder acquires a want and a price.

## Patterns

**A faction is a want plus a price.** Both columns are filled or the row is a
place name. `Wants` is what they are trying to get, stated concretely enough
that a party could hand it over. `Trades` is what a party can get out of them,
and it is usually not coin: safe conduct, a count, a route, a name, a door left
open.

**A faction that will trade nothing still fills the column.** State the refusal
and what it does instead. Something that only ever asks is a real position and
it is more interesting than a shop.

**Nobody rules.** The setting has no living authority: a faction reaches as far
as it can walk and no further. Write reach as a fact — where they are, how far
their agreement holds — rather than as a claim.

**Wants must be able to conflict.** Two factions that want compatible things are
one faction. At least one pair here should want the same object for opposite
reasons, so a party carrying it has to choose.

**Keep the count low.** Five or six. A faction is a standing pressure a referee
holds in their head across a campaign, and past six they blur into a directory.
This is the one table that sits under the standard band on purpose.

**Each faction is met before it is named.** Say, in the `Trades` column or
beside it, what a party sees of these people before anyone tells them who they
are: the cut reeds, the fresh rope, the closed door.

## Excluded patterns

- **A leader, a roster, or an internal structure.** People a party can meet are
  `T-CRE`. This table holds the pressure, not the personnel.
- **A faction with a plan that unfolds on a schedule.** That is a metaplot. A
  faction wants something and keeps wanting it.
- **An alignment, a moral position, or a villain.** Write what they want. The
  table decides what that makes them.
- **A faction that exists everywhere.** If it has no seat and no reach, it is a
  condition of the world and belongs in `GENRE.md`.
- **A statement of what they will do to the party.** Reactions are location
  content and they branch on what the party does.

## Design questions

1. **Who holds each setting-level container, and what do they want?** The
   roster already named them; this row prices them.
2. **Who wants something the fallen power left, and who wants it left alone?**
3. **What can each faction give that a party could not otherwise buy?**
4. **Which two want the same thing for opposite reasons?**
5. **What does a party see of each faction before they meet anybody?**
6. **Which faction knows an `S-TRU` item and gains by not saying it?**
