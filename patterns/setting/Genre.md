# Setting - Genre

## Decides
The three-question flow that produces GENRE.md's customizable spine, and what each axis
must constrain rather than decorate.

## Read at
Step 1a, before anything else - GENRE.md is the first artifact in the build.

## Spec

```
GENRE
  1     Q1 - a broad genre family, then a second pass narrowing it to a specific,
        well-known trope within that family
  1     Q2 - a set of binary/dial axis questions, answered together
  1     Q3 - three written trope proposals consistent with Q1 and Q2, each carrying three
        seed tags - one is picked, or a fourth is requested along a stated axis
  3-5   Axis bullets in the finished GENRE.md, each a named constraint with a one-line
        elaboration, drawn from the chosen Q3 proposal
  25    A Tags section in the finished GENRE.md: short thematic tags built from all three
        Q3 proposals' seed tags plus more in the same vein, giving every later step a wide
        bank to pull three constraining tags from instead of converging on one example
  1     The fixed "What a line has to earn" three tests, reproduced verbatim from
        `templates/Genre.md` - never reauthored per genre
  1     A naming-convention line, settled by Q2/Q3 rather than assumed
```

**This is the one place seeding is intentional.** Every other artifact's worked examples in
this library are illustrations to be varied from; Q3's seed tags, and the wider 25-tag bank
built from them, are the opposite - they exist specifically to be carried forward into
`setting/Setting.md` and beyond, the same way a Region Overview's claims are meant to be
cashed out by its locations. Building a wide bank here, from *this run's* actual answers to
Q1 and Q2, is what keeps every later step's three tags a real pick rather than a reach for
whatever fixed example a pattern file happened to show - the failure mode a single vivid
worked example invites, however many times that example gets varied.

## Q1 - Broad genre, then trope

**Part A - broad genre family.** Offer a short list of broad fantasy-RPG genre families,
weighted toward OSR's own territory but not limited to it - pushing past classic fantasy is
fine when the user wants it:

- **Classic Fantasy** - the default: 1970s-80s tabletop fantasy, a points-of-light frontier,
  Tolkien-adjacent-but-grimier, Conan-esque sword and sorcery.
- **Weird / Gothic Fantasy** - folk horror, cursed bloodlines, a land that is wrong rather
  than merely dangerous.
- **Post-Apocalyptic / Science-Fantasy** - a fallen high-technology age read as myth, ruins
  that are machines, magic that is misunderstood science.
- **Nautical / Archipelago Fantasy** - islands, drowned coasts, ships as the only safe
  ground.
- **Desert / Silk-Road Fantasy** - caravans, oases, a hostile interior between rich cities.
- **Frozen / Frontier-North Fantasy** - ice, isolation, a hard season that is itself the
  antagonist.
- **Urban Intrigue Fantasy** - one city, factions instead of wilderness, the dungeon is
  underneath it.
- **Mythic / Fairy-Tale Fantasy** - the old stories taken literally and made dangerous
  again.

A user's own family, named freehand, is always valid - the list is a starting menu, not a
constraint on Q1 itself.

**Present Part A in two stages, not one crowded list.** Split the eight families across two
short rounds of four rather than forcing all eight into a single prompt - a shorter list is
easier to weigh honestly, and the two-stage shape (a strong first four, then "or one of
these instead") reads better than a single wall of options. **The two rounds are
alternatives, not a compound question** - if a response somehow answers both at once, that
is ambiguous by construction; confirm which one was actually meant before moving to Part B
rather than guessing, or treating it as a blend unless the user says so themselves.

**Part B - narrow to a trope.** Within the chosen family, name a specific, well-known trope
- specific enough that two different answers would produce visibly different settings.
Illustrative, not exhaustive: *Classic Fantasy* → a border keep on the marches, a lost
colony, a dying kingdom's last province. *Nautical* → a pirate-haunted archipelago, a
drowned empire's remaining islands, a whaling frontier. *Urban Intrigue* → a city built in a
dead god's ribcage, a free port with no crown, a city one season from famine.

A trope is well-specified when it constrains Q3 below. If any of three unrelated settings
could still fit the trope as stated, narrow it further before moving on.

## Q2 - Binary/dial axes

Answer each as a dial, not necessarily a hard binary - "mostly X, leaning Y" is a valid
answer, and "same as always" is a valid answer too, though an axis answered that way for
every question was probably not worth asking. Suggested axes - add more where Q1's genre
calls for one not listed here:

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

Answer the axes that actually distinguish this genre from a generic instance of Q1's
family - an axis that doesn't change anything downstream was a wasted question. This list
keeps growing rather than being exhaustive; a genre that needs an axis not named here
should get one invented for it on the spot.

## Q3 - Three trope proposals

Using Q1's trope and Q2's dial answers, write **three** candidate proposals. Each is a
trope, not a setting - no proper nouns, no specific history, no named places or people (that
is `setting/Setting.md`'s job, at step 2a, once one proposal is chosen). Each carries:

- A one-sentence pitch: the situation the trope puts a party into.
- **Three seed tags** - short, thematic, and *constraining* the same way `setting/Setting.md`'s
  own tags must constrain (see `patterns/setting/Setting.md`). Unlike a worked example in a
  template, these are meant to be reused as a running start rather than merely illustrated -
  seeding here is intentional, which is the whole point of doing it at this step instead of
  leaving it to accident later.
- What the trope has that a generic instance of Q1's broad family does not.

**The three proposals must differ from each other along at least one Q2 axis each.** If all
three read as the same trope in different window-dressing, Q2's answers were not actually
used to generate them. Present all three; the user picks one, or asks for a fourth along a
named axis.

## Building GENRE.md from the chosen proposal

The chosen proposal's pitch becomes the genre-identity paragraph. Its three seed tags,
plus whichever Q2 axes actually mattered, become the 3-5 axis bullets - each stated as a
constraint the way the current Low Magic / Points of Light / Mythic Underworld bullets
constrain, never as mood. Its naming-convention answer becomes the naming-convention line.
**What a line has to earn** is copied from `templates/Genre.md` verbatim, regardless of
which proposal was chosen.

**Building the Tags section.** Pool all nine seed tags from the three Q3 proposals - not
just the chosen one - and add enough more in the same vein, drawn from the same Q1 trope and
Q2 axis answers, to reach twenty-five. Every tag must pass the same intentionality test as a
seed tag (below): traceable to this run's actual answers, not filler that would fit any
generic instance of Q1's family. This bank is what `setting/Setting.md` and every later
step's own three tags are drawn from, so it needs real range - a mix of places, objects,
customs, and pressures, not twenty-five variations on the same image.

## Patterns

**What makes a trope well-specified (Q1B)** - it names a concrete situation (a border, a
season, a founding, a collapse) rather than a mood; two referees given only the trope name
would build recognizably similar settings from it; it survives being stated in one sentence
without needing a proper noun to anchor it.

**What makes a seed tag intentional rather than accidental (Q3)** - it traces back to this
run's actual Q1/Q2 answers. If a proposal's three tags could have been generated without
reading this run's Q1 and Q2 at all - if they'd fit any Classic Fantasy border-keep setting
equally well - they are decorative, not seeded, and Q3 has failed at the one job this step
exists for.

**Guardrails, regardless of genre chosen** - low magic does not mean *no* magic unless Q2
explicitly chose that; points of light does not mean *no* settlements, only that they don't
add up to a governed world; a Mythic Underworld does not require literal dungeons if Q1
chose a family where that trope wears different dressing (a nautical genre's underworld may
be a drowned city, a post-apocalyptic genre's a buried machine, an urban genre's the sewers
under the one city that exists) - the *function*, a physical place that is ruin and chaos
made manifest, is the constant across genres; its dressing is not.

**Pushing past OSR.** Nothing above requires 1981 B/X specifically - Q1's family list is a
menu, not a ceiling, and a user naming their own genre outside it is answered on its own
terms. What doesn't move regardless of genre chosen is the fixed three-test section and the
container/data, stub-before-file, and cash-out mechanics the rest of this framework is built
from - those are the load-bearing parts, not the genre dressing.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
</content>
