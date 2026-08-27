# SAFE_HIGH

> The people and places worth returning for.

A `SAFE_HIGH` location is the reason a settlement is on the party's map after
they have left it. It holds something that exists nowhere else in the region, or
somebody whose standing toward the party can change, and it keeps a ledger of
what has passed between them. Every region carries at least the floor set by
`region_weights.<weight>.high_min` in `config/weights.yaml`, and in a `SAFE`
region those are the returns.

## What belongs here

- **One thing available here and nowhere else in the region.** A working device
  nobody understands, a road opened by permission rather than by walking, a
  person who can read the empire's layer of a name, a hold that will keep a
  thing safe while the party is out. Name what it is, name its price, and name
  what a party does instead if they will not pay.

- **Standing that moves in both directions.** State the party's opening standing
  and what raises it and lowers it, in named actions rather than in degrees.
  Something done here is remembered the next time they walk in, and the location
  is written so a referee can tell what changed without inventing it.

- **An obligation ledger.** What is owed, by whom, and what calls it in. This is
  the cell's characteristic currency: a favour is cheaper than coin at the
  moment it is taken and more expensive later, and that difference is what makes
  a party come back.

- **A person written to be met twice.** One want they state, one they do not,
  one thing they are wrong about, and a schedule that puts them somewhere
  findable. Their want survives being served, because a want that is discharged
  in one visit is a quest and this cell does not deal in those.

- **A refusal that is a door rather than a wall.** The refusal here is the one
  with an answer, and the answer is priced: a longer road, a darker road, or a
  road watched by something worse. Both branches are costed and the text never
  says which is the mistake.

- **A hidden layer worth the second visit.** Something in this location is
  legible only to a party that has been out into the region and come back with a
  name, a root, a token or a measurement. Write both readings: what it is to a
  party arriving cold, and what it is to a party arriving with the thing.

## Where the boundary falls

- **Down to `SAFE_MEDIUM`** when everything here is available two streets over
  at a worse price. Convenience is `MEDIUM`. Uniqueness and standing are `HIGH`.

- **Down to `SAFE_LOW`** when the person is the whole location and they hold no
  ledger, no unique service and no standing that moves. That is one door.

- **Not this cell** when the thing worth returning for is a place out in the
  region rather than a person or a service inside the settlement. The lit place
  holds who sends a party there and what it costs; the thing itself is a `WILD`
  or `DANGEROUS` landmark.

## Form

- **Player Overview:** eight to twelve sentences, and it shows standing rather
  than stating it: who is greeted, who is not, what is kept where, what has been
  set aside. Bold four or five nouns and give each a feature.
- **Features:** four to six. One is the unique service. One is the ledger, in
  whatever physical form it takes. One carries the hidden layer.
- **Referee Overview:** opening standing, what moves it and by how much in
  named actions, the unique service and its price, the priced refusal and its
  answer, and what is owed at the start of play.
- **Exits:** two or more. State which of them the party has permission to use
  and which they do not, because permission is the cell's version of a door.
- **No combat statistics.** Consequence here is exclusion, calling in a debt,
  and being spoken about. State the exclusion physically: which door closes.
- **Tables it leans on:** `T-PRC` for what the unique service yields, `T-KEY`
  where the permission is a physical token and the gate is elsewhere, `T-LNG`
  and `T-NAM` where the person reads names, `T-LOR` for what is kept and
  legible, `T-TRE` where the unique thing is an object.

## Worked example

An illustration of the shape and the register. Nothing in it is canon, and the
codes are stand-ins.

**Player Overview.** The hold is a single empire vault with its outer door gone
and a timber frame built into the socket where it stood. Inside, **the shelved
wall** is stacked with wrapped and corded parcels, each with a tag, and none of
the tags carry names. **The corded book** on the stand by the door is open, and
the page is a column of tag numbers against a column of marks that are not
letters. The keeper looks at the party's hands rather than their faces.

**Referee Overview.** *Service:* he will hold anything, dry, for as long as it
takes, and he has never lost a parcel. *Cost:* not coin. He takes the tag mark
of somebody who will vouch, and the party has none at the start of play. *The
answer that is not the gate:* he will hold on the word of anyone already in the
book, and there are three such people in the settlement; each of them wants
something first, and each want costs a trip out of the lit ground. *Standing:*
lodging a parcel and coming back for it inside the season raises it. Sending
someone else for it lowers it, whatever the reason. *Hidden:* the marks in the
book are the empire's layer, and a party carrying a root from the registry can
read the column and learn which parcels have been unclaimed for how long.

## Excluded patterns

- **A quest giver.** A person with a want is met. A person with a task, a
  reward and a completion condition is a plot, and the setting is a standing
  situation.
- **A shop of unique items.** One thing available nowhere else is a landmark.
  Six of them is a market, and a market is `MEDIUM`.
- **Standing written as a number or a track.** Name the action and name what
  changes. A scale is a mechanic, and mechanics live in `MECHANICS.md`.
- **A patron who explains the region.** What they know is bounded by where they
  have been, and most people in a lit place have not been out.
- **A safe place that is secretly a trap.** This is the cell a party is meant to
  be able to trust. Reversal is funded elsewhere, and turning the return into
  the ambush spends every straight instance in the region at once.
- **Combat statistics.** Not in a `SAFE` region. Exclusion is the consequence,
  and it is stated as a door.
