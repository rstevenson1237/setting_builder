# Links.md - DANGEROUS

## Purpose
What ties one DANGEROUS region's rooms to somewhere else, `setting/region/[Region Code]/Links.md`:
every lock a key elsewhere opens, and everything here someone elsewhere wants, one row each.

## Context
Read first:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- `patterns/dangerous/Lock.md`, `patterns/dangerous/Quest.md`
- this file's stub rows; the `Exits.md` or `Challenges.md` row each lock sits On; the `setting/Keys.md` and `setting/Quests.md` stubs the rows name, and the far location each stub names

## Instructions
- Every row here is connected - it answers a location the stub names elsewhere - so it is
  written once every location it names has its tables filled, in the pass that fills the
  setting's connected stubs. The format is `templates/region/Allocation.md`'s.
- Write every empty cell; never re-decide a tag allocation settled.
- A lock matches its Keys row: the key elsewhere and the lock here are made to fit.

## Template
```
# Links of [Region Code] [Region Name]

## Lock
| ID | Location | [patterns/dangerous/Lock.md's labels] | Realized |

## Quest
| ID | Location | [patterns/dangerous/Quest.md's labels] | Realized |
```
