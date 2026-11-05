# Stair vestibule

A small room whose job is to hold a stair: the way down or up, with one door into the level.

```kdl
Layout stair-vestibule name="A room that holds a stair" tags="stair, vestibule, exit" source="drawn from maps 1 and 2"
Part role=vestibule width="10-15" length="10-15"
Socket name=door part=vestibule bearing=south width=5
Socket name=stair part=vestibule bearing=north width=5
```
