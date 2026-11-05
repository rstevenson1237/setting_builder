# Layout Schema

What `layouts/` holds: one file a layout, `layouts/[id].md`, a motif of rooms and the ways between
them. A design (`patterns/Region_Schema.md`'s `Design`) uses a layout by id, binds its roles to
location codes and chains its sockets to other layouts' sockets. A layout is flexible: it
expands to rooms and ways that `dungeon layout` places, so it states how many rooms, how big
and how they join, and leaves where to the solver. Sizes are ranges in feet on the 5 ft grid.

```kdl
enum Part_Kind room passage
enum Constraint_Kind mirror straight   // advisory until the engine can hold them

node Layout {               // opening with its id, as its file is named
  name gloss
  tags tag list             // what `design.py layouts` is searched by
  source string             // "drawn" and the map it was abstracted from, or "written"
  one-of Param Part Tie Socket Constraint
}
node Param {                // a number a Use may set, within its range
  name tag
  range string              // "N-M": a count, or feet
}
node Part {                 // a room or passage the layout holds
  role tag                  // what a Bind names; a role with a `count` binds that many locations
  kind Part_Kind
  shape Room_Shape opt      // rect where unset
  width string opt          // "N-M" feet, or a Param's name
  length string opt
  count string opt          // "N", or a Param's name; one where unset
  at string opt             // "[role] [Compass]": the side of another part it lies on
  focal tag opt             // "focal" where the layout is built round this part
}
node Tie {                  // a way between two parts, by role
  a tag
  b tag
  kind Link_Kind
  wall Compass opt          // the wall of a it leaves by
}
node Socket {               // where the layout joins another, or leaves the block
  name tag
  part tag                  // a role
  bearing Compass
  width feet
}
node Constraint {           // what the placed layout should hold to
  kind Constraint_Kind
  parts tag list opt        // the roles it holds between; all where unset
}
```
