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
                            // the template reads; or BRIEF:[name], a BRIEF.md line by name
enum Scope setting "[Region Code]"
enum Shape gazetteer seed brief tables          // or a Setting_Schema.md table
enum Run "--location" "--pending" "--brief" "--read-set" "--skeleton"   // tools/validate_setting.py's reports
enum Once written                               // read only once it exists

// -- The fence holds one template line, then read, run, field and step lines.
node template {
  scope Scope
  writes path               // space-separated
  shape Shape list opt      // what the schema draws as the step's skeleton; with none, the template's own
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
```
