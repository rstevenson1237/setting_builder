# Safe - Authority

## Provides
Where a claim to authority is exercised, on what basis, and what a stranger has to do to
get anything out of it.

## Spec

```
AUTHORITY
  1     Claim - by what claim it is held here
                                   {elected | inherited | seized | granted | assumed}
  1     Holder - who holds it, from the region's People roster
  1     Settles kind - what actually gets settled here, as opposed to what is claimed
                                              {a right | a debt | a boundary | who may}
  1     Settles - that matter, never the abstract fact of order
  1     Limit - the limit of the claim: where it stops being obeyed, however far
        GENRE.md's Authority answer says a writ reaches
  1     Hearing - what a stranger must do to get a hearing: this Kind's answer to
        safe/Settlement.md's gate                                         {HEARING}
  40%   Rival - a rival claim, and who backs it
  30%   Posted - something posted, current and specific, naming who posted it
  20%   Custom kind - a custom a stranger will break without knowing
                                                  {a place | a word | a day | a debt}
  1     Custom - where a custom was drawn: that custom, never stated to anyone who
        already knows it
```

```
HEARING - exactly one
  wait         - a wait, and who decides how long
  fee          - a fee, stated
  vouching     - somebody known here speaks for them
  writing      - an approach made in writing, in the proper form
  subordinate  - a subordinate's own price for passing it on
  favour       - a favour owed first
```

## Constraints

- **No authority defaults to legitimacy.** Somebody holds it by a specific arrangement,
  and an entry with no limit stated has left out the fact a party's leverage lives in.
