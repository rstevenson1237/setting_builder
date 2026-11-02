# artgen - what the framework writes, and why

How each key behaves is artgen's to say: `node tools/artgen/artgen-maps.js schema <dungeon|settlement|map> --keys`,
`schema dungeon --checks` for the ids `dungeon check` gives, and image_tools' `docs/DUNGEON.md`. This note lists only
the choices `tools/dungeon.py` and `tools/maps.py` make. What artgen lacks, and what the framework built round it, is
`plans/dungeon-maps/report-artgen.md`.

## Dungeon (`dungeon.block_map`)

| Key | What the framework writes, and why |
|---|---|
| `scale.perCell` | 5 ft a cell, so a 10-ft passage is `width: 2`. |
| `rooms[].shape` | `rect` and `circle` as themselves; any other shape as a `poly` of its own outline, so its walls stand where `tools/route.py` put the doors. |
| `rooms[].number` | `false`: the code alone labels a room. |
| `corridors[].from`/`to` | `{room, side, offset}` for a rect, `{room}` for any other shape, with `via` giving every bend of the passage `tools/route.py` routed. |
| `connections[]` | A door or opening where two rooms touch. |
| `furniture.place` | `outside`, so nothing stands on the map. |
| `style` | On a packed level `sharedWalls: true`, `wall: 2.5` and `hatch: full`, so a wall between two floors reads as one. |
| `overlay` | Stairs as `stairs-up`/`stairs-down` symbols with a `note` naming the way, and traps. |

- `tools/route.py` keeps passages a cell off every wall but their doors'.
- The location cuts are `render --room CODE --margin N`.

## Settlement (`maps.settlement_map`)

| Key | What the framework writes, and why |
|---|---|
| `kind` | `castle`, with its own walls: the block's, where it has one, rather than the engine's. |
| `buildings[]`, `areas[]`, `water[]`, `roads[]` | Each location as one of these, by its type and the words of its name; a Gate as the wall's gate. |
| `underlay` | The home sheet's terrain map, beneath. |
