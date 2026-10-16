# Connections of A Roadsend Keep

```kdl
Way A.1 to="B.1" orientation="west, along the road"
Way A.2 to="C.1" orientation="north, into the wood"
Way A.4 to="A.12" orientation="south, down a ladder" { Secret trigger="pull the third barrel" tell="scraped floor by casks" }
Way A.12 to="A.4" orientation="north, up a ladder"
Way A.10 to="A.13" orientation="east, under the floor" { Secret trigger="turn the dais ring" tell="ring polished by hands" }
Way A.13 to="A.10" orientation="west, up steps"
```
