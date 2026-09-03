# Hex Describe Table Analysis

A study of the supplied random-table corpus (`table.txt`) against this repository's
templates and patterns. **No framework files were changed by this analysis** - this is a
findings report only.

---

## 1. What the corpus is

The file is the *default table* for **Hex Describe**, written by Alex Schroeder and
dedicated to the public domain (stated in its first two lines). Hex Describe is the
descriptive half of a two-part toolchain: Text Mapper draws a hex map and tags each hex
with a terrain keyword; Hex Describe consumes those keywords and expands them into prose
through a weighted, recursive substitution grammar. It is, structurally, the exact
problem this repository solves with a model instead of a grammar.

### Scale

| Measure | Count |
|---|---|
| Named tables (`;name` headers) | 2,079 |
| Total weighted entries | 36,188 |
| Lines / bytes | 40,720 / 939 KB |
| `X stats` tables (creature statblocks) | 169 |
| `X name` tables (name generators) | 83 |
| `X desc` tables (room dressing by room type) | 58 |
| `X companions` tables (lair guard rosters) | 22 |
| `X decoration` tables (per-deity iconography) | 21 |
| `X treasure` tables (hoards typed by owner) | 19 |
| `X boss` / `X dungeon` / `X encounter` / `X feature` sets | 16 / 16 / 15 / 22 |

For comparison, this repository's entire authored guidance - `GENRE.md`, all 17
`patterns/`, all 16 `templates/`, `STEPS.md` - is 979 lines. The corpus is roughly 40×
larger, and essentially all of that mass is **leaf vocabulary**: the concrete nouns,
materials, smells, trades, dishes, and named things that our patterns instruct a model to
produce but never supply.

That asymmetry is the frame for everything below. Our unit of authorship is the *whole
location file*; theirs is the *sentence fragment*. Fragments compose and accumulate;
whole files do not. So the corpus is not a competitor to our approach - it is a catalogue
of the specific vocabulary and structural moves our patterns currently leave to the
model's discretion, and therefore the places where our output regresses to the mean.

### The grammar (relevant because it encodes design decisions)

```
;table name
3,text with [other table] references and [1d6+1] dice
1,alternative entry            # first field is the weight; 0 disables an entry
```

Beyond plain substitution the engine carries a small but consequential vocabulary of
operators, each of which corresponds to a design capability:

| Operator | Uses | What it buys |
|---|---|---|
| `[same X]` | 454 | Referential consistency **within one description** - the same dragon keeps one name across five sentences |
| `[here X]` | 207 | **Per-hex memory** - a value saved to this hex, retrievable later |
| `[nearby X]` | 80 | **Cross-hex lookup** - fetch (or force the creation of) a value in a *neighbouring* hex |
| `[other X]` | few | A value from a *different, non-adjacent* hex |
| `[store X as Y]` / `[save X as Y]` | 169 | Bind a rolled value to a named slot |
| `[global ...]` | 6 | **Map-wide state** - used to instantiate the three warring factions once, for the entire map |
| `[with X]` / `[and X]` | 303 | Force *distinct* picks from one table in one sentence (no "cloth, cloth and cloth") |
| `[link to adjacent hex]` | - | Emit an actual hyperlink to the neighbouring hex's entry |
| `[capitalize X]`, `[normalize-elvish X]`, `[quote X]` | 37/10/- | Orthographic post-processing |
| `[NdM+K as level]` | ~45 | Roll and format as a character level |
| `[redirect URL]` | 22 | Pull an external NPC portrait or dungeon map image |

The `[nearby]`/`[here]`/`[global]` triad is the single most important thing in the file
and is discussed at length in Finding 1.

---

## 2. Binning the corpus into SAFE / WILD / DANGEROUS

### The honest caveat first

**Hex Describe has no danger axis.** Its axes are *terrain type* × *nesting depth*
(hex → site → complex → room). Danger is a property of individual entries, not of
regions: the same `grass` table that yields "cows grazing in the distance" also yields a
basilisk's poisoned spring and a six-dozen-strong lizard-folk village. Our SAFE / WILD /
DANGEROUS rating is a *referee-facing promise about intensity*, applied region-wide;
theirs is a *terrain label*, applied hex-wide, with intensity rolled fresh each time.

So the binning below is a projection, and the places where it strains are exactly the
places where the corpus is doing something our three ratings cannot express. Those strains
are flagged.

### `;START` - the top-level terrain keys, binned

| Corpus key | Our rating | Basis |
|---|---|---|
| `thorp` | **SAFE d4** | 10-40 humans, a leader, a smith, a settlement event |
| `village` | **SAFE d6** | 50-300 humans, defences, a leader with a class and level, a temple, secret societies |
| `town` | **SAFE d8** | 100-600, keep + wall, a 15-slot tradesperson roster, feuding societies |
| `large-town` | **SAFE d10** | 1,000-6,000, castle, ruler, multiple temples |
| `soil` | **SAFE d4** | Cleared farmland, field detail + animal husbandry - the settlement's hinterland |
| `trees`, `firs` | **SAFE/WILD boundary** | Explicitly "indicate a human settlement"; worked forest. See strain (a) |
| `law`, `chaos` | *no clean bin* | A temple or an elementalist school **overlaid on** a settlement hex. See strain (b) |
| `grass` | **WILD d6** | Open ground; landmark + one incident |
| `bush`, `bushes` | **WILD d8** | Badlands/drylands; forts, outlaws, hobgoblins, a green dragon |
| `hill`, `forest-hill` | **WILD d8** | Gorges, lookouts, treants, ogre hills, barrows |
| `forest`, `fir-forest` | **WILD d8** | Named forest, getting-lost rules, centaurs, ettercaps, wood elves |
| `swamp` | **WILD d10** | Guides required, boats, lizard folk, bog wights, a black dragon |
| `water` | **WILD d8** | Lakes; nixies, froglings, sunken ruins |
| `mountain`, `mountains` | **WILD d10** | Valleys, passes, lindwurms, dwarf forges, necropoli |
| `white mountain` | **WILD d12** | Glacier, ice monsters, white dragon, giant apes; explicitly needs a guide and skis |
| `sand desert`, `dust desert` | **WILD d6** | Deliberately sparse - weight 30 on "nothing here" |
| `[dungeon]` (invoked from any terrain) | **DANGEROUS** | 5/7/10/12/14 keyed rooms, a wandering-monster table, a themed boss |
| Named lair complexes (~20 of them) | **DANGEROUS, small** | See Finding 9 |

### Where the projection strains

**(a) Worked wilderness has no home in our scheme.** `trees`, `firs`, `soil`,
`signs of human activity`, and `signs of human activity in a fir-forest` describe land
that is neither settlement nor wilderness: coppiced stumps, swineherd trails, orchard
clearings, charcoal kilns, a shrine at a crossing. Our SAFE patterns are all
*establishment* patterns (Hospitality, Services, Market Square, Authority) - built things
inside a settlement. Our WILD patterns are all *unclaimed* (a beast's territory, a
hazard, a ruin). Neither covers "a forest somebody is quietly making a living in," which
is the natural buffer between the two and, in Points-of-Light terms, is where most actual
play happens.

**(b) Overlay hexes.** `law` and `chaos` do not describe terrain at all; they add a
temple or a wizards' school *on top of* whatever the hex already is. The corpus routinely
composes a hex from independent layers (terrain + landmark + inhabitant + current event +
deep-time remnant). Our model composes a *region* from locations but composes a
*location* from exactly one pattern bullet - `templates/Location.md` says so explicitly:
"choose one bullet now… and shape the Feature(s) around only that bullet; do not draw on
other patterns." That is a deliberate anti-mush guardrail and it works, but it means we
cannot layer, and layering is how the corpus gets density without incoherence.

**(c) Their dungeons are smaller than ours.** The `rooms` table weights 5 rooms at 5,
7 at 4, 10 at 3, 12 at 2, 14 at 1 - an average of about 7.8 rooms. Our DANGEROUS regions
are 3× the die: 12 rooms at d4, 36 at d12. Their room-content mix, from `room feature`,
is 2/6 monster+treasure, 1/6 trap+treasure, 1/6 special, 2/6 empty dressing - roughly
33% creature, 17% trap, 50% empty-or-dressing, with a boss in the final room and a
themed entrance. **Our framework states no low/medium/high ratio anywhere.**
`templates/Location_Gazetteer.md` defines the three weights and never says how many of
each a region should have. That is a genuine gap, and the corpus supplies a defensible
default (about 1 high, ~50% medium, ~40% low, plus a distinct entrance).

---

## 3. Findings: what it reliably produces that we do not

Ordered by how much a pattern change would improve our output.

---

### Finding 1 - Cross-location state: the errand economy

**What it does.** `[nearby X]` fetches a value from a neighbouring hex, *creating it there
if it does not yet exist*. This turns flavour text into map-wide connective tissue:

- `treasure map` → "map to the [nearby hidden treasure]" / "map of the dungeon *[nearby dungeon name]*"
- `alchemist job` → "*[name]* is looking for *[nearby magic plant]*"
- `patron plot hook` → "*[patron]* is secretly enthralled by the witch *[nearby witch]*"
- `library mission` → "the last visitor to this library was *[nearby book thief]*. Would you retrieve that book?"
- `caravan facts` → "They know rumours about the goings on in *[nearby village name]*, having recently been through there"
- `giant ant queen chamber` → `[here store royal jelly as alchemist quest]`, which a
  *different* hex's alchemist will later ask for by name

The last one is the pattern worth studying: a dungeon's set-piece writes a *demand hook*
into the map, and a settlement elsewhere picks it up as a *supply hook*, with a stated
price (5,000gp) and a stated split (`sharing agreement`). Neither hex knows about the
other at authoring time.

**Where we stand.** We have exactly one cross-location mechanism: `patterns/Keys.md`,
which is a *gate* (object A opens door B). It is well specified and it is the only one.
`patterns/Safe.md`'s **Task** bullet asks for "a specific, statable job, not a vague 'help
us'" but imposes no requirement that the job's *target* be a real place, creature, or
object that exists elsewhere in the setting - and `templates/Location.md`'s Context
section deliberately forbids reading other setting files wholesale, so at generation time
the model usually has no way to name a real target. The predictable result is tasks
pointed at invented, unreachable nouns.

**The gap in one line.** We can gate across locations; we cannot *errand* across them.

---

### Finding 2 - Persistent factions with visual identity and accumulating facts

**What it does.** `history init` runs once per map and instantiates three war parties as
**globals**, each with a generated blazon and a human-readable main colour. Thereafter
`[a war party]`, `[the war party]`, `[a different war party]`, `[the war party blazon]`,
and `[the war party colour]` render the *same* heraldry everywhere on the map. Six
`history text` variants then set the three parties into a specific configuration -
invasion, betrayed alliance, two-front war, a vampire domain in the north - which is
map-wide standing context, not a plot.

`[record war fact]` and `[nearby war fact]` are a shared journal: a corpse-strewn hillside
in the badlands writes

> `[here store captain *[human name]* was last seen in the badlands near *[nearby village name]* carrying the banner of *[the war party]* as war fact]`

and a caravan two hexes over can later repeat that fact as a rumour. **Discovered
information becomes an asset of the map.**

The blazon generator itself deserves attention: it structurally enforces the heraldic
tincture rule ("metal should not be placed upon metal, nor colour upon colour") by
branching on metal-vs-colour rather than filtering afterwards, and it carries the real
vocabulary - escutcheon, lozenge, billet, roundel, annulet, mullet pierced, water bouget,
bendlets sinister, chevronels, indented, dancetty, rayonny, nebuly, engrailed, invected,
embattled, raguly - each with a hover-title gloss.

**Where we stand.** `setting/Factions.md` gives each faction AD, Resources, Knowledge,
Tactics, Reactions, and Goals. It gives them **no visual identity** - no blazon, banner,
colour, sigil, maker's mark, or livery. There is consequently nothing for a location to
show a party that identifies a faction without naming it, which is the primary way
factional presence gets communicated in play ("a torn azure banner, three mullets"). And
we have no journal mechanism: a fact discovered at C.7 cannot be cited at A.3 unless a
human notices and edits both files.

`GENRE.md` asks for "period customs" and "specific, precise vocabulary before accessible,
general vocabulary." Heraldry is precisely that, and it appears nowhere in our patterns.

---

### Finding 3 - The settlement as an economy, not a set of landmarks

**What it does.** A `town` entry emits an ordered roster of shops and offices, each an
independent `X or not` coin-flip: alchemist, antiquarian, cleric, gossip, guildmaster,
herbalist, horse trader, innkeeper, jeweler, moneylender, provisioner, smith, tavern
owner, trader, zealot, plus a factional deputy - then an inner-bailey list of bailiff,
captain, castellan, corporal, marshal, scribe. Entry to the outer bailey costs 1sp per
person. Each tradesperson carries a `townsperson goal` - usually a *secret allegiance* to
one of the three war parties - and the entry closes with an actual referee procedure:

> (For a rumor about allegiances, roll a d10 and a d6. On a d6 of 1-3, tell the truth
> about the tradesperson corresponding to the results of the d10; on a 4-6, lie.)

`local smith` generates a named smith plus a 3-6 item inventory drawn from a `local smith
item` list. The `gossip` table alone is ~300 trade names in alphabetical order (clerk,
clock-maker, cobbler, cooper, courier, crier, cutpurse, dyer, falconer, farrier,
felt-maker, fletcher, furbisher, gong-farmer…), sliced alphabetically so it can slot into
a sorted roster.

**Where we stand.** `patterns/Safe.md` has eleven strong bullets, but each produces **one
landmark**. Because `templates/Location_Gazetteer.md` sizes a SAFE region at about its die
in locations, a d6 SAFE region gets six landmarks total - which must cover hospitality,
services, market, revelry, notices, authority, tension, custom, task, routine, and
aftermath. A settlement therefore reads as six good vignettes rather than a functioning
town, and there is no artifact anywhere that lists *who is in this settlement* the way the
corpus's roster does.

The corpus's insight is that a settlement is a **roster with optional slots**, and the
interesting information is which slots are *empty*. Our Services bullet gestures at this
("any notable gap or specialty") for one shop; nothing does it for the settlement.

---

### Finding 4 - The current situation: a temporal layer over static description

**What it does.** Every settlement description ends with `[settlement event]`, which is a
weighted pull across: a war event, a bard, a dragon hunter, a treasure hunter, a mercenary
company, a trade caravan, a travelling circus, a disaster (flood / plague / famine /
drought / locusts), a fortunate event (harvest / animal / holiday), or devil troubles.
These are **things happening now**, and they change what the place *is* this month:

> Judging is underway for a prize-winning [vegetable] contest, including some of the
> largest you've ever seen: fit for a giant's table.

> With fruits ripening in abundance, the townsfolk have distilled a new spirit… already
> they are in trade-talks with the dwarf [name], who plans to sell it in *[nearby village
> name]*. "Will you travel with me?"

Note the second one closes the loop back to Finding 1 - a fortunate event generates an
errand to a named neighbouring settlement.

Wilderness gets the same treatment at lower rates: `forest event` is weighted 9-to-1
toward *nothing*, with the single non-empty result being "the light elves are on the
march" - a rare, map-significant movement.

**Where we stand.** `templates/Region.md` gives SAFE regions a d6 **Events** table "rolled
on entry and each week thereafter." That is the right idea at the wrong altitude: it is a
region-level table of six terse lines, not a written-in current state that shapes the
location entries themselves. At the location level, `patterns/Safe.md`'s **Aftermath**
bullet is the only temporal pattern we have and it is explicitly *past tense* ("visible
evidence of something that happened recently"). We have no pattern for an **ongoing,
unresolved situation currently occupying a place** - no siege in progress, no festival
underway, no quarantine, no company of soldiers camped outside who have not yet left.

---

### Finding 5 - Consequence chains: situations with a stated trajectory

**What it does.** This is the corpus's best single technique and it is almost invisible
unless you follow the nesting. A `war event` places mercenaries outside a settlement -
and then appends a blockquote drawn from `the presence of mercenaries is a problem`,
which is a table of **escalation states for the same situation**:

- The captain is making them pay for food, but the locals are selling their winter stores.
- Already the mercenaries are drinking far too much; the locals clench their fists and know now is not the time.
- The captain is recruiting - a gold piece a day and a share of the loot - and the young are falling for it; elderly parents weep outside the captain's tent.
- The captain had trouble filling the ranks, so they are now terrorising locals into giving up their children, offering to pay their parents' debts.
- Young [name] has been assaulted and a delegation is with the captain right now.
- Young [name] has been found dead; they want the soldier hanged, and discipline is visibly slipping.

Parallel tables exist for refugees, corpses, and temple influence. Each is the *same
situation* at a different point on a curve, with a named captain (`[same captain]`,
carried by `[store … as captain]`), named victims, and a legible next step.

**Where we stand.** `patterns/Safe.md`'s **Tension** bullet asks the right questions -
"Who's on each side, and what's actually at stake?… Is it escalating, stable, or already
curdling into something worse?" - and supplies no mechanism, no cast, and no examples.
The output is reliably one abstract paragraph about a dispute. The corpus's move is
concrete and copyable: **name the party responsible, name the victim, and state which rung
of the ladder the situation is currently on**, so the referee knows both what is happening
and what happens next if the players do nothing.

---

### Finding 6 - Constructed-language name morphology

**What it does.** Names are built from morpheme inventories, not picked from lists:

- Elvish: 139 prefixes (`achar`, `adertha`, `amartha`, `awartha`, `díhena`, `edledhia`,
  `gwathra`…) × 568 root words × gendered suffix sets (`elvish male suffix`,
  `elvish female suffix`, `elvish neutral suffix`), run through `[normalize-elvish]` to fix
  the resulting orthography.
- Dwarven: 977 male + 255 female name elements, plus `dwarf clan 1/2` compounding and a
  separate `dwarven inscription` table.
- Orcish: `orcish rune 1` × `orcish rune 2` × `orcish rune colour` × `orcish rune location`.
- Settlements: `village name1` (120) × `village name2` (128) × `village name3`.
- Forests, hills, rivers, trails, lakes, gorges, crags, bridges: each a `[X 1] [X 2]`
  compound with its own halves (`forest 1` = Dark/Deep/Murky/Shivering/Whispering/Knotted
  Oak/Thorny Vine…, `forest 2` = Forest/Wood/Copse/Thicket/Weald/Grove).

The consequence is that every elf name in the setting shares a phonology, every dwarf name
shares a different one, and the two are *audibly* different cultures.

**Where we stand.** `GENRE.md` explicitly requires this: "Favor constructed language for
names - invented words and coinages over generic real-world borrowings." We satisfy it one
name at a time, by taste, with no shared inventory. Nothing in `templates/` or `patterns/`
holds a phoneme set, a suffix convention, or a compounding rule for any culture in the
setting. Within a single region our names usually cohere because they were written in one
sitting; **across regions and across sessions they will not**, and there is no artifact
whose job is to keep them coherent. This is the most direct, most mechanical fix available
to a stated `GENRE.md` requirement.

---

### Finding 7 - Room-type vocabulary: 58 dressing tables for 28 named room purposes

**What it does.** `interior room` is a weighted list of *named room functions*, each
delegating to its own `X desc` table with 3-6 concrete dressings:

> Antechamber, Arena, Barracks, Bedroom, Chantry, Chapel, Cistern, Common Room, Crypt,
> Debris Room, Dining Room, Firewood Room, Great Hall, Guano Pit, Guard Chamber,
> Guardroom, Kiln, Kitchen, Larder, Living Quarters, Mined Wall, Mushroom Farm, Nursery,
> Prison Cells, Shrine, Slave Pen, Smithy, Storeroom, Torture Chamber, Vault, Vestry,
> Well, Workshop

Sample (`crypt desc`): "1d4+1 old stone sarcophagi line the wall here. The lid of each has
been removed and cast into a pile." / "Metal doors conceal niches filled with the
picked-clean bones of ancient lords." / "Stacked meticulously along the walls in a morbidly
beautiful arrangement are thousands of bones and hundreds of skulls."

Note the weighting: `interior religious room` carries weight 18 against 4 for each secular
room, so temples, chapels and shrines dominate - a deliberate thematic thumb on the scale.

**Where we stand.** `patterns/Dressing.md`'s **Purpose** section is excellent guidance -
"State what the room was built or used for, and whether that use still holds… A former
purpose is a source of detail on its own (tool marks, worn grooves, leftover fixtures)" -
and supplies **zero example purposes**. `patterns/Dangerous_Low.md` compresses all 28 room
types into a single bullet: "Dungeon room that once served a mundane purpose, now decayed
or abandoned."

One bullet standing in for 28 room types is why low-weight rooms in generated output
converge on the same four or five (storeroom, guardroom, collapsed passage, shrine). The
fix is not a new pattern - it is a *vocabulary list* attached to the existing Purpose
section.

---

### Finding 8 - Empty rooms that are still worth entering, and a stocking ratio

**What it does.** `empty dressing` is 33 entries of *stuff in a room with no encounter, no
trap, and no treasure*: cobwebs; small organised mounds of sand; a heap of rotten tubers; a
midden; phosphorescent fungus glowing balefully; rat tunnels; a minor rockfall, the
remaining ceiling seems stable enough; a partial cave-in and a half-buried skeleton;
thousands of dead insects that crunch underfoot; a crate of rotten furs; an abandoned
backpack containing a salvageable 50ft hemp rope; a doll lying inside a dingy crib; a
slaughtered pig hanging from a hook; a small bag with a collection of teeth.

`special` adds twelve larger set-dressings for the same purpose - pools of coloured
liquid, smashed terracotta statues, frescoes, a magic mouth reciting a story, a room
filled waist-high with coloured mist, runes gouged into the wall spelling a dwarf's name,
a stairwell down into a maze of unmappable corridors filled with the skeletons of past
visitors.

The file also records its stocking discipline in a comment:

> Moldvay Unguarded Treasure Stocking: Monsters have treasure on a 1-3 (50%), Traps on a
> 1-2 (33%), and Empty rooms on a 1 (16%).

**Where we stand.** `patterns/Dangerous_Low.md` describes exactly this room ("with debris
or remains that reward careful looking without demanding action") and supplies no
inventory. And as noted in §2(c), **we state no ratio of low/medium/high at all** - our
gazetteer defines the three weights and never says how many of each a region needs. The
corpus gives us a defensible default and a rationale for it.

---

### Finding 9 - The lair: a 4-8 room complex generated as one coherent unit

**What it does.** Roughly twenty named complexes are generated as single artifacts with
internal logic. `giant ant lair` is the clearest:

> mound (with 1d3+1 radiating deer-wide paths, and a 20% chance an ant is outside) →
> entrance chamber (50% ants) → two or three tunnels, each with a stated compass
> direction → a `giant ant area` (fungal garden / egg room / larder / new excavations /
> treasure room) → and, always last and deepest, "the air gets hot and humid," the
> `giant ant queen chamber` with the 5,000gp royal jelly

Others in the same family: `goblin town` (entrance, factions, water supply, fight pit,
market, and five separate animal-relation tables - beetles, spiders, weasels, wolves,
each with its own name table); `witch cottage` (cottage type, door, other entry, main
room, cauldron, cellar, attic, annex, prisoner, thrall, familiar); `fire giant fortress`
(opening, courtyard, ground floor, passage, reception, top floor, temple, statues,
guards); `necropolis` (gate, central area, sphinx); `dwarf forge` (three stages, plus a
variant where netherworld elves have taken it over); `ettercap lair` (forest, ground
level, harbour, lake, trading post, brood mother, prisoners); `green tower` (entrance,
two upper floors, top, underwater room, and a `green tower connection` table for how you
even reach it).

Three properties make these work:

1. **One inhabitant group owns the whole complex** - so every room reads as belonging to
   the same household.
2. **The rooms are functionally interdependent** - larder feeds nursery, fungal garden
   feeds the colony, the queen chamber is the payoff the rest exists to protect.
3. **They are session-sized** - four to eight rooms, one expedition.

**Where we stand.** This is the largest structural gap in the report. Our framework has
exactly two scales: the **single location** (`templates/Location.md`) and the **whole
DANGEROUS region** (12-36 rooms). Nothing sits between them.

`patterns/Wild_Hidden.md` gets closest - "A smaller camp, den, or cache belonging to
whatever already occupies the parent Landmark" - but that is one child location, and the
Hidden tier's stated purpose is to flesh out a Landmark, not to constitute a holding.
There is no artifact that says *"locations B.4 through B.9 are one creature's lair; their
contents are interdependent; generate them together."* Consequently a WILD region's
locations are, by construction, a scatter of unrelated sites, and a DANGEROUS region is a
single 24-room dungeon with no sub-structure - no wings, no households, no territory
boundaries within it.

---

### Finding 10 - Traps that state their tell

**What it does.** All 29 entries in `trap` follow one rigid format, recorded as a comment
in the file: `hint; hint; hint → effect; effect`.

> **darts**: walls nicked and holes on the opposing side; raised floor segment indicates
> pressure plate → roll attacks +0 against the first person: 1d4/1d4/1d4

> **deep pit**: a deep pit with a visibly crumbling edge supported by rotting wooden beams
> → 1-2 in 6 it collapses, fall 30ft for 3d6

> **rope trap**: straw covers the floor; sweeping the straw reveals the rope; a curtain
> hides a large stone on a rope above a small well → stepping on the trigger releases the
> stone… loud crash attracts wandering monsters

> **fog chest**: traces of a metallic green condensate all over it; transformation magic
> detectable; a tiny plaque reads "🜁:🜚→🝗" (gold to ashes) → opening it releases fog that
> transforms any exposed metal of the indicated type to dust: armour, unsheathed weapons,
> rings, diadems, bracelets worn

Every trap is *solvable by description*. And `concealed trap` is maintained as a
**separate table** - the corpus distinguishes "a trap you can spot by looking" from "a
trap deliberately hidden to guard treasure," and uses the concealed set only in the latter
role.

**Where we stand.** `patterns/Traps.md` is well built on the resolution side - three impact
tiers, TEST OF CONSTITUTION vs. TEST OF FATE, WOUND vs. CONDITION - and lists twelve
mechanisms. It **never requires a visible tell.** `patterns/Secrets.md` states the
principle precisely - "A Secret without a stated Clue isn't discoverable - it's just a
fact the referee knows and the players can never find" - and Secrets are explicitly a
*separate layer* from traps, so that requirement does not reach them.

The result is a pattern that, followed exactly, produces traps players can only find by
declaring a search or by triggering. For an OSR framework whose whole premise is player
skill over character skill, that is arguably the single clearest defect this analysis
surfaced. It is also the cheapest to fix: one sentence in `patterns/Traps.md`, plus the
hint/effect format, plus the spot-able/concealed split.

---

### Finding 11 - Presence rolled separately from description

**What it does.** `[20% ant here]`, `[50% ants here]`, `[maybe barrow]`, `[maybe island
barrow]`, `[maybe a book]`, `[maybe a sage]`, `[maybe griffon eggs]`, `[maybe there is a
boat]`, and the whole `X or not` family decide **whether something is present** as a
separate roll from **what it looks like**. A described room is not necessarily an occupied
room; a described lair is not necessarily a lair with its owner at home.

**Where we stand.** Every location we generate is written fully populated and statically
occupied. We have no notion of an inhabitant being *out*, of a resource being *already
taken*, or of a feature being *absent this time*. In practice this makes our dungeons feel
staged rather than lived-in, and it removes the standard OSR consequence of wandering
monsters - that the thing you're avoiding is not in the room it "should" be in.

---

### Finding 12 - Lair logistics: food, water, waste, and young

**What it does.** The corpus asks, consistently, what an inhabitant *eats*, where its
*waste* goes, and where its *young* are: `giant ant larder` + `giant ant larder contents`,
`giant ant food`, `giant ant fungal garden`, `giant ant egg room`, `giant ant new
excavations`, `goblin town water`, `druid larder`, `guano pit desc`, `nursery desc`,
`den kill`, `honey pot ants`, `worker ants` vs. `warrior ants`, `mushroom farm desc`,
`forge orc mushroom dish`, `orc cheese` / `orc tofu` / `orc yogurt` (each with its own
adjective and texture tables).

That last cluster is worth singling out: an entire non-human culture characterised through
its *dairy and fermentation* rather than its violence. It is a strong, cheap technique for
making a humanoid faction read as a people.

**Where we stand.** `patterns/Dressing.md`'s Purpose section covers *built* purpose - what
a room was made for. It does not cover *ongoing living* - what currently sustains whoever
is here. `patterns/Creatures.md` scales a creature's threat to the region's die and says
nothing about its household. So our inhabited DANGEROUS regions have guards, bosses and
treasure but no larder, no water source, no midden, and no young - which is precisely the
set of details that turns a dungeon into somewhere something actually lives, and which
gives players non-combat leverage (poison the well, burn the stores, take the eggs).

---

### Finding 13 - Deep-time layering within a single location

**What it does.** The corpus routinely stacks three occupancies in one place: builder →
later occupier → current squatter.

> "Up in these drylands, a massive fortress built by giants long ago is home to the *[evil
> tribe]* tribe." - and in a sibling entry, the *same* giant-built fortress instead holds
> an outlaw camp.

> "On one of the rock faces you can still see the markings of the old dwarf forge *[here
> dwarf forge]*" → `forge ruin`, with a variant: `dwarf forge taken over by netherworld
> elves`.

> `small landmark` positions things "at the old *[wight realm]* milestone" - a
> throwaway reference to a fallen kingdom, used as a *road sign*.

Supporting this are dedicated deep-time generators: `ruins of the ancients`, `ancient
capital` (beginning / middle / end), `wight realm` (12 kingdom names), `orc war` (12 named
wars - The Resettlement, The War of the Blood Tide, The Great Butchering, The Sunless
Days), `barrow` with its own colour / construction / shape / dig / loss tables.

**Where we stand.** We hold the strata - `setting/History.md` and `setting/Truths.md` -
but `templates/Location.md`'s Context section deliberately excludes them: a location may
consult those files "only to look up a name the stub or region overview already
references - never to pull in new material wholesale."

That guardrail exists for a good reason, stated in the template itself ("deliberately
narrow so the entry stays shaped by its stub and region rather than washed out by the full
setting"), and it should not simply be removed. But its cost is real and worth naming: a
location can only reflect history that its Region Overview happened to mention, so
**history reaches locations only through a single bottleneck**, and any stratum the Region
Overview omits is unreachable at the location level. The corpus's approach - a small,
fixed set of *named* deep-time nouns (a fallen realm, a named war, an ancient builder
people) that any location may cite by name without reading the history file - would thread
this needle without widening the Context section.

---

### Finding 14 - Named minor features used as coordinates

**What it does.** `small landmark` exists purely to give positions a name: "under the
gallows," "under the hanging tree," "at the old *[wight realm]* milestone," "at the barrow
of *[old name]*," "by the tanner's stinking vats," "near [hill name]," "by the *[elf
name]* elf stone." `grass landmark` (21 entries), `hills landmark`, and `signs of human
activity` do the same at a larger scale - a burnt-out roadside toll-booth still smouldering;
seven wind-worn statues of dancing figures; dilapidated driftwood fence posts with the
slats long since salvaged for firewood; several huge clay ovens seeding the air with the
smell of baking bread.

These are not destinations. They are *reference points* - things a referee can say a
location is "half a mile past."

**Where we stand.** `patterns/Dressing.md`'s Position section requires a WILD Landmark to
state where it sits: "a cardinal direction, or a bearing/distance from another named
Landmark or the region's entry point." That works, but it can only reference *other full
locations*, of which a WILD region has only its die's worth. The corpus's approach -
disposable *named* micro-features that are never themselves locations - gives far denser
positional grounding at near-zero authoring cost, and reads much better at the table
("north of the tanner's vats" beats "roughly 400 yards north-northeast of B.3").

---

### Finding 15 - Sensory and material vocabulary as an actual inventory

**What it does.** `smells` is 172 entries. `sounds` is comparable. `sound volume` supplies
eleven registers (faint, muffled, muted, subdued, indistinct, feeble, loud, intense,
clamorous, obstreperous, shrill) and `sound direction` ten bearings (above, ahead,
all-around, approaching, behind, below, distant, off to the left, off to the right,
receding) - so a sound can be placed in space, not just named. Materials get their own
inventories: `masonry mat`, `metal mat`, `precious metal mat`, `stone mat`, `wood mat`,
`cloth mat`, `skin mat`, `hide mat`, `horn mat`, `bone type`, `plant mat`, `paper mat`,
`money mat`, `tool mat`, `handful mat`, `clump mat`, plus `size`, `height`, `length desc`,
`colour` and a per-colour synonym table (`red synonym`, `green synonym`, `grey synonym`…).

**Where we stand.** `patterns/Dressing.md` mandates "at least one sensory detail beyond
the visual - a smell, a sound, a temperature, a texture underfoot" and "Favor a detail
that reinforces the region's theme or the room's purpose over a generic one." It supplies
no vocabulary whatsoever, and there is **no material vocabulary anywhere in the
repository**. `GENRE.md`'s instruction to "reach for specific, precise vocabulary before
accessible, general vocabulary - real architectural terms, medieval weaponry, period
customs and trades" is therefore stated as an aspiration with nothing behind it. Generated
smells converge on damp, rot, and woodsmoke; materials converge on stone, iron, and wood.

---

### Finding 16 - Material culture: food, drink, trade goods

**What it does.** A full culinary stack: `dish` = `rural meat prep` + `food meat` +
`seasoning method` + two `food seasonings` + two `veg prep` + two `food veg`. Around it:
`breads`, `exotic breads`, `bread desc1/2`, `cheese producer` / `cheese texture` /
`cheese portion` / `exotic cheese producer`, `distilled beverage`, `fruit`, `berries`,
`nuts`, `root veg` / `leafy veg` / `vine veg` / `legumes veg` / `wild veg`, `freshwater
fish`, `freshwater shellfish`, `domesticated meats` / `wild meats` / `unusual meats` /
`varmint meats`, `iron rations`, `snack`, `sauces`. Trade goods resolve twice - `trade
goods` picks a category, then `[category] goods` picks the specific commodity, so a
caravan carries "cloth goods, jars goods, and cages goods" resolved to three distinct
actual products.

**Where we stand.** `setting/Treasure4.md` (Luxury and Trade Goods) is a d20 table and is
the closest we come. We have no foodways, no drink, no local specialty, and no
culture-specific cuisine - despite `patterns/Safe.md`'s Hospitality bullet explicitly
asking for "a signature dish" and `templates/Region.md`'s SAFE-only **People** field asking
for "goods or foodstuffs they're known for." Both fields exist; nothing supports them.

---

### Finding 17 - Treasure typed by its owner, and a stated economy

**What it does.** Nineteen `X treasure` tables typed by **who holds it and why**: poor,
average, rich, dead, robber, scout, leader, terror, encounter, unguarded, empty, ancient,
neolithic, dwarven, dwarven stronghold, elf, dragon, valuable grave goods, trap treasure -
plus `leader treasure for fighter` / `for magic user` variants. Values are pinned: a
`gems` d20 table (10 / 20 / 50 / 75 / 100 / 250 / 750 / 1000gp), jewelry at 3d6×100,
royal jelly at 5,000, an elephant tusk at 1d6×100, `junk price` for salvage. Three named
`sharing agreement` terms let an NPC state their cut in their own voice ("I am generous:
two shares for me…" / "I will provide all the expertise: five shares…").

**Where we stand.** Our five Treasure tables are typed by **kind of thing** (Scavenged
Loot, Equipment and Armaments, Gems and Jewelry, Luxury and Trade Goods, Treasure Cache).
`patterns/Treasure.md` then maps each to contexts in prose - "Table II… tied to a person or
creature: a fallen traveler, a guardian, a bandit's kit."

Neither axis is wrong, but theirs makes placement automatic (a bandit rolls robber
treasure; a boss rolls leader treasure) while ours requires a judgement call at every
citation. The genuinely missing piece is not the axis - it is the **stated economy**: we
give values in cn on the tables and nothing anywhere states what a hireling costs, what a
job pays, or how a party splits a haul. `patterns/Safe.md`'s Task bullet asks "What's
offered in return: coin, goods, information, standing?" with no scale to answer against.

---

### Finding 18 - Procedures stated as procedures

**What it does.** The map's header carries `;procedures` - the operating rules, in plain
text, before any content:

> Random encounters are 1 in 6 per day and 1 in 6 per night if you're not behind walls.
> Travel time is 1 hex/day without a trail, 2 hexes/day on a trail. If you're **looking
> for something** that isn't as obvious as a town or village built in plain sight, your
> chance of finding it is 1 in 6 per day; each search party also has to roll for their own
> random encounter. Underground encounters are 1 in 6 every two turns, e.g. whenever
> leaving a room.

The middle clause is the important one: **searching has a stated cost and a stated
chance**, and the cost is another encounter check.

**Where we stand.** `templates/Region.md`'s Layout field states a time assumption per
rating - WILD at 4 hours per action, SAFE untimed, DANGEROUS on the Danger countdown -
which is good and matches the corpus's intent. What is missing is the search procedure.
Our entire WILD tier system (`Landmark` / `Hidden` / `Secret`) is *about findability*, and
nothing anywhere states the odds or the cost of looking. `patterns/Wild_Hidden.md` says a
Hidden location is "found by actually investigating a specific Landmark"; `patterns/
Wild_Secret.md` says a Secret location needs a Clue/Trigger/Payload. Neither says what
"investigating" costs in time slots or what it rolls against - so the tier distinction is
fictional rather than procedural, and at the table it collapses into referee fiat.

---

## 4. What our framework does that the corpus cannot

Stated for balance, and because these are the things not to trade away.

1. **Coherence by construction.** Every one of our locations is answerable to a single
   region overview, and every region to one setting. The corpus's hexes are independent
   samples; a village can sit beside a hex whose contents it has no relationship to. The
   `[nearby]` mechanism patches this locally and cannot produce a *theme*.
2. **A stated genre with active enforcement.** `GENRE.md` filters everything. The corpus
   has no such filter and is, in consequence, tonally omnivorous (see §5).
3. **Exits as a typed, validated graph.** `Connections.mmd` plus `tools/validate_setting.py`
   gives us a checkable spatial structure with normal / hidden / one-way edge types. The
   corpus emits prose adjacency ("a tunnel sloping downward to the north") with no graph
   and nothing to validate against.
4. **Deliberate escalation of stakes.** Our low/medium/high weights and the
   `Lore`/`Keys`/`NamedCreatures`/`UniqueTreasures` registries let content be *placed* for
   dramatic effect. The corpus rolls each room independently; its only escalation is
   "the last room has the boss."
5. **Two-phase authoring.** Steps 4c/4d (stub during location generation, write fully
   afterward) let a Named Creature or a Key be introduced at one location and completed
   with knowledge of every location that references it. The corpus has no second pass.
6. **Judgement checks.** `checks/` reviews for genre drift and cross-level coherence -
   categorically outside what a substitution grammar can do, and the reason a model-driven
   approach is worth the loss of scale.

---

## 5. Genre-fit filter: what not to import

A large fraction of the corpus is flatly incompatible with `GENRE.md` and importing its
*content* would cause exactly the drift `CLAUDE.md` names as this project's main failure
mode.

**Reject outright:**

- **Norse cosmology and planar travel.** `another realm` (Asgard, Alfheim, Midgard,
  Myrkheim, Jötunheim, Vanaheim, Niflheim, Muspelheim), with `road to` / `tunnel to` /
  `exit to` tables for each. Directly contradicts Points of Light and Mythic Underworld -
  a dungeon that is a doorway to a named heaven is not a manifestation of chaos.
- **Named pantheon with relics and iconography.** Freya, Odin, Thor, Mitra, Set, Orcus,
  Hel, Pazuzu, Nergal - each with `relic of X`, `X decoration`, `small temple dedicated to
  X`, `guardian of X`. `GENRE.md`'s Points of Light explicitly denies "an implied central
  authority," and an organised, mapped pantheon is one.
- **High-magic bestiary.** Unicorns, pegasi, treants, dryads, nixies, sprites, froglings,
  tengu, myconids, jinn, marids, ifrits, salamanders, phase spiders, mirror-realm
  vampires. Conan-esque means sorcery is rare, foreign and priced; this is a monster manual.
- **Spell and spellbook apparatus.** 16 spellbook tables, named famous spellbooks per
  school (aeromancer, aquamancer, geomancer, necromancer, pyromancer, vivimancer), an
  appendix of spells, `random 1st level spell`. Low Magic means magic is not a system with
  schools.
- **The moon-monolith teleport network.** A map-wide fast-travel network by full moon.
- **External service calls.** `[redirect]` to portrait and dungeon-map generators - our
  artifacts are plain text by design.
- **Quoted public-domain riddles.** Thirty 18th-century verse riddles pulled from Project
  Gutenberg - correct for that project's licence posture, wrong for `GENRE.md`'s voice.

**Import the *mechanism*, discard the *content*:**

- The **monolith network** is a good structural idea (one recurring object type that links
  many locations, creating map-wide connective tissue with no plot attached). A
  Low-Magic-appropriate object could do the same job.
- The **`[X decoration]` per-deity tables** are a way to give an entity consistent
  iconography across every location it touches. Same idea as blazons (Finding 2), applied
  to whatever our setting actually has instead of gods.
- The **`X or not` slot** and the **`maybe X`** roll (Finding 11) are entirely
  genre-neutral.
- **`;procedures`** (Finding 18) is genre-neutral and directly fills a real gap.

---

## 6. Prioritised training recommendations

Ranked by (impact on output quality) ÷ (size of change). All are pattern/template
additions; none require touching generated `setting/` content or the validator.

| # | Change | Target file(s) | Finding | Cost |
|---|---|---|---|---|
| 1 | Require every trap to state a **visible tell**; adopt `hint → effect` format; split spot-able from concealed | `patterns/Traps.md` | 10 | ~5 lines |
| 2 | Add a **room-purpose vocabulary** (the 28 named room types) to the Purpose section | `patterns/Dressing.md`, `Dangerous_Low.md` | 7 | list |
| 3 | State a **low/medium/high ratio** (~1 high, ~50% medium, ~40% low, + entrance) | `templates/Location_Gazetteer.md` | 8, §2(c) | 1 line |
| 4 | Add **sensory and material vocabulary** behind the existing mandates | `patterns/Dressing.md` | 15 | list |
| 5 | Add **faction visual identity** (blazon/colour/sigil/maker's mark) to each faction | `templates/Factions.md` | 2 | 1 field |
| 6 | Add a **name-morphology artifact** (per-culture morpheme inventories and compounding rules) | new `setting/Names.md` + `templates/` | 6 | new artifact |
| 7 | Add a **lair tier**: N contiguous locations owned by one inhabitant group, generated together, with interdependent contents | new `patterns/Lair.md`; `Location_Gazetteer.md` | 9, 12 | new pattern |
| 8 | Add an **errand mechanism** - a Task must name a target that exists, the way a Key names its lock | `patterns/Safe.md`, `patterns/Keys.md` | 1 | ~5 lines |
| 9 | Add an **ongoing-situation pattern** (present tense, named cast, stated next rung on the ladder) | `patterns/Safe.md` | 4, 5 | 1 bullet |
| 10 | Add **lair logistics** (food, water, waste, young) to the Purpose section | `patterns/Dressing.md`, `patterns/Creatures.md` | 12 | ~3 lines |
| 11 | Add a **search procedure** (odds + time cost) for Hidden/Secret discovery | `templates/Region.md` Layout, `Wild_Hidden.md`, `Wild_Secret.md` | 18 | ~3 lines |
| 12 | Add **named micro-features as positional coordinates** to the Position section | `patterns/Dressing.md` | 14 | ~3 lines |
| 13 | Add a **worked-wilderness pattern** (the SAFE/WILD buffer: coppice, charcoal, orchard, herding, tolls) | new bullets in `Wild_Landmark.md` or a new file | §2(a) | ~6 lines |
| 14 | Add a **settlement roster** artifact (who is present, and which slots are empty) | new template, SAFE regions only | 3 | new artifact |
| 15 | Add **presence-vs-description separation** ("this occupant may be out") | `patterns/Creatures.md` | 11 | ~2 lines |
| 16 | Add a small set of **named deep-time nouns** (a fallen realm, a named war, an ancient builder people) any location may cite without widening Context | `setting/Truths.md` or new | 13 | ~5 lines |
| 17 | Add **foodways** to the SAFE People field and Hospitality bullet | `templates/Region.md`, `patterns/Safe.md` | 16 | ~3 lines |
| 18 | State a **coin economy** (a day's wage, a job's fee, a share split) | `templates/Treasure.md` or `setting/Setting.md` | 17 | ~3 lines |

Items 1-5 are cheap, self-contained, and would measurably change the next generated
region. Items 6, 7 and 14 are new artifacts and should be scoped separately. Items 9 and
13 are the two places where the corpus exposes a *category* of content our patterns
currently have no bullet for at all.

---

## 7. The one-paragraph summary

The corpus and this repository solve the same problem from opposite ends. It achieves
variety through 36,188 authored fragments and coherence through six state operators; we
achieve coherence through a strict generation order and a genre filter, and variety
through the model. The comparison is useful because the corpus's mass is concentrated
almost entirely in the layer our patterns leave empty - **concrete leaf vocabulary**
(room purposes, smells, materials, trades, dishes, heraldic charges, name morphemes) - and
its six state operators encode exactly the three structural capabilities we lack: **lairs**
(a mid-scale unit between location and region), **errands** (content that names real
targets elsewhere on the map), and **current situations** (a temporal layer over static
description). Nothing here argues for changing the framework's architecture. It argues
that our patterns should carry the vocabulary the corpus carries in leaf tables, and
should name the three structural units it has and we do not - and that, separately, two
of our existing patterns have real defects the comparison made visible: traps with no
stated tell, and no stated ratio of location weights.
