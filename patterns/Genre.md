# Genre

## Provides
The root of the pattern tree: the questions a genre has to answer before anything is
generated, and one edge to every pattern file a build enters from. `GENRE.md` is the
answer to this file's GENRE block, authored rather than generated; every other node is
reached from here.

What each node is made of is `patterns/SPEC.md`'s; the order the nodes are generated in is
`STEPS.md`'s.

## Spec

```
GENRE - answered in GENRE.md
  1     Reference - the fiction the genre is modelled on, and what it sets against what
  1     Lethality - what one wrong roll costs a character
  1     Magic level - how rare sorcery is, and what it costs whoever wields it
  1     Authority - how far any one power's writ reaches
  1     Population density - how far apart the settled places sit, and what lies between
  1     Decay - how far past its peak a settled place stands
  1     Player characters - who they are, and what stands behind them
  1     Naming - which tongue proper nouns are coined from, and which are left plain
```

```
SETTING - one of each
  1     Tags                                           (patterns/setting/Tags.md)
  1     Procedures                                     (patterns/setting/Procedures.md)
  1     Language                                       (patterns/setting/Language.md)
  1     Setting                                        (patterns/setting/Setting.md)
  1     History                                        (patterns/setting/History.md)
  1     Truths                                         (patterns/setting/Truths.md)
  1     Rumours                                        (patterns/setting/Rumours.md)
  1     Bestiary                                       (patterns/setting/Bestiary.md)
  1     Factions                                       (patterns/setting/Factions.md)
  1     Treasure                                       (patterns/setting/Treasure.md)
  1     Lore                                           (patterns/setting/Lore.md)
  1     Keys                                           (patterns/setting/Keys.md)
  1     Quests                                         (patterns/setting/Quests.md)
  1     Named Creatures                        (patterns/setting/NamedCreatures.md)
  1     Unique Treasures                     (patterns/setting/UniqueTreasures.md)
```

```
REGION - each region's overview, exactly one by its rating
  1     {safe | wild | dangerous}      (region/Safe.md, region/Wild.md, region/Dangerous.md)
```

```
LOCATION - each gazetteer stub, exactly one by its region's rating and its own class
  1     {safe | wild landmark | wild hidden | wild secret | dangerous high |
         dangerous medium | dangerous low}
                        (safe/Settlement.md, wild/Landmark.md, wild/Hidden.md,
                         wild/Secret.md, dangerous/High.md, dangerous/Medium.md,
                         dangerous/Low.md)
```

## Constraints

- **A genre question is answered once, in `GENRE.md`.** A pattern file below this one
  cites `GENRE.md` for an answer; it never restates one, and it never answers a GENRE
  question differently for its own level.
- **Nothing setting-specific belongs here.** This file is permanent across every build;
  what changes between genres is `GENRE.md`, never the questions it answers.
