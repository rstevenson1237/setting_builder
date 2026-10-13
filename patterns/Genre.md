# Genre

## Provides
The root of the pattern tree: the questions a genre has to answer before anything is
generated, and an edge to each region pattern. `GENRE.md` is the answer to this file's
GENRE block, authored rather than generated. The order things are generated in is
`STEPS.md`'s; what a setting file or a location holds is its schema's,
`patterns/*_Schema.md`.

## Spec

```
GENRE - answered in GENRE.md
  1     Reference - the work the genre is modelled on, and what it sets against what
  1     Lethality - what one wrong roll costs a character
  1     Magic level - who can work magic, how often, and what it costs them
  1     Authority - how far any one power's writ reaches
  1     Allegiance - what sides the world divides into, if any, and how a stranger's side
        is read
  1     Population density - how far apart the settled places sit, and what lies between
  1     Decay - how far past its peak a settled place stands
  1     Player characters - who they are, and what stands behind them
  1     Reward - what the characters are after, and what having it does for them
  1     Naming - which tongue proper nouns are coined from, and which are left plain
```

```
REGION - each region's overview, exactly one by its rating
  1     {safe | wild | dangerous}      (region/Safe.md, region/Wild.md, region/Dangerous.md)
```

## Constraints

- **A genre question is answered once, in `GENRE.md`.** A pattern file below this one
  cites `GENRE.md` for an answer; it never restates one, and it never answers a GENRE
  question differently for its own level.
- **Nothing setting-specific belongs here.** This file is permanent across every build;
  what changes between genres is `GENRE.md`, never the questions it answers.
