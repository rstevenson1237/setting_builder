# Introspective and implementation plan

Running state, not authority. `STEPS.md` and `patterns/SPEC.md` win wherever this file
disagrees with them. This file exists to be executed and then cut down: each task below
names what it changes and what proves it done, and a task that lands should be struck
here in the same commit. When every task is struck, delete the file.

Written from a full read of this repository at commit `ae492fa` (108 commits, at least
six generated settings wiped and rebuilt), of the predecessor
`rstevenson1237/drakenhold` (66 commits), and of the `Rules_Light_TTRPG_Design_Notes.md`
that project mirrors.

## How to use this file

- **An Opus agent executes one task per session**, in the order given, unless a task says
  it may run in parallel. Read the task, read only the files it names, do the work, run
  `python3 tools/validate_setting.py`, commit with the task id in the subject, strike the
  task here.
- **Phases are ordered by what invalidates what.** Phase 1 changes the prose grammar, and
  every later phase generates prose, so it goes first. Phase 3 changes where pattern
  content lives, and Phase 5 changes what steps run, so neither starts until the grammar
  they will write to is fixed.
- **Nothing here authorises deleting Telar** (the current generated setting) until task
  P1.6 says so. It is the only corpus the checks have been tuned against.
- **The open questions at the end need the user**, and the recommended answer is stated
  for each. A task that depends on one says which, and proceeds on the recommendation if
  no answer has arrived.

---

## Part one: state of the repository

### What exists

| Layer | Files | Words | Role |
|---|---|---|---|
| Authorities (`CLAUDE.md`, `README.md`, `GENRE.md`, `STEPS.md`) | 4 | 4,600 | loaded every session |
| `templates/` | 23 | 12,100 | one per artifact type |
| `patterns/` + `SPEC.md` | 66 | 45,800 | five folders: setting, region, safe, wild, dangerous |
| `tools/` | 5 | 3,950 lines | validator, site, PDF |
| `setting/` (Telar) | 100 | 30,600 | 5 regions, 64 locations, 5 registries |
| `checks/` | 3 | 155 lines | judgement check output |

The framework is 62,000 words. The setting it has produced is 30,600. That ratio is the
first fact worth knowing: two words of rule for every word of output, and a generation
step reads most of the rules every time.

### What a location costs to generate

Read set per `tools/validate_setting.py --read-set 4c`, measured in words the generator
has in context for one location, including `CLAUDE.md`, `README.md` (injected by the
session hook), `GENRE.md`, the region overview, Truths, Procedures, Language and the
template:

| Location | Words in context |
|---|---|
| DANGEROUS medium | 23,900 |
| WILD landmark | 18,000 |

Region E (24 locations) was built across `3a`-`5c` in one PR. At roughly 20,000 words of
context per location plus output, that is the shape of the Pro-plan problem: the budget
is spent re-reading rules, not writing rooms.

### Where the prose is now

The last PR (#41) closed the Feature grammar to `,` and `->`, eight words per segment,
four segments per line. It cut mean Feature length from 42.8 words to 22.3 and cut
"rather than" from 61 of 206 Features to 25 of 209 (46 today across all files). Those
are real gains against the trailing-clause failure the commit describes.

It also produced this, in `setting/region/E/22.md`:

```
**Sealed Air:** Thin and heavy, costing real effort, working hard here counting double
against the, Danger track, except from the dais steps.
```

The comma after "the" is there to pass the segment-length check. `E/20.md`'s "Braced
shut with a timber bar seated, in stone sockets on this side" is the same thing. The
grammar is mechanically satisfiable by breaking English, and the generator found that
out. The rule cut the failure mode it was aimed at and introduced one the checks cannot
see.

### What the six rebuilds were for

| Setting | PRs | What changed underneath it |
|---|---|---|
| unnamed regions A-C | #1-#10 | initial framework, patterns as archetype lists, validator and CI |
| Khirengaard | #11 | first full build to step 4 |
| Brackvaen | #13 | five-folder `patterns/` layout, Spec blocks with rates |
| Sundfall | #16 | word budgets, chains |
| Duen, The Last Writ | #17 | seed-and-narrow Genre questionnaire |
| Fellward / Carrdun | #19-#22 | setting-level pattern consolidation, then the genre/tag reset |
| Telar | #23-#41 | System B tags, blocks, Door, forced damage, Feature grammar |

Every rebuild followed a structural change to `patterns/` or `templates/`, and every one
discarded the previous content rather than migrating it. The framework has been the
variable and the setting the casualty. A template repo inverts that: the framework is
frozen per release and the setting is the only thing that varies.

---

## Part two: what to keep

The agent executing this plan must not tear these down. They are the parts that
work, and several were arrived at twice, here and in Drakenhold independently.

1. **The three tests in `GENRE.md`** and the fixed "What a line has to earn" block. They
   are the right top of the ladder. Drakenhold's `J7` show-don't-tell check is the same
   rule, and the corpus that passes it is the corpus worth playing.
2. **The read-set graph**: `STEPS.md` names a template, a template names its pattern entry
   points, a Spec line names what it draws, and `validate_setting.py` walks it. 65 of 65
   files reachable, zero orphans. This is what makes the library a single tree.
3. **Rated Spec blocks** (`1`, `40%`, `{a | b | c}`). An unrated menu collapses to its
   first option; the rates are what make a key or a piece of Lore get drawn at all.
4. **The four blocks** (substrate, challenge, reward, registry) and their per-rating
   variants (WILD adds access, SAFE has a gate and a transaction). A line that fits none
   of them belongs to another class.
5. **Blocks as the DANGEROUS generation unit**, one functional quarter each, with one
   typed mermaid diagram per block and existence-only diagrams above. Drakenhold's five
   diagram tiers reached the same contract from the other direction.
6. **Two-ended elements as obligations**: a Key's supply end writes a `setting/Keys.md`
   row naming the location it opens, and that location draws the lock at rate 1. Zero
   unconsumed obligations at the close of a build is the invariant that makes a set of
   regions a network.
7. **The container/data split**: a location cites, a registry holds, and registry
   entries are written at 4d with every citing location in view.
8. **`setting/Language.md` as a living root list** with coinage recorded back. Drakenhold
   kept its roots inside Truths and could not receive coinage; this is the fix.
9. **The validator's posture**: strict on format, relaxed on content, a missing file is
   a warning. Plus `--pending` and `--read-set`, which are the closest thing this repo has
   to a handoff document, and better than one because they are derived.
10. **`build_site.py` and `build_pdf.py`**, with the pattern reference page. A finished
    module ships as a site and a PDF from one source with no second copy.
11. **The three judgement checks**, especially `Setting_Judgement_Check.md`'s upward audit
    (claims made at region level must be delivered by rooms) and its Room to Grow list.
12. **Step ids that grow by suffix and are never renumbered.**

---

## Part three: findings

Each finding states the evidence, why it matters against the user's stated targets, and
the task that answers it.

### F1. The prose target is not written down, so every rule aims at a failure instead of at a style

`GENRE.md` says what a line must not be. `templates/Location.md` instruction 5 says what
punctuation it may use. Nothing in the repository says what a good location reads like.
There is no exemplar, no worked example of the target register, and no statement of what
is being taken from *The Hole in the Oak*, *Arden Vul* and *B4 The Lost City*
respectively.

The consequence is visible in the commit history. Each PR from #35 to #41 identified a
prose failure by reading the output, wrote a rule against that failure, and the next
build found a new failure the rule permitted: mood, then trailing clauses, then
unwitnessable claims, then glosses, then comma splices. A generator given a prohibition
list and no positive target will always find the next unprohibited way to be bad.

The three references actually agree on a form, and this repository's template is already
close to it:

| Reference | What it does | What this repo already has |
|---|---|---|
| *The Hole in the Oak* | Room name, one or two italic sentences, then bold-labelled bullets, each one thing. Branches written as `Label: result. Label: result.` with colons | Player Summary, Referee Notes, bold Feature labels |
| *B4 The Lost City* | Numbered rooms, plain referee paragraphs, stat lines and mechanics in parentheses, tiers of the pyramid as blocks | citation format in parentheses, blocks |
| *Arden Vul* | Density: every object has a paragraph, but each paragraph is one object, and the referee text states facts in full sentences with dimensions | Feature decomposition, Referee Notes dimensions |

What none of them do is ban the full stop. The Hole in the Oak's branch form needs a
colon and a second sentence. The grammar in instruction 5 forbids both, which is why a
Feature that wants to say "pressed at the near edge: swings open. Pressed at the far edge:
a reservoir lets go" has to be crammed into one comma-spliced line.

**Answered by** P1.1 (a `STYLE.md` with a positive contract), P1.2 (exemplars the
generator reads), P1.3 (a sentence budget replacing the punctuation ban).

### F2. Feedback becomes a specific prohibition, never a general rule with a check

The user names this directly, and the tree confirms it:

- `GENRE.md`'s standing consequences reached thirteen bullets across #31, #40 and
  #41, each PR adding the rule its own failure needed.
- 40 of 65 pattern files carry Constraints; entries include "Never write a bare 'a
  door'", "Never give a swarm a countable number", "Never let a room that simply ends
  pay out a route off the map". Each is correct, each is one incident, and none has a
  check.
- `templates/Location.md` instruction 5 is 340 words of punctuation law written in one
  PR after one measurement.
- 25 pattern files have an empty Constraints section, which `SPEC.md` says "fills as
  negative patterns are identified". The design is to accrete.

There is no intake procedure. Drakenhold had one (the six routes in
`OPEN_QUESTIONS.md`: strike, direct edit, editorial note, regenerate, ratify, refer
out) and it was the single most effective process document in that repository. This
repository has nothing between "the user said X" and "add a bullet".

The missing rung is the one between the three tests (unfalsifiable by a script) and a
Constraint (too narrow to matter twice). It is a **tell list**: a measurable signature
of a class of failure. "rather than" density, absence claims ("in living memory",
"nobody has"), conclusion tells ("which is why", "proof enough"), glosses (a term
followed by "-" and its definition). The commit messages for #41 already computed
these by hand. Nothing keeps computing them.

**Answered by** P2.1 (a feedback intake with routes), P2.2 (a tell list the validator
reads as data), P2.3 (an audit of existing Constraints into general, exemplar, or cut).

### F3. The tag system is three half-systems, and the genre compile has never run

The user is right that tag work is currently happening inside the pattern files. The
state is:

1. `setting/Tags.md` and `setting/region/[Code]/Tags.md`: flat 25-tag pools, pure
   colour, two tags per stub, "no structural role" by the System B decision in #24.
2. `## Design patterns` in 37 pattern files (about 10,000 words): the actual
   genre-specific content, defined by `SPEC.md` as "rewritten at step 1b from the
   chosen genre reference". A grep for any Telar, Conan or Howard noun across those
   sections finds zero hits. They were written once, by hand, as generic OSR fantasy
   (corbel, lintel, chokedamp, smith, farrier) and have never been compiled from a
   reference. The #24 commit says so: "the existing content mostly already served as
   the compile output; the work here is the structural split, not a rewrite."
3. The rejected System A, recoverable from history at `b6e0bf7`: three tag files
   (`tags_fantasy.md`, `tags_scifi.md` for Mothership, `tags_apoc.md` for Fallout) with
   three facets each (Institution/Condition, Agent/Threat, Site-Type), proven
   genre-portable by a nine-location vertical slice with zero cross-genre leakage, then
   dropped for "OSR/fantasy only for now".

The user wants a B/X 1981 baseline plus parameters (lethality, population, magic, and
genre of fiction up to modern investigative and sci-fi horror). System B cannot do
that: its genre content is inside neutral files, so a second genre means hand-editing
37 files. `patterns/setting/Genre.md`'s seed pool is 100% fantasy. The axis dials in
`GENRE.md` are prose bullets that no Spec rate reads.

**Answered by** P3.1 (genre packs as a separate tree), P3.2 (the B/X 1981 baseline
pack), P3.3 (axis dials wired to Spec rates), P3.4 (a second pack as a portability
regression).

### F4. The rules the setting is meant to sit on are not in the tree, and Procedures drifts from them

The user states that `Rules_Light_TTRPG_Design_Notes.md` is the system-neutral
foundation and this project should "build its shape around it". Drakenhold mirrored it
read-only and referred every mechanical gap back to the rules project. This repository
seeds `setting/Procedures.md` generically at 1c and tailors it at 2h, and the seed has
drifted:

| Topic | The Notes | `setting/Procedures.md` |
|---|---|---|
| Forced Danger | one Test, binary: Complication = Wound, Failure = Wound at disadvantage | `Xd` = number of Tests to pass; 1 = full, 2-3 = complication grade |
| Which die | Constitution = Combat die, Sanity = Magic die, Fate = Skill die | "whichever die fits, flat d6 if none" |
| Wounds | a count against a maximum, permanent, d6 effect table per type | a state; a second of the same kind kills |
| Treasure types | I Scavenged, II Foraged, III Caches, IV Hoards, V Unique | I Scavenged, II Equipment, III Gems, IV Luxury, V Cache |
| Search | a move: Success = 1 secret, Failure = Danger Die advances | "a stated detail investigated is found, no roll" |
| Difficulty roll | 1 fail, 2-3 complication, 4+ success | same |

Some of that drift is deliberate and good (the no-search-roll rule is the framework's
own and better than the Notes' Search move for secrets). But it is undocumented as
divergence, and the location Features cite `(Test of Constitution, 1d, Crushing)` in a
notation the Notes do not define. A referee holding the Notes cannot run the output
without a translation nobody wrote.

The Notes also carry procedures the framework never wires in: the SAFE downtime moves
(Carousing by die, Training, Research, Recruitment, Gather Information at 1 die per
100 cn), the WILD moves (Navigate at 3 miles per hour, Explore, Track, Forage, Make
Camp's three rolls, Camaraderie, Reflection), the DANGEROUS moves (Careful Movement
120 feet, Rushed Movement, Chase, Search, Listen, Rest), Faction Turns with relation
dice, Hireling rates, and the Weather table. Those are the play loop of the game the
module is for.

**Answered by** P4.1 (a `rules/` slot, pinned snapshot, read-only), P4.2 (Procedures
as a thin adapter citing Notes headings, with divergences listed), P4.3 (regional moves
wired into the Region template per rating).

### F5. One path, one profile: no one-shot, no per-region close, no ship, no playtest

`STEPS.md` runs 1 through 5 for a full setting. The user wants both a one-shot module
and a long-form campaign, built iteratively: one region, feedback, another region, wire
them, ship when content. Against that:

- **No profile.** Region count, die defaults and location counts are decided in prose
  at 3a. A one-shot (one thorp, one stretch of country, one 12-room dungeon) has no
  named shape.
- **4d and 5c are end-of-build.** "Once every region has completed 4a-4c, write the
  full entry for each stub row." In practice Region E's PR ran 4d and 5c for E alone,
  which is the right behaviour and contradicts the step text.
- **Reinforcement is outside the build.** 5c names Room to Grow candidates and "authors
  nothing". Wiring regions together is exactly the user's expected workflow and has no
  step.
- **No ship step.** The site and PDF build on every push to `main`, but nothing marks
  a release, and a module under development and a shipped one look identical.
- **No playtest intake.** Drakenhold's step 11 and its `[[ playtest: ... ]]` mark, with
  the rule that one table is not a finding, have no analogue.

**Answered by** P5.1 (profiles), P5.2 (per-region close), P5.3 (a wiring step), P5.4
(ship), P5.5 (playtest intake through the feedback procedure).

### F6. WILD is the weakest rating, and B/X wilderness is a hex crawl

Region B: 6 locations, 4 edges, two disconnected components (validator TOPOLOGY line).
`patterns/region/Wild.md` puts "the connective texture the referee narrates between
points" in the Terrain field and stops. There is no travel procedure, no distance
table, no revelation radius, no camp choice. The Notes' Navigate/Explore/Forage/Camp
moves are exactly that procedure and are not cited anywhere in `patterns/wild/`.
Drakenhold's `WILD_LOW.md` reached the governing insight ("a dungeon's negative space
is place; a road's negative space is time; you cannot key time, so you run it") and
this repository does not carry it.

B/X's assumed wilderness (X1) is a hex crawl with distance-triggered encounter checks.
The point-crawl model here is a legitimate choice, but it should be a profile or pack
decision, not the only option.

**Answered by** P4.3 (regional moves in the WILD overview), P3.2 (the B/X pack states
the hex-crawl option), open question Q5.

### F7. SAFE under-serves a campaign home base

`patterns/safe/` is the thinnest folder. The Notes' SAFE moves (Carousing minimum spend
by die, Philanthropy, Training, Research, Recruitment, hireling rates) are the
downtime economy a campaign runs on, and none has a home in the Region Overview or the
Settlement pattern. A one-shot does not need them. A long-form region does.

**Answered by** P4.3 (SAFE overview gains a Downtime block, drawn only under the
campaign profile).

### F8. Classic material has no slot

The user's original rule "B/X cameo: classic material is salt and pepper, never the
spine; the pleasure is a player recognising an old danger wearing a new name" is not in
the repository. Drakenhold wrote nine `FOR THE TROPE PASS` inventories and never spent
them because no step owned the pass. This framework has neither the inventory nor the
step. "Text reminiscent of classic TSR adventure modules" needs recognisable furniture
at a low rate: the mask that calms the bees, the statue that speaks, the rival party,
the predecessor's corpse.

**Answered by** P3.2 (each pack carries a `Cameo.md`), P3.3 (class files draw from it
at a stated rate under the pack).

### F9. The "poetry for the players" register was dropped without a decision

The user's original rules list has two registers: Hemingway for the referee, Tolkien
for the players. Drakenhold's `STYLE` section kept both. This repository's Player
Summary is two sentences under the same segment grammar as a Feature. That may be the
right call for a B4-style module, which has no boxed text at all, but it was never
decided, and the user's targets disagree with each other on it (*Arden Vul* has
read-aloud; *B4* does not).

**Answered by** P1.1 (STYLE.md names the read-aloud register as a dial), open
question Q2.

### F10. Prose in pattern files restates what Spec blocks already say, and it is most of the read set

`SPEC.md` forbids restating the fenced block in the prose beneath it. Measured, the
prose is where the words are: `patterns/dangerous/Door.md` is 137 lines of which 14 are
Spec. Much of that prose is explanation of why a line exists, which is commit-message
material by the repository's own rule. It is read on every location.

**Answered by** P6.1 (a measured cut of pattern prose to what a generator needs, with
`--read-set --words` as the instrument).

### F11. The validator has no fixture, so every check is tuned against live content

`check_summary_promises` was "tuned against the corpus" to one finding. There is no
`fixtures/` tree of known-good and known-bad locations, so a change to a check is
verified by whether Telar still passes, and a rewrite of Telar (P1.6) will lose that.

**Answered by** P1.2 (the exemplars double as the known-good fixture), P2.2 (known-bad
fixtures for each tell).

### F12. The user's original rules, mapped

| Original rule | Where it lives now | Gap |
|---|---|---|
| Follow the TTRPG Design Notes | nowhere; `Procedures.md` is a generic seed | F4 |
| Follow the Playbook template; illustrative content never enters | `templates/`, each with a Template section | none |
| Sandbox: situations not stories | `GENRE.md` consequence "Give situations, not stories" | none |
| Lived-in world: constructed language, no tropey shorthand | `Language.md`, `Naming.md` | none |
| The path is not clear: more than one route, players may lose the way | DANGEROUS topology (loop, divide, branch); nothing for WILD | F6 |
| Every gate has an answer that is not the gate, priced | `GENRE.md` consequence | none |
| Negative space: thirds, half stubbed, empty rooms | class mix 30/50/rest; LOW as residue; "withholding is content" | the thirds and half-stubbed rules were replaced, deliberately; fine |
| Three tiers of detail | `templates/Location.md` obvious/trigger/secret chain | none |
| Layers of history | `region/Dangerous.md` three occupancies; `History.md` Left lines | none |
| Player mechanics: written from how a player meets it; clues always exist | Clue/Trigger/Payload per class; `GENRE.md` clue rule | none |
| Prose for the referee: Hemingway, measurements, cardinal directions | Referee Notes, Dressing size line | not stated as a style; F1 |
| Poetry for the players: Tolkien | absent | F9 |
| OSR playstyle | `GENRE.md` | none |
| B/X cameo | absent | F8 |
| Tables follow classification; Danger counts down | `templates/Region.md` | none |
| Names compound from root vocabulary; roots proposed not coined | `Language.md` REGISTER block | none |

---

## Part four: the target shape

What the repository looks like when this plan is done. The point is a clone that can
be customised at step 1 and rerun.

```
CLAUDE.md  README.md  STEPS.md  GENRE.md        as now; GENRE.md is generated at 1a
STYLE.md                                          NEW  the positive prose contract (P1.1)
FEEDBACK.md                                       NEW  intake procedure and log (P2.1)
templates/                                        as now, Location.md grammar revised
patterns/                                         NEUTRAL ONLY: Provides / Spec / Constraints
genre/                                            NEW  one pack per genre (P3.1)
  bx-1981/                                        the baseline pack (P3.2)
    PACK.md                                       identity paragraph, axis defaults, seed pool
    Tags.md                                       the ~25-tag setting pool seed
    Cameo.md                                      classic furniture per rating, drawn at rate
    Vocabulary.md                                 per-rating word lists
    patterns/<folder>/<File>.md                   the Design patterns overlay, same path as patterns/
    Bestiary.md                                   seed entries, renamed via Language
    Procedures.md                                 deltas against rules/ only
  <second-pack>/                                  P3.4 proves the shape
rules/
  README.md                                       what goes here and how it is replaced
  Notes.md                                        pinned snapshot of the Design Notes, read-only (Q1)
profiles/
  one-shot.md  campaign.md                        region shape, dice, counts, which steps run per region (P5.1)
style/
  exemplars/                                      six golden entries, hand-approved, read at 4c (P1.2)
  tells.txt                                       the tell list the validator reads (P2.2)
fixtures/                                         known-bad entries per tell, for the validator (P2.2)
tools/                                            as now, plus metrics and --status (P6)
setting/                                          the only variable output
checks/                                           as now, plus Playtest.md (P5.5)
```

What is frozen per release: everything except `setting/`, `checks/`, `GENRE.md`, and
the selected profile. What a user customises: `GENRE.md` via the step 1a questionnaire
(pack + dials), the profile, and `rules/Notes.md` when a new revision lands.

Success criteria for the template:

1. A fresh clone plus one step-1 session produces `GENRE.md`, `setting/Tags.md`,
   `Procedures.md` and `Language.md` under the B/X pack and the one-shot profile.
2. Under the one-shot profile, one SAFE + one WILD + one DANGEROUS region reach 5c in at
   most six further sessions, validator at zero errors, and the site builds.
3. A second genre pack passes the nine-location vertical slice with no fantasy nouns
   leaking into it.
4. Every feedback item since the plan landed is logged in `FEEDBACK.md` with a route,
   and every route that added a rule also added a tell or an exemplar.
5. The per-location read set is at or under 12,000 words for every rating.

---

## Part five: the plan

Conventions: each task has an id, a goal, the files it touches, the steps, and an
acceptance test. "One session" means one Pro-plan sitting for an Opus agent. Tasks
inside a phase run in order unless marked parallel.

### Phase 0: freeze and measure (one session)

**P0.1 Tag the baseline and record metrics.**
- Files: none changed except a new `tools/metrics.py`.
- Steps: tag `HEAD` as `framework-v0`. Write `tools/metrics.py` (stdlib only) that
  prints, for `setting/region/*/[0-9]*.md`: location count, mean and max words per
  Feature, mean sentences per Feature, counts of each tell in `style/tells.txt` (until
  that file exists, hard-code the four from #41: `rather than`, absence claims,
  conclusion tells, gloss pattern `**Term:** ... - the ...`), and total framework words
  versus setting words. Print the read-set word count per 4c entry point by walking the
  same graph `--read-set` walks.
- Acceptance: the numbers in Part one of this file are reproduced within rounding.
  Record the output at the foot of this file under "Baseline metrics".

### Phase 1: the house style (four to six sessions)

**P1.1 Write `STYLE.md`.**
- Files: new `STYLE.md`; `CLAUDE.md` gains one line naming it beside `GENRE.md` as
  re-read at every generation step.
- Steps: write the positive contract, under 900 words. It states, in this order:
  1. **The three sources and what is taken from each**, as the table in F1, extended
     with one short quoted-shape example per source (shape only, never quoted text).
  2. **The referee register**: full sentences, present tense, dimensions in feet indoors
     and yards outdoors, cardinal direction for every exit, materials named as
     materials, no adjective of mood. A Feature is one to three sentences. A branch is
     written `Label: outcome.` The Hole in the Oak's form is the model.
  3. **The read-aloud register**: one to three sentences, spoken, may carry one image,
     never a conclusion, and its bolded nouns are promises. Whether it is terse (B4) or
     lyrical (Tolkien) is a dial the genre pack sets; default terse (Q2).
  4. **The tells**: the classes of failure, each with two or three signatures, pointing
     at `style/tells.txt` as the machine-read list.
  5. **The sentence budget** that replaces the punctuation ban (P1.3 writes it into the
     template; STYLE.md states it once).
- Acceptance: a reader who has never seen the repository can write one Feature and
  one Player Summary from `STYLE.md` alone. The user approves the draft before P1.2.

**P1.2 Write the exemplars.**
- Files: new `style/exemplars/` holding six entries plus `README.md`: one SAFE working
  location, one WILD landmark carrying a hidden child, one DANGEROUS high, medium and
  low, and one region overview (DANGEROUS). Set nowhere: codes `X.n`, no Telar nouns,
  the way Drakenhold's worked examples were set nowhere so they cannot be quarried.
- Steps: write each to `STYLE.md` and to the matching class file's Spec, exactly as
  4c would, then hand-edit until it reads like the target. Every rated line the class
  file draws at `1` is visibly present. Add to `templates/Location.md`'s Context list:
  "the exemplar for this rating and weight, `style/exemplars/`". Add the six files to
  the validator as a fixture set that must pass with zero errors and zero warnings.
- Acceptance: the user approves all six. `validate_setting.py --fixtures` (P2.2 adds
  the flag; until then, run the location checks against the directory by hand) passes
  clean. These six are the regression floor for every later grammar change.

**P1.3 Replace the punctuation ban with a sentence budget.**
- Files: `templates/Location.md` instruction 5; `tools/validate_setting.py`
  `check_feature_grammar`.
- Steps: instruction 5 becomes: a Feature is one to three sentences, each at most about
  twenty words; `Label: outcome.` branches are sentences; `->` still means trigger to
  effect and nothing else; a citation sits last in its own parentheses; no trailing
  ` - ` clause (the explanatory slot) and no parenthetical aside other than a citation.
  Delete the eight-words-per-segment rule and the comma-only separator rule. Rewrite
  `check_feature_grammar`: error on a trailing ` - ` clause and on a non-citation
  parenthesis; warn on a fourth sentence or a sentence over about twenty-five words;
  warn on each tell from `style/tells.txt` (P2.2; until then the four hard-coded).
- Acceptance: the six exemplars pass clean. The E.22 "against the, Danger track" line
  now fails (a comma before a noun phrase with no clause on either side is a warning:
  "comma inside a phrase"; implement as a heuristic that flags `, the ` and `, a `
  preceded by a preposition). Telar reports errors again; that is expected and P1.6
  clears them.

**P1.4 Bring the Region Overview under the same style.**
- Files: `templates/Region.md`; `STYLE.md` gets a short region section.
- Steps: the Overview three-sentence cap stays. Every other field gets a sentence
  budget instead of prose guidance, and the field descriptions in the template are cut
  to one line each, pointing at the region exemplar. Move the paragraphs of rationale
  currently in the template's field bullets into `STYLE.md` where they are style, or
  delete them where they are history.
- Acceptance: `templates/Region.md` under 60 lines. The region exemplar unchanged and
  still the target.

**P1.5 Bring the setting-level artifacts under the same style.** May run in parallel
with P1.4.
- Files: `templates/History.md`, `Truths.md`, `Rumours.md`, `Bestiary.md`,
  `Factions.md`; `patterns/setting/` counterparts only where a prose rule is a style
  rule in disguise.
- Steps: apply the sentence budget: a History event is two sentences plus a Left line;
  a Truth is one sentence plus a Handle; a rumour is one or two sentences in a
  speaker's voice; a Bestiary Description is one to three sentences. Most of this is
  already stated; the task is to say it once in `STYLE.md` and cite it, not restate it
  per template.
- Acceptance: no template restates a rule `STYLE.md` owns.

**P1.6 Rewrite Telar to the new grammar, one region per session, and measure.**
- Files: `setting/region/*/[0-9]*.md`, `setting/region/?.md`.
- Steps: region by region, in the order A, C, B, D, E (SAFE first because it is
  cheapest). Rewrite every Feature and Summary to the budget, with the matching
  exemplar open. Nothing a party can find is removed; every citation, exit and Test is
  unchanged. Run `tools/metrics.py` after each region and record the delta in the
  commit body, as #41 did.
- Acceptance: zero validator errors across `setting/`; mean sentences per Feature
  between 1.2 and 2.0; zero comma-inside-phrase warnings; "rather than" under 15
  across the corpus; the user reads two regions and accepts the register. This is the
  point at which Telar may later be regenerated rather than kept (Q3).

### Phase 2: feedback intake and the rule ladder (two sessions)

**P2.1 Write `FEEDBACK.md`.**
- Files: new `FEEDBACK.md`; `CLAUDE.md` gains one rule: "User feedback on generated
  content is routed through `FEEDBACK.md` before any file is changed."
- Steps: the file has two parts. **The routes**, adapted from Drakenhold's six:
  - **R1 Content**: the finding is about one location or field. Fix it in `setting/`.
    No rule changes.
  - **R2 Exemplar**: the finding is a register the exemplars do not show. Edit or add
    an exemplar. No prose rule is written.
  - **R3 Tell**: the finding is a class of failure that recurs and has a textual
    signature. Add a line to `style/tells.txt` and a known-bad fixture. The validator
    warns from now on. Nothing else is written.
  - **R4 Rule**: the finding is a class of failure with no textual signature. Add one
    sentence to `STYLE.md` or one consequence to `GENRE.md`, and only if it can name
    the judgement-check item that will look for it. The consequences list is capped at
    fifteen; adding one past the cap means merging two.
  - **R5 Constraint**: the finding is about what one pattern file produces and no
    other. Add the Constraint there. This is the last resort, not the first.
  - **R6 Pack**: the finding is that the content is generic, or the wrong genre. It goes
    to `genre/<pack>/`, never to `patterns/`.
  - **R7 Rules project**: the finding is a mechanic the Notes do not cover. Log it and
    stop; write nothing into `Procedures.md`.
  **The log**: one line per item, date, quote, route, commit. Struck when landed.
- Acceptance: the user approves the routes. The three most recent PRs' rule additions
  are retroactively classified in the log as a worked example.

**P2.2 Make the tells data, with fixtures.**
- Files: new `style/tells.txt`, new `fixtures/bad/` and `fixtures/good/`;
  `tools/validate_setting.py` gains `--fixtures`.
- Steps: `tells.txt` is one regex per line with a `# reason` comment, starting with
  the four from #41 plus the comma-inside-phrase heuristic from P1.3. `fixtures/bad/`
  holds one minimal location file per tell that must produce exactly that warning;
  `fixtures/good/` is a symlink or copy of `style/exemplars/`. `--fixtures` runs the
  location checks on both directories and fails if any good file warns or any bad file
  fails to. CI runs `--fixtures` beside the main run.
- Acceptance: CI green with the fixtures; adding a tell is a one-line change plus one
  fixture file.

**P2.3 Audit the existing Constraints and consequences.**
- Files: every `patterns/*/*.md` Constraints section; `GENRE.md` and
  `templates/Genre.md` consequences.
- Steps: list every entry in a table in the commit body with one of: keep (it closes a
  pathway and names the file it protects), promote (it is a tell, move to `tells.txt`
  and cut), exemplify (it is a register, covered by an exemplar, cut), merge (it
  duplicates another), cut (history). Apply. Expect to cut a third.
- Acceptance: `GENRE.md` consequences at or under twelve; no Constraint whose
  substance a tell already catches; `templates/Genre.md` and `GENRE.md` byte-identical
  in the fixed block.

### Phase 3: genre packs (four to five sessions)

**P3.1 Split `patterns/` into neutral files and a pack overlay.**
- Files: all 37 files on the step 1b compile list; new `genre/bx-1981/patterns/`;
  `patterns/SPEC.md`; `STEPS.md` 1b; `tools/validate_setting.py` compile-list and
  read-set checks; `tools/build_site.py` patterns page.
- Steps: for each file on the compile list, move its `## Design patterns` section
  verbatim into `genre/bx-1981/patterns/<folder>/<File>.md` under a `## Design
  patterns` heading with a one-line `## Provides` naming the neutral file it overlays.
  The neutral file keeps Provides / Spec / Constraints. `SPEC.md`'s skeleton becomes
  three sections, and its compile-list paragraph becomes "the pack carries an overlay
  for exactly the files on the list". The validator checks the list both ways against
  the pack directory instead of against a section. `--read-set` adds the overlay file
  to every entry it lists when the pack is selected. The site's pattern page renders
  neutral and overlay side by side.
- Acceptance: zero errors; `--read-set 4c` lists the same 65 neutral files plus 37
  overlays; the site builds; no `## Design patterns` heading remains under `patterns/`.

**P3.2 Build the B/X 1981 baseline pack.**
- Files: `genre/bx-1981/PACK.md`, `Tags.md`, `Cameo.md`, `Vocabulary.md`,
  `Bestiary.md`, `Procedures.md`; `patterns/setting/Genre.md` seed pool.
- Steps:
  - `PACK.md`: the identity paragraph for the assumed setting of 1981 B/X, stated the
    way `GENRE.md`'s paragraph is (points of light, shadow of a ruined empire, mythic
    underworld, low magic, from the Notes' Implied Setting section), the literary
    references the Notes name (de Camp and Pratt, Howard, Leiber, Vance, Lovecraft,
    Merritt), the module touchstones (B2, B4, X1, S4, U1, I6, S3), and the default
    value of every axis in `patterns/setting/Genre.md`'s Q2 list.
  - `Tags.md`: the seed pool step 1b draws the setting pool from; ~40 candidates so 1b
    can pick 25.
  - `Cameo.md`: per rating, ten to fifteen pieces of classic furniture stated as
    shape and constraint, never as a named monster (the mask that calms the guardians,
    the pool that grants and takes, the rival party, the predecessor's kit). One
    caution per rating carried from Drakenhold: one central mechanism per HIGH, one
    lethal off-road site per WILD region.
  - `Vocabulary.md`: the per-rating word lists currently inside the Dressing and
    mechanism overlays, gathered so a pack can replace them wholesale.
  - `Bestiary.md`: fifteen to twenty seed entries in `templates/Bestiary.md`'s shape,
    each a classic under a plain descriptive name, to be renamed through `Language.md`
    at 2e. This is the "old danger wearing a new name" rule made concrete.
  - `Procedures.md`: empty under this pack, stating so.
  - The seed pool in `patterns/setting/Genre.md` gains a "TTRPG lines" entry for B/X
    itself and is marked as the pack's, not the framework's.
  - Class files gain one rated line each, in the registry block: `10% A cameo, per
    genre/<pack>/Cameo.md` (SAFE 5%, WILD 10%, DANGEROUS 15%).
- Acceptance: the validator knows the pack (a `PACK.md` with an identity paragraph and
  every axis defaulted is required); `--read-set 4c` includes `Cameo.md` for each
  class file; one location per rating generated from the exemplar shape under this pack
  reads as B/X to the user.

**P3.3 Wire the axis dials to Spec rates.**
- Files: `patterns/setting/Genre.md`; the Spec blocks of `dangerous/Hazard.md`,
  `wild/Hazard.md`, `dangerous/Mystery.md`, `dangerous/Residual.md`,
  `dangerous/Door.md`, `patterns/setting/UniqueTreasures.md`, `region/Safe.md`,
  `templates/Region_Gazetteer.md`; `tools/validate_setting.py`.
- Steps: the Q2 axis list gets, per axis, the Spec lines it moves and the values. Each
  such Spec line carries an inline bracket, in this form and no other:
  `20%   lethal   [lethality: low 10% | high 30%]`. The bracket is the only place a rate
  varies; the generator reads `GENRE.md`'s axis value and applies it. Axes to wire now
  and nothing more: lethality (hazard tiers, Xd caps), magic level (ward and illusion
  cap per region, residual rate, Unique Treasure count), population density (SAFE
  region count and default die; WILD location count), supernatural visibility
  (whether a Bestiary Guardian's condition is common knowledge, as a Rumours line),
  read-aloud register (terse or lyrical, in `STYLE.md`). The validator checks that
  every axis `GENRE.md` states is referenced by at least one bracket and that no
  bracket names an axis `GENRE.md` does not.
- Acceptance: validator clean; changing `GENRE.md`'s lethality to low and regenerating
  one DANGEROUS medium location from the exemplar changes its hazard tier draw.

**P3.4 Prove portability with a second pack.**
- Files: new `genre/scifi-horror/` skeleton recovered from `git show b6e0bf7^:`'s
  `tags_scifi.md` and the vertical slice file; a new `fixtures/slice/` with three
  locations per pack.
- Steps: build the skeleton to the same file set as P3.2 at a third of the depth
  (`PACK.md`, `Tags.md`, `Cameo.md`, `Vocabulary.md`, overlays for the three Dressing
  files and the three Creature files only; the rest fall back to the neutral file with
  a stated "no overlay" line). Regenerate the nine-location vertical slice: one
  location per rating per pack, same class and weight held constant. Diff the noun
  vocabulary across packs as #24 did.
- Acceptance: zero cross-pack noun overlap outside behavioural primitives; the slice
  passes the validator; the user reads the three sci-fi entries and confirms no fantasy
  furniture leaked. This pack is a proof, not a supported product, and its `PACK.md`
  says so.

### Phase 4: the rules adapter (three sessions)

**P4.1 Create the `rules/` slot.** Depends on Q1.
- Files: new `rules/README.md`; new `rules/Notes.md` (the pinned snapshot) if Q1 is
  answered as recommended; `.github/workflows/validate.yml` unchanged.
- Steps: `README.md` states: read-only, replaced wholesale, never edited, carries a
  revision line at its head, and every mechanic term in `setting/Procedures.md` or a
  pattern Spec must resolve to a heading in it. If the user prefers the Notes out of
  tree, `rules/Notes.md` is gitignored and the README says the agent asks for it at
  step 1c and proceeds on the seed if it is absent.
- Acceptance: `rules/Notes.md` present or explicitly absent by decision; the validator
  warns when `setting/Procedures.md` exists and `rules/Notes.md` does not.

**P4.2 Rewrite Procedures as a thin adapter.**
- Files: `templates/Procedures.md`, `patterns/setting/Procedures.md`,
  `setting/Procedures.md`; `tools/validate_setting.py` forced-damage grammar.
- Steps: the template's sections become the Notes' own headings that a setting touches
  (Forced Danger, Tests, Wounds and Madness, Conditions, Regional Modes, Tracking Time,
  Faction Turns, Non-Player Characters) and each section holds only what the setting
  adds or diverges on, citing the Notes heading by name. Every divergence in the F4
  table is decided one way: adopt the Notes (Constitution uses the Combat die; wounds
  are a count; one Test per Forced Danger, with `Xd` retained only if Q4 keeps it as a
  stated house rule) or record it as an R7 proposal in `FEEDBACK.md`. The forced-damage
  citation grammar in `templates/Location.md` is revised to whatever survives, and the
  validator with it. The no-search-roll-for-secrets rule stays and is written as the
  setting's explicit divergence from the Notes' Search move.
- Acceptance: every mechanic term in `setting/Procedures.md` resolves to a Notes
  heading (a validator warning otherwise); the treasure taxonomy matches the Notes
  unless Q4 says otherwise; a referee holding the Notes can read a location Feature's
  citation without a translation.

**P4.3 Wire the regional moves into the Region template.**
- Files: `templates/Region.md`, `patterns/region/Safe.md`, `Wild.md`, `Dangerous.md`;
  the region exemplar.
- Steps: each rating's Overview gains one field, filled by citing the Notes' moves and
  stating only what this region changes:
  - **SAFE, Downtime** (campaign profile only): which of Carousing, Training, Research,
    Recruitment, Gather Information and Philanthropy are available here, at what
    minimum spend given the die, and the hireling roster with day rates. Under the
    one-shot profile the field reads "none beyond Rest and Commerce".
  - **WILD, Travel**: distances between Landmarks in hours at 3 miles per hour,
    terrain rate, what a watch buys, Make Camp's three rolls with any local modifier,
    the revelation radius (what a party sees from high ground), and the encounter
    cadence (per failed Difficulty roll, resolving next watch, not forced). This is
    where "the ground between" is run rather than keyed.
  - **DANGEROUS, Movement**: Careful and Rushed Movement distances, what Listen hears
    here, what Rest recovers, and the Danger Die reset rule.
  `region/Wild.md`'s topology gains "every Landmark reachable" as an error rather than
  a report, which closes Region B's disconnected components.
- Acceptance: the region exemplar carries the new field; Region B rewritten so its
  graph is connected; validator clean.

### Phase 5: profiles, the iterative workflow, and shipping (three sessions)

**P5.1 Write the profiles.**
- Files: new `profiles/one-shot.md`, `profiles/campaign.md`; `STEPS.md` step 1 gains
  `1e. Choose a profile`; `templates/Region_Gazetteer.md` reads the profile for count
  and dice.
- Steps: each profile is under 40 lines and states: region count and rating mix; die
  defaults; location count per rating; whether blocks are levels (campaign) or a single
  block (one-shot); which registries are required at the close of each region; whether
  4d and 5c run per region or at the end; the session plan (one region per session, one
  block per turn for DANGEROUS, commit after each step). One-shot: one SAFE thorp at d8
  with four to five locations, one WILD at d6, one DANGEROUS at d6 with twelve rooms in
  one block, about 24 locations, targeted at two to four sessions of play. Campaign: the
  current shape, plus a megadungeon region as many blocks with one block per level and a
  block-to-block existence diagram, and the Downtime field on.
- Acceptance: `STEPS.md` cites the profile; a fresh `GENRE.md` questionnaire session
  ends by naming one.

**P5.2 Make 4d and 5c per-region.**
- Files: `STEPS.md` 4d and 5c; `templates/Lore.md`, `Keys.md`, `Quests.md`,
  `NamedCreatures.md`, `UniqueTreasures.md` two-phase instructions;
  `tools/validate_setting.py` `build_complete` logic.
- Steps: 4d becomes "at the close of each region, write the full entry for every stub
  row whose citing locations are all written; a row citing unwritten ground stays a
  stub and is an obligation". 5c runs per region as it already does in practice, and
  a final sweep at the end of a profile is 5d, new id. `build_complete` becomes
  per-region so the registry floor and rumour-settling checks fire when a region
  closes, not only when everything does.
- Acceptance: `--status` (P6.3) shows a region as closed when its 4d rows are full;
  Region E's existing history is the worked example.

**P5.3 Add the wiring step.**
- Files: `STEPS.md` gains step 6, `Wire`; `templates/Setting_Judgement_Check.md` Room
  to Grow gains an "acted on at" column.
- Steps: step 6 is region-scoped and additive only: take the Room to Grow list, choose
  candidates with the user, and for each write the reinforcement into locations already
  on disk (a motif's fourth appearance, a Named Creature heard of, a Key's second
  sighting) or draw a new cross-region edge in both region diagrams and both Exits
  lines. Never a new location; a new location is a new region pass. Record each act in
  the Room to Grow row. This is the step the user's workflow ("add regions, wire
  regions together") was missing, and Drakenhold's finding that baseline-then-reinforce
  beats forward-declared threads is the reason it is additive.
- Acceptance: one wiring pass over Telar lands at least three Room to Grow rows and
  the validator stays clean.

**P5.4 Add the ship step.**
- Files: `STEPS.md` gains step 7, `Ship`; `tools/build_site.py` and `build_pdf.py`
  gain `--release <tag>`; `README.md` commands section.
- Steps: ship is a tag on `main` plus the site and PDF built with the tag in their
  title page, and a `checks/` snapshot. Nothing is stripped: this framework keeps no
  authoring scaffolding in the output, which is a deliberate difference from
  Drakenhold's one-way strike and should be recorded in the step text as the reason
  ship can run more than once. The T/P/F column and the Settled-at column are
  referee-facing and stay.
- Acceptance: `python3 tools/build_site.py --release v1 --out _site` produces a site
  whose index names the release.

**P5.5 Playtest intake.**
- Files: new `checks/Playtest.md`; `FEEDBACK.md` gains route R0.
- Steps: a playtest note records what happened and where, never what to do about it,
  in a table: date, region, location, observation. Route R0 in `FEEDBACK.md`: a
  playtest note becomes a feedback item only when the same observation arrives from a
  second session or when re-reading the clue chain finds a real gap; otherwise it stays
  a note. "One table is not a finding" is the rule, stated once.
- Acceptance: the file exists with its rule and an empty table.

### Phase 6: session economics (two sessions)

**P6.1 Cut the read set to the budget.**
- Files: the prose under Spec blocks in every `patterns/*/*.md`; `tools/metrics.py`
  and `--read-set --words`.
- Steps: measure per entry point. For each pattern file, keep under the Spec block only
  prose that changes what a generator writes (a distinction between two lines, a
  reading of a rate, a boundary against a sibling). Cut prose that explains why a line
  exists (commit messages own it), restates the block, or restates another file. The
  target is a DANGEROUS medium location at or under 12,000 words in context, WILD
  landmark under 10,000, with overlays counted.
- Acceptance: `--read-set 4c --words` reports the targets met; the six exemplars
  regenerate from the trimmed files without losing a rated line (spot-check by the
  user on two).

**P6.2 Cut the setting-level read set.**
- Files: `templates/*.md` Context lists; `README.md`.
- Steps: `README.md` is injected by the session hook on every turn at 600 words. Cut
  it to the directory map and the commands. Every template's Context list is checked
  against what the step actually needs; `templates/Location.md` already models the
  narrow list. Truths and Procedures at every location stay (decided in #31);
  `Language.md` is needed only when a proper noun is coined, so it moves to "consult
  when coining".
- Acceptance: `README.md` under 400 words; no Context list names a file the step's
  output never cites.

**P6.3 Add `--status` as the handoff.**
- Files: `tools/validate_setting.py`.
- Steps: `--status` prints, per region, which step it has reached (files present per
  the templates), open obligations from `--pending`, unfilled registry rows, and
  unsettled rumours. This replaces any handoff document; Drakenhold's `HANDOFF.md`
  grew to 45KB and drifted, and the lesson is that a handoff must be derived.
- Acceptance: a fresh session can pick the next task from `--status` plus `STEPS.md`
  alone.

### Phase 7: the campaign profile's long form (two sessions, after a one-shot has shipped)

**P7.1 Block connective documents for a megadungeon.**
- Files: new `templates/Block.md`; `patterns/region/Dangerous.md` BLOCKS spec;
  `templates/Block_Connections.mmd` header.
- Steps: under the campaign profile, each block of a DANGEROUS region with more than
  one block gets a short connective document: its purpose family, what it hands to
  neighbouring blocks (a route, a resource, a threat that moves), its own Danger table
  override if any, and its unnamed-fill description (what the rooms between the stubs
  are, so negative space is run rather than left blank). Drakenhold's `blocks/` carried
  exactly this and it was load-bearing for 22 regions stacked in three peaks.
- Acceptance: the validator requires a `Block.md` per block under the campaign profile
  and none under one-shot.

**P7.2 Regenerate a shipped example under the B/X pack.** Depends on Q3.
- Files: `setting/` wiped and rebuilt under `genre/bx-1981/` and `profiles/one-shot.md`.
- Steps: run steps 1 through 7 as a user would, one session per step or region, logging
  every friction point in `FEEDBACK.md` as it is met. This is the acceptance test for
  the template repository as a whole.
- Acceptance: success criteria 1, 2 and 5 in Part four hold; the shipped site is the
  repository's example.

---

## Part six: open questions for the user

Each has a recommendation. A task that depends on one proceeds on the recommendation
if no answer has arrived.

**Q1. The Design Notes: pinned snapshot in `rules/`, or kept out of tree?**
Recommendation: pin a snapshot, replaced wholesale, never edited, with a revision line.
The user's reason for keeping it out (it is a moving target) is the argument for
pinning: a module is built against one revision, and the file says which. Drakenhold
did this and it worked.

**Q2. Read-aloud register default: terse (B4, B2) or lyrical (Tolkien, the original
"poetry for the players" rule)?**
Recommendation: terse by default, lyrical as a pack dial. B4 and The Hole in the Oak
have no boxed text; a spoken two-sentence summary is what a referee actually reads at
a table. The lyrical register survives as an option because the user asked for it and
Arden Vul uses it.

**Q3. Telar: keep as the exemplar setting, or regenerate under the B/X pack after
Phase 3?**
Recommendation: keep it through Phase 1 as the rewrite corpus (it is what the checks
were tuned on), then regenerate at P7.2 as a one-shot under the baseline pack, and let
that regenerated module be the shipped example. Telar is Conan, not B/X, and the
template's example should be the template's default.

**Q4. Forced damage and treasure: adopt the Notes wholesale, or keep `Xd` and the
five-table taxonomy as stated house rules?**
Recommendation: adopt the Notes for Forced Danger (one Test, Combat die for
Constitution) and for the treasure taxonomy, and raise the Equipment table and the
`Xd` tier ladder as proposals to the rules project through R7. The framework should
sit on the Notes, not beside them.

**Q5. WILD: point crawl only, or a hex-crawl option?**
Recommendation: point crawl stays the structure (it is what the graph and the checks
already model), and the Travel field from P4.3 carries hex-style distance-triggered
checks as its cadence. A full hex map is a different data model and is not worth it
until a campaign asks for one.

**Q6. The `## Design patterns` overlays: does the user want the B/X pack's content
rewritten from the touchstone modules now, or the existing generic-fantasy text moved
as-is and rewritten later?**
Recommendation: move as-is in P3.1, rewrite in P3.2 only the files where the content
is thin or generic enough to fail "be specific, not generic" (Cameo, Bestiary and the
three Dressing overlays first). A full rewrite of 10,000 words is a separate pass.

---

## Baseline metrics

Recorded by P0.1. Until then, the figures in Part one stand.

| Metric | Value at `ae492fa` |
|---|---|
| Framework words (authorities + templates + patterns) | 62,500 |
| Setting words | 30,600 |
| Locations | 64 |
| Mean words per Feature | 22.3 |
| "rather than" occurrences in `setting/region/` | 46 |
| Absence-claim tells | 6 |
| Conclusion tells | 1 |
| Read set, DANGEROUS medium location | 23,900 words |
| Read set, WILD landmark | 18,000 words |
| Validator | 0 errors, 9 warnings (all hidden-edge far-side confirmations) |
| Pattern files with empty Constraints | 25 of 65 |
| `GENRE.md` standing consequences | 13 |
