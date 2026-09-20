# Dangerous - Key

## Provides
When a DANGEROUS location holds an object whose real function is opening something
somewhere else.

Criteria for what earns a row are in `patterns/setting/Keys.md`.

## Spec

```
KEY - supply, a key lying here
  1     The object, and what it physically is
  1     How it is held here - carried, fitted, buried, mounted, owed
  1     A stub row in setting/Keys.md naming this location and the location it
        opens - the second is the obligation
  40%   A clue connecting object to lock, where the connection is not obvious
  20%   Evidence it has been used before

KEY - demand, a lock an obligation named here
  1     The lock, and what it physically is
  1     The feature it sits on, matching the setting/Keys.md row that named it
  20%   Evidence it has been forced at, and held
```

A Key and a Quest are the same shape seen from opposite ends. A Quest is asked first and
fulfilled later; a Key is found first and used later. Both are two-ended, both connect
locations, and both are the reason a point crawl is a network rather than a list.

**The supply end does not name its lock.** It records a `setting/Keys.md` row and stops; the
row's `Unlocks` line is written at 4d, per `templates/Keys.md`. A stub exists for every
location before any location file is written, but a stub carries a name, a weight and two
tags and no features - so naming a feature at 4c names something that does not exist yet.

**What the row does instead is create an obligation**, and the obligation is what the far
location's weight file draws at rate `1`. An obligation may name a location in this block, or
in a block or region not yet generated; it may never name one already written, because there
is no longer a draw to honour it. Reinforcement, not an obligation, is how a connection into
finished ground gets made. Nothing is owed at the close of 4c: an unconsumed obligation is a
dangling thread by definition.

## Design patterns

**Forms** - an actual key, and the lock it fits is nothing like a door; a rod, pin, or bar
cut to a profile; a stone, gem, or disc fitted to a socket; a seal, signet, or stamp; a
token given as proof; a specific bone; a phrase or name recorded on something portable; a
measured length of something; a piece broken off a larger thing, still here.

**How it is held** - carried by something that will not give it up; fitted into a fixture
where it is doing another job; buried with whoever last used it; set into a wall as
decoration; owed - somebody here has it and will trade; split, and this is one part.

**Connections that are not obvious** - the object and its lock share a maker's mark, a
material, a tongue from `setting/Language.md`, or a measurement. The connection is itself
a discovery, and where the drawing class conceals it, that class's own concealment line
states the Clue, Trigger and Payload.

## Constraints

- **A key is drawn from two places at two rates, and that is not a duplication.** The
  object found here is treasure, drawn by `dangerous/Treasure.md`; the lock here that
  something elsewhere opens is registry, drawn by the weight file. Per
  `patterns/setting/Keys.md` a key gates something elsewhere and the two ends are
  deliberately apart, so one location very rarely holds both - and where it does, they
  are two different keys.
