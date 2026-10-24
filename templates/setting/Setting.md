# Setting.md

## Purpose
Defines the setting's name, its tag line and a short referee-facing outline - the
foundation every other document builds on.

## Context
```kdl
template scope="setting" writes="setting/Setting.md"
format {
  line name pattern="[Setting Name]"
  line form pattern="Form: [Place_Form]"
  line tagline pattern="[Tag line]" hint="one phrase, the setting one step past its name"
  line outline pattern="*[Setting Outline]*" hint="two or three sentences outlining the setting for the referee"
}
```

## Instructions
Give the setting a name and its Place_Form, a tag line, then a two or three sentence outline
for the referee. A `tongue` name is recorded first in `setting/Language.md`.
