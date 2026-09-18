# Control arm 2: the framework

The same twelve-room map as `arm0-prompt.md` and `arm1-prompt.md`, run through the
framework as `STEPS.md` stands today: steps **3c** and **4c**, as one DANGEROUS region of
one block, with a two-line brief.

See `INTROSPECTIVE.md` P0.2 for how the three arms compare.

---

## What was supplied to this arm

- The two-line brief at `arm2-brief.md`.
- The map, verbatim, from `arm1-prompt.md`, converted by hand into `Locations.md` and a
  block diagram - `tools/map.py` does not exist yet (P4.3), and D9 says the user never
  writes either by hand, so the conversion below is what that script will have to do.
- Everything `templates/Region.md` and `templates/Location.md` name in their own Context
  sections, which for this run is `GENRE.md`, the setting-level artifacts of Telar,
  `patterns/region/Dangerous.md`, and `patterns/dangerous/*.md`.

## Output

- `arm2/region/F.md` - the Region Overview (3c)
- `arm2/region/F/Tags.md` - the region tag pool (3c)
- `arm2/region/F/Locations.md` - the gazetteer, converted from the map (4a)
- `arm2/region/F/Connections.mmd` - block existence (4b)
- `arm2/region/F/Court.mmd` - the block's typed location graph (4b)
- `arm2/region/F/1.md` ... `12.md` - the twelve locations (4c)
- `arm2/registry-stubs.md` - the registry rows 4c wrote, held here rather than in
  `setting/` so the control does not alter the corpus the checks are tuned against

## Conversion notes - what the map did not carry

Three decisions the room list could not settle, recorded because `tools/map.py` will have
to settle them too:

1. **The corridor is unkeyed.** Five rooms (1, 3, 9, 10, 11) name `corridor` as a
   destination. The framework has no node for an unkeyed passage - locations connect only
   to locations - so the corridor became edges. Read as one passage, its mouths run in the
   order 1, 3, 11, 9, 10, which is the only order consistent with the map's own compass
   directions. An interior mouth therefore carries two edges through one opening, and
   those rooms' Exits lines name the same door twice with two destinations.
2. **The map supplies no vertical and no one-way edges.** Of thirteen location-tier edges,
   two are secret (15%, on target) and eleven are open (85%, against a 60% target). The
   one vertical edge in the region is the entrance stair, and it only exists because it
   crosses into B.6 Old Approach Road, which is what realizes the region-level B-F edge.
   `patterns/region/Dangerous.md`'s EDGE KIND MIX cannot be met from this map, and per D4
   the map wins.
3. **Both of room 10's doors lead to room 9.** The map gives it a south door to 9 and an
   east door to the corridor, whose north end terminates at 9's east door. Left as the map
   has it.
