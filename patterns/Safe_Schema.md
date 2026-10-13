# Safe Schema

A SAFE region's tables: every location reached from the region itself.

```kdl
enum Safe_Type Inn Merchant Bank Market Authority

folder Safe type=Safe_Type {
  Locations Location
  Dressing Dressing
}
```
