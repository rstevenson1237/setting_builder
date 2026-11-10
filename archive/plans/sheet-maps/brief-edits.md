# Brief - hand edits kept across regeneration (artgen A8)

For an artgen session in `rstevenson1237/image_tools`, from setting_builder's sheet-maps plan
(`implementation.md` T2.6; `spec.md` D7 and 9 A8). It needs `brief-engines.md`.

setting_builder rebuilds every map from its tables. A wrong map is fixed on the map: a river
moved, a room nudged off its neighbour, a label shifted. Only what no table states may survive
a rebuild. What a table states is rebuilt from the table, and a hand edit that contradicts it
is reported, not kept.

## What phase 1 found

- **No hand edit survived.** The prototype deleted each map to rebuild it, so the Ravine's
  river, its rock walls and its painted gorge were passed in again as strings on every run
  (`to_map.py` `<edits>`).
- **Every entry is anonymous.** Edits, rooms, corridors, labels and symbols carry no record of
  who wrote them. A consumer cannot replace its own entries and leave the rest.
- **The hand edits are what `Ground.md` reads.** The Ravine's walls and river decide each
  mouth's height, so losing them changes the facts the writing was done against.

## What to build

1. **`origin` on every entry**: rooms, corridors, edits, requirements, labels and symbols. It
   is an optional string, so the format version is unchanged. An entry without one is a hand
   entry. The per-change commands take `--origin`.
2. **`artgen map sync` and `artgen dungeon sync --file target.json --from new.json --origin
   tables`**
   - Every entry of that origin in the target is replaced by the entries of `new.json`, which
     all carry that origin. Every other entry is kept, in order.
   - Hand edits apply after generated ones, so a hand `elevate` still shapes ground made from
     requirements.
   - A room or corridor keeps its id across a sync when the consumer gives the same id.
3. **Conflicts reported, never resolved silently.** `sync --json` lists:
   - each hand entry that refers to an id the sync removed (it is dropped);
   - each hand entry that moves or resizes an entry of that origin, such as a hand `x` on a
     generated room. The table's value wins, and the hand value is reported.
   - each hand label or symbol now inside a room or over another mark.

## The cases

| Case | Change | Facts the test holds it to |
|---|---|---|
| `ravine` (exists) | The marks, road and requirements carry `origin: tables`; the river nudge and the wall `elevate` are hand edits. Synced from a file with E.2 moved 3 squares north. | The hand edits are kept, in order, after the generated ones. E.2's mark moves. The river is where the hand edit put it. |
| `warren` (exists) | Every room and corridor `origin: tables`; one hand symbol (a `web` in F.3); one hand `x` on F.4. Synced with F.5 removed. | The web is kept. F.4's hand `x` is reported and the table's kept. The corridor F.3-F.5 is gone, and nothing refers to F.5. |
| `shrine-crypts` (from `brief-engines.md`) | A hand label inside M.8; synced with M.8 resized to cover it | The label is reported as inside a room |

## Done when

- Sync keeps hand entries and replaces one origin's, on both kinds, each covered by a test.
- Each conflict kind is reported on its case.
- A file with no `origin` anywhere syncs as all hand entries, and is left unchanged by a sync
  of an empty origin.
- The CHANGELOG describes `origin` and `sync`.

## setting_builder's side

- T3.6 to T3.8 write every generated entry with `origin: tables` and update a committed map
  only by `sync`.
- A conflict is a finding sent to the user, as D7 says: drawing a map is also a review, and a
  table changes only on their word.
- This lands before any hand edit is made (T2.6 before T4.7).
