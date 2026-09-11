# Safe - Wealth

## Provides
What a settlement's own cache of treasure, lore, or both actually holds, who it belongs to,
and what stands between a party and it.

## Read at
Step 4c, for a SAFE location whose kind is a strongroom, hoard, shrine cache, or vault.

## Design questions

```
WEALTH
  1     Contents                   {Treasure | Lore | Both}
  1     Who it belongs to, or belonged to - and whether they know it is still here
  1     Protection, exactly one    {hidden | gated | guarded | trapped} - see Patterns
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

- **hidden** reuses `safe/Secrets.md`'s Clue/Trigger/Payload structure directly, guaranteed
  by this design question rather than by that file's own 10% settlement-wide roll. A Wealth
  location whose Protection is hidden has already spent its Secret; do not also roll
  `safe/Secrets.md`'s independent rate against it.
- **gated** means the cache's existence is known and unconcealed - access needs a stated,
  non-secret condition instead.
- **guarded** cites a creature already present in this region's Overview under Creatures,
  by name - per `region/Safe.md`, anything non-Man in a SAFE region is already
  working, penned, or a problem, and a guardian is the "working" case. Do not invent a new
  Bestiary entry here; if none fits, that is a signal to use a different Protection.
- **trapped** follows the format below, using `setting/Procedures.md`'s impact tiers.

**A SAFE trap is usually somebody's work, not a dungeon mechanism.** Per `safe/Secrets.md`'s
own principle, prefer an alarm, a marking dye, a lock that jams or maims, or a mechanism
that ruins the goods rather than the person - a Lethal tier here should be rare and
deliberate, reserved for a Wealth location the region's Situation already justifies treating
that seriously. Write it in the same line format every Feature uses:

`**Name:** tell; tell → effect; effect`

**Nominal Authority does not stop at the wall.** Per `GENRE.md`, a settlement being SAFE
means it is safe from the wilderness, not that everything inside it is accounted for or
under anyone's real control - a Wealth location is where that gap becomes something a party
can act on.

**Contract.** A Wealth location owes: contents (Treasure, Lore, or both), whose it is or
was, and exactly one Protection with its own discovery structure. Genre-neutral and
permanent. What the cache actually holds and what conceals it is not - the Examples below
are this build's compile of it, from this setting's chosen genre reference.

## Design patterns

**What it holds** - coin and plate too heavy to move casually; a founder's or a family's
kept wealth; tithes or tolls banked rather than spent; something taken and never returned;
a temple's or guild's reserve; an item in an older or dead tongue nobody here can read; the
one thing in this settlement everyone has heard of and nobody has seen.

**Whose it is or was** - the authority, banked against a bad season; a temple, as a relic or
a reserve; a family, three generations back; a guild's common fund; somebody dead whose
heirs do not know it exists; the settlement itself, held in common and guarded by custom
rather than a person.

**Hidden** - a wall thinner than it should be; a floor that does not match the joists below
it; a chest bricked into a foundation; a compartment behind an altar or a hearth; a stair
with one step too many; a room smaller inside than out. Per `safe/Secrets.md`, the Clue must
already be legible to somebody paying attention.

**Gated** - a phrase known only to a family or an order; a password changed every season; a
condition tied to a date or event - a saint's day, a full granary, market day; a permission
that must come from one specific living person, not an office; a price only a founder's line
can pay; proof of a claim rather than a key.

**Guarded** - a temple's kept beast; something that came with the vault and was never
removed because nobody living knows how; a creature already a standing problem elsewhere in
the region's Overview, reframed here as the reason nobody has cleared this out - dealing
with it has always cost more than the wealth is worth.

**Trapped** - an alarm bell or released animal that alerts a specific person; a marking dye
or scent that gives a thief away later; a lock that takes a finger rather than a life; a lid
weighted to hold shut from the inside; a mechanism old enough to half-work, and worse for
it.

**A second protection layer compounds rather than repeats** - hidden and trapped means
finding it is not the same as surviving opening it; gated and guarded means knowing the
phrase still leaves whatever is standing behind it.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
