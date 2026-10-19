# Spec - typed fields wherever prose holds a value

What `intake.md` asks for, as proposals to approve line by line. Each proposal has an id
and a box: tick it, strike it, or amend it. A proposal marked **depends on** stands only if
that one is approved too. Section 5 lists every field left as prose, with the reason, so any
of them can be overruled.

Each proposal gives the type, what reads it, the check it allows, and what it costs:
the write-ups and briefs that turn it back into prose, and the Thornmarch entries it
rewrites.

Two patterns already in the schema do most of the work:

- **An enum field opens with one of its items, and may go on after ` - ` in prose**
  (`Common_Schema.md`). A field that names one of a closed set in its first words becomes
  that enum, and keeps its prose after the dash. Nothing is lost, and a check can read the
  item.
- **A child node** (as `Hazard { Secret ... }`) carries several values that one gloss packs
  together today. This works in region tables only. Setting tables are `Label: value`
  entries, so there a packed value becomes a `value` type with a declared form instead.

---

## 1. Common values

- [x] **C1. `coin`.** `value coin // N cn or N-M cn; or pennies, the copper Procedures.md
  never counts`. Read by R5's `price`, S1's finds, and any later field holding coin. Check:
  the form, and a range low to high. *(`Treasure` `Value` stays a bare `number`: its unit is
  the table's.)*

- [x] **C2. `time`.** `enum Time_Unit Round turn hour watch day week` and
  `value time // N or N-M, then a Time_Unit: "2 turns", "1 watch"`. These are the units
  `Procedures.md`'s Time and Distance keeps (Round, turn, watch, day), plus hour and week,
  which the prices use. Read by R3 and R4. Check: the form, and a unit the region's rating
  keeps time in (a SAFE delay in turns is a warning).

sheet-maps adds `feet`, `distance`, `Compass` and `Distance_Unit` (its `spec.md` 5.1 and
5.3). These proposals reuse them and do not redefine them.

---

## 2. Region tables

- [x] **R1. A hazard states its Test and its cost.** Today the table holds only `type` and
  `damage`, and each write-up decides the rest. Thornmarch's write-ups add it in prose, 14
  times, as `(Test of Constitution, 2d, Crushing)`, and no check can see it. `Hazard`, in
  DANGEROUS and WILD, gains:

  ```kdl
  enum Test Constitution Fate Sanity          // Procedures.md's Forced Dangers: the die each Test rolls
  node Hazard {
    type Hazard_Type
    damage Damage_Type
    test Test
    wound Wound_Type opt     // a Constitution Test's Wound; required for one
    condition gloss opt      // a Fate Test's named Condition; required for one
    ...
  }
  ```

  - Check: a `wound` is one of the Wound tables `BRIEF.md`'s `Procedures wounds=` lists. A
    `condition` is a name in `Procedures.md`'s Conditions, which the validator already
    reads. A Sanity Test carries neither, and is a warning outside a Chaos source, as
    Forced Dangers rules.
  - Cost: 13 Hazard lines gain two fields. 5b keeps writing the parenthesis, now from the
    table.

- [x] **R2. An encounter's reaction opens with one of a closed set.** Every one of
  Thornmarch's 51 `reaction` values already opens with a disposition word: Hostile 32,
  Wary 16, then Fearful, Desperate and Cunning once each. Proposed:
  `enum Reaction Hostile Wary Fearful Neutral Friendly`, with `reaction Reaction`, and
  prose after the dash: `"Wary - parley for coin, bolt if rushed"`.
  - Check: the opening item. `metrics.py` reports the mix. A `BRIEF.md` mix can then ask for
    fewer Hostile, which is how a hostile-heavy setting would be caught.
  - Cost: 51 values, three of them re-read (Desperate and Cunning are not dispositions; the
    word moves after the dash).

- [x] **R3. A DANGEROUS encounter states how soon it answers an alarm.** A DANGEROUS
  brief's `Alarm` states "who comes from where, how many turns later", but a brief is
  written "from the tables alone" (`Region_Schema.md`), and no table holds a delay. So 5e
  invents it. `Encounter` in DANGEROUS gains `answers time opt`: how soon it reaches an
  alarm raised elsewhere in its region. Unset means it does not come. **Depends on C2.**
  - Check: a turn or Round unit.
  - Cost: 31 DANGEROUS Encounters to consider, set where the Alarm already names them. 5e
    writes Alarm from them.

- [x] **R4. A garrison's call and delay are fields.** `answers string` packs a trigger, a
  count and a delay into one value (`"the alarm drum; twenty in two turns"`), and the count
  repeats `present`. It becomes `call gloss` (what brings it out) and
  `within time` (how soon). **Depends on C2.**
  - Check: the time form. The count is `present` alone.
  - Cost: two Garrison lines.

- [x] **R5. A purchase's price is typed.** Thornmarch's 19 prices take five forms: coin and
  a unit (`"10 cn a night"`), a coin range (`"50-100 cn each"`), a rate (`"3% of the
  sum"`), the price list (`"listed prices"`) and pennies (`"pennies a round"`). `Purchase`
  becomes:

  ```kdl
  value price               // a coin; or N% of the sum handled; or listed, at Procedures.md's prices
  node Purchase {
    type Purchase_Type
    item string
    price price
    per gloss opt           // what one price buys: "a night", "each", "a Condition"
    limit gloss opt
  }
  ```

  **Depends on C1.**
  - Check: the form. A `listed` price names an item `Procedures.md`'s Coin and Prices
    lists, and the Setting Judgement Check compares a coin price against the list's.
  - Cost: 19 Purchase lines split into `price` and `per`.

- [x] **R6. A block states its passages' width and height.** A DANGEROUS seed's
  `Conditions` gives one passage size for every room (`"passages 4 feet high and 3
  wide"`), as prose a map cannot read. sheet-maps' `Block` (its `spec.md` 5.2) gains
  `width feet` and `height feet` for its passages, and a Connection gains the same two as
  `opt`, where its passage differs. **Depends on sheet-maps T3.2.**
  - Read by `maps.py`: a corridor drawn at its width. The seed still states the size as
    prose, for the reader.
  - Check: a Connection's own size falls within its rooms' footprints.
  - Cost: one width and height per block; Connections only where they differ.

---

## 3. Setting tables

- [x] **S1. A hoard's finds are a declared value, and `Total` retires.** Items already
  carry `(N cn, N wt)` per find, and `validate_setting.py` reads them with a pattern
  (`PRICED_RE`) to check a `Total` that only restates their sum.
  `value finds // finds split by "; ", each prose then "(N cn, N wt)"` makes the pattern a
  type, and `Total` is dropped: the site and PDF print the sum. **Depends on C1** for the
  coin.
  - Check: the form of each find. The sum check goes, because nothing is left to disagree.
  - Cost: 7 Hoards lose their `Total` line, and `check_hoard_totals` goes.

- [x] **S2. A creature states how many one lair or band holds.** `Range` packs where it
  lives, what it eats and a count (`"a warren holds thirty or so"`). `Bestiary` gains
  `Numbers number opt`, and the count leaves `Range`.
  - Check, as a warning: in a DANGEROUS region of `Kind` single holding, the count of that
    creature across its Encounters, plus the `present` of each Faction whose `Fields` name
    it, lies within `Numbers`. F holds 2 kobolds, 20 of the Gubak and Nib, against a
    Bestiary's "thirty or so": close enough here, and the check would show it.
  - Cost: 11 Bestiary entries.

- [x] **S3. An event's age opens with one of a closed set.** `When` is "years ago, vaguer
  the older it is". The vagueness is the point, so the prose stays, and its order becomes
  readable: `enum Age recent living old ancient` (within ten years; within living memory;
  recorded but not remembered; before any record), with `When Age` and the prose after the
  dash: `"living - thirty years ago"`.
  - Check: the entries are written oldest first. The site draws a timeline in that order.
  - Cost: 4 History entries.

- [x] **S4. A local procedure's roll opens with its die.** `Roll` is "the die and whose it
  is, and what it decides". All 8 of Thornmarch's name one: a Skill die, the region's
  Difficulty die, or a d6. `enum Roll_Die Combat Skill Magic Difficulty d6`, with `Roll Roll_Die`
  and the prose after the dash.
  - Check: the die is one the ruleset rolls. `Procedures.md`'s Ruleset names them.
  - Cost: 8 entries.

- [x] **S5. A quest's terms open with the kind of payment.** The schema's own comment
  already closes the set: "a fee, share, favour, loan, or bait". `enum Pay fee share favour
  loan bait`, with `Terms Pay` and the giver's words after the dash:
  `fee - "Five cn a disc, paid by the guild..."`.
  - Check: the opening item. `BRIEF.md` may ask for a mix.
  - Cost: 5 Quests.

---

## 4. Rules for every proposal

- A typed field is stated once, in its table. A write-up (5b) or brief (5e) carries it as a
  sentence and never restates it as a second value.
- `tools/tables.py`'s `check_field` gains each new `value`, as it holds `number` and `dice`
  today. An enum-opening field needs nothing new.
- Each new type lands with its check and with `templates/region/Tables.md` or the setting
  template that writes it, in one commit (`CLAUDE.md`).
- `tools/metrics.py`'s read-set report is run before and after. No step's read set grows by
  more than the types it reads.

---

## 5. Left as prose

| Field | Why it stays |
|---|---|
| `Purchase.limit` | Stock, hours and terms take no common form (`"two rooms only"`, `"up to 500 cn"`, `"two at a time"`), and nothing reads them but the referee. |
| `Secret.when` | A time of day or a condition. Thornmarch sets none, so there is nothing yet to type it from. |
| `Faction.members`, `Garrison.members` | Who they are and how they are armed; the count is `present`'s. |
| `Factions.Relations` | Already a declared value (`relation`), checked line by line by `check_relations`. |
| `"Local Procedures".Stakes` | Coin bounds, rates and rulings mixed in one statement. Typing the coin alone would split one sentence into fragments. |
| `Magic.Lasts` | Already an enum. The charge count after it is read only by the referee. |
| `Encounter.far`, `left` | A sign, not a distance. Distance is `Procedures.md`'s Encounters table. |
| `Person` fields | Voice and motive, read only by the referee. |
| `Dressing`, `Mystery.effect`, `Reward.container`, `Stop.sight` | Description. Sizes move out of `layout` under sheet-maps 5.1. |
| Region seeds and briefs | Prose by design. R3 and R6 move what they held that a table should. A SAFE seed's `Law` fines, and a WILD seed's crossing time, are left: the first is read only by the referee, and the second is derivable from typed `at` once sheet-maps lands. |
| `Procedures.md` | A document the ruleset reads, not a table. Its prices and units are what C1, C2 and R5's checks read from. |

---

## 6. Order

This plan lands after sheet-maps' T3.2, which edits `Common_Schema.md` and the DANGEROUS
and SAFE schemas first. R6 waits for it. The rest is independent of sheet-maps and could go
first, but landing it after avoids two plans editing the same files at once.
`implementation.md` is written from the approved set.
