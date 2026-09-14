# Setting - Secrets

## Provides
What a concealed detail is made of, and what makes it findable.

## Read at
**Mode: ingredient.** Step 4c, cited by every line that conceals something. The rate is
never here: it varies by rating and, in DANGEROUS, by weight and by the location's own exits, so it belongs
to the line that draws. Distinct from the `Mystery` files, which are content and may stand
in plain sight, and from `wild/Secret.md`, which is a whole concealed *location* rather
than a detail inside one.

## Spec

```
SECRET
  1     Clue    - already visible through ordinary observation, and not itself the secret
  1     Trigger - the specific action that acts on the clue
  1     Payload - what the trigger produces
```

**A Secret sits on top of a feature the location already has** rather than being a feature
of its own, which is why it can be drawn last and still change what an earlier line means.

**Clues, and where they come from.** Concealment is undone by something, and that
something is what a party sees:

- **Underground, by construction** - a wall that does not match its neighbours in course,
  colour or wear; a floor worn toward a blank face; a draft where there should be none; a
  hinge, a groove or a seam; a fixture that has been moved; something too clean; a repair;
  a sound that carries further than the room accounts for; a thing built to be reached
  that no longer can be; an inscription one word short.
- **Outdoors, by weather and time** - a hollow that has slumped; a covering rotted
  through; a plant growing where the ground was disturbed; frost or dew melting in a
  shape; snow lying differently; water draining where it should pool; a stone moved and
  settled wrong; growth younger than the growth around it; a path worn to nowhere; a mark
  cut above standing height; a cairn that is a marker rather than a grave.
- **In a settlement, by people** - a room smaller inside than out; a lock better than the
  door deserves; a stock that does not match the trade; an entry in a ledger with no
  matching goods; a bricked opening; a key on a ring with nothing to open; somebody's
  reaction to an ordinary question; a person never left alone with strangers.

**Triggers** - pressing, turning, lifting, prising or sliding a stated fixture; placing or
removing weight; digging at a stated spot; fitting an object carried from elsewhere;
speaking something recorded elsewhere; opening in a stated order; entering water; climbing
to a stated vantage; waiting for a time, tide or weather; flooding, draining, lighting or
extinguishing; breaking something on purpose; something left rather than taken. **In a
settlement they are as often social** - asking the right person the right thing; being
trusted; being absent when everyone assumes you are present; buying the thing nobody buys;
paying a debt.

**Payloads** - a cache, cited from a table; a way through, on or off the map; a way in or
out of a settlement that is not the gate; a piece of Lore; a Key; a hazard neutralised
before it fires, or understood before it is walked into; a trap revealed before it is
sprung; a mystery answered in one step instead of several; a shortcut back to somewhere
already cleared; a sight of somewhere not yet reached; proof of who somebody is; the truth
behind a rumour the party arrived with.

**In a settlement, a secret belongs to somebody**, and that is what makes it different to
find. A concealed cellar has an owner who knows it is there; a false ledger page was
written by a person still in the room. State who finds out that the party knows, how soon,
and what they do - that is the second half of the Payload, and it is why a settlement's
secret is worth more than its contents. A dungeon's has nobody to notice.

## Constraints

- **A Secret without a stated Clue is not discoverable.** It is a fact the referee knows
  and the players can never find, and it is the most common way this structure fails. The
  clue has to be legible to a player paying attention before they know there is anything
  to find - and outdoors it fails more easily, because a party can walk past a whole
  hillside.
