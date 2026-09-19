# Safe - Commerce

## Provides
What a location where goods and services change hands offers, at what price, and what it
cannot supply.

## Spec

```
COMMERCE
  1     What it deals in, and who runs it - drawn from the region's People roster
        {hospitality | a trade | dealing | a market}
                                (genre: commerce-hospitality, trades, commerce-dealing,
                                 commerce-market)
  1     What is in stock, stated concretely              (genre: commerce-stock)
  1     What it cannot supply, and what it says to do instead
  1     Prices, in cn, for the two or three things a party will actually ask for -
        a night, a meal, and whatever this place is for
  40%   Something unusual in stock, and why it is here
  30%   A condition on trade beyond price - credit, membership, a grudge, a shortage
  20%   Something the proprietor wants that money will not buy
```

**The gap is more useful than the stock.** A party can assume a smith sells nails; what
changes their plans is that this smith has no steel until the barge comes, or will not sell
to them, or will trade but not for coin.

**Price is this Kind's answer to `safe/Settlement.md`'s gate line.** The rated condition
above is a *second* gate on top of it: the case where coin alone does not do it.

## Constraints

- **Prices are stated, not implied.** A location that makes the referee invent prices at
  the table has left its job unfinished.

- **Draw the trade from what the settlement's living justifies.** A place that mills grain
  has a miller and probably a baker; one that has neither has been stocked from a list.
