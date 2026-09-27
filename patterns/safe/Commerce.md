# Safe - Commerce

## Provides
What a location where goods and services change hands offers, at what price, and on what
terms beyond price.

## Spec

```
COMMERCE
  1     What it deals in, and who runs it, from the region's People roster     {TRADE}
  1     What is in stock, stated concretely                                    {STOCK}
  1     Prices, in the setting's coins, for the two or three things a party will
        actually ask for - this Kind's answer to safe/Settlement.md's gate line
  1     Where hospitality: what a night and a meal cost, whether the food is any good,
        and what the place is known for. Where market: which day it runs, who may set
        up, and what a stranger pays over a local
  40%   Something unusual in stock, and why it is here
  30%   A condition on trade beyond price      {credit | membership | grudge | shortage}
  20%   Something the proprietor wants that money will not buy
```

```
TRADE - exactly one
  hospitality  - food, drink, and a bed
  craft        - a trade the settlement's own living justifies
  dealing      - general goods, bought and sold
  market       - a market's own day, and its stalls
```

```
STOCK - at least one
  arrived      - what came in recently
  rationed     - what is held back, and sold in measures
  known        - what is sold only to people known here
  underpriced  - what was taken in trade and is worth more than the taker knows
```

## Constraints

- **Never leave a price implied.** A location that makes the referee invent prices at the
  table has left its job unfinished.
