# Template Schema

Every generation template's Context: one ```kdl fence of the nodes below, under
`## Context`, written in `patterns/Common_Schema.md`'s values and these. A node's `arg=`
names the member its line opens with; every other member is a property. A review template
(step 5) reads what it judges, so its Context stays prose.

```kdl
// -- Every template reads these, so none lists them.
enum Standing "GENRE.md" "STYLE.md" "BRIEF.md" "patterns/Common_Schema.md"

value path                  // a repository path; a bracketed name such as [Region Code] stands for each one
value step                  // a STEPS.md step id, as 4a
value length                // N exactly, N-M, N+ at least, or -M at most
value source                // a table, node or member (Truths.Truth, Encounter, Dressing.mark); a file
                            // the template reads; or BRIEF:[name], a BRIEF.md line by name, then
                            // .[property] for one of its properties
enum Scope setting "[Region Code]"
enum Shape gazetteer seed brief tables          // or a Setting_Schema.md table
enum Run "--location" "--pending" "--brief" "--read-set" "--skeleton"   // tools/validate_setting.py's reports
enum Once written                               // read only once it exists

node fence {                // a template's Context
  one-of template read run field step format cite
}
node template {             // the fence's first line, and its only one
  scope Scope
  writes path               // space-separated
  shape Shape list opt      // what the schema draws as the step's skeleton; with none, its format
}
node read arg=path {
  path path opt             // a file
  part text opt             // the part of it read
  once Once opt
  naming string opt         // in place of a path: a Setting_Schema.md table, read as the region entries naming its entries
}
node run arg=flag {
  flag Run                  // then its arguments
  once Once opt
}
node field arg=name {       // one field: what it pulls from and how long it runs
  name source               // Table.Field, Node.member, or a node or brief field
  from source list opt      // where it pulls from; with none, the writer authors it
  words length opt
  sentences length opt
  items length opt          // a list's `- ` items
}
node step arg=id {          // what one step of several adds
  id step
  writes path opt           // space-separated, in place of the template line's
  one-of read run field
}

// -- A file no schema table shapes, or what a shaped one opens with before its entries, in
//    order. A pattern is the line as written: each [name] is a field, the rest literal.
enum Count one optional many
node format {
  one-of line section table
}
node line arg=name {
  name gloss
  pattern string
  count Count opt           // one, unless it says otherwise
  out Out opt               // how the site and PDF set it, where not as written
  hint text opt             // what the skeleton says its last field holds
}
node section arg=name {     // a `## [name]` section
  name gloss
  out Out opt               // prose, unless it says otherwise; a table is d6 rows 1 to 6
  head gloss opt            // a table's result column
  item string opt           // a bullets section's item, as a pattern
  each source opt           // a `### ` table for each item BRIEF:[name].[property] lists
  when source opt           // present only where BRIEF:[name].[property] is set and not 0
}
node table {                // a table copied as written
  head string list
  one-of row
}
node row arg=cells {
  cells text                // its cells, one argument each
}

// -- A citation another file's text carries, beyond a Setting_Schema.md table's cite=.
node cite arg=name {
  name gloss
  form string               // as a pattern
  example string            // one written out, which the form and the tool reading it both match
  note text opt
}
```
