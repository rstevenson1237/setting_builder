# Vertical Slice - 9 Locations from the Tag Pools

Nine locations - one SAFE, one WILD, one DANGEROUS, for each of `tags_fantasy.md`,
`tags_scifi.md`, `tags_apoc.md` - generated in clean-room isolation from the real Carrdun
setting, to see what the three-facet tag pools actually produce once a location has to be
written from them.

## Method and deliberate deviations

This is a prototype, not a real generation pass, and it skips real dependencies
`templates/Location.md`'s Context normally requires:

- **No real Region Overview or gazetteer stub.** Each location invents a one-line settling
  (a settlement name, a Ruin's setting, a High-weight room's setting) instead of reading
  one. Position/Exits cite invented, unbuilt sibling locations by name - clearly marked, not
  meant to imply a finished region.
- **No `setting/Bestiary.md`, People roster, or Language.md.** Creatures are described
  inline (which `dangerous/Creature.md` and `wild/Creature.md` both explicitly allow when no
  Bestiary entry fits), and the SAFE Commerce spec's "a person, drawn from the region's
  People roster - never invented here" is violated on purpose - there's no roster to draw
  from in isolation, so a name is invented and flagged.
- **Fantasy uses this repo's real `GENRE.md`.** Sci-fi and post-apoc have no real GENRE.md
  in this repo, so each location assumes the one-paragraph genre-spine already stated at the
  top of `tags_scifi.md` (Mothership) and `tags_apoc.md` (Fallout) as its GENRE.md stand-in.

Everything else follows the real pattern files as written: `safe/Settlement.md` +
`safe/Commerce.md` (Kind, held constant across all three SAFE examples so the comparison is
fair) + `safe/Dressing.md` + `safe/Secrets.md`; `wild/Landmark.md` + `wild/Ruin.md` (Kind,
held constant) + `wild/Dressing.md` + `wild/Secrets.md`; `dangerous/High.md` +
`dangerous/Dressing.md` + `dangerous/Secrets.md` + `dangerous/Mystery.md`, weight held
constant at High across all three DANGEROUS examples.

**Tags were hand-picked, not randomly rolled**, one per facet per location, chosen so the
three tags could plausibly share one location (per every Dressing file's own Integration
rule) - the point of this slice is to see what a *coherent* draw produces, not to stress-test
random combinations yet.

---

# Fantasy (Robert E. Howard / Conan)

## SAFE - Kind: Commerce, Prominence: working

**Tags drawn:** Institution/Condition - *Caravans*; Agent/Threat - *Debt Collector*;
Site-Type - *Counting House*

```
A.1 **The Tallyhouse** - *Caravans, Debt Collector, Counting House*
A low stone counting house where every caravan pays its weighing fee before the gate opens
to the market beyond. The **ledger clerk** keeps a longer memory than anyone paying him
would like.
*Twenty feet on a side, one door to the yard and one to the strongroom behind. Built for
this - the walls are thick enough to muffle an argument, and the floor is kept swept clean
of the mud everyone tracks in from the caravan yard. Smells of tallow and old paper; the
scales in the corner click faintly whenever the wind gets under the door.*
**Tallyman Orsk:** Weighs and taxes every caravan's cargo; keeps two ledgers, and only
shows travelers one of them.
**The Open Ledger:** Storage at 2cn/day, weighing at 1cn/load, a letter of passage for 5cn
- no credit extended, ever.
**The Locked Ledger:** Records who actually owes the Tallyhouse, and Orsk answers to
whoever holds that debt above him.
**The Debt Collector's Visit:** A hard-eyed collector comes monthly for what the locked
ledger says is owed - and asks after names, not coin. (Quest: The Locked Ledger)
**Exits:** low door, north wall -> the caravan yard; iron-bound strongroom door, east wall
-> A.2 The Grain Tower
```

## WILD - Kind: Ruin, Classification: landmark

**Tags drawn:** Institution/Condition - *Totem Claim*; Agent/Threat - *Sorcerous Exile*;
Site-Type - *Watch Cairn*

```
A.1 **The Sentinel Cairn** (landmark) - *Totem Claim, Sorcerous Exile, Watch Cairn*
A drystone watchtower, roofless and leaning, crowns the only high ground for miles.
Bird-skulls and knotted cord ring its base - a **totem line** marking ground a local clan
still claims as its own.
*Forty yards north of the ford, on the only rise in sight. Raised two generations back by
clan-builders to watch the river approach; the roof went in a storm nobody living
remembers, and the inner stair has slumped to rubble. Smells of cold ash - someone still
fires the beacon here - and the wind never fully stops at the top.*
**Totem Line:** A ring of bird-skulls and knotted cord at the base; crossing it uninvited
is noticed, and answered.
**Beacon Pit:** Ash still warm some mornings, though no one's been seen lighting it in
living memory.
**Warded Sill:** tell: the doorstone's carvings are worn smooth but for one glyph; the worn
glyph -> drops anyone through the rotted floor beneath; the untouched glyph opens it clean.
(Lore: The Exile's Ward)
**Exits:** slumped inner stair, west wall -> down into the cairn's lower chamber,
unmapped; a cleared path, south -> A.2 the ford
```

## DANGEROUS - Weight: high

**Tags drawn:** Institution/Condition - *Tomb-Warden Order*; Agent/Threat - *Feral
Guardian*; Site-Type - *Ossuary*

```
A.1 **The Warden's Ossuary** (high) - *Tomb-Warden Order, Feral Guardian, Ossuary*
Row upon row of the dead are stacked here by rank, watched over by an order that outlived
every one of them. The **bone-warden** still walks its rounds, and no longer knows the
difference between an intruder and an heir.
*Sixty feet, vaulted, the dead stacked in niches numbered by the Tomb-Warden Order's own
rank system. Decayed - dust and settling stone, but nothing here shows signs of force.
Corbelled ceiling ribbed in black stone unlike anything quarried nearby, the builders' own
signature repeated nowhere else in the region. Smells of dry dust and old tallow;
footsteps carry twice as far as they should.*
**Bone-Warden:** A robed, faceless construct that patrols by rank-order and attacks
whoever stands where rank says they shouldn't.
**Rank-Stone:** A dais niche, empty of bones, carved with a rank no living warden answers
to; standing in it halts the Warden mid-step.
**Sealed Niche:** Bricked over rather than left open, marked with the one rank higher than
any other - and sitting on the Warden's own patrol route. (Treasure V, d20)
**The Last Rank-Holder:** (Named Creature: Verashi, the Tomb-Warden) A warden fragment
that still remembers being someone; it wants its bones moved to the empty niche.
**Exits:** low corbelled arch, west end -> A.2 the sealed vault; collapsed gap, ceiling,
north corner -> the surface, unmapped
```

---

# Sci-fi (Mothership 1e)

## SAFE - Kind: Commerce, Prominence: working

**Tags drawn:** Institution/Condition - *Black Market*; Agent/Threat - *Corporate Spy*;
Site-Type - *Scrapyard Dock*

```
A.1 **Dock Nine** - *Black Market, Corporate Spy, Scrapyard Dock*
A salvage dock where hull plate and parts change hands with no manifest asked for. The
**broker**, Yevrin, moves anything for the right price - and the wrong questions get you
nothing.
*Forty feet of open dock behind a rated blast door, cargo racks bolted to both walls.
Repurposed - this was a company inspection bay before the company stopped caring. Smells
of ozone and scorched metal; the overhead lights buzz on the same failing ballast as the
rest of the ring.*
**Yevrin's Rates:** Hull plate at 8cr/sheet, O2 scrubbers at 40cr, passage off-ring
negotiated, cash only.
**What's Not For Sale:** No weapons, no bio-samples - Yevrin's one rule, enforced
personally.
**The Unlisted Crate:** A sealed company crate nobody's claimed; Yevrin won't say how he
got it.
**The Company Man:** A quiet regular who asks careful questions - not a customer, a
corporate spy logging who trades here. (Quest: Who Sent Him)
**Exits:** rated blast door, aft -> A.2 the ring's mess hall; scarred hatch, dorsal -> the
docking umbilical, unmapped
```

## WILD - Kind: Ruin, Classification: landmark

**Tags drawn:** Institution/Condition - *Distress Beacon*; Agent/Threat - *Signal Ghost*;
Site-Type - *Derelict Hull*

```
A.1 **The Long Silence** (landmark) - *Distress Beacon, Signal Ghost, Derelict Hull*
A derelict hull drifts nose-down against a rock, its distress beacon still cycling the
same automated call after who knows how long. Something answers the hail sometimes, and
it isn't the ship.
*Two hundred yards of broken hull, half-buried in ice-choked rock. Adrift for decades -
micrometeor scarring across the whole starboard face, plating peeled back like foil in
three places. Smells of stale recycled air where the hull still seals; the beacon's
carrier tone is audible on any open channel within a hundred yards.*
**The Beacon:** Still transmitting its original distress call, decades stale - and
lately, a second voice rides the same frequency.
**Boarding Scar:** A breach amidships, cut from outside, not blown - somebody got in on
purpose, once.
**Crew Manifest:** Still racked in the airlock; every name crossed out but one.
**The Second Voice:** Speaks in the crew's own manifest names, always one step ahead on
comms; answering back by the wrong name draws it closer.
**Exits:** cut breach, amidships -> the interior corridors, unmapped; scarred docking
collar, bow -> A.2 the debris field beyond
```

## DANGEROUS - Weight: high

**Tags drawn:** Institution/Condition - *Black-Site Research*; Agent/Threat - *Xenoform
Infestation*; Site-Type - *Containment Ward*

```
A.1 **Ward Seven** (high) - *Black-Site Research, Xenoform Infestation, Containment Ward*
A containment ward built for research the company never filed. Something is still alive
in the far cell, and the failure light on its door has been blinking longer than anyone's
been here to see it.
*Thirty feet, three cells behind blast glass, one observation desk. Abandoned mid-shift -
a coffee cup still sits on the desk, cold for decades. Blast baffles line the ceiling, a
black-site design absent from the station's public blueprints. Smells of sealant and
something faintly organic; the failure light's click is the only sound.*
**Cell Three:** Something pale and segmented presses against the cracked blast glass
whenever the lights cycle; the crack is widening.
**The Cold Terminal:** A dead console logged into a research directive nobody's cleared
to read; the right clearance code silences Cell Three's alarm, the wrong one wakes it.
**The Auditor's Case:** A locked, company-sealed evidence case under the desk, holding
whatever the black-site was proving. (Treasure V, d20)
**The Handler:** (Named Creature: Dr. Osei's Remains) Not fully xenoform, not fully human
anymore; it still remembers the access codes.
**Exits:** sealed blast door, forward -> A.2 the research wing; wide vent shaft, aft,
crawlable -> the station's dead sections, unmapped
```

---

# Post-Apoc (Fallout)

## SAFE - Kind: Commerce, Prominence: working

**Tags drawn:** Institution/Condition - *Trade Caravan Route*; Agent/Threat - *False
Trader*; Site-Type - *Trading Post*

```
A.1 **Rustwater Post** - *Trade Caravan Route, False Trader, Trading Post*
A trading post built from three shipping containers, the only stop on the caravan route
for two days either way. The **postmaster**, a sharp old woman named Yeva, trusts the road
more than she trusts most people on it.
*Three welded containers around a courtyard, one gate facing the road. Repurposed - built
from a pre-war supply depot's own shipping stock. Smells of rust and boiled water; the
wind through the gate gap never fully stops.*
**Yeva's Board:** Clean water at 2 caps/jug, scrap parts by weight, no guns sold - only
traded for.
**What She Won't Do:** Extend credit to anyone she hasn't seen twice; first-timers work a
shift instead.
**The New Buyer:** A well-supplied trader who showed up last week, paying caps too easily
for goods that don't add up.
**The Manifest:** Yeva wants to know what the new buyer is really here for, before he
buys anything else. (Quest: The New Buyer's Manifest)
**Exits:** welded gate, road-facing -> A.2 the crater flats beyond; patched hatch, rear
container -> the scrap yard, unmapped
```

## WILD - Kind: Ruin, Classification: landmark

**Tags drawn:** Institution/Condition - *Contested Ruin Claim*; Agent/Threat - *Rival
Scavenger Crew*; Site-Type - *Broadcast Ruin*

```
A.1 **The Tower** (landmark) - *Contested Ruin Claim, Rival Scavenger Crew, Broadcast Ruin*
A pre-war broadcast tower still stands over the flats, its dish half-collapsed but its
base intact. Two settlements both claim it, and neither's willing to say so first.
*Sixty yards up, visible for miles across the flats. Storm-battered - the dish took wind
damage decades back and never got fixed. Built to broadcast, per the intact transmission
room at its base; nobody's transmitted from it in years. Smells of hot rust in the sun;
wind through the lattice makes a low, constant note.*
**Claim Markers:** Two settlements' paint marks the base, each painted over the other's,
repeatedly.
**Transmission Room:** Equipment mostly intact, one working relay - whoever holds this
tower controls the flats' only radio range.
**Scavenger Crew:** A rival crew already working the base for parts, and not willing to
share the climb.
**The Builder's Plate:** Names the pre-war company that built it - useful to whoever's
negotiating the claim. (Lore: Who Built the Tower)
**Exits:** buckled service ladder, base -> up into the tower, unmapped; a worn path,
south -> A.2 Rustwater Post, two days' walk
```

## DANGEROUS - Weight: high

**Tags drawn:** Institution/Condition - *Containment Directive*; Agent/Threat -
*Automated Defense Grid*; Site-Type - *Containment Cell*

```
A.1 **Cell Block Delta** (high) - *Containment Directive, Automated Defense Grid,
Containment Cell*
A row of containment cells, sealed under a standing order nobody alive gave. The old
defense grid still answers to that order, and it hasn't been told the war ended.
*Forty feet, six cells behind barred hatches, one control alcove. Active - the grid still
runs, though nothing else on this level does. Military-grade blast shielding, unlike the
civilian sections above. Smells of ozone and old coolant; the turrets' servo whine never
fully stops.*
**Turret Row:** tell: three ceiling mounts track motion, red lenses lit; entering without
the override -> gunfire down the row; the override sits in the alcove.
**The Standing Order:** A terminal still displaying a containment directive, sealed
decades ago, naming a subject in Cell Four; clearing it by the book unlocks the row -
clearing it wrong fires every turret at once.
**Cell Four:** Whatever the directive was protecting, still sealed behind the one hatch
the grid won't open on its own. (Treasure V, d20)
**Exits:** sealed barred hatch, north -> A.2 the reactor chamber; grid-covered access
shaft, south -> the surface, unmapped
```

---

## Observations

**All three facets did real structural work in all nine, not decoration.** In every case
Institution/Condition shaped the room's organizational history (rank-order niches, a
company research directive, a caravan route's own economics), Agent/Threat became the
actual mechanical challenge, and Site-Type was the room itself - none of the three ever sat
as an inert label competing with the prose. That's the result this slice needed to see:
the tag pool doesn't just color a location, it gives the model something concrete to build
the Feature list *out of*, at the point where a blank class-file roll would otherwise have
to invent from nothing.

**Genre register held with no bleed.** Re-reading all nine together, nothing in the sci-fi
or post-apoc set could be mistaken for a reskinned fantasy room, or each other -
"corbelled ceiling ribbed in black stone" reads nothing like "military-grade blast
shielding" or "welded shipping containers," which is the same result the raw tag-pool
overlap check already showed, now confirmed at the level of finished prose rather than
just vocabulary lists.

**A genuine finding for Plan 4: Agent/Threat doesn't map 1:1 onto "creature."** Apoc
DANGEROUS's *Automated Defense Grid* tag resolved mechanically as a **trap** (the Turret
Row uses `dangerous/Trap.md`'s exact tell format), not a creature, even though the tag
reads agent-like. The other two DANGEROUS Agent/Threat tags (*Feral Guardian*, *Xenoform
Infestation*) did resolve as creatures. This means Plan 4's pre-assignment pass can't
assume an Agent/Threat tag always feeds the Creature slot - it needs to stay agnostic
between creature/trap/mystery the same way the class file's own Challenge line does, and
resolve which one only once 4c's own roll lands.

**Two honest craft misses, worth flagging rather than quietly fixing:**
- `wild/Dressing.md` requires *Size and shape* and *Position within the region* as two
  separate mandatory lines. The fantasy WILD entry did both ("Forty yards north of the
  ford" is a real bearing). The sci-fi and post-apoc WILD entries conflated position into
  the size line ("Two hundred yards of broken hull..."; "Sixty yards up...") and never
  stated a bearing from an entry or another Landmark. Left as written, not silently
  patched, because it's a useful data point on its own: this is an easy line to drop when
  a location's premise (a derelict adrift, a tower on flat ground) doesn't obviously
  suggest "a bearing from what."
- `safe/Commerce.md`'s "what this place cannot do, and where it sends them instead" is
  fully satisfied in the post-apoc SAFE entry (credit refused -> work a shift instead) but
  only half-satisfied in the fantasy and sci-fi SAFE entries (states what's refused, never
  states where that sends the party). Both are real spec misses, not stylistic choices -
  flagged rather than corrected after the fact, since a real 4c pass should be expected to
  make this same mistake sometimes and `checks/SettingJudgementCheck.md` or
  `tools/validate_setting.py` is the place that should be catching it, not a
  after-the-fact author pass.

**Not tested here:** the actual `setting/Tags.md` generation mechanism (these tags were
hand-drawn, not rolled by a template following a Spec), Plan 3's Kind axis (DANGEROUS Kind
doesn't exist yet, so Site-Type did double duty as both flavor and de facto room-purpose),
and Plan 4's pre-assignment pass (there's no sibling location for any of these nine, so
there was nothing to distribute *against*).
