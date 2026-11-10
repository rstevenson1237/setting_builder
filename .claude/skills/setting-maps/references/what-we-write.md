# artgen - what the framework writes, and why

How each key behaves is artgen's to say: `node tools/artgen/artgen-maps.js schema <dungeon|settlement|map> --keys`,
`schema dungeon --checks` for the ids `dungeon check` gives, and image_tools' `docs/DUNGEON.md`. This note lists only
the choices `tools/dungeon.py` and `tools/maps.py` make.

## Dungeon (`dungeon.block_map`)

| Key | What the framework writes, and why |
|---|---|
| `scale.perCell` | 5 ft a cell, so a 10-ft passage is `width: 2`. |
| `rooms[].shape` | `rect`, `circle`, `cave`, `octagon` (`cut` 1/(2+√2), so a square one is regular) and `hexagon` as themselves; a `poly` outline as a `poly`. |
| `rooms[].number` | `false`: the code alone labels a room. |
| `corridors[]` | Where two rooms do not touch: `route: "maze"`, `width: 2`, its ends `{room, side}` or `{room, port}` at the wall the Connection names, else `{room}`. Written shortest first, as `dungeon layout` routed them, so the map draws the passages `pack` measured. A passage into a round, octagonal or polygon room whose route ends by a diagonal leg takes a `port` on its outline (artgen ends it at the room's centre); two passages that leave one wall of a rect room over each other are given their own `offset`. Each change is kept only where `check` then finds no more than before. |
| `connections[]` | A door or opening where two rooms touch. |
| `furniture.place` | `outside`, so nothing stands on the map. |
| `rooms[].exits` | Each way out of the block, a stair or arrow by the wall facing it, with a note naming the way. artgen keeps the notes on the floor and spreads marks sharing a wall. |
| `bounds`, `areas[]` | A block's poly outline, and each of its Rock as a `rock` area. |
| `style` | On a packed level `wall: 2.5` and `hatch: full`; shared walls are on by default. |
| `overlay` | A trap in the middle of its way, or in its doorway. |

- `pack` writes a layout graph (`dungeon layout --graph`), not a file: rooms in 5-ft cells, each way with the bearing it keeps.
- The location cuts are `render --room CODE --margin N`.

## Settlement (`maps.settlement_map`)

| Key | What the framework writes, and why |
|---|---|
| `kind` | `castle`, with its own walls: the block's, where it has one, rather than the engine's. |
| `buildings[]`, `areas[]`, `water[]`, `roads[]` | Each location as one of these, by its type and the words of its name; a Gate as the wall's gate. |
| `underlay` | The home sheet's terrain map, beneath. |
