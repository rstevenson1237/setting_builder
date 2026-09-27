# Region - Wild

## Provides
One WILD Region Overview: the stretch of country as a whole, which its Landmarks sit in.
How many locations it holds, in what classification mix, and how they connect is
`templates/Location_Gazetteer.md`'s and `templates/Region_Connections.mmd`'s; what one
location holds is its classification's own file.

## Spec

```
WILD REGION
  1     Overview - three sentences: what this stretch of country is, who uses it and for
        what, and why it stays as empty as GENRE.md's Population density answer has it
  1     Ambiance - what it looks, sounds and smells like across the whole region, how
        weather and season change it, and how anything built here recurs
  1     Terrain - the ground, and how hard it is to move through beyond what Layout's
        distances say: the texture the referee narrates between any two points
                                                                          {TERRAIN}
  1     Foraging - plants, game and geological goods findable here, whether rare or
        abundant, and what they are called locally; any healing or magical value held to
        GENRE.md's Magic level
  1     Layout - its shape and extent, the distances between Landmarks in yards or miles,
        where its notable Features and Dangers sit, and what one action buys here, per
        setting/Procedures.md's Time
  1     Features - what a party meets across the region rather than at one point:
        crossings, weather, footing, what high ground shows, what the region does at night
  1     Dangers - whether the country is indifferent and merely lethal, or watched
  1     Creatures - what lives here, by setting/Bestiary.md name, its range, and how it
        meets a party                    {hunting | watching | avoiding | following}
  1     Factions - which of setting/Factions.md claim ground here - a Landmark held, a
        route kept, a stretch worked - or `none`
  1     Secrets - what the region hides and roughly where, enough for every Secret-tier
        location to have somewhere to come from
  1     Treasure - what rewards exploration here, and which tables it leans on
  1     Tables - a d6 Encounter table, rolled on each failed Difficulty roll
```

```
TERRAIN - one, or two in combination
  hills        - rolling high ground, cut by valleys
  mountains    - high ground that has to be climbed or gone around
  plains       - open, level ground with little cover
  forest       - ground under trees
  swamp        - standing water and ground that will not bear weight
  desert       - ground without water
  jungle       - ground under growth too dense to see through
  coast        - ground at the edge of the sea
```

## Constraints

- **Game is Foraging's, danger is Creatures'.** Anything dangerous enough to be an
  encounter is cited from the Bestiary under Creatures, never listed as game.

- **Never write terrain as a location.** A slope, a brook, a field is what the region looks
  like, and belongs in Terrain; a location is somewhere that can be named, revisited and
  connected to.
