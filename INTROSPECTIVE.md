# Introspective and implementation plan

Running state, not authority. `STEPS.md` and `patterns/SPEC.md` win wherever this file
disagrees with them. This file exists to be executed and then cut down: each task below
names what it changes and what proves it done, and a task that lands is struck here in
the same commit. When every task is struck, delete the file.

Written from a full read of this repository at commit `ae492fa` (108 commits, at least
six generated settings wiped and rebuilt), of the predecessor
`rstevenson1237/drakenhold` (66 commits), and of the `Rules_Light_TTRPG_Design_Notes.md`
that project mirrors. Revised twice: after the user's corrections on the rules interface,
the tag system's intent, profiles, cameos and voice (the first draft's errors on those
are recorded under Part four so the reasoning can be read back), and again after the
user answered every open question, which are now the decisions in Part seven.

**The scripting boundary, stated once.** The user tried a deterministic generator that
built most of the context window and left the model only the prose, and it was too
complex to make work. What is in scope here is narrower: scripts that draw, assemble
context, count and check. No script writes prose, and no script decides what a room is
for. `tools/draw.py` and `tools/context.py` sit inside that line; anything that reads
like a generator sits outside it and is not to be built.

## How to use this file

- **An Opus agent executes one task per session**, in the order given, unless a task says
  it may run in parallel. Read the task, read only the files it names, do the work, run
  `python3 tools/validate_setting.py`, commit with the task id in the subject, strike the
  task here.
- **Phases are ordered by what invalidates what.** Phase 0 measures what the framework is
  earning before anything is cut. Phase 1 fixes the prose grammar every later phase
  writes to. Phase 3 moves content between trees, so nothing that reads pattern files
  is rewritten until it lands.
- **Nothing here authorises deleting Telar** until task P7.2 says so. It is the only
  corpus the checks have been tuned against, and per D3 it is removed, not kept, when
  the work is done.
- **Part seven records the user's decisions.** A task does not reopen one; a task that
  finds one wrong logs it in `FEEDBACK.md` and proceeds as decided.
- **Six tasks are marked DEFERRED** after the user's final check against the baseline
  (the Drakenhold brief, the templates, a bare rules reference). They stay in the file
  with their reasoning and are not executed until the condition each names is met.
  The minimum path, in order: P0.1, P0.2 (a reading), P1.1, P1.2, P1.3, P1.4, P1.5,
  P2.1, P2.2, P2.3, P2.4, P3.1, P3.2, P3.3, P4.1, P4.2, P4.3, P5.1, P5.2, P5.3, P6.1,
  P6.2, P6.3, P7.2. About 24 sessions.

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

The framework is 62,000 words. The setting it has produced is 30,600. Two words of rule
for every word of output, and a generation step reads most of the rules every time.

### What a location costs to generate

Words in context for one location, per `--read-set 4c`, including `CLAUDE.md`,
`README.md` (injected by the session hook), `GENRE.md`, the region overview, Truths,
Procedures, Language and the template:

| Location | Words in context |
|---|---|
| DANGEROUS medium | 23,900 |
| WILD landmark | 18,000 |

Region E (24 locations) was built across `3a`-`5c` in one PR. At roughly 20,000 words
of context per location plus output, that is the shape of the Pro-plan problem: the
budget is spent re-reading rules, not writing rooms.

### Where the prose is now

PR #41 closed the Feature grammar to `,` and `->`, eight words per segment, four
segments per line. It cut mean Feature length from 42.8 words to 22.3 and "rather than"
from 61 of 206 Features to 25 of 209. Those are real gains against the trailing-clause
failure the commit describes.

It also produced this, in `setting/region/E/22.md`:

```
**Sealed Air:** Thin and heavy, costing real effort, working hard here counting double
against the, Danger track, except from the dais steps.
```

The comma after "the" is there to pass the segment-length check. `E/20.md`'s "Braced
shut with a timber bar seated, in stone sockets on this side" is the same thing. The
grammar is mechanically satisfiable by breaking English, and the generator found that
out.

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
variable and the setting the casualty. A template repo inverts that.

---

## Part two: what the infrastructure is earning

The user's working baseline reliably produces a one-shot at roughly 90% of the mark,
and it is smaller than the first draft of this file assumed: about 80 words of prompt
("OSR design philosophy. Classic 1981 Basic D&D theme. Use tags and short descriptive
sentences. B/X stat lines. Do not create a story."), the Design Notes as context, and a
numbered room list with dimensions and exits. The Notes carry the genre, since their
Implied Setting, Literary References and Creature Types sections are the 1981 baseline
stated once. That is the control this framework has to beat, and it has never been
measured against it. What follows is the assessment; P0.2 is the measurement.

**A one-shot fits in one context window.** Every room, every clue's far end, every coined
name is in view at once, so consistency is free and 80 words of prompt is enough. The
problem this project was started for is the other case: a module larger than a window,
where drakenhold's clues went unclosed and motif text filled the gap. Consistency of
detail across a large module is a memory problem, and the parts of this framework that
answer it are small and mechanical:

- the five registries and the two-phase stub-then-fill rule (container/data);
- obligations: a Key's supply end binding the location it opens to draw the lock at
  rate 1;
- `Language.md` as a root list that receives coinage back;
- the typed diagrams, one per block, existence-only above;
- the validator that reconciles all of the above, and `--pending` and `--read-set`.

That is perhaps 8,000 words of tools and templates, and it earns its keep: nothing else
holds a sixty-room module together across ten sessions.

**The other 46,000 words are pattern prose, spent on prose quality and variety.** That
is the problem the 80-word prompt already solved to 90%, and prose rules are the wrong tool
for the remaining 10%, for two reasons the user has already stated:

1. **A question returns the average.** `SPEC.md` gives a Spec line two forms, a question
   or a pattern to match, and says to prefer the question. A question asked of a model
   returns the most probable answer every time: the right door for the situation, and
   always the same door. Variety comes from matching against a list and choosing one of
   twenty. Most of `patterns/` is questions with explanatory prose under them.
   `dangerous/Door.md` grew to 137 lines and a 500-word menu of doors, and the output
   still needed a Constraint banning "a door". Prose about doors does not make doors
   vary.
2. **A rule against a symptom costs a rebuild.** Six settings wiped. Each of the last
   seven PRs cut one failure and the next build found the next unprohibited one, ending
   in a grammar a model satisfied by inserting a comma into a noun phrase.

**So the framework earns cross-session coherence, and pays for it with a 24,000-word read
set per location, most of which is prose doing a die's job.**

**How to do it differently.** Keep the four trees the user names and make the split do
the work:

| Tree | Owns | Size target |
|---|---|---|
| `templates/` | the output format, including the rules interface as a citation grammar | as now, trimmed |
| `patterns/` | the contract: Provides, rated Spec, Constraints; no prose beneath the block that a generator does not need | 46,000 words to about 10,000 |
| `genre/` | every menu and every "what it is" line resolved as a list, generic to specific, tropes included as a facet | the 10,000 words of Design patterns, moved and grown |
| `setting/` | the only variable | as now |

And one addition nobody has tried here: **the draw is arithmetic, not taste.** A model
handed a list of twenty still picks the probable three. A Spec line that reads
`1 Door (genre: doors)` is resolved by a small stdlib script that takes the location code
and the list and returns the index, so the generator is told which door it got. Variety
becomes a property of the pipeline, and the user rerolls a draw they dislike without
touching a rule. Every place a Constraint currently says "never write X" because X is
what the model always writes is a place a list and a die would have prevented the
Constraint.

The rest follows: feedback routes to a list entry, an exemplar or a tell before it may
become a rule; the region brief the user wrote for Region E becomes a first-class
input, which is the profile mechanism and the iterative growth mechanism at once;
Procedures becomes an interface, not a rulebook.

### The baseline, read

The user supplied the output of the conversational prompt (`fixtures/control/
arm1b-output.md`, with its map), noting that formatting was not strict and the target
was not this rule set, but that the prose is good reference. Read against the same
tells as Telar:

| Measure | Baseline (Morthek) | Telar |
|---|---|---|
| Keyed locations | 26 plus a 4-location town | 64 |
| Words per keyed room | 322 | 182 |
| Mean words per sentence | 14.3 | Feature grammar, 22 per line |
| "rather than" | 3 in 11,200 words | 46 in 11,700 |
| Absence claims | 4 | 6 |
| Referee asides ("Referee:") | 8 | 0 |
| Motif recurrence: Suelle | 5 rooms, named nowhere as a motif | see F11 |

Three findings, in order of weight.

**Nearly every standing consequence in `GENRE.md` is present, unprompted.** A guardian
that is a condition (the guard-post skeleton lets people in and stops them leaving; the
Wight pauses at Morthek's mark; the ghoul negotiates). Every gate with a priced answer
that is not the gate (the portcullis forced with noise, or the lever, or the crawlspace
with gear off). Withholding as content (the False Vault; cell 20D's soldier "unresolved,
and will remain so"). A clue outside the room it opens (the duty roster in the armory
names the Wight two levels down; the cipher key in a jar and the sequence under a desk
open a door in another wing). Repetition before explanation (Suelle in five rooms, the
eye in every carved surface, never explained). Rumours marked true and partial with
the false half named. The consequences are a description of what a competent module
already does. They were written as if generative. They are diagnostic, and the model
had them from the genre before any file in this repository named them.

**The register that reads as a module has voice, and the framework's tests would cut
it.** "Morthek's joke. He found this genuinely funny." "Do not protect fools." "Referees
who read it aloud tend to find that their players remember this room longer than the
ones with treasure." Each fails a test in `GENRE.md` (unwitnessable, mood, a conclusion
written down), and each is what B2 and B4 sound like. The first test, every word is
translated, is right about facts and wrong about the referee's ear: an aside that tells
the referee how to run a room is translated, into a ruling. `STYLE.md` (P1.1) has to
say which asides are allowed, and the answer is the ones addressed to the referee about
running the room, never the ones that state what the players will feel. The
"conclusion tells" that #41 cut were the second kind; the baseline shows the first kind
is the module's voice and should stay.

**The form is the framework's form, at paragraph length.** Numbered room, an italic
line of dimensions and fixtures, bold sub-labels each holding one thing, a stat line in
a blockquote, exits with construction and state. It is `templates/Location.md` with
full stops. Sentences average fourteen words and a sub-label carries two to four of
them. That is the sentence budget P1.3 should set, measured rather than guessed: one to
four sentences per Feature, around fifteen words each, with the trailing explanatory
clause banned and nothing else.

**How much of this is over-engineering, against the user's own baseline.** The user
named the baseline as the Drakenhold brief, the detailed template files, and a bare
rules reference: about 15,000 words. Against that, what this plan adds that is new is
small: `STYLE.md` and six exemplars, `FEEDBACK.md`, the lists under `genre/`, and four
scripts (draw, context, map, metrics). Everything else is a reduction of what exists.
Six tasks were over that line and are marked DEFERRED in Part six: rewriting Telar
wholesale, axis dials, a second pack, a release flag, playtest intake, block documents.
Roughly a third of the plan's sessions. What should not be cut further is `context.py`
and the memory layer it reads, because motif saturation across sessions is the one
failure observed six times and nothing in a one-shot baseline prevents it.

What the baseline does not do, and what the framework is for: it has no registries, so
Suelle's five appearances were held in one context window and would not survive a
second session; its dimensions are stated but no check reconciles them to the map; its
exits are listed in prose and no script confirms both ends; its treasure is priced in a
currency the Notes do not use; and at 26 rooms it is at the edge of what one window
holds. Those are the memory problems of Part two, and nothing in the prose rules
addresses them.

---

## Part three: what to keep

The agent executing this plan must not tear these down. Several were arrived at twice,
here and in Drakenhold independently.

1. **The three tests in `GENRE.md`** and the fixed "What a line has to earn" block.
2. **The read-set graph**: `STEPS.md` names a template, a template names its pattern entry
   points, a Spec line names what it draws, and `validate_setting.py` walks it.
3. **Rated Spec blocks** (`1`, `40%`, `{a | b | c}`). An unrated menu collapses to its
   first option.
4. **The four blocks** (substrate, challenge, reward, registry) and their per-rating
   variants.
5. **Blocks as the DANGEROUS generation unit**, one typed diagram per block,
   existence-only diagrams above.
6. **Two-ended elements as obligations**, and zero unconsumed obligations at close.
7. **The container/data split** and 4d with every citing location in view.
8. **`setting/Language.md` as a living root list** with coinage recorded back.
9. **The validator's posture** and its `--pending` and `--read-set` modes.
10. **`build_site.py` and `build_pdf.py`**.
11. **The three judgement checks**, especially the upward audit and Room to Grow.
12. **Step ids that grow by suffix and are never renumbered.**
13. **The rules interface already half-built**: `(Test of Constitution, ...)` citations
    checked by grammar, with the rulebook as the referee's reference.

---

## Part four: findings

Each finding states the evidence, why it matters, and the task that answers it. Where
the first draft of this file got the intent wrong, the correction is recorded.

### F1. The prose target is not written down, so every rule aims at a failure instead of at a style

`GENRE.md` says what a line must not be. `templates/Location.md` instruction 5 says what
punctuation it may use. Nothing says what a good location reads like: no exemplar, and
no statement of what is taken from *The Hole in the Oak*, *Arden Vul* and *B4* each.
Each PR from #35 to #41 identified a failure by reading output, wrote a rule against it,
and the next build found the failure the rule permitted. A generator given a
prohibition list and no positive target finds the next unprohibited way to be bad.

The three references agree on a form the template already has: room name, a sentence or
two of what is obvious, bold-labelled bullets each holding one thing, mechanics in
parentheses. What none of them do is ban the full stop. The Hole in the Oak's branch
form is `Label: outcome. Label: outcome.`, which instruction 5 forbids, which is why a
Feature that wants two branches is comma-spliced into one line.

**Answered by** P1.1, P1.2, P1.3.

### F2. Feedback becomes a specific prohibition, never a list entry, an exemplar or a check

40 of 65 pattern files carry Constraints such as "Never write a bare 'a door'", "Never
give a swarm a countable number". `GENRE.md`'s consequences reached thirteen. Instruction
5 is 340 words written after one measurement. There is no intake procedure. Drakenhold's
six routes were the most effective process document in that repository and have no
analogue here.

Read against Part two, most of these Constraints are a missing list entry: the model
wrote the average door, the average swarm, the average dead end, and the fix landed as a
prohibition on the average instead of a list the draw could land elsewhere on. The
missing rungs between the three tests and a Constraint are: a list entry in `genre/`,
an exemplar, and a **tell** (a measurable signature of a class of failure, which #41
computed by hand and nothing keeps computing).

**Answered by** P2.1, P2.2, P2.3.

### F3. The genre tree is the deferred half of a two-part design, and the Spec's question-or-pattern rule is why it matters

*Correction.* The first draft read System B as a design choice that closed the door on
portability. The user's account: System B was sequencing, one target at a time, with the
`genre/` tree always intended as the fourth tree. The finding stands with its intent
corrected.

State: `setting/Tags.md` and region pools are pure colour, two tags per stub. The
`## Design patterns` sections in 37 files, about 10,000 words, are the genre content,
and they are generic fantasy written once by hand, never compiled from a reference.
System A's three-facet pools (Institution/Condition, Agent/Threat, Site-Type) for
fantasy, Mothership and Fallout, proven portable by a nine-location slice, are
recoverable at `b6e0bf7`.

The rule that makes the tree load-bearing is `SPEC.md`'s own: a Spec line is a question
or a pattern to match. A question yields the logical average; a match against a list
yields diversity. Every menu currently written as prose in a Design patterns section is
a list waiting to be drawn from, and the trope layer the original "B/X cameo" rule asked
for is one facet of the same lists. Cameos do not need a step or a file of their own.

**Answered by** P3.1 through P3.4.

### F4. Procedures re-derives mechanics the rules should only be cited for

*Correction.* The first draft read the absence of the Notes' moves as a gap and proposed
wiring them into the region templates. The user's account: they were left out because
they forced generation to integrate procedures that need no content (a Search move
says what happens while searching, not how well; Carousing needs no location, only
the social places that already exist). The rules should not shape the content; they
should provide an interface, and the interface is a locked output format the referee
picks up in the rulebook.

The finding then is the opposite of the draft's: `setting/Procedures.md` does too much,
not too little. Its seed re-derives a Test ladder, an `Xd` notation, wounds as states, a
Conditions list and a treasure taxonomy, and each has drifted from the Notes (one Test
versus `Xd`; Combat die versus "whichever fits"; wounds as a count versus a state; the
five treasure tables). Some divergence is the moving rules target, which is expected.
The rest is a seed doing a rulebook's job. What survives is the interface already in
`templates/Location.md`'s Citations section: a fixed citation grammar per kind of
mechanical hook, checked by the validator, resolved by the referee against whatever
revision of the Notes they hold.

**Answered by** P4.1, P4.2.

### F5. The region brief is the profile, and it has no template

*Correction.* The first draft proposed a `profiles/` tree. The user's account: genre was
meant to carry some of this, and Region E shows the real mechanism: a specific brief
from the user, built to. Iterative growth as players explore is expected, so a profile
changes during development.

What is missing is small: the brief has no template and no place. Region E's brief
lives in a PR description. `STEPS.md` 3a decides region count in prose. 4d and 5c are
end-of-build in the text though E ran them per region. Reinforcement is "outside the
build". Nothing marks a release.

**Answered by** P5.1 (the brief), P5.2 (per-region close), P5.3 (wiring), P5.4 (ship).

### F6. WILD is the weakest rating

Region B: 6 locations, 4 edges, two disconnected components. `region/Wild.md` puts the
ground between points in the Terrain field and stops. Drakenhold's `WILD_LOW.md` reached
the governing insight, a road's negative space is time and cannot be keyed, and this
repository does not carry it. Per F4 the fix is not a travel procedure; per F12 it is
the user's map: hexes with landmarks placed in them, distances readable off it, and a
connectivity error in the validator so a region cannot ship in two pieces.

**Answered by** P4.3.

### F7. The voice question is a world-building rule, not a register

*Correction.* The first draft raised the dropped "poetry for the players" register. The
user's account: ninety percent of the text is for the referee, the page-to-referee-to-
player translation is already the standing rule, and what "hinting at a larger world"
actually asks for is a world-building rule of its own. Agreed: a fact that points past
the edge of the map, stated once per region, is a `GENRE.md` consequence, not a Tolkien
register. It already half-exists as `Settled at: nowhere on this map`.

**Answered by** P1.1 (STYLE.md keeps one register) and P2.3 (the consequence is added
in the audit, and the count stays under the cap by merging).

### F8. Pattern prose is most of the read set and restates the block

`SPEC.md` forbids restating the fenced block in the prose beneath it. Measured, the prose
is where the words are, and much of it explains why a line exists, which is
commit-message material by the repository's own rule.

**Answered by** P3.1 and P6.1.

### F9. The validator has no fixture

Checks are tuned against Telar. A rewrite of Telar loses the tuning.

**Answered by** P1.2 and P2.2.

### F11. The setting in the tree corrupts the context that generates the rest of it

The user's account of the six regenerations: leaving an existing setting in the tree
tends to corrupt context, which is why owed debts, tally sheets and boundary stones,
each fine once, recur to the point of the ridiculous. The mechanism is plain once
named: the generator reads sibling rooms and registries while writing a new room, and
what it reads it reinforces. Telar has three Tallies in Region E's three master niches
and a Ledger, a Tally and a Toll in the first two regions; `GENRE.md`'s "repetition
before explanation" rule licenses the motif and nothing bounds it.

Two consequences. A **motif-saturation tell**: a noun that appears in more than a
stated share of a region's rooms is a warning, computed by a script, not by taste.
And a **context discipline**: a room is generated from its contract, its draws, its
brief, its region overview, its graph edges and the exemplar, never from its sibling
rooms. The registries are read only for a name a citation needs. `tools/context.py`
is what enforces that, because a model told "consult only to look up a name" does not.

The same fact decides where a shipped example lives: not in `main`'s `setting/`. The
template ships with an empty `setting/` (the validator's fresh-start state), and a
built module lives on its own branch or release tag.

**Answered by** P2.4 (the tell), P3.2 (the assembler), P7.2 (where the example lives).

### F12. The map is meant to be an input, and 4b treats it as an output

The user's account of Q4: the expected output performs well for both hex crawl and
point crawl because the user draws the map first, hexes for WILD with landmarks placed
in them, a dungeon map for DANGEROUS, and hands the generator a target of connections
and room sizes; with that, generated content is close on the first try.

`STEPS.md` 4b has the generator draw the diagram. The format the user actually writes
a map in is a numbered room list, one line per room: dimensions, fixtures, and exits
as `door heads west->2`, with `corridor` and `Entrance` as off-map ends
(`fixtures/control/arm1-prompt.md`). That is lighter than `Locations.md` plus mermaid
and carries everything the framework's two files hold: code, size, edge, edge kind
(door, opening, double door, secret door, stairs), direction. Converting it is a
script's job, inside the scripting boundary. This also settles "the path is not clear"
for WILD without a travel procedure: a human draws the loops.

**Answered by** P4.3 (map-first at 4a and 4b, with `tools/map.py`) and P5.1 (the brief
points at the map).

### F10. The user's original rules, mapped

| Original rule | Where it lives now | Gap |
|---|---|---|
| Follow the TTRPG Design Notes | the citation grammar in `templates/Location.md`; `Procedures.md` overreaches | F4 |
| Follow the template; illustrative content never enters | `templates/` | none |
| Sandbox | `GENRE.md` consequence | none |
| Lived-in world, constructed language | `Language.md`, `Naming.md` | none |
| The path is not clear | DANGEROUS topology; nothing for WILD | F6 |
| Every gate has an answer that is not the gate | `GENRE.md` consequence | none |
| Negative space | class mix, LOW as residue, "withholding is content" | replaced deliberately; fine |
| Three tiers of detail | obvious/trigger/secret chain | none |
| Layers of history | three occupancies; Left lines | none |
| Player mechanics, clues always exist | Clue/Trigger/Payload per class | none |
| Prose for the referee | Referee Notes, Dressing size line | not stated as a style; F1 |
| Poetry for the players, hinting at a wider world | absent | F7, as a world-building rule |
| OSR playstyle | `GENRE.md` | none |
| B/X cameo | absent | F3, as a list facet |
| Tables follow classification | `templates/Region.md` | none |
| Names compound from roots | `Language.md` REGISTER | none |

---

## Part five: the target shape

```
CLAUDE.md  README.md  STEPS.md  GENRE.md        as now; GENRE.md generated at 1a
STYLE.md                                          NEW  the positive prose contract (P1.1)
FEEDBACK.md                                       NEW  intake routes and log (P2.1)
templates/                                        the output format; Location.md grammar revised;
                                                  Brief.md added (P5.1); Procedures.md an interface (P4.2)
patterns/                                         CONTRACTS ONLY: Provides / Spec / Constraints (P3.1)
genre/                                            NEW  the fourth tree (P3.1)
  bx-1981/                                        the baseline pack (P3.2)
    PACK.md                                       identity, axis defaults, seed pool
    lists/<name>.md                               one draw list per name a Spec line cites:
                                                  doors, containers, purposes, clues-underground,
                                                  clues-outdoors, demeanours, tropes-safe, ...
    Tags.md                                       the setting-pool seed
    Vocabulary.md                                 per-rating word lists
    Bestiary.md                                   seed entries, renamed via Language
  <second-pack>/                                  P3.4 proves the shape
rules/
  README.md                                       the interface contract; Notes.md optional, pinned (Q1)
style/
  exemplars/                                      six golden entries, read at 4c (P1.2)
  tells.txt                                       the tell list the validator reads (P2.2)
fixtures/
  bad/  good/                                     known-bad entries per tell; the exemplars (P2.2)
  briefs/drakenhold.md                            the campaign-scale brief, committed (P0.2)
  control/                                        the three control arms and their outputs (P0.2)
tools/                                            as now, plus draw.py, context.py, map.py, metrics.py, --status
setting/                                          EMPTY on main; the only variable in a build (F11)
  region/[Code].brief.md                          the user's brief per region (P5.1)
  region/[Code]/Locations.md, *.mmd               may be authored by the user: the map (P4.3)
checks/                                           as now, plus Playtest.md (P5.5)
```

Frozen per release: everything but `setting/`, `checks/`, `GENRE.md`. Customised by
the user: `GENRE.md` via the step 1a questionnaire (pack plus dials), one brief and
optionally one map per region. The rules stay out of tree (Q1); only the citation
grammar in `templates/` couples to them, and `templates/` is the one place the user
expects to keep tweaking as the rules move.

**The output format is not on the table.** The user is largely happy with the formatted
output as it stands: the location header, the Player Summary, the Referee Notes, the
bold Feature labels, the Exits line, the citation forms, the region fields and tables.
Every task below that touches `templates/` changes sentence-level grammar or adds a
field; none changes the shape a referee sees. Tweaks to setting references (how a
Feature cites a registry or a table) are the one area the user named as open.

Success criteria:

1. P0.2's control comparison is recorded and the framework beats the short prompts on
   the one-shot, or the cuts in Phase 3 and 6 are made without regret.
2. A fresh clone plus one step-1 session produces `GENRE.md`, `setting/Tags.md`,
   `Procedures.md` and `Language.md` under the B/X pack.
3. One brief per region, three regions, reach 5c in at most six further sessions at
   zero validator errors, and the site builds.
4. A second pack passes the nine-location slice with no fantasy nouns leaking.
5. Every feedback item since the plan landed is logged with a route, and every route
   that added a rule also added a list entry, a tell or an exemplar first.
6. `context.py 4c` prints at or under 6,000 words for every rating, and no sibling
   location is ever in a room's context.
7. Two generations of the same location under the same brief draw different doors,
   containers and clues, by arithmetic.
8. The motif-saturation tell reports nothing above threshold on the shipped example.

---

## Part six: the plan

Each task has an id, goal, files, steps, and an acceptance test. "One session" is one
Pro-plan sitting for an Opus agent.

### Phase 0: freeze, measure, and run the control (two sessions)

~~**P0.1 Tag the baseline and record metrics.**~~ Landed. `tools/metrics.py` prints the
report and **Baseline metrics** below is its output, naming the two figures in Part one
it does not reproduce and the one push that section still owes.

~~**P0.2 Run the control, three arms, on the user's twelve-room map.**~~ Landed.
`fixtures/control/COMPARISON.md` is the acceptance table, item by item and arm by arm, with
the arm outputs beside it: `arm0-prompt.md`/`arm0-output.md`, `arm1-output.md`, and
`arm2-prompt.md`/`arm2-brief.md`/`arm2/`. Three results bind later phases and are recorded
there rather than restated here: the framework wins the four registry-shaped items and
loses "short descriptive sentences" and "B/X stat lines" to the eighty-word prompt;
`templates/Region.md`'s Overview field mandates an absence claim `GENRE.md` forbids, and
`templates/Location.md`'s one-sentence Feature rule produces 27.9 words per sentence
against the endorsed baseline's 13.8, both of which P1 has to settle; and arm 1 ran without
its Notes, which the comparison's Methodology section prices.

### Phase 1: the house style (four to six sessions)

**P1.1 Write `STYLE.md`.**
- Files: new `STYLE.md`; `CLAUDE.md` names it beside `GENRE.md` as re-read at every
  generation step.
- Steps: under 800 words, in this order: the three published sources and what is taken
  from each, with one shape example per source (shape, never quoted text), and the
  baseline output at `fixtures/control/arm1b-output.md` as the fourth source, the one
  the user has endorsed and the one the exemplars are written against; the one
  register, the referee's, and how the spoken Player Summary differs from it (spoken,
  one to three sentences, bolded nouns are promises, never a conclusion); **which
  referee asides are allowed**: an instruction about running the room ("do not prompt
  them", "let them interpret") stays, a statement of what the players will feel or
  conclude goes, and an unwitnessable claim about the setting goes; the sentence
  budget, taken from the baseline's measured shape (one to four sentences per Feature,
  about fifteen words each); the tells, pointing at `style/tells.txt`.
- Acceptance: a reader who has never seen the repository writes one Feature and one
  Summary from `STYLE.md` alone. The user approves before P1.2.

**P1.2 Write the exemplars.**
- Files: new `style/exemplars/`: one SAFE working location, one WILD landmark with a
  hidden child, DANGEROUS high, medium and low, one DANGEROUS region overview. Codes
  `X.n`, no Telar nouns.
- Steps: write each to `STYLE.md` and the class file's Spec exactly as 4c would, then
  hand-edit to the target with `fixtures/control/arm1b-output.md` open as the register
  to match: its Area 8 (a trap with visible mechanics and a pit that is a containment,
  not a kill) is the DANGEROUS medium shape, its Area 6 (the dwarves) is a faction
  presence with a want, a stance and a betrayal threshold, and its Cobb's Landing
  entries are SAFE working locations with prices and a refusal each. Every line the
  class file draws at `1` is visibly present. Add to `templates/Location.md`'s Context:
  "the exemplar for this rating and weight".
- Acceptance: the user approves all six; they pass the location checks with zero
  warnings; they are the regression floor for every later grammar change.

**P1.3 Replace the punctuation ban with a sentence budget.**
- Files: `templates/Location.md` instruction 5; `check_feature_grammar`.
- Steps: a Feature is one to three sentences, each about twenty words or fewer;
  `Label: outcome.` branches are sentences; `->` still means trigger to effect; a
  citation sits last; no trailing ` - ` clause and no non-citation parenthesis. Delete
  the eight-word segment and comma-only rules. The check errors on the trailing clause
  and stray parenthesis, warns on a fourth sentence or a long one, warns on each tell,
  and warns on a comma inside a phrase (`, the ` or `, a ` after a preposition).
- Acceptance: the exemplars pass clean; E.22's line now warns; Telar reports errors,
  cleared by P1.6. The rendered shape of a location (site and PDF) is unchanged: this
  task touches sentences, not the format.

**P1.4 Bring the Region Overview under the same style.** Parallel with P1.5.
- Files: `templates/Region.md`; `STYLE.md` region section.
- Steps: field descriptions cut to one line each pointing at the region exemplar;
  rationale paragraphs moved to `STYLE.md` where they are style, cut where history.
- Acceptance: `templates/Region.md` under 60 lines.

**P1.5 Bring the setting-level artifacts under the same style.**
- Files: `templates/History.md`, `Truths.md`, `Rumours.md`, `Bestiary.md`, `Factions.md`.
- Steps: state each budget once in `STYLE.md` and cite it.
- Acceptance: no template restates a rule `STYLE.md` owns.

**P1.6 DEFERRED: rewrite Telar to the new grammar.** Cut at the user's final check:
five sessions on content D3 removes. The exemplars are the fixture; if the checks need
tuning against a whole region, rewrite Region A only, as part of P1.3.

Original task, kept for its measurements:
- Files: `setting/region/*`.
- Steps: order A, C, B, D, E, exemplar open. Nothing a party can find is removed; every
  citation, exit and Test unchanged. `metrics.py` delta in each commit body.
- Acceptance: zero errors; mean sentences per Feature 1.2 to 2.0; zero comma-inside-
  phrase warnings; "rather than" under 15; the user reads two regions and accepts.

### Phase 2: feedback intake and the rule ladder (two sessions)

**P2.1 Write `FEEDBACK.md`.**
- Files: new `FEEDBACK.md`; one `CLAUDE.md` line: feedback on generated content is
  routed through it before any file changes.
- Steps: the routes, in the order they are tried:
  - **R1 Content**: about one location or field. Fix `setting/`. Nothing else.
  - **R2 List**: the output was the average, or generic. Add entries to the
    `genre/<pack>/lists/` file the Spec line draws from. This is the route most
    existing Constraints should have taken.
  - **R3 Exemplar**: a register the exemplars do not show. Edit or add one.
  - **R4 Tell**: a recurring class with a textual signature. One line in
    `style/tells.txt` and one known-bad fixture.
  - **R5 Rule**: a class with no signature and no list. One sentence in `STYLE.md` or
    one `GENRE.md` consequence, only if it names the judgement-check item that will look
    for it. Consequences capped at twelve; past the cap, merge.
  - **R6 Constraint**: about one pattern file's output and no other. Last resort.
  - **R7 Rules project**: a mechanic the interface cannot cite. Log and stop.
  - **R0 Playtest**: an observation from the table, logged here as a line until P5.5
    exists; becomes an item only on a second session or a failed chain re-read.
  A log: date, quote, route, commit; struck when landed.
- Acceptance: the user approves the routes; the last three PRs' rule additions are
  retro-classified as a worked example, and most land on R2.

**P2.2 Make the tells data, with fixtures.**
- Files: new `style/tells.txt`, `fixtures/bad/`, `fixtures/good/` (the exemplars);
  `validate_setting.py --fixtures`; CI.
- Acceptance: CI green; adding a tell is one line plus one fixture.

**P2.3 Audit the Constraints and consequences.**
- Files: every Constraints section; `GENRE.md` and `templates/Genre.md`.
- Steps: table each entry as keep, list (move to a `genre/` list, cut here), tell,
  exemplar, merge, or cut. One more column: **does the baseline break it?** Read each
  Constraint and each consequence against `fixtures/control/arm1b-output.md`. A rule
  the baseline honours unprompted is diagnostic, not generative, and is a candidate for
  the judgement checks rather than for generation-time context; a rule the baseline
  breaks and the user still endorses the output of is a rule to cut. Add the "one fact
  per region points past the edge of the map" consequence (F7) and stay under twelve
  by merging.
- Acceptance: consequences at or under twelve; no Constraint a list or tell already
  covers; the fixed block byte-identical in both files.

**P2.4 The motif-saturation tell.**
- Files: `tools/metrics.py`; `tools/validate_setting.py`; `style/tells.txt` gains a
  section for it.
- Steps: measured on Telar while writing this task, the user's named motifs are not
  dense inside one region; they are spread across regions: "tally" in 6 rooms across 4
  of 5 regions, "toll" in 8 rooms across 4, "cairn" in 5 across 3, "sealed" in 17 rooms
  across 3. A per-region density count misses them and is swamped by structural words
  (exits, feet) and nouns a region legitimately owns (mound, niche). So the tell counts
  **region spread**: for each content noun (after a stopword list, the structural
  vocabulary, Bestiary, faction and `Language.md` names), the number of regions it
  appears in and the number of rooms. Warn at three or more regions and five or more
  rooms: "motif 'tally' in 6 rooms across A, C, D, E". A second signal is the
  setting-level seed: the same nouns counted across `setting/*.md` and the region
  overviews (toll 54, Essath 48, sealed 38, bound 24 on Telar) so the user can see
  which motifs the context is seeding before a room is written. Both thresholds live
  in `tells.txt`.
- Acceptance: the check reproduces the tally, toll and cairn findings above without
  being told the words; it is a warning, never an error.

### Phase 3: the four trees (five sessions)

**P3.1 Reduce `patterns/` to contracts and create `genre/`.**
- Files: all `patterns/*/*.md`; new `genre/bx-1981/`; `SPEC.md`; `STEPS.md` 1b; the
  validator's compile-list and read-set checks; the site's pattern page.
- Steps: for each of the 37 files on the compile list, move the `## Design patterns`
  section into `genre/bx-1981/lists/`, split by what it lists: the menus become one file
  per list (`doors.md`, `door-condition.md`, `containers.md`, `purposes.md`,
  `clues-underground.md`, `clues-outdoors.md`, `clues-social.md`, `demeanours.md`,
  `dispositions.md`, `mechanisms-nuisance.md`, and so on), one entry per line, numbered.
  The neutral file keeps Provides, Spec and Constraints, and every Spec line that was a
  menu or a "what it is" question now cites its list: `1 Type (genre: doors)`. Prose
  beneath the block is cut to what changes a generator's output; expect two thirds to
  go. `SPEC.md`'s skeleton becomes three sections and gains the list-citation form.
  The validator checks every `(genre: name)` resolves to a list in the selected pack
  and every list is cited by at least one line; `--read-set` adds the cited lists.
- Acceptance: zero errors; no `## Design patterns` under `patterns/`; `patterns/` at
  or under 12,000 words; the site renders contract and lists side by side.

**P3.2 Make the draw arithmetic, and assemble the context.**
- Files: new `tools/draw.py`, new `tools/context.py`; `templates/Location.md`
  instructions; `STEPS.md` 4c.
- Steps: `draw.py <location-code> <list-name>...` returns, per list, an index and the
  entry, derived from a hash of the code and the list name, with `--reroll N` to move
  on. Rated lines (`40%`) resolve the same way against a fixed threshold.
  `context.py 4c <location-code>` then prints, in one stream and nothing else: the
  class contract, the drawn entries (not the lists), the region brief, the region
  overview, this location's stub and its edges from the diagram with the far ends'
  names only, `setting/Truths.md`, the exemplar for this rating and weight, the
  template, and the citation grammar. It never prints a sibling location, and it
  prints a registry only as the names a citation may use. 4c's instruction becomes:
  run `context.py`, write to what it printed. The site's location page may show the
  draw record as a collapsed note for the user's review; the PDF never.
- Acceptance: criterion 7 in Part five; the user rerolls one draw on one exemplar and
  the entry changes without a rule changing; `context.py 4c` for a DANGEROUS medium
  location prints under 6,000 words, which is where the Pro-plan budget is actually
  won.

**P3.3 Build the B/X 1981 baseline pack.**
- Files: `genre/bx-1981/PACK.md`, `Tags.md`, `Vocabulary.md`, `Bestiary.md`; the
  `lists/` from P3.1 extended; `patterns/setting/Genre.md` seed pool.
- Steps: `PACK.md` is derived, with the Notes open once, from the sections that gave
  the user's one-shots their baseline: Implied Setting (points of light, ruined empire,
  mythic underworld, low magic), Literary References (the six authors and seven
  modules), Creature Types, and the Treasure types. It states the assumed setting the
  way `GENRE.md`'s paragraph does and every Q2 axis default. The Notes are then closed;
  the pack carries the content so the Notes need not be in context at generation. The lists gain a
  `tropes-<rating>.md` facet, ten to fifteen shapes per rating, each a shape and a
  constraint and never a named monster; class files draw it at a low rate in the
  registry block. The lists moved as-is in P3.1 are rewritten only where they fail "be
  specific, not generic" (Q6). `Bestiary.md` holds fifteen to twenty classics under
  plain names, renamed through `Language.md` at 2e.
- Acceptance: the validator requires `PACK.md` with every axis defaulted; one location
  per rating generated from the exemplar shape under this pack reads as B/X to the user.

**P3.4 DEFERRED: wire the axis dials to Spec rates.** A pack states its axes in
`PACK.md` and the generator reads them; inline brackets and a checker are worth
building only when a second pack exists. Original task:
- Files: `patterns/setting/Genre.md`; the few Spec lines that should move (hazard
  tiers, ward and residual caps, Unique Treasure count, SAFE count and die, WILD count).
- Steps: inline brackets on those lines only: `20% lethal [lethality: low 10% | high
  30%]`. The validator checks every axis `GENRE.md` states is referenced by a bracket and
  no bracket names an unstated axis.
- Acceptance: setting lethality low and regenerating one exemplar changes its tier draw.

**P3.5 DEFERRED: prove portability with a second pack.** Scope is OSR fantasy for now
(the user's System B decision). Run when a second genre is wanted. Original task:
- Files: `genre/scifi-horror/` recovered from `b6e0bf7^`'s `tags_scifi.md`; a
  `fixtures/slice/` of three locations per pack.
- Acceptance: zero cross-pack noun overlap outside behavioural primitives; the user
  confirms no fantasy furniture leaked. A proof, not a supported product.

### Phase 4: the rules interface (two sessions)

**P4.1 State the interface, verified once against the Notes.**
- Files: new `rules/README.md`. No `rules/Notes.md` in tree (Q1).
- Steps: `README.md` states the contract: the rules are external and moving; the
  framework's only coupling is the citation grammar in `templates/Location.md`; a
  citation names a Test kind and what is at stake and nothing about resolution; the
  referee resolves it against whatever revision they hold. Lists the citation forms
  and where each is checked. Then, once, with the Notes the user supplied open, check
  every form against the rulebook's own vocabulary: Test of Constitution, Sanity and
  Fate exist there; the six damage types exist there; Conditions are the Notes'
  free-form name/effect/duration and the setting's list is an instance of that; `Xd`
  does not exist there and is recorded as the framework's proposal, which the user
  says is a candidate for the next rules revision if playtesting proves it. The Notes
  are then closed and not cited again; the README records the revision date checked.
- Acceptance: the README is under 300 words, every citation form it lists has a
  validator check, and the one-time verification is recorded in the commit body.

**P4.2 Cut `Procedures.md` to the interface.**
- Files: `templates/Procedures.md`, `patterns/setting/Procedures.md`,
  `setting/Procedures.md`.
- Steps: remove from the seed everything that restates or re-derives a mechanic the
  rules own: the Test ladder, wound effects, the Search rule as a mechanic (the
  no-roll-for-secrets rule stays, as a content rule in `GENRE.md` where it already is),
  the Scaling section beyond the AD ladder the Bestiary needs. What remains: the
  citation grammar with one line per form, `Xd` included (Q2: it stays as the
  template's current form and is the kind of thing the user expects to keep tweaking
  in `templates/` as the rules move); the Conditions list, because a citation names one
  and the referee needs the name resolved; Time by rating in one line each; Region
  Dice in three lines; currency and wage as setting facts; the treasure taxonomy as a
  setting fact.
- Acceptance: `setting/Procedures.md` under 600 words; every term in it is a citation
  form, a Condition name, or a setting fact; nothing in it tells the referee how a roll
  resolves.

**P4.3 Map first: 4a and 4b accept a user-authored map, via `tools/map.py`.**
- Files: new `tools/map.py`; new `templates/Map.md`; `STEPS.md` 4a and 4b;
  `templates/Location_Gazetteer.md`; the validator's stub parser and Referee Notes
  check; `patterns/region/Wild.md`.
- Steps: `templates/Map.md` is the user's own room-list format, stated once: one line
  per room, `N. WxL. fixtures. exits`, exits as `<kind> heads <direction>-><N>`, with
  `corridor`, `Entrance` and the like as off-map ends; for WILD, one line per hex or
  landmark with distances in place of dimensions. `map.py <region-code> <map-file>`
  writes `Locations.md` stubs (name left as the fixture phrase until 4c names it, size
  carried in parentheses after the name), the block diagram with edge kinds read off
  the exit words (door and opening are `---`, secret door `-.-`, stairs and shaft
  `---|vertical|`, a one-way phrase `-->`), and the block header. It never invents an
  edge or a room; a map with no exit to a room is an error it reports. 4a and 4b state
  that a user map is authoritative and the generator fills only what is absent.
  `check_location_file` warns when the Referee Notes' stated dimension disagrees with
  the stub's. `region/Wild.md` says distances come off the map and are stated in
  Layout; "every Landmark reachable" becomes an error. Region B is connected by hand
  as the worked example, and `fixtures/control/arm1-prompt.md`'s map is the DANGEROUS
  fixture the script is tested on.
- Acceptance: `map.py` round-trips the control map into a `Locations.md` and a block
  diagram that pass the validator with zero errors; a user-authored map survives 4c
  untouched; TOPOLOGY reports B as one component.

### Phase 5: the iterative workflow (three sessions)

**P5.1 The region brief.**
- Files: new `templates/Brief.md`; `STEPS.md` 3a and 3c; `setting/region/[Code].brief.md`
  per region.
- Steps: the brief is what the user hands the generator per region and what Region E's
  PR description was: rating, die, size, what the region is for, what it must contain,
  what it must not, which existing elements it touches, and whether a map is supplied
  (P4.3). Under 20 lines. 3a reads the briefs that exist rather than deciding count in
  prose; a one-shot is three briefs. A brief may be amended as play reveals what the
  region needs, and an amendment is a new region pass, not an edit to written rooms.
  Region E's brief is recovered from its PR and committed as the region-scale worked
  example; `fixtures/briefs/drakenhold.md` is the campaign-scale one, and its gazetteer
  lines (rating, die, one paragraph, a location count where the user cared) are the
  shape a region brief compresses to when the user is in a hurry.
- Acceptance: every region in Telar has a brief file; 3a cites the template.

**P5.2 Per-region close.**
- Files: `STEPS.md` 4d and 5c; the five registry templates' two-phase text;
  `build_complete` in the validator.
- Steps: 4d runs at the close of each region for every stub whose citing locations are
  all written; a row citing unwritten ground stays a stub and is an obligation. 5c runs
  per region; the end-of-profile sweep is 5d, a new id. `build_complete` becomes
  per-region.
- Acceptance: `--status` shows a region closed when its rows are full.

**P5.3 The wiring step.**
- Files: `STEPS.md` step 6; `templates/Setting_Judgement_Check.md` Room to Grow gains
  "acted on at".
- Steps: region-scoped, additive only: choose Room to Grow candidates with the user and
  write the reinforcement into rooms already on disk, or draw a cross-region edge at
  both ends. Never a new location. Drakenhold's finding that baseline-then-reinforce
  beats forward-declared threads is the reason.
- Acceptance: one pass over Telar lands three rows; validator clean.

**P5.4 The ship step, reduced to a tag.**
- Files: `STEPS.md` step 7 only.
- Steps: ship is a git tag on the example branch and the Pages build that already runs.
  No flag, no code. Nothing is stripped; the output carries no authoring scaffolding,
  so ship can run per edition.
- Acceptance: one sentence in `STEPS.md`.

**P5.5 DEFERRED: playtest intake.** Drakenhold built it before any session ran and it
stayed empty. Write it after the first playtest of the example, when its shape is
known; until then a playtest observation is a `FEEDBACK.md` line. Original task:
- Files: new `checks/Playtest.md`.
- Steps: a table of what happened and where, never what to do about it; route R0.
- Acceptance: the file exists with its rule.

### Phase 6: session economics (two sessions)

**P6.1 Cut the read set to the budget.**
- Files: pattern prose left after P3.1; `--read-set --words`.
- Steps: measure per entry point; cut prose that explains why a line exists or restates
  another file. Targets: DANGEROUS medium at or under 10,000 words with lists counted;
  WILD landmark under 8,000.
- Acceptance: targets met; the exemplars regenerate from the trimmed files without
  losing a rated line, spot-checked on two.

**P6.2 Trim the setting-level read set.**
- Files: `README.md`; every template's Context list.
- Steps: `README.md` (600 words, injected every turn) to the map and commands, under
  400. `Language.md` moves to "consult when coining".
- Acceptance: no Context list names a file the step's output never cites.

**P6.3 `--status` as the handoff.**
- Files: `tools/validate_setting.py`.
- Steps: per region, the step reached, open obligations, unfilled rows, unsettled
  rumours. A handoff document drifts; this is derived.
- Acceptance: a fresh session picks its next task from `--status` and `STEPS.md` alone.

### Phase 7: long form (two sessions, after a one-shot has shipped)

**P7.1 DEFERRED: block connective documents.** Premature until a DANGEROUS region with
more than one block is built. Original task:
- Files: new `templates/Block.md`; `region/Dangerous.md` BLOCKS.
- Steps: for a DANGEROUS region with more than one block, a short document per block:
  purpose family, what it hands to neighbours, an optional Danger table override, and
  the unnamed-fill description so negative space is run rather than left blank.
  Drakenhold's `blocks/` carried this for 22 regions in three peaks.
- Acceptance: required per block when a region has more than one; none otherwise.

**P7.2 Regenerate a shipped example under the B/X pack, off `main`.**
- Files: `setting/` wiped on `main` to the fresh-start state; a branch
  `example/<name>` where three briefs are built under `genre/bx-1981/`.
- Steps: per Q3, Telar is written against through Phase 1 and then removed entirely.
  The regenerated module is built on its own branch, one session per step or region,
  logging every friction point in `FEEDBACK.md`, and shipped from that branch with
  P5.4's release tag and the Pages site. `main` keeps `setting/` empty so that no
  built content sits in the context of the next build (F11). The user's tweaking phase
  on the example is minor edits and playtest rework, not a rewrite.
- Acceptance: criteria 2, 3, 6 and 7 in Part five hold on the example branch; `main`
  validates as a fresh start; the site is built from the tag.

---

## Part seven: decisions recorded

The six open questions of the previous revision, answered by the user. These are not
to be re-litigated by a task; a task that finds one wrong logs it in `FEEDBACK.md`.

**D1. The rules stay out of tree.** The Notes combine the user's house rules, speculation
and a genre context that can misalign with a build's target. They are used once, at
P4.1, to build and verify the citation interface, then closed. No `rules/Notes.md`.

**D2. `Xd` stays, in the template.** A Test specifying a number of rolls to proceed
unscathed is a test case the user will fold into the rules if playtesting proves it.
The output format is the user's own moving target, which is why `templates/` is
separate from `patterns/` and is where that tweak is made when it changes.

**D3. Telar is written against, then removed.** Phase 1 rewrites it as the target
corpus; after the work is complete the tree is emptied and a module is regenerated on
its own branch (P7.2). Leaving a setting in tree corrupts context (F11). The user's
tweaking phase is playtest rework, never a rewrite.

**D4. Map first, and both crawls.** The user draws the hexes or the dungeon map, places
landmarks, states connections and room sizes; the generator writes to it (P4.3). Point
crawl and hex crawl are the same output with a different map behind it.

**D5. The lists moved from Design patterns are kept where the content is good**, and
grown through route R2. No wholesale rewrite.

**D6. The control has three arms**: no prompt, the user's short prompt, the framework,
all on the user's twelve-room map (P0.2). The prompt and map are committed verbatim at
`fixtures/control/arm1-prompt.md`; the Notes attach at run time. The Drakenhold brief
at `fixtures/briefs/drakenhold.md` is the campaign-scale brief example, not the
control's input.

**D9. The map format is the user's room list.** One line per room, dimensions,
fixtures, `->` exits. The framework converts it (`tools/map.py`, P4.3); the user never
writes `Locations.md` or mermaid by hand.

**D7. The output format is settled.** What changes is sentence grammar and setting
references, never the shape a referee sees.

**D8. Scripts draw, assemble, count and check. They never write prose.**

---

## Baseline metrics

`5780bd9` is the state every later phase is measured against, and `framework-v0` is the
tag for it. The tag is made locally; pushing it needs credentials a session does not
carry, so it is owed - `git tag -a framework-v0 5780bd9 && git push origin
framework-v0`. The sha is what the figures below are anchored to either way.

What follows is `python3 tools/metrics.py` as the commit landing P0.1 prints it. That
commit adds the tool, two README lines and this section, and touches no pattern file,
template or location, so the corpus figures are `5780bd9`'s. Re-run it rather than
editing these figures: a number typed here by hand is a second copy of the corpus.

```
CORPUS
  regions            : 5 (A, B, C, D, E)
  keyed locations    : 64
  words              : 11,690
  words per location : 183
    A:  8 locations,  1,422 words
    B:  6 locations,  1,152 words
    C:  8 locations,  1,164 words
    D: 18 locations,  3,604 words
    E: 24 locations,  4,348 words

FEATURES
  Features           : 209
  words per Feature  : mean 22.3, max 42 (body with citation)
  prose words        : mean 20.2, max 41 (citation stripped)
  segments           : mean 3.6, max 6
  sentences          : mean 1.00, max 1
  longest            : setting/region/D/9.md 'Unworn Panel'

TELLS
  rather than      :   47   the trailing clause, per PR #41
  absence claim    :    8   absence across time or space, per GENRE.md
  conclusion tell  :    0   the players' conclusion written down, per GENRE.md
  gloss            :   20   a term carrying its own definition, per Location.md
                     'rather than' is in 25 of 209 Features

BUDGET
  authorities    :    4 files,   4,641 words
  templates/     :   23 files,  12,124 words
  patterns/      :   66 files,  45,774 words
  setting/       :   99 files,  33,501 words
  checks/        :    3 files,   1,633 words   (neither framework nor setting)
  fixtures/      :    4 files,  15,092 words   (neither framework nor setting)
  tools/         :    5 files,   4,349 lines
  framework      : 62,539 words
  setting        : 33,501 words
  ratio          : 1.87 words of framework per word of setting

READ SET (step 4c)
  CLAUDE.md                :    835
  README.md                :    636
  GENRE.md                 :  1,592
  templates/Location.md    :  1,851
  setting/Truths.md        :    394
  setting/Procedures.md    :  1,967
  setting/Language.md      :  1,173
  region overview          :    687-998 across 5 regions, mean 830
  fixed context            :  9,278 (with the mean region overview)

  entry point              files  pattern  in context
  dangerous/Creature.md        1    1,179      10,457
  dangerous/High.md           20   14,668      23,946
  dangerous/Low.md            20   15,126      24,404
  dangerous/Medium.md         20   14,886      24,164
  safe/Settlement.md          17   11,014      20,292
  wild/Creature.md             1      535       9,813
  wild/Hidden.md              17    9,338      18,616
  wild/Landmark.md            18   10,042      19,320
  wild/Secret.md              16    8,804      18,082
```

**Where Part one does not reproduce.** Two figures move, and both are Part one's
estimate rather than the tool's arithmetic. Setting words read 33,501 against Part one's
30,600, over 99 `.md` files against its 100, so the framework-to-setting ratio is 1.87
and not the two words of rule per word of output that paragraph rounds to. And the WILD
landmark read set is 19,320 against 18,000, which does not change what that section
concludes - DANGEROUS medium lands at 24,164 with the mean region overview and 24,021
with region D's own, against 23,900. The rest holds: templates at 12,124, patterns at
45,774, authorities at 4,641 (4,600 before this commit's two README lines), 64
locations, 183 words per keyed location, a mean Feature of 22.3 words, and "rather than"
in 25 of 209 Features. Three figures the old table carried are outside what this tool
measures and were re-counted directly: 0 validator errors and 9 warnings (`python3
tools/validate_setting.py`), 25 of 65 pattern files with an empty `## Constraints`, and
13 standing consequences in `GENRE.md`.

**What calibrates the three inexact tells.** Each was run against the corpus as it stood
before PR #41 rewrote it, and against the same tree now - `--tells` over
`setting/region` whole in both cases, so the two are like for like:

| Tell | Before #41 (`a239d81`) | Now (`5780bd9`) |
|---|---|---|
| `rather than` | 132 | 69 |
| absence claim | 75 | 26 |
| conclusion tell | 25 | 4 |
| gloss | 27 | 20 |

The conclusion tell is the sharpest: 25 hits before, 0 across the keyed locations now,
and its per-file listing names the lines the #41 commit body says it cut. The gloss is
the loosest, moving least and over-reporting most - 20 hits, of which D.18's Corbelled
Ceiling, the one documented instance, is no longer one.

Read against the baseline module, `--tells fixtures/control/arm1b-output.md` returns 3
for `rather than` and 4 absence claims, which are the hand counts in Part two's table
exactly. It also returns 11 conclusion tells against the keyed locations' 0, which is
the register finding in **The baseline, read** stated as a number - and what P1.1 has to
rule on before that figure means better or worse.
