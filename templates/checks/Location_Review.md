# Location_Review.md

## Purpose
The review closing each pass of the content loop: a context that wrote none of this
pass's write-ups judges them, and sends each finding to the step that fixes it. Appended
to `setting/checks/Review.md`, one section per pass.

## Context
- `GENRE.md`, `STYLE.md`
- the output of `python3 tools/validate_setting.py`, `python3 tools/validate_setting.py --pending` and `python3 tools/metrics.py`
- the last section of `setting/checks/Review.md`
- each region's Overview, `setting/region/[Region Code].md`
- each write-up this pass wrote, with its entries from `python3 tools/validate_setting.py --location [Location Code]`
- the header and Player Summary of every other write-up in the same block

## Instructions
- Open the section with the readings, and what moved since the last pass: errors,
  warnings, stubs, stale write-ups, tells, and each mix against its target.
- Judge each write-up against:
  - **entries match** - every entry carried, nothing written without one;
  - **one room** - it reads as one place, not its entries side by side;
  - **distinct** - it shares no Feature, shape or sentence frame with its block;
  - **said once** - nothing restated from the Overview, a setting entry or another room;
  - **the tests** - each line passes `STYLE.md`.
- Each finding names its fix: an entry (5a), a write-up (5b), a placement (5d), or the
  framework (`plans/`). A finding raised on the last pass and not fixed is carried, not
  repeated.
- Write no content. A pass with no findings and readings unchanged from the last says so;
  the loop has exited.

## Template
```
## Pass [N]

Readings: [errors, warnings, stubs, stale, tells, mixes] - [moved since pass N-1]

- [Location Code] - [item]: [finding] -> [5a / 5b / 5d / plans]
```
