# Setting Judgement Check - 2026-09-04, Brackvaen, first full pass at end of build

Run across `setting/` at every level, following `templates/Setting_Judgement_Check.md`,
after step 4d completed all three regions and all five registries.
`tools/validate_setting.py` reports 0 errors and 1 warning, and the warning is correct
behaviour (B.6's mundane exit back to B.3 is the far side of an already-triggered Secret).

Brackvaen holds together. The spine - salt does not let go, debt is weighed and inherited,
Old Rede letters are obeyed by people who cannot read them - reaches every level and cashes
out into things a party can pick up: the eleven pillars at C.7 and their copies through the
pans, the fourth board rack at A.9, the ninety feet of deteriorating hand at C.23. The genre
holds; there is no authored plot anywhere in it, no commonplace magic, and no central
authority - the Assize is explicitly a settlement about salt being asked to do a
government's work and visibly failing.

Five things need attention, and two of them are the same failure: something promised at
region level that the locations underneath never deliver.

---

## Setting-level

- **Discrete and discoverable, not vague: Needs Attention.** The setting is built almost
  entirely from concrete, findable objects, and where it is specific it is exceptionally
  so - the tide board at A.5 with three winters of readings four feet below every year
  before them; the wear at C.10 that stops dead six feet outside the room; the two of nine
  cords at B.3 that record a reach not sounded in eighteen years, their last knots reading
  deeper, deeper, deeper, and then stopping. Position and dimension are stated
  consistently: every location gives a size and a shape, features say which wall or corner
  they sit in, and no two exits in any location read identically.

  The failure is in one place and it is the region's own central discoverable.
  `setting/region/C.md` states that every opening in Siwapelu carries the Old Rede
  character for *immo* cut into the underside of its cap stone, and that "a party that
  starts checking cap stones will find the character present on every threshold in the
  complex except three, and those three are the whole of what this region has to say." The
  Unique Treasure at C.24 depends on the party having done exactly that, and says so: "a
  party that has been checking cap stones since the stair will understand that they have
  found one." But of roughly thirty-eight arches named in Exits lines across the
  twenty-four rooms, only eleven state the cap character or its absence. Twenty-seven say
  "corbelled arch in the east wall" and stop. A referee running C.9, C.11, C.16, C.18 or
  C.21 has no prompt to mention the thing the region is built on, and a party checking caps
  gets silence rather than confirmation - so the evidence for "every one except three" is
  never actually laid down. This is a one-line-per-exit fix and it is the highest-value
  edit available in the setting.

  Two smaller items. Region B has three exits that name no destination - B.1's causeway
  running west out of the region, B.2's four miles of unstaked wading east toward the
  flats, B.3's "no fixed way leads on from here". All three are correct for a point crawl
  and well written; none has a form in `templates/Location.md` and none is visible to the
  validator. Separately, B.3 Ghutrrun has no stated approach at all: its own Exits line
  says no fixed way leads on, and `setting/region/B/Connections.mmd` connects it only to
  its Secret child, so nothing in the setting says how a party reaches the one Vingash
  fastness a Marchman has ever been invited onto. Roaming is the intended answer and it is
  never written down.

- **Genre held across levels: Confirmed.** This is the strongest thing about Brackvaen.

  *Low Magic.* There are exactly two magical objects in forty locations, and both are
  priced in the way GENRE.md asks. The Selora Lamp burns where nothing else will and its
  cost is that it removes the guttering flame that is the Gorm track made visible - a party
  carrying it walks into step five in good light and excellent spirits. The Immo Cap cannot
  be taken without bringing down the only arch out of the deepest room anyone has returned
  from. Everything else strange in the setting is a Truth behaving consistently rather than
  a spell: salt keeping what is put in it, the gorm collecting below the waterline, cut
  letters being obeyed.

  *Points of Light.* Torsgaard exists in spite of the fen rather than beside it, has no
  walls because the fen is the wall, and has no smith, no healer, no priest and no lord.
  Lindmarn is unsettled and stays that way for stated reasons. Nobody governs anything.

  *Mythic Underworld.* Siwapelu is a lid rather than a mine, and the setting never says so
  in a document - it says so in the architecture, in the drainage built to keep the lowest
  course flooded forever, and in three blank cap stones. That is the genre's best form.

  *Situations, not plots.* Every hook is a standing condition. Region A's Situation moves a
  rung a season whether or not the party engages. All three factions want things they
  wanted before the party arrived; the Faelhond do not know they caused the water to drop,
  the Vingash do not know why it dropped, the Assize will not read its own board eleven,
  and none of those is waiting to be resolved. The three Quests are work offered, and each
  states an obstacle rather than a sequence.

- **Recurring elements actually recur: Needs Attention.** Three problems of different
  sizes.

  *The treasure tables.* Five d20 tables were written in full at step 2h, and across forty
  locations there are six citations, all of them Table I or Table II. Tables III, IV and V
  are never cited by any location in the setting. That would be a minor imbalance if the
  region overviews had not promised otherwise: `setting/region/C.md` says Siwapelu "leans
  hardest on `setting/Treasure5.md` and `setting/Treasure3.md` - Odarath silver and copper
  in quantity, grave-plate from a people who left no graves, unset stones", and
  `setting/region/B.md` says anything off an Odarath stone is Table III and bog oak and
  pelts are Table IV. None of that reaches a room. `patterns/setting/Treasure.md` calls
  Table V "the only table where a single result should be able to change a party's plans"
  and `patterns/dangerous/Treasure.md` assigns it to "high weight, and the room the rest of
  the region is arranged around" - and Siwapelu's three high-weight rooms cite, between
  them, one Table II pull. The reason anyone goes down the stair is stated in the region
  overview and is not in the dungeon.

  *The Bestiary.* Ten of the twenty entries are never named in any location file. Most of
  those ten are legitimately handled at region level or on B's Encounter table - a WILD
  population is met by the table, not keyed to a landmark - but one is not. The Drowned
  Chorus is 9d6+4, one of the two entries the party is meant to be frightened of, and
  `setting/region/C.md` places it specifically "in the third course's flooded runs". C.17,
  C.18, C.19 and C.20 are the flooded third course and none of them mentions it. It exists
  in the region overview and as entry 3 on the Danger table, and a referee running those
  four rooms has no prompt for it.

  Related and smaller: creature naming in Features drifts from the Bestiary entry names.
  `templates/Location.md` says to "name the creature directly by its `setting/Bestiary.md`
  entry name within the Feature - no separate citation syntax needed", but C.1 writes
  "**Faelhond:** ... 3d6 each" rather than naming Faelhond Digger, and B.3 writes "Eleven
  Vingash live here" rather than naming Vingash Reedwatcher. The stats get restated inline
  instead, which is what the Bestiary exists to prevent.

  *The Named Creatures.* `patterns/setting/NamedCreatures.md` states the entry criterion
  plainly: "A slot here is earned by recurrence. An individual that appears once is a
  Bestiary creature with a name in its Feature line." Five of the six rows appear at exactly
  one location - Gellen Torsling (A.2), Druva Halmling (A.7), Vetha Naugling (A.9),
  Zhakur-of-Nine (B.3), Odaranu (C.10). Only Ondtla Faelling appears at two, A.10 and C.1,
  and she is the best entry in the file for exactly that reason. The other five are all
  excellent writing and all earn a row on the file's *other* stated ground - "heard of
  before met", which Vetha (rumour 17) and Zhakur (region B's Creatures field) genuinely
  do. The tension is in the pattern rather than the content, and is recorded in
  `checks/PatternJudgementCheck.md`; the content fix, if one is wanted, is easy, since
  Zhakur, Ondtla and Odaranu are all mobile by their own descriptions.

  What does recur, and well: the three-notch Assize device appears at A.1, A.2, B.1 and on
  Table I; the grey salt smear appears at A.7, A.10 and in the Bestiary's Faelhond Digger
  Sign; the bitter-iron rings run from B.3 to B.6 to the Sump-Kin entry and into
  Zhakur-of-Nine's Remembers line; the groove runs faint at C.3, six inches deep at C.13,
  and is the whole of C.15. Faction identity is consistent everywhere it appears, which is
  what `patterns/setting/Factions.md` asked for and got.

---

## Region A - Torsgaard (SAFE, d10)

- **Region reinforces the setting: Confirmed.** Every setting-level element is visibly
  present and load-bearing. The Salt Assize of sixty years ago is the region's central
  institution; the Gell Year of eighteen years ago is a live feud between families who lost
  pans and families who kept them; the three-years-ago water drop is the Situation. All
  three Truths that bear on a settlement - salt keeping, debt attaching to goods, the
  Brined as a category of person - are the region's actual mechanics rather than colour:
  the weigh-house sees every haul, a dead stranger's kit carries weight, and forty Brined
  work, drink and lodge in the holding without being able to inherit. The People field's
  absences - no smith, no healer, no priest, no lord - do more work than its presences and
  are exactly what `patterns/region/Safe.md` asks for.

- **Locations reinforce this region: Needs Attention**, on two counts, against a strong
  baseline. The Situation lands visibly at eight of ten locations (fresh lead at A.1, the
  summons and the unclaimed death at A.2, mis-stamped barrels at A.3, Sallow's short-crewed
  rank at A.4, the tide board at A.5, the pan-crew corner at A.7, the whole of A.9, the
  cook fires at A.10), and the two that do not - A.6 and A.8 - are the region's clearest
  liner notes. Prominence variance is good: three locations at two features, four at three
  or four, three at five. The topology is a correct shallow hub, ten locations for a d10.

  *The People roster carries no people.* `patterns/region/Safe.md` is explicit that this
  field "carries the roster... **who is here**", and `patterns/safe/People.md` is explicit
  in return: "Draw from the roster; do not invent a cast... If somebody is needed who is
  not on the roster, add them to the roster." `setting/region/A.md`'s People field names
  trades, absences and standing, and not one individual. Seven named individuals were then
  invented at locations - Halmen Weldling, Gellen Torsling, Druva Halmling, Vetha Naugling,
  Naugen Gelling, Bracka Druvling, Ondtla Faelling - and none was added back. They are
  consistent with each other and with the region, so nothing has gone wrong in the fiction,
  but the mechanism that was supposed to guarantee that was inverted, and a referee reading
  the region overview to find out who is in Torsgaard is told about trades rather than
  people.

  *The settlement type is never stated.* `patterns/safe/Settlement.md` requires a type
  from {steading, thorp, village, town, seat}, and says "the gate is what a type cannot
  hold... it is the type that tells the party what to expect from the next place they
  find." No file in `setting/` states one. Reconstructed, the two halves disagree:
  Torsgaard's four hundred people put it at the bottom of **town**, and its holdings are a
  **village** or less - no walls (stated, and for a good reason), one lodging house, no
  temple, no smith, no healer, no garrison, no court. That gap is defensible and is
  arguably the most Points-of-Light thing about the place, but it is currently undeclared,
  so nobody can tell whether it is a deliberate departure or an accident. State the type
  and state the departure.

## Region B - Lindmarn (WILD, d6)

- **Region reinforces the setting: Confirmed.** Nessekire is the region - eighty square
  miles of standing water over a drowned grid of the Odarath's own pans, so the setting's
  four-hundred-year-old catastrophe is literally the ground. The Vingash are here in force
  and their knowledge (the barrier did not fail) is the region's most valuable
  conversation. Salt-keeping shows up as the Cured Man's range and the Sump-Kin's
  eighteen-year tenancy; Old Rede shows up at B.1's milestone and B.4's pillar. The
  Terrain field does the heavy lifting `patterns/region/Wild.md` demands of it: the water
  is not a gradient but a grid of chest-deep cuts between knee-deep walls, and that single
  fact governs every movement decision in the region.

- **Locations reinforce this region: Confirmed.** Six locations for a d6, and the
  classification split is 3 landmark / 2 hidden / 1 secret - within the 50-60 / 30-40 /
  10-20 bands. Depth is carried the right way: each of the three landmarks has a child
  rather than a heavier entry, which is precisely what `patterns/region/Wild.md` prescribes.

  Every hidden and secret connection traces back to a stated detail at its parent, which is
  the criterion most likely to fail and does not: B.4 is reached from a squared shape
  sighted north-north-west from B.1's milestone, six hundred yards off; B.5 from the one
  break in B.2's four-foot tide crust, low on the north face, where something punt-wide has
  been dragged through repeatedly; and B.6 from a full Clue/Trigger/Payload at B.3 - eleven
  iron rings laid facing water nobody looks at, a question or a returned ring, and an elder
  who names the reach and describes the channel accurately while asking the party not to
  go. All three are legible before the party knows there is anything to find.

  The one gap is the approach to B.3 itself, noted under Setting-level: nothing states how
  a party reaches the fastness. The seasonal swing - reed at eight to ten feet closing
  sightlines to nothing in summer, flat and open for miles in winter - is stated in the
  region and honoured at B.1, which is the right place for it.

## Region C - Siwapelu (DANGEROUS, d8)

- **Region reinforces the setting: Confirmed**, and this is where Brackvaen pays off. The
  three occupancies `patterns/region/Dangerous.md` asks for are all present and all
  legible: the Odarath built it, Nessekire took it, the Faelhond squat it, and only the
  third knows it is third. The eleven pillars at C.7 explain, physically, why boundary
  stones cut by illiterate Marchmen are obeyed - which is a setting-level Truth given a
  mechanism rather than a justification. The salt across the threshold at C.23 and the
  ninety feet of one instruction repeated four thousand times explain what the complex is
  for. Nothing in the region is told to the party; all of it is cut into something.

- **Locations reinforce this region: Needs Attention**, on the cap-stone motif above and
  three structural items.

  The class mix is exactly on spec - 3 high, 8 medium, 13 low across 24 rooms at a d8,
  against the 10/35/55 the pattern gives for a region this size - and the low-weight rooms
  earn their class: C.3's faint groove that becomes C.13's six-inch one and C.15's whole
  reason for existing, C.4's draught in a sealed dead end, C.21's nine hundred bands with
  eighteen yellow ones at the top. `patterns/dangerous/Low.md`'s five node roles are read
  rather than ignored.

  *C.9's node role is wrong, and the file says so twice in two ways.* The role table in
  `setting/region/C/Connections.mmd` marks C.9 Doraianu a divide, and C.9's own entry says
  "there is nothing to choose between them by looking, which is what makes this a divide
  rather than a branch." But C.9's two onward ways reconverge - C.10 to C.12 to C.13 to
  C.16, and C.11 to C.16 - so by `patterns/dangerous/Low.md`'s definitions it is a branch:
  "everything returns here, so the choice is reversible and the cost is time." The prose
  under the same graph names C.19 as the region's divide and is right. C.19 is written
  correctly as one, with both ways legible on evidence. The fix is to relabel C.9 a branch
  and rewrite its one sentence; the room itself works either way, since its exits are told
  apart by the drainage channel's direction rather than by looking.

  *C.9 describes four arches and lists three exits.* The Feature line reads "Four openings
  off the gallery, two north and two south", and the Exits line gives one north ("first of
  the two on that side"), one south, and the east ramp. The graph has three edges. Two
  stated openings lead nowhere, are not in Exits, are not Features with triggers, and are
  not in `Connections.mmd` - so a party that walks the gallery counting doors gets an answer
  the region cannot honour. The validator cannot catch this because it checks Exits against
  edges and not Feature prose against Exits.

  *Three medium-weight rooms carry no challenge.* `patterns/dangerous/Medium.md` guarantees
  one, obvious, and drawn from {creature | trap}: "medium weight means the location presents
  **one thing to deal with**, and presents it plainly." Five of the eight do - C.1 the
  Faelhond, C.10 Odaranu, C.17 the Brine Eel, and C.11 and C.16 both a hazard arising from
  the region's own condition, which the file's Patterns list explicitly allows. C.5 Peluora,
  C.19 Azzakire and C.24 Sizoreth carry none. All three are good rooms - C.5 holds the
  pump key and forty Odarath tools, C.19 is the region's divide, C.24 is the deepest room
  anyone has come back from - and all three read as set-pieces without a thing to deal with.
  C.23, a high-weight room, is the same case: `patterns/dangerous/High.md` guarantees a
  challenge from {creature | trap | mystery} and C.23's is the decision to turn around,
  which is thematically the point of the region and is not any of the three. Either these
  four rooms want a challenge added, or the two class files want their challenge sets
  widened to include a mystery and a choice - which the rooms themselves make a good case
  for.

  Feature-level Secrets run about half rate. `patterns/dangerous/Secrets.md` gives 50% at a
  low-weight dead end, 30% at other low weight, 40% at medium; across 21 low and medium
  rooms that is roughly eight, and there are five with a full Clue/Trigger/Payload - C.2's
  lit niche, C.4's draught, C.11's bright pins, C.22's unverdigrised sockets, and C.16's
  wedged block. Two of the three low-weight dead ends carry one, which is the number that
  matters and is correct. The rate is light rather than clustered, and every one that
  exists has a genuinely legible clue.

---

## Open Items

1. **Carry the cap-stone motif into the Exits lines.** Twenty-seven of thirty-eight arches
   in region C do not state whether their cap carries the *immo* character. It is the
   region's central discoverable, the C.24 Unique Treasure depends on the party having been
   checking, and the region overview promises the character is present on every threshold
   but three. One clause per exit. Highest-value edit in the setting.

2. **Cite Tables III, IV and V somewhere.** No location in Brackvaen cites them. Region C
   promises Table V and Table III explicitly and its three high-weight rooms deliver one
   Table II pull between them; region B promises Table III for anything off an Odarath
   stone and Table IV for bog oak and pelts. Add a Table V citation at C.7 or C.15, a Table
   III at C.7, C.19 or B.4, and a Table IV where B's bulk-and-distance problem actually
   bites. Until then three of five tables are written and dead.

3. **Key the Drowned Chorus to a room.** It is 9d6+4, it is placed by the region overview
   in the flooded third course, and none of C.17, C.18, C.19 or C.20 mentions it. Its Sign
   - the gorm thickening fast enough to kill a lamp in under a minute, standing water
   moving against the fall of the ground - is exactly the kind of thing those rooms are
   already good at, and it is the warning the party's whole chance depends on.

4. **Put the cast in region A's People roster,** and state Torsgaard's settlement type
   along with the way it departs from that type - four hundred people with a village's
   holdings and no walls. Both are required by `patterns/region/Safe.md` and
   `patterns/safe/Settlement.md` and neither is currently anywhere.

5. **Fix C.9.** Relabel the node role branch rather than divide in
   `setting/region/C/Connections.mmd` and in the room's own sentence, and reconcile "four
   openings" with the three exits the room and the graph actually have.

6. **Record C.10 Wosaora in `setting/Language.md`.** It is the one coined proper noun in
   the setting that never got written back, and the write-back is what all three
   `Naming.md` files call not optional. The roots are already present: *wosa* (flesh, the
   living part) + *-ora* (the place where), which is a good name for that room and worth
   having on the record.

7. **Decide about the nine unused coinages.** `setting/Language.md` carries Gellyald,
   Brackstad, Mornhalm, Urweld, Skeirling, Meselaani, Kangzhin, Rrikgash and Narrur, and
   none appears anywhere else in the setting. `patterns/setting/Language.md` describes the
   file as growing *from* coinages made elsewhere; these went the other way and never
   landed. Several are good and want a home - Skeirling is the knife every pan crew
   carries, Urweld is the holding's best material, Mornhalm is a soured western pan. Either
   use them or let them go.

8. **Consider the medium- and high-weight challenge question in region C** (C.5, C.19,
   C.24, C.23). This is a judgement call between editing four good rooms and widening two
   class files, and it should be decided deliberately rather than left as a silent
   deviation. See `checks/PatternJudgementCheck.md`.

9. **State B.3's approach,** and decide what `templates/Location.md` should do with the
   three region-B exits that leave the map. Both are recorded in
   `checks/TemplateJudgementCheck.md` as template gaps; the content side is that one of the
   setting's best locations currently has no written way in.
