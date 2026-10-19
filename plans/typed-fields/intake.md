# Intake - typed fields wherever prose holds a value

## The request, verbatim

From the sheet-maps decisions (`plans/sheet-maps/intake.md`, D5):

> I would not make size a general string. kdl big strength is being able to define
> arbitrary types so we should take advantage of it, but yes it should be defined as part of
> the room dressing (and other location data as appropriate)

> yes one of the big strengths of kdl is we can add very fine grained schema, optional
> when it makes sense and then the agent builds these fields back into prose for the user -
> we could probably use a full review of the schema for these opportunities

The review is `plans/sheet-maps/implementation.md` T0.4, made a plan of its own.

## How each clause is read

| Clause | Read as |
|---|---|
| "a full review of the schema" | Every field in `patterns/`: `Common_Schema.md`'s values, every `Setting_Schema.md` table, and the Safe, Wild and Dangerous nodes. A region's seed and brief are prose by design, and are reviewed only for values a table should hold instead. |
| "for these opportunities" | A field whose `text`, `string` or `gloss` holds a value: a number, a unit, a count, a time, a die, a price, a choice from a closed set, or a reference to another entry. |
| "very fine grained schema" | New `value` and `enum` types in `Common_Schema.md` where several fields share a value (coin, time, distance), and typed child nodes where one field packs several values (a trigger, a count and a delay in one gloss). |
| "optional when it makes sense" | A typed field is `opt` wherever some entries have no such value. A required one is required because every entry has it and a check reads it. |
| "the agent builds these fields back into prose for the user" | The write-ups (5b) and briefs (5e) turn typed fields back into sentences. A typed field's value is stated once, in the table, and a write-up carries it. |

## What the review weighs

A field is proposed for typing only when the gain is real:

- **Code reads it**: a sum, a map, a site or PDF render, a cross-reference.
- **A check could catch a wrong one**: a price with no coin, a delay with no time, a die that
  is not one.
- **Entries are compared on it**: cheapest, nearest, soonest.

Each field typed costs something too. Every write-up and brief that carries it must turn it
back into prose. And each read set grows by the type's definition: `tools/metrics.py` counts
that cost. A field that only a reader reads, and that an agent would only write back as the
same sentence, stays prose.

## Already settled elsewhere

`plans/sheet-maps/spec.md` 5.1 and 5.3 already type the footprint on Dressing (`width`,
`length`, `height`, `shape`), each Location's and Stop's `at`, and each Connection's and Way's
`orientation`. The review takes those as given and does not reopen them.

## First sweep: where prose holds a value

Out of every field line across the four table schemas, 113 are `text`, `string` or `gloss`,
with a node shared by several ratings counted once in each. Those likeliest to hold a value,
with what Thornmarch shows in them today:

| Field | Holds today | Example |
|---|---|---|
| Safe `Purchase.price` | coin and a unit, or neither | `"10 cn a night"`; `"pennies a round"` |
| Safe `Purchase.limit` | a stock, hours or terms | `"two rooms only"` |
| Safe `Garrison.answers` | a trigger, a count and a delay | `"the alarm drum; twenty in two turns"` |
| Safe and Wild `Secret.when` | a time of day or a condition | unused in Thornmarch |
| `Hoards.Total` | a sum of coin and weight that the items already state | `"590 cn, 3 wt"` |
| `Hoards.Items` | a list of finds, each with its value | |
| `"Local Procedures".Roll` and `Stakes` | a die and whose it is; coin bounds and rates | `"A stake of 5 to 100 cn per player"` |
| `History.When` | years ago, vaguer the older it is | `"thirty years ago"`; `"many centuries ago"` |
| `Bestiary.Range` | a count the land supports, among prose | `"a warren holds thirty or so"` |
| `Factions.Relations` | one line per faction, each with a `Relation` | |
| `Quests.Terms` | one of a closed set (fee, share, favour, loan, bait), in the giver's words | |
| Dangerous seed `Conditions` | passage height and width, for every room | `"passages 4 feet high and 3 wide"` |
| `Procedures.md` | the ordinary prices, travel rates and encounter distances that other fields' values are checked against | |

Already typed, and so the pattern to follow: `Treasure` `Value` and `Wt` (`number`), each
`count` and `present` (`number`), `AD` (`dice`), `presence` (`percent`).

## State of the repository at intake

- `patterns/Common_Schema.md` defines 13 values and 4 enums. It has no coin, time or
  distance value. sheet-maps adds `feet`, `distance`, `Compass` and `Distance_Unit`.
- `tools/tables.py` checks each table against its schema, and `tools/validate_setting.py`
  owns every other check. Both would gain a check for each new type.
- `tools/site_common.py` reads several of these fields as prose. For example, `parse_at`
  takes `at` apart with a pattern, and sheet-maps retires that.

## Deliverables

- `intake.md`: this file.
- `spec.md`: one numbered proposal per field, each with its type, what reads it, its check,
  and what it costs, so each proposal can be approved line by line. Every field it leaves as
  prose is listed too, with the reason.
- `implementation.md`: written from the approved set, ordered to land after sheet-maps'
  T3.2 so the two plans don't both edit `Common_Schema.md` at once.

Nothing in `patterns/`, `templates/`, `STEPS.md` or `tools/` changes under this intake.
