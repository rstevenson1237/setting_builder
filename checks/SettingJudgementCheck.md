# Setting Judgement Check - Telar, five regions complete (A, B, C, D, E)

Run after adding Region E (Nakhash, DANGEROUS d8), the Serpent Cult's own burial complex,
built 3a through 5c against the existing four regions. 64 locations across five regions.
`python3 tools/validate_setting.py` runs clean (0 errors); its remaining warnings are the
expected soft flags on genuinely secret exits, discussed under Open Items.

## Setting-level
- Discrete and discoverable, not vague: Confirmed - every Feature across all 64 locations
  names an object, a person, or a trigger a party can act on. Region E's gated doorways
  name exactly what each wants (three regalia pieces and a spoken name) rather than
  gesturing at "an ancient seal."
- Genre held across levels: Confirmed - Low Magic held even under pressure: Region E wanted
  three "warded gate" beats by the brief's own wording, and only the above-ground Sealed
  Approach (E.1) actually drew `dangerous/Mystery.md`'s ward fixture, honoring
  `dangerous/Door.md`'s "a region carries at most one warded way" - the Sanctum's two
  internal gates are built as `Door.md` "wanting a fitted object" locks instead, priest-craft
  rather than sorcery cast fresh. Fragmented Authority, Scarce Population, and Decay are
  untouched. No authored plot has crept in: the Serpent Cult cell digging at Nakhash wants
  the same three things the party might come for, and nothing states who should win that
  race.
- Recurring elements actually recur: Confirmed, and strengthened. The three-coil serpent
  motif now appears in two regions rather than one - Region E's Architecture field states
  it explicitly as the same turn already seen at Daghash, cut into chamber thresholds rather
  than lintels. `Stone Ward` (D.18, now also E.24 x6), `Barrow Wight` and `Barrow-Kin` (B.3,
  now also E.5/E.9), and `Threshold-Bane` (D.7, now also E.1) all recur rather than each
  region inventing its own one-off guardian - `checks/SettingJudgementCheck.md`'s own prior
  Room to Grow flagged Threshold-Bane and Grave-Mould as appearing only once; both now
  appear a second time (E.1, E.17). `setting/Keys.md` grew from 3 entries to 5,
  `setting/Quests.md` from 2 to 3, `setting/Lore.md` from 5 to 8, `setting/NamedCreatures.md`
  from 1 to 2, `setting/UniqueTreasures.md` from 1 to 2 - and the two Unique Treasures now
  reference each other (the Vaalsenn Tablet's own entry already named the Serpent Cult's
  interest in Daghash; the Kaash Collar backfilled into D.18 pays that off from the other
  direction).

## Region A (Tolkar, SAFE d8)
- Region reinforces the setting: Confirmed, unchanged.
- Locations reinforce this region: Confirmed. A.8's new quest Feature (The Debt on the
  Dosing Table) uses the location's own pre-existing `Tribute` tag rather than inventing an
  unrelated hook, and gives Region A its first quest that both gives and resolves inside its
  own borders (A.8 to A.6), distinct from the two existing quests that both resolve into
  Region B.

## Region B (Marfen, WILD d6)
- Region reinforces the setting: Confirmed, and its longest-standing Open Item is closed
  this pass - see Open Items below.
- Locations reinforce this region: Confirmed. B.3 Burial Mounds now carries the connection
  south into Nakhash as a stated Feature (the Worn Track South) rather than an assumption,
  and its own Untried Mound and rumour 14's settled explanation are untouched - the new
  content sits beside the old rather than restating or contradicting it.

## Region C (Velar, SAFE d8)
- Region reinforces the setting: Confirmed, unchanged.
- Locations reinforce this region: Confirmed, unchanged.

## Region D (Daghash, DANGEROUS d6)
- Region reinforces the setting: Confirmed, and reinforced further - D.18 Nirguk's Hoard's
  pre-existing `Serpent Cult` tag is now paid off with an actual Feature (the Kaash Collar),
  which the tag alone had only gestured at previously.
- Locations reinforce this region: Confirmed, unchanged from the prior pass, with one
  addition: D.18 carries a new Feature and Truths.md's second Handle now cites it alongside
  D.9 and D.13.

## Region E (Nakhash, DANGEROUS d8)
- Region reinforces the setting: Confirmed. The Overview's claims are all delivered: the
  Serpent Cult holding Nakhash as a position (E.8, per `dangerous/Faction.md`'s off-site-
  consequence test - Vray's cell, a standing order, a stated consequence if she's lost);
  the "defenses test what a party is carrying" claim (E.24's six Stone Wards, triggered by
  the regalia specifically); and the region's own new `setting/History.md` event (the cell
  reopening the tomb) is carried by E.2, E.3, and E.8 rather than asserted once and dropped.
- Locations reinforce this region: Confirmed. Class mix is 7 high / 12 medium / 5 low
  against the 30/50/rest spec exactly. Two blocks (Barrow Field, Dying; Sanctum, Believing)
  at 12 locations each - the first region built in two blocks, and the cross-block
  discipline held: the two vertical edges (E.2->E.13, E.3->E.13) are declared identically in
  both `Barrow Field.mmd` and `Sanctum.mmd`, closing the gap `checks/SettingJudgementCheck.md`
  previously flagged as untested. Doors carry open, secret, vertical, and gated kinds; the
  region's die (d8) is the setting baseline rather than an outlier, matching the brief's
  explicit instruction rather than the harsher d6 Daghash uses - the region's tension comes
  from its traps and its living faction rather than a harsher countdown.
- Information tiered, and the chain holds: Needs Attention going in, Confirmed after this
  pass - three hidden exits (E.13->E.16, E.3->E.8, E.8->E.3) were initially stated only on
  their Exits lines with no Clue in the obvious tier, which `templates/Location.md`'s own
  chain rule flags as the costliest failure (content the referee knows and the players
  cannot reach). Each now carries a Feature (a wall-hanging, fresh tool-marks, a second coil
  of rope) that puts the Clue where a party can actually find it. E.5/E.6 and E.15/E.19 were
  already correct on both ends.
- Secret tier rationed across the region: Confirmed - 8 of 24 locations carry a concealed
  detail or hidden exit, close to a third, in line with `dangerous/Low.md`'s and
  `dangerous/Medium.md`'s stated rates rather than every room or none.

## Room to Grow
Claims made upward with no location under them yet - not defects, just named openings.

- **The old crown seat**, **a burned keep east of the ford**, **the hedge-sorcerer
  downriver**, and **the Trackless Waste** - carried forward from the prior check, unchanged
  by this pass. The Trackless Waste's own rumour (13) was repointed to Nakhash's digging and
  hoard this pass, since it was the one rumour explicitly pointing away from the map rather
  than into it; the Waste itself is untouched as a setting fact and remains named here as a
  deliberate absence rather than a loss.
- **Gholuk's own sealing order** (`setting/Lore.md`, Gholuk's Tally, found at E.23) - the
  Sanctum's last master ordered every threshold sealed and gave no reason; nothing else
  found in Nakhash says why, or whether he was still inside when it was carried out. The
  plainest new growth point this region adds.
- **Vray's cell has four members named only by role** (the Rope-Watch at E.2, the Younger
  Cultist and three others at E.8, the two cultists forcing the Second Hall's gate at E.18) -
  none individually earn a `setting/NamedCreatures.md` row yet, but a return visit to Nakhash
  is the natural place one of them would, per that file's own "heard of before met" guidance.
- **Table II is cited twice in the whole setting** (A.3, and now E.20) - still the thinnest
  of the five tables; equipment remains what a party at this altitude wants most and is
  handed out least.

## Open Items
- **B.3 Burial Mounds' isolation is closed.** The prior check's standing Open Item - B.3 had
  no edge in `region/B/Connections.mmd` - is resolved: B.1---B.3 closes the region-internal
  gap, and B.3---E.11 is the new region-to-region connection this build needed anyway.
- **B.6's exit to B.2 is written as mundane where `Connections.mmd` marks it hidden.**
  Carried over from the prior two passes, still unresolved, and out of scope for this
  build - it belongs to Region B's own content, not to anything Region E touches.
- **Region E's own eight secret-exit warnings are the expected case, not a defect.** Per
  `tools/validate_setting.py`'s own comment, an edge the block diagram marks hidden but
  whose Exits line reads as mundane is the legitimate far-side-of-an-already-triggered-secret
  pattern (E.15's crawl-space into E.19 reads open from either end once found, for
  instance). Reviewed individually above under Information tiered; none of the eight needed
  a change beyond the three chain gaps already fixed.
