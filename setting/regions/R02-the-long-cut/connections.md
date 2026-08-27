---
code: R02
scale: region
schema_version: 1
---

# Location connections

Location to location, and typed. Tier 4 is the one tier that draws connection type. A row with One-way `no` must appear in the Exits table of both locations.

| From | To | Type | One-way |
| :--- | :--- | :--- | :--- |
| R02-L01 | R02-L02 | raised span | no |
| R02-L01 | R02-L07 | cut edge | no |
| R02-L02 | R02-L03 | raised span | no |
| R02-L02 | R02-L07 | step off the stone | no |
| R02-L03 | R02-L04 | raised span | no |
| R02-L03 | R02-L12 | step off the stone | no |
| R02-L04 | R02-L05 | raised span | no |
| R02-L04 | R02-L07 | step off the stone | no |
| R02-L05 | R02-L06 | raised span | no |
| R02-L07 | R02-L08 | cut lane | no |
| R02-L07 | R02-L09 | cut lane | no |
| R02-L07 | R02-L11 | reed face | no |
| R02-L08 | R02-L10 | old lane | no |
| R02-L09 | R02-L12 | cut lane | no |
| R02-L10 | R02-L11 | closing lane | no |
| R02-L12 | R02-L05 | step off the stone | no |
| R02-L06 | R03-L01 | raised span | no |
| R02-L03 | R04-L06 | kept lane | no |
