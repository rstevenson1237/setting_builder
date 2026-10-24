# Language.md

## Purpose
The setting's tongues - phoneme inventories, syllable shapes, affixes, and a growing root
list - so that proper nouns coined weeks apart still sound like they come from the same
world. The framework's one living artifact: seeded, tailored once the setting is written,
and appended to every time a proper noun is coined.

## Context
```kdl
template scope="setting" writes="setting/Language.md" shape="Language"
read "setting/Setting.md"
read "setting/Bestiary.md"
read "setting/Factions.md"
field "Language.Coined here" from="Person.name, Person.form, Named Creatures.Form, Factions.Form, Location.name"
```

## Instructions
Each tongue states who speaks it, its consonants and vowels, its syllable shape, its
affixes, and its roots, for each tongue `BRIEF.md` names.

A coinage is recorded only for a name that coins it: a being's name (person, creature or
faction) whose Name_Form is `tongue` or `family`, or the setting's or a region's name whose
Place_Form is `tongue`. A location's name may point at a coinage already recorded. Each is
`Noun = root + root`, every part a root or affix of its own tongue, then what it means.
Where it is used is read from the names, never written here; a coinage no name uses or
points at is cut, and a name that coins one is recorded before it is written.
