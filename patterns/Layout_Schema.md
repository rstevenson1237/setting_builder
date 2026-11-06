# Layout Schema

What `layouts/` holds: one file a layout, `layouts/[id].md`, a motif of rooms and the ways between
them. A design (`patterns/Region_Schema.md`'s `Design`) uses a layout by id, binds its roles to
location codes and joins its sockets to other layouts' sockets. A layout is flexible: it
expands to rooms and ways that `dungeon layout` places, so it states how many rooms, how big
and how they join, and leaves where to the solver. Sizes are ranges in feet on the 5 ft grid.

A layout file holds one `Layout` line, then its `Param`, `Part`, `Tie`, `Socket` and `Constraint`
lines, each a line of its own like a table entry.

```kdl
enum Constraint_Kind mirror straight   // advisory until the engine can hold them

node Layout {               // opening with its id, as its file is named
  name gloss
  tags tag list             // what `design.py layouts` is searched by
  source string             // "drawn" and the map it was abstracted from, or "written"
}
node Param {                // a number a Use may set, within its range
  name tag
  range string              // "N-M": a count, or feet
}
node Part {                 // a room the layout holds; a passage is a room of shape hall
  role tag                  // what a Bind names; a role with a `count` binds that many locations
  shape Room_Shape opt      // rect where unset
  width string opt          // "N-M" feet, or a Param's name
  length string opt
  count string opt          // "N", or a Param's name; one where unset
  at string opt             // "[role] [Compass]": the side of that role it lies on; its own role, each room on that side of the one before
  focal tag opt             // "focal" where the layout is built round this part
}
node Tie {                  // a way between two roles: the rooms of one and of the other, each of a few to the one, or room to room
  a tag                     // a role; the same role twice joins each room to the next
  b tag
  kind Link_Kind
  of_a tag opt              // first, last or a number: the one room of a role with several that the way ends at
  of_b tag opt
}
node Socket {               // where the layout joins another, or leaves the block
  name tag
  part tag                  // a role
  of tag opt                // first, last or a number, where the role has several rooms
  bearing Compass           // the way out, from the room
  width feet
}
node Constraint {           // what the placed layout should hold to
  kind Constraint_Kind
  parts tag list opt        // the roles it holds between; all where unset
}
```
