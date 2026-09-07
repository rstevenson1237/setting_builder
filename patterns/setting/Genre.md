# Setting - Genre

## Decides
The seed-and-narrow flow that produces GENRE.md's customizable spine: a pool of specific
genre references, three rounds of narrowing questions that pick one, and what axes still
get dialed once it's picked.

## Read at
Step 1a, before anything else - GENRE.md is the first artifact in the build.

## Spec

```
GENRE
  20-30 Seed - discrete, specific genre references: authors, single books or series, and
        TTRPG lines - never a genre label alone. Each is stated as both the specific thing
        and the general tropes it fulfills
  3     Rounds of narrowing questions, from the user's general request down to one chosen
        reference
  1     The chosen reference, restated in GENRE.md's own identity paragraph as both the
        specific thing and the general tropes it fulfills
  1     Q2 - a set of binary/dial axis questions, answered together, defaulted to what the
        chosen reference implies and dialed elsewhere only where the user wants to diverge
  3-5   Axis bullets in the finished GENRE.md, each a named constraint with a one-line
        elaboration, drawn from the chosen reference and Q2
  1     A short paragraph stating what player characters are here, stated the way GENRE.md's
        B/X-Conan default states it - not heroes, not the resolution of anything
  1     The fixed "What a line has to earn" three tests, reproduced verbatim from
        `templates/Genre.md` - never reauthored per genre
  1     A naming-convention line, settled by Q2 rather than assumed
```

**This is the one place seeding is intentional.** Every other artifact's worked examples in
this library are illustrations to be varied from; the Seed pool below is the opposite - it
exists specifically to be carried forward into `setting/Setting.md`, `setting/Tags.md`
(step 1b), and the compiled tier-2 pattern files beyond, the same way a Region Overview's
claims are meant to be cashed out by its locations. A named, specific reference gives every
later step real material - an actual body of work with its own creatures, factions,
objects, and texture - instead of an abstract family label that has to be invented from
nothing at every step that touches it.

## Seed - 20-30 specific references

Not a family, not a mood - a **named, real thing**: a specific author's body of work, a
single book or series, or a specific tabletop RPG's own genre. The pool below is a starting
menu, kept in this file and refreshed as taste and availability change, spanning enough
different corners of fantasy that Round 1 has real distance to work with. A user's own
reference, named freehand and passing the eligibility test below, is always valid - the
pool is a menu, not a ceiling.

**Authors** (the reference is their body of work, not one title):

- **Robert E. Howard** - pulp sword-and-sorcery: a barbarian's raw vitality against
  decadent, doomed civilization.
- **Fritz Leiber** - Lankhmar-style low fantasy: wit, squalor, and thieves' guilds sharing a
  city with gods who take contracts.
- **Jack Vance** - baroque far-future decadence: magic as a dwindling, jealously hoarded
  resource in a world too old and tired to care.
- **Michael Moorcock** - the doomed sorcerer-champion: cosmic law-vs-chaos balance carried
  on the back of one ruinous protagonist.
- **Clark Ashton Smith** - ornate decadent doom: magic as poison, empires already rotting
  when the story starts.
- **Gene Wolfe** - unreliable far-future-as-myth: a narrator who cannot be fully trusted,
  in a world where technology has become religion.
- **Mervyn Peake** - crumbling ritual-bound grotesquerie: a castle whose ceremony has
  outlived its reason, and a nobility rotting inside it.
- **China Miéville** - weird biology-industrial fantasy: monstrous cities, remade bodies,
  politics that bite.

**Single book or series**:

- **Glen Cook's The Black Company** - grunt's-eye grimdark: mercenaries chronicling their
  own compromises while serving a power they didn't choose and can't defeat.
- **Steven Erikson's Malazan Book of the Fallen** - continent-spanning empire fantasy:
  buried gods, common soldiers, and a history too vast for any one character to see whole.
- **Joe Abercrombie's The First Law** - morally bankrupt heroic fantasy: war as machinery,
  and nobody in it is who the story first suggested.
- **George R.R. Martin's A Song of Ice and Fire** - dynastic low-magic war: succession,
  betrayal, and a supernatural threat everyone in power is too busy to notice.
- **N.K. Jemisin's The Broken Earth** - apocalyptic-geology fantasy: an oppressed
  power-caste and a world that periodically tries to kill everyone on it.
- **Andrzej Sapkowski's The Witcher** - monster-hunter-for-hire fantasy: folk-horror
  creatures, political rot, and a job that pays badly for a reason.
- **Susanna Clarke's Jonathan Strange & Mr Norrell** - genteel returning-magic fantasy: a
  world that forgot how to be magic, remembering badly and at a cost.
- **Katherine Addison's The Goblin Emperor** - court-intrigue fantasy: an outsider thrust
  into a throne and a bureaucracy built to grind him down.
- **Ursula K. Le Guin's Earthsea** - true-name wizardry: balance, consequence, and power
  that is always a debt against something.

**TTRPG lines**:

- **Mörk Borg** - apocalyptic doom-metal fantasy: a dying world on a lit fuse, played out
  in the time it has left.
- **Dolmenwood** - fairy-tale-gone-feral folk horror: an English wood with its own laws,
  older and stranger than the villages at its edge.
- **Troika!** - baroque absurdist science-fantasy: a dying, bureaucratic multiverse played
  for wit as much as danger.
- **Into the Odd / Electric Bastionland** - industrial-magic collision: expeditions run as
  business ventures into a world where the strange is a resource.
- **Wolves Upon the Coast** - Bronze-Age-myth-adjacent raiding fantasy: blood-price, oath,
  and gods who still answer.
- **Ultraviolet Grasslands** - psychedelic silk-road fantasy: a caravan crossing a dying
  magical world for profit and curiosity in equal measure.
- **Symbaroum** - corrupting-wilderness fantasy: an ancient forest reclaiming a fallen
  empire, and the price of taking anything out of it.
- **Forbidden Lands** - Viking-adjacent survival fantasy: a cursed, depopulated land and
  the logistics of simply staying alive in it.
- **Warhammer Fantasy Roleplay** - grim-and-perilous low fantasy: corruption seeping into
  ordinary life, and career over vocation.
- **Yoon-Suin** - hallucinatory river-delta fantasy: a slug-oil economy, decadent
  city-states, and a mythic geography that doesn't behave.
- **Trophy Gold** - cursed-wilderness delving fantasy: greed as the actual monster, and a
  wilderness that corrupts whoever takes from it.
- **Best Left Buried** - body-horror dungeon fantasy: wounds that don't heal clean, and a
  depth that changes what goes down into it.

## What makes a reference eligible

**It must point to a body of work more broad than the sentence that names it here.** An
author's whole career, a multi-book series, or an actively developed TTRPG line all clear
this bar - each has more texture in it than any one summary can hold, which is exactly what
gives later steps real material instead of an exhausted one-liner. A single short story, a
lone one-shot module, or an isolated image with no world behind it does not clear it,
however evocative - there's nothing left to draw on past the sentence describing it.

**It is stated as both things, never one alone.** The specific reference (a name a person
could look up) and the general trope cluster it fulfills (what it would still be if that
specific name meant nothing to whoever's reading GENRE.md). Naming only the specific thing
assumes everyone at the table has read it; naming only the general trope throws away the
texture the specific thing was chosen for. Both halves of the pool entries above model this
- keep the same shape when the user names their own reference freehand.

## Three rounds of narrowing

Start from whatever the user actually said, however general - "dark fantasy," "something
about a frontier keep," "surprise me." Each round narrows the field; none of them re-asks a
question the last one already answered.

**Round 1 - which corner.** From the user's opening request, offer a short spread across
the Seed pool's different corners - four to six references pulled from visibly different
places in the list above (a pulp author, a grimdark series, a TTRPG line, a decadent-baroque
pick), not four variations on the same one. The user picks a corner, names their own
reference instead, or asks for a different spread if none of these are close.

**Round 2 - which reference.** Within the chosen corner, offer two to four specific
references (if Round 1's pick wasn't already a single reference) alongside one or two
distinguishing dial questions - tone, scale, era, protagonist relationship to power. Narrow
to one or two finalists.

**Round 3 - confirm the one.** State the finalist as both the specific thing and the
general tropes it fulfills, per the eligibility test above, and confirm before moving to
Q2. A user who wants a different finalist gets one more pass through Round 2's remaining
candidate, not a restart from Round 1.

**A user's own reference short-circuits all three rounds.** If they already know what they
want, confirm it clears the eligibility test above and skip straight to Q2 - the rounds
exist to help someone find a reference, not to gatekeep one already in hand.

## Q2 - Binary/dial axes

Answer each as a dial, not necessarily a hard binary - "mostly X, leaning Y" is a valid
answer, and "same as always" is a valid answer too, though an axis answered that way for
every question was probably not worth asking. **Default each axis to what the chosen
reference actually does**, and only dial it elsewhere when the user wants this setting to
diverge from its touchstone - Q2 is where that deliberate divergence happens, not a
from-scratch questionnaire. Suggested axes - add more where the chosen reference calls for
one not listed here:

- **Lethality** - high (death is common and cheap) vs low (survivable, forgiving).
- **Population density** - well-populated (settlements close together) vs scarce (true
  wilderness between isolated points) - the intensity dial on Points of Light itself.
- **Magic level** - high (common, integrated into daily life) vs low (rare, dangerous,
  costly).
- **Authority** - centralized (a real government whose writ runs) vs fragmented (no
  overarching rule of law).
- **Tone** - grim/bleak vs hopeful/heroic; picaresque humor permitted vs played straight.
- **Violence** - graphic and visceral vs implied and off-page.
- **Power curve** - rapid escalation vs slow, grounded advancement.
- **Technology** - primitive (bronze/iron age tools) vs advanced (gunpowder, early
  industry) - independent of magic level.
- **Supernatural visibility** - hidden and deniable (folk horror) vs overt (everyone knows
  monsters are real).
- **Economy** - subsistence/barter vs a real coin economy.
- **Naming convention** - constructed-language-heavy vs a named, disclosed real-world
  inspiration vs sparse/utilitarian.
- **Player origin** - locals defending home turf vs outsiders/arrivals with no prior stake.
- **Death's permanence** - final and irreversible vs resurrection or undeath is a known, if
  costly, option.
- **Religion/cosmology** - gods are active, provable forces vs distant, unprovable, a
  matter of faith.
- **Non-human relations** - humans effectively alone/dominant vs coexisting uneasily with
  rival non-human peoples as equals.
- **Historical legibility** - history is well-documented and known vs mostly lost,
  mythologized, contested.
- **Law and justice** - formal law and appeal exist somewhere reachable vs pure
  might-makes-right, no appeal.
- **Climate/season stability** - stable, predictable seasons vs an ongoing crisis (endless
  winter, drought, an encroaching ice or sea).
- **Scale of civilization** - one known civilization vs multiple rival civilizations or
  empires in living contact.

Answer the axes that actually distinguish this setting from a straight instance of the
chosen reference - an axis answered exactly as the reference would answer it was probably
not worth asking aloud. This list keeps growing rather than being exhaustive.

## Building GENRE.md from the chosen reference

**The identity paragraph states both halves, in that order.** The specific reference first
(named plainly - "Modeled on Glen Cook's The Black Company"), then the general trope
cluster it fulfills, then the one-sentence situation this puts a party into. All three in
two or three sentences total; this is the same dual statement the Seed pool entries model,
now anchored to one chosen reference instead of illustrating the whole pool.

**Axis bullets come from the reference and Q2 together.** Pull three to five constraints
that the reference actually enforces (what Points of Light means for it, what its version
of a Mythic Underworld looks like, what its magic costs) and fold in whichever Q2 axes the
user dialed away from the reference's own defaults. State each as a constraint the way the
current Low Magic / Points of Light / Mythic Underworld bullets constrain, never as mood.

**What a line has to earn** is copied from `templates/Genre.md` verbatim, regardless of
which reference was chosen.

**The location-name exception is fixed regardless of naming convention.** Whichever of Q2's
three naming options is chosen - constructed-language-heavy, a disclosed real-world
inspiration, or sparse/utilitarian - a location's own name is still plain and descriptive,
drawn from the common tongue, not freshly coined, though it may carry a name coined
elsewhere and glossed for the referee. State this the same way regardless of genre.

Tags no longer live in this file - `patterns/setting/Tags.md` owns tag-building now
(what a tag is, the intentionality test, the pool shape), read at the new step 1b right
after this one. What stays here is everything about *choosing and stating the reference
itself* - the tag bank was always downstream of that choice, not part of making it.

## Patterns

**What makes a reference well-chosen** - it names a concrete body of work (an author, a
series, a TTRPG line), not a mood; two referees given only the reference name would build
recognizably similar settings from it; it survives being stated in one sentence per half
(specific, then general) without needing to explain either half to be understood.

**Guardrails, regardless of reference chosen** - low magic does not mean *no* magic unless
Q2 explicitly chose that; points of light does not mean *no* settlements, only that they
don't add up to a governed world; a Mythic Underworld does not require literal dungeons if
the reference wears that trope differently (a nautical reference's underworld may be a
drowned city, a post-apocalyptic reference's a buried machine, an urban reference's the
sewers under the one city that exists) - the *function*, a physical place that is ruin and
chaos made manifest, is the constant across references; its dressing is not.

**Pushing past the Seed pool.** Nothing above requires picking from the list in this file -
it is a menu, not a ceiling, and a user naming their own reference outside it is answered on
its own terms once it clears the eligibility test above. What doesn't move regardless of
reference chosen is the fixed three-test section and the container/data, stub-before-file,
and cash-out mechanics the rest of this framework is built from - those are the load-bearing
parts, not the genre dressing.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
