# Spec - the location schema, reviewed against the archive

Every proposal has an id and a box. Tick, strike or amend each one. A proposal marked
**depends on** something only stands if that proposal is approved too.

How the schema already absorbs most of the archive:

- **`Secret` (trigger, tell)** stands in for every archived clue/trigger/payload triple.
  That covers concealed details, a hazard's clue, a mystery's act, a hidden cache and a
  secret door. The payload is whatever it is attached to.
- **One-of children** on `Reward` and `Connection` stand in for Treasure's Disposition
  and Guard and Door's Gate, Gate trap and Ward. When there is no child, nothing guards it.
- **`Purpose.signs`** reverses the archive's Foreshadow. The HIGH room lists the rooms
  that point at it, instead of each MEDIUM or LOW room drawing a foreshadow.
- **`Encounter.left` / `far`** take over Encounter's Sign and Lair's Sign and Territory.
- **The Overview** holds what Block, Alarm and Inhabitants used to say per room.

So the archive's colour lines are left out: Tried, Left because, Caught, Unwilling,
Second occupancy and the like. The table at the end of each section lists them. What
follows are the gaps where the schema has no way to say something a player meets.

---

## 1. DANGEROUS - what to pull in

### Schema

- [ ] **D1. A mystery states what a wrong attempt costs.** `Mystery` gains
  `wrong string`. Today it carries only `effect`, the correct act's result. With no cost
  for getting it wrong, pressing every button is free, and the mystery is a chore rather
  than a decision. *(dangerous/Mystery.md "Wrong"; wild/Mystery.md "Wrong"; the
  Mystery/Hazard boundary in both Provides lines)*

- [ ] **D2. Quests get a pathway.** `Location.md` cites `(Quest: Title)`, but no table
  names a quest, so step 4e never writes one. Three changes fix this:
  - `table Quests entry file="setting/Quests.md"`
  - `Quests` is added to `Contents_Type`. The thing a quest is after lies here, which is
    the target end.
  - `Encounter` gains `asks entry Quests opt`. Whoever is met here gives it, which is the
    giver end. A SAFE location uses this most, and a prisoner in a cave can too.

  *(dangerous/Quest.md, safe/Quest.md, wild/Quest.md; patterns/setting/Quests.md "A
  quest with one end is not a quest")*

### Template defaults - `templates/dangerous/Tables.md` Instructions

The defaults below are replaced wherever `BRIEF.md` says otherwise. The rates are the
archive's own.

- [ ] **D3. Hazard damage mix.** 20% Lethal, 40% Damaging, Nuisance the rest. A hazard's
  damage is never raised because its room matters. *(dangerous/Hazard.md TIER and its
  Constraint)*

- [ ] **D4. Reward contents mix.** Treasure I-V 55%, Keys 20%, Lore 20%. The other 5% is
  split across Magic, Unique Treasures, Magical Tomes and Hoards, held to `GENRE.md`'s
  Magic level. Without a stated mix, rewards collapse to the table roll. Region A already
  shows this: four table rolls and one key. *(dangerous/Treasure.md "What", and its reason
  for rating it)*

- [ ] **D5. Connection children are rated per edge, not per side.** About one edge in
  five carries a child. A lock or a guard is decided once and written on both sides'
  entries. *(spec E3 at 9c1354b: gates on 43% of exit-ends because each end drew its own;
  dangerous/Door.md GATE 40% was the rate that produced it)*

- [ ] **D6. What can kill is read before it is met.** An Encounter whose creatures could
  kill a party carries `left` or `far`, and a Lethal hazard's `tell` is in plain view.
  *(dangerous/Encounter.md "Sign ... a room early where Lethality means it could kill
  them"; GENRE.md Lethality)*

- [ ] **D7. Rooms in a block stay distinct.** No two rooms in one block share a `former`,
  and no two hazards in a region share a type. *(dangerous/Dressing.md "Do not reuse a
  purpose already used in this block"; spec E1: one hazard shape six times)*

### Lint - `tools/tables.py`

- [ ] **D8. Keys pair.** Each `Keys: Title` pulled as contents is matched by a
  `Lock key=Title` somewhere in the setting, and each Lock by a pull. While one end is
  missing, the lint warns; once the build is complete, a missing end is an error.
  *(dangerous/Key.md "a Keys row whose far location draws no lock is a dangling thread";
  dangerous/Lock.md "A lock with no Keys row is a wall")*

- [ ] **D9. A key is never behind its own lock.** The location holding a key can be
  reached from the region's entrance without passing a Connection locked by that key.
  This is an error. *(archive/templates/region/Composition.md proof: "no part behind the
  gate it opens")*

### Cleanup

- [ ] **D10.** `patterns/setting/Keys.md`'s Provides still names "its rating's own
  `Key.md`", which is now archived. It should name `patterns/Schema.md`'s `Lock` and
  `Reward` instead.

### Not pulled in

| Archive line | Why not |
|---|---|
| Trap / Environmental / Residual (Parts, Cause, Course, Maker...) | `Hazard_Type`'s two levels name the mechanism. The rest is how the Location file describes it. |
| Damage type (Piercing, Crushing...) | `Hazard_Type`'s leaf implies it (Spike, Fire/Lava, Gas). Step 4f writes it in the forced-damage citation. |
| Mystery Detail 1-3 | The `Secret` tell is the clue it is reasoned from. More detail is the Location file's Feature. |
| Creature Shape, Scale, Demeanour; swarm uncountable | The Overview's Inhabitants and `Encounter.doing` / `reaction` carry them. |
| Faction Position, If lost, Order | The Overview's Alarm holds what happens elsewhere. `Encounter.doing` holds the order. |
| Door Opening / Material / Make / Wear; one-way, vertical | `Connection_Type` and `orientation` ("barred this side", "down a shaft"). |
| Block (Basis, Family, Household) | The Overview's Places and the `Connections.mmd` subgraphs. |
| Low's CLUE and TRIGGER lists | A `Secret` per Connection or Reward covers them. The lists could return as suggestions in Tables.md if rooms come out samey. |
| Treasure Tried, Left because, Lesser thing; Key Used; Lock Forced; Hazard Caught; Lore Survived | Colour. The Location file is free to add it. |
| Residual needs a History event; ward and illusion held to the Magic level | `History.md` is empty unless `BRIEF.md` asks for it. `GENRE.md` already holds the Magic level for every step. |

---

## 2. SAFE - build-out

The archive's SAFE location was a person behind a gate, a transaction, and a hook. Each
part maps onto the schema:

- The person is an `Encounter` with a new `Person` child.
- The transaction is a new `Offer`.
- The hook is D2's `asks`, or a `Reward`.

What the archive split into six Kind files (Commerce, Authority, Social, People, Wealth,
Garrison) becomes `Safe_Type` plus these nodes.

### Schema

- [ ] **S1. `Temple` joins `Safe_Type`.** `BRIEF.md`'s outer bailey has "trade, lodging
  and worship", and the shrine's agent hides at the keep. There is no garrison type: per
  `BRIEF.md`, the garrison is folded into the locations it guards, as `Faction`
  encounters at `Authority` locations.
  ```kdl
  enum Safe_Type Inn Merchant Bank Market Authority Temple
  ```

- [ ] **S2. `Person`, an Encounter child naming someone from the Overview's People
  roster.** `doing`, `reaction`, `want` and `know` then answer archive People, Social and
  Authority as written: never idle, how they meet a stranger, what they want, and what
  they know and won't say. Dangerous gets it for free (a captive, the shrine's agent).
  ```kdl
  node Person {
    name string                   // as the region Overview's People names them
  }
  node Encounter {
    one-of Creature NamedCreature Faction Person
    ...
  }
  ```

- [ ] **S3. `Offer`, what a party can get here and what it costs.**
  ```kdl
  node Offer {
    thing string                  // a good, a service, a word, a permission
    price gloss                   // in coin, or the terms that stand in for it
    contents pull Contents_Type opt   // where the thing is a key, lore, a quest's object
    one-of Secret opt             // sold only to whoever asks the right way
  }
  ```
  *(safe/Settlement.md transaction; Commerce Prices; Authority Hearing; Social Talked to;
  Garrison Lets through; Key Get by; Lore Access)*. An Offer is what only this location
  has. A price the Overview's Services already states is not repeated (`STYLE.md`: said
  once).

- [ ] **S4. `Offer` gains `sends location opt`.** This is where a party asking for what is
  not here gets sent. It ties the settlement's locations to one another. *(safe/
  Settlement.md Cannot / Sends to)* **Depends on S3.**

- [ ] **S5. `Secret` gains `noticed gloss opt`.** It records who learns the secret is
  found, and what they do about it. Every rating can use it, for example the chief seeing
  the chest open. *(safe/Settlement.md Finds out / How soon / Response; safe/Wealth.md
  hidden payload "who notices")*

- [ ] **S6. The Safe folder.**
  ```kdl
  folder Safe type=Safe_Type {
    Locations Location
    Purpose Purpose
    Dressing Dressing
    People Encounter
    Offers Offer
    Rewards Reward
    Connections Connection
    rate Inn Purpose="0-1" Dressing=1 People="1-2" Offers="1-2"
    rate Merchant Purpose="0-1" Dressing=1 People=1 Offers="1-3"
    rate Bank Purpose="0-1" Dressing=1 People=1 Offers=1 Rewards=1
    rate Market Purpose="0-1" Dressing=1 People="1-3" Offers="2-4"
    rate Authority Purpose="0-1" Dressing=1 People="1-2" Offers=1 Rewards="0-1"
    rate Temple Purpose="0-1" Dressing=1 People=1 Offers=1
  }
  ```
  `Purpose` is decided rather than rolled (see S8). `Rewards` is the vault or the
  treasury: what is there to be stolen, guarded by a `Lock`, an `Encounter` or a
  `Hazard`. **Depends on S1-S3.**

### Template - new `templates/safe/Tables.md`

The defaults are replaced wherever `BRIEF.md` says otherwise.

- [ ] **S7. Count from the settlement's size.** The size comes from the Overview's
  SETTLEMENT entry: steading 1-2, thorp 3-4, village 5-7, town 8-12, seat or hold 10-15.
  The type mix follows from what that settlement has. *(patterns/region/Safe.md
  SETTLEMENT)*

- [ ] **S8. Purpose is placed, not rolled.** The location where the Overview's Situation
  shows most carries a `Purpose`, and its `signs` are where it shows in passing. A town or
  larger may have a second. *(safe/Settlement.md "central ... where the region's Situation
  is most visible"; safe/Situation.md)*

- [ ] **S9. Every `Person` is on the roster.** Someone needed and not on the roster is
  added to the Overview, not invented in a row. *(safe/People.md "Never invent a cast")*

- [ ] **S10. Write the transaction, not the room.** `Dressing` stays short. The words go
  to `Offer` and to what people want. *(safe/Dressing.md Constraint)*

- [ ] **S11. Concealment has an owner.** A `Secret` in a SAFE region was put there by
  someone living, who is named in `noticed` or the Overview's Secrets. *(safe/
  Settlement.md "Never conceal something in a settlement that nobody living put there")*

### Lint

- [ ] **S12. `Person name` must appear on its region Overview's People list.** It is an
  error once the Overview exists. **Depends on S2.**

### Not pulled in

| Archive line | Why not |
|---|---|
| PROMINENCE (liner note / working / central) | `Safe_Type` rates set the count of entries, and S8 places the Situation. A third axis would be bookkeeping. |
| DETAIL BUDGET; Dressing Departs, Signs of use | `Dressing.obvious` / `former` / `condition`. |
| Commerce Stock kind, Unusual, Condition; Authority Claim, Limit, Rival, Posted, Custom | One-off colour, or the Overview's Law. Any of it can be an `Offer` or an `Encounter.know`. |
| Faction presence (Want, Known, Return...) | A `Faction` or `Person` encounter, plus the Overview's Secrets. |
| safe/Situation.md (Visible, Worse off, Rung, Next...) | `Purpose.pressure` / `signs`, and the Overview's Situation rungs. |
| Wealth PROTECTION | `Reward`'s one-of (`Secret`, `Lock`, `Encounter`, `Hazard`). |
| Exit "Who may use" | An `Encounter` on the `Connection` (the gate guard), or `orientation`. |

---

## 3. WILD - build-out

`Wild_Type` (Landmark, Route, Hidden, Secret) already replaces the archive's class files.
The Kind files (Ruin, Lair, Natural Feature, Crossing) become what `Dressing.former` and
the location's encounters say. What the schema still needs is a way between places that
is country rather than a door, hazards and mysteries that belong outdoors, and the
Hidden/Secret access rules.

### Schema

- [ ] **W1. `Path`, the WILD connection.** `Connection_Type` holds door makes, so the
  wild gets its own node. It is checked against `Connections.mmd` exactly as `Connection`
  is.
  ```kdl
  enum Path_Type Road Track Trail Ford Bridge Climb Overland
  node Path {
    to location
    type Path_Type
    orientation gloss             // a bearing, or a relation to something in view
    time number                   // in setting/Procedures.md's WILD Time unit
    one-of Encounter Hazard Mystery Secret Lock opt
  }
  ```
  *(wild/Exit.md; wild/Dressing.md Position; patterns/region/Wild.md Terrain "what one
  action buys in distance")*. **The lint** keys its diagram check on the `Connections`
  file and not on the node name, so it needs no change.

- [ ] **W2. Outdoor hazards.**
  ```kdl
  enum Hazard_Type {
    Mechanical Pit Spike Dart Hammer Gas Snare
    Magical Runes Field Attack
    Environmental "Fire/Lava" Water Ice "Ravine/Climb" "Broken/Weak Floor" Bog Rockfall Exposure
    Living Thorns Spores
  }
  ```
  *(wild/Hazard.md MECHANISM set / ground / living)*

- [ ] **W3. Outdoor mysteries.** `Mystery_Type` gains `Stone Tree Pool Cairn`.
  *(wild/Mystery.md Thing: placed / grown / a property of the place)*

- [ ] **W4. The Wild folder.**
  ```kdl
  folder Wild type=Wild_Type {
    Locations Location
    Purpose Purpose
    Dressing Dressing
    Challenges Encounter Hazard Mystery
    Rewards Reward
    Connections Path
    rate Landmark Purpose=1 Dressing=1 Challenges="50%" Rewards="25%"
    rate Route Dressing=1 Challenges="50%"
    rate Hidden Dressing=1 Challenges="40%" Rewards="25%"
    rate Secret Dressing=1 Challenges="40%" Rewards="40%"
  }
  ```
  A Landmark's `Purpose` is its reason to stop. Its `signs` are where it shows from
  elsewhere, such as smoke seen from the road or tracks at the ford. A Route is a stretch
  of the way through, such as a ford, a pass or a bridge, and half of them carry what
  complicates crossing. The Hidden and Secret rates are the archive's; the Landmark's
  Challenge rate goes from 35% to 50%, since `BRIEF.md`'s landmarks are mostly lairs and
  camps. **Depends on W1.**

### Template - new `templates/wild/Tables.md` and `templates/wild/Connections.mmd`

- [ ] **W5. Count and mix.** The count is 2x the die. The mix is 60% Landmark and 20%
  Route, with Hidden the rest; there is at most one Secret, and only where the Overview's
  Secrets names one. *(archive/templates/wild/Locations.md)*

- [ ] **W6. Hidden and Secret hang off a parent.** Each connects only to its parent. A
  Hidden location's `Path` from the parent is visible and easy to miss, and is written in
  `orientation`. A Secret location's `Path` carries a `Secret`, and its diagram edge is
  drawn `-.-`. *(wild/Hidden.md Lead; wild/Secret.md access triple; "A Hidden way in is
  visible and easy to miss; a Secret way in is concealed until acted on")*

- [ ] **W7. Nothing is pristine outdoors.** A `Reward` container states what weather has
  done to it, and lore outdoors is cut, never written. *(wild/Treasure.md, wild/Lore.md
  Constraints)*

### Lint

- [ ] **W8. Access rules.** Each of these is an error:
  - a Hidden or Secret location with more than one neighbour;
  - a Secret location whose `Path` in carries no `Secret`;
  - a Secret location whose parent is itself Hidden or Secret, because that puts it two
    triggers deep.

  *(wild/Secret.md "A Secret location carries no child")*. **Depends on W1.**

### Not pulled in

| Archive line | Why not |
|---|---|
| Kind files (Ruin, Lair, Natural Feature, Crossing) | `Dressing.former`, the encounters, and `Route` for what was Crossing. |
| Creature Doing / Noticed / Limit / Range | `Encounter.doing` / `reaction` / `far`, and the Overview's Inhabitants. |
| Hazard WARNING list; Mystery Price | The `Secret` tell, and D1's `wrong`. |
| Treasure Why here / Reach / Claim; Key How here | The `Reward` container and its one-of child. W7 holds the weathering rule. |
| Dressing Weathered / Position | `Dressing.ambiance`, and `Path.orientation` / `time`. |
| Quest ROLE (waypoint / obstacle / supply / giver) | D2: `Encounter.asks` or `Quests` contents. |

---

## 4. Carried by any approved set

These follow from approval rather than being proposals of their own:

- `STEPS.md` phase 4 names the SAFE and WILD templates, and loses "SAFE and WILD regions
  have no table templates yet".
- `templates/region/Location.md`: the `Offer` and `Path` lines join the Exits and
  Features instructions.
- `tools/validate_setting.py` and `tools/tables.py` are extended for each lint line
  approved (`CLAUDE.md`).
- `README.md` is unchanged except for the new template paths.
