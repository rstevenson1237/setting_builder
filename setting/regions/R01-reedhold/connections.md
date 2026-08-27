---
code: R01
scale: region
schema_version: 1
---

# Location connections

Location to location, and typed. Tier 4 is the one tier that draws connection type. A row with One-way `no` must appear in the Exits table of both locations.

| From | To | Type | One-way |
| :--- | :--- | :--- | :--- |
| R01-L01 | R01-L02 | boarded walk | no |
| R01-L01 | R01-L03 | cut ground | no |
| R01-L01 | R01-L04 | kept lane | no |
| R01-L01 | R01-L05 | lit path | no |
| R01-L01 | R01-L06 | cinder track | no |
| R01-L02 | R01-L06 | barrow run | no |
| R01-L03 | R01-L07 | doorway | no |
| R01-L03 | R01-L10 | doorway | no |
| R01-L04 | R01-L08 | side door | no |
| R01-L05 | R01-L04 | cut edge | no |
| R01-L07 | R01-L09 | yard door | no |
| R01-L07 | R01-L11 | weighing floor | no |
| R01-L08 | R01-L10 | street | no |
| R01-L09 | R01-L10 | street | no |
| R01-L10 | R01-L12 | back passage | no |
| R01-L11 | R01-L02 | salt walk | no |
| R01-L01 | R02-L01 | raised span | no |
