# Genre

## Provides
The root of the pattern tree: the questions a genre has to answer before anything is
generated, and one edge to every pattern file a build enters from. `GENRE.md` is the
answer to this file's GENRE block, authored rather than generated; every other node is
reached from here. The order the nodes are generated in is `STEPS.md`'s, and what a
location holds is `patterns/Schema.md`'s.

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
SETTING - one of each
  1     Procedures                                     (patterns/setting/Procedures.md)
  1     Language                                       (patterns/setting/Language.md)
  1     Setting                                        (patterns/setting/Setting.md)
  1     History                                        (patterns/setting/History.md)
  1     Truths                                         (patterns/setting/Truths.md)
  1     Rumours                                        (patterns/setting/Rumours.md)
  1     Bestiary                                       (patterns/setting/Bestiary.md)
  1     Factions                                       (patterns/setting/Factions.md)
  1     Treasure                                       (patterns/setting/Treasure.md)
  1     Magic                                          (patterns/setting/Magic.md)
  1     Lore                                           (patterns/setting/Lore.md)
  1     Keys                                           (patterns/setting/Keys.md)
  1     Quests                                         (patterns/setting/Quests.md)
  1     Named Creatures                        (patterns/setting/NamedCreatures.md)
  1     Unique Treasures                     (patterns/setting/UniqueTreasures.md)
  1     Magical Tomes                           (patterns/setting/MagicalTomes.md)
  1     Hoards                                         (patterns/setting/Hoards.md)
```

```
REGION - each region's overview, exactly one by its rating
  1     {safe | wild | dangerous}      (region/Safe.md, region/Wild.md, region/Dangerous.md)
```

```
LOCATION - each location
  1     Name                                           (patterns/setting/Naming.md)
```

## Constraints

- **A genre question is answered once, in `GENRE.md`.** A pattern file below this one
  cites `GENRE.md` for an answer; it never restates one, and it never answers a GENRE
  question differently for its own level.
- **Nothing setting-specific belongs here.** This file is permanent across every build;
  what changes between genres is `GENRE.md`, never the questions it answers.
