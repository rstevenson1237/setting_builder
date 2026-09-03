# Safe - Secrets

## Decides
Whether a SAFE location hides something, and the three parts that make it findable.

## Read at
Step 4c, for every SAFE location - consulted unconditionally to decide whether there is a
secret at all.

## Spec

```
SECRET
  1     Clue    - already visible through ordinary observation, not itself the secret
  1     Trigger - the specific action that acts on the clue
  1     Payload - what the trigger produces
```

Rate:

```
INCLUSION
  10%   of SAFE locations carry a secret
```

The lowest rate of the three ratings, and deliberately so. A settlement where every
building has a hidden compartment is not a settlement, it is a dungeon with a market.

**In SAFE, a secret is usually somebody's rather than something's.** A concealed cellar has
an owner who knows about it; a false ledger page was written by a person who is still in
the room. This makes the Trigger social as often as physical - and it means a discovered
secret in a settlement has a *consequence*, because somebody finds out the party knows.

**A Secret without a stated Clue is not discoverable.** The clue must be legible to a
player paying attention before they know there is anything to find.

## Patterns

**Clues** - a room that is smaller inside than out; a lock better than the door deserves;
a stock that does not match the trade; a floor worn toward a wall; a repair that hid
something rather than fixed it; an entry in a ledger with no matching goods; somebody's
reaction to an ordinary question; a bricked opening; a key on a ring with nothing to open;
a person who is never left alone with strangers.

**Triggers, and they may be social** - asking the right person the right thing; being
trusted; being absent when everyone assumes you are present; buying the thing nobody buys;
paying a debt; the physical ones too - lifting, prising, counting, moving a fixture that
moves too easily.

**Payloads** - a cache or a strongbox; a way in or out of the settlement that is not the
gate; a document, per `safe/Lore.md`; a person who is here and should not be; proof of who
somebody is; a Key; the truth behind a rumour the party arrived with; what the settlement's
authority is actually taking.

**Consequence.** Unlike a dungeon's, a settlement secret has an owner who will notice. State
who finds out, how soon, and what they do - that is the payload's second half and the
reason a SAFE secret is worth more than its contents.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
