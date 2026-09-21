# Safe - Wealth

## Provides
What a settlement's own cache of treasure, lore, or both actually holds, who it belongs to,
and what stands between a party and it.

Alone among the five Kinds it may answer that file's gate line with its Protection
rather than with a person's terms, which is what the parenthetical on that line allows
for.

## Spec

```
WEALTH
  1     Contents                   {Treasure | Lore | Both}
                        (patterns/setting/Treasure.md,
                         patterns/setting/UniqueTreasures.md, safe/Lore.md)
  1     Who it belongs to, or belonged to - an authority's reserve, a family's or
        temple's kept wealth, a guild's common fund, or the settlement's own,
        held in common - and whether they know it is still here
  1     Protection, exactly one    {hidden | gated | guarded | trapped}
          hidden: guaranteed by this line, and states
            Clue    - what the building gets wrong about itself, legible to
                      somebody paying attention
            Trigger - a stated act on the clue
            Payload - the cache, and who notices it has been found
  30%   A second protection, of a different kind than the first
  20%   Somebody else wants it, and is closer to getting it than the party
```

**Treasure** is cited from a table, per `setting/Treasure1.md` through `Treasure5.md`, or
stated as a Unique Treasure stub per `patterns/setting/UniqueTreasures.md`. **Lore**
follows `safe/Lore.md`'s fields - physical form, whose voice, what it does - with one
deliberate exception: `safe/Lore.md` frames SAFE lore as *obtainable rather than
discovered*, because its obstacle is normally a living holder. A Wealth location's lore is
the opposite case on purpose - nobody currently holds it, or the holder does not know it is
here - which is what makes it worth a Protection line instead of an access clause.

**Protection is exactly one, chosen for the Kind, not rolled.** The four are not
interchangeable flavor text - each implies a different discovery structure:

- **hidden** states its Clue, Trigger and Payload on this line, guaranteed, rather than at
  `safe/Settlement.md`'s 10% settlement-wide rate. A Wealth location whose Protection is
  hidden has already spent its Secret; do not roll that rate against it as well.
- **gated** means the cache's existence is known and unconcealed - access needs a stated,
  non-secret condition instead.
- **guarded** cites a creature already present in this region's Overview under Creatures,
  by name - per `region/Safe.md`, anything non-Man in a SAFE region is already
  working, penned, or a problem, and a guardian is the "working" case. Do not invent a new
  Bestiary entry here; if none fits, that is a signal to use a different Protection.
- **trapped** follows the format below, at 5% lethal, else 35% damaging, else nuisance -
  a ladder short of DANGEROUS's on purpose, for the reason in the next paragraph.

**A SAFE trap is usually somebody's work, not a dungeon mechanism.** Prefer an alarm, a
marking dye, a lock that jams or maims, or a mechanism that ruins the goods rather than
the person - a Lethal tier here should be rare and
deliberate, reserved for a Wealth location the region's Situation already justifies treating
that seriously. Write it in the same line format every Feature uses:

`**Name:** tell; tell → effect; effect`

**Nominal Authority does not stop at the wall.** Per `GENRE.md`, a settlement being SAFE
means it is safe from the wilderness, not that everything inside it is accounted for or
under anyone's real control - a Wealth location is where that gap becomes something a party
can act on.

**A second protection layer compounds rather than repeats** - hidden and trapped means
finding it is not the same as surviving opening it; gated and guarded means knowing the
phrase still leaves whatever is standing behind it.

## Constraints
