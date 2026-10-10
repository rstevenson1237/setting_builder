# The pattern file spec

What every pattern file in `patterns/` is made of. `patterns/Schema.md` is not a pattern
file: it is what every location table is checked against.

A pattern specifies one unit - one entry, one event; how many units, and in what mix, is
its template's.

## The three fields

Every file carries `## Provides`, `## Spec` and `## Constraints`, in that order.

- **Provides** - what exists once the file is read, in a sentence, and where it ends
  against any sibling file.
- **Spec** - a fenced block of lines, each opening with `1` where it is always answered or
  a percentage where it is answered at that rate, and each one of:
  - an **edge** - another pattern file, named in parentheses, that the generator reads;
  - a **question** - something the generator answers, which may carry suggestions: words
    and phrases in the register wanted, guiding the answer without limiting it;
  - a **draw** - a set the generator picks from, inline `{a | b | c}`, or named `{NAME}`
    and listed as its own fenced block below.
- **Constraints** - what the file must never do.

## Citation format

A citation from one pattern file to another is `folder/File.md`, except a
`patterns/setting/*.md` file, which keeps its prefix, since a bare `setting/File.md` names
the generated file.
