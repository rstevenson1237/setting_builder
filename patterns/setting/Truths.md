# Setting - Truths

## Provides
One rule this setting keeps that a generic setting of its genre does not. How many truths
the setting holds is `templates/setting/Truths.md`'s; what the genre itself keeps is `GENRE.md`'s.

## Spec

```
TRUTH
  1     Kind                                                              {KIND}
  1     Truth - the rule, in one sentence: the rule, not the feeling of the rule
  1     Costs - who it costs, and what they do about it
  1     Learned - by being told, or only by acting and seeing what happens
  1     Handle - what a party does about it, as an act a referee could adjudicate
  1     Codes - the Location Code(s) where it can be done
  1     Shows - at each rating: what a settlement builds because of it, what open
        country does because of it, what a dungeon's builders guarded against
```

```
KIND - exactly one
  land         - a rule the land keeps, that people work around
  object       - a class of thing that behaves consistently and strangely
  custom       - something everyone does whose reason is forgotten
  standing     - a kind of person treated differently, and why
  limit        - something that cannot be done here, and what happens when it is tried
  price        - a cost attached to a whole class of action
  border       - a boundary that is real rather than agreed
  the dead     - something the dead do here that they do not do elsewhere
  idea         - a political or religious idea, held as a rule
  mystery      - a question the setting holds open on purpose: what can be seen of it
                 and where, with its answer left to the referee
  open         - a gap left on purpose for the referee to fill - a site unstocked, a
                 name unassigned - stated so it reads as a decision, not an omission
```

## Constraints

- **A mystery or an open Truth says it is one.** Its rule line states that the answer, or
  the content, is the referee's by design; everything else it carries - what can be seen,
  where, what acting on it costs - is written as for any Truth. It is the one place an
  unanswered question is a decision rather than a gap.

- **A Truth is a class, not an instance.** One cursed book is an object, and belongs in
  `setting/UniqueTreasures.md`; a rule that makes a whole class of book behave one way is
  a truth.

- **A truth that only ever appears once was a location feature wearing a costume.** One
  that cannot show at more than one rating is not a Truth.

- **A Truth must sharpen the genre, never override it.** A Truth that answers one of
  `GENRE.md`'s questions differently from `GENRE.md` - more magic, a nearer authority, a
  fuller map - has broken the setting rather than distinguished it.

- **Never restate `setting/Setting.md` or `setting/History.md`.** A truth that says what
  either already established is a second copy, not a rule.
