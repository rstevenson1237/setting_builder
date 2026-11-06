# Secret bypass

A hidden passage between two rooms the main route also reaches: a shortcut for those who know it.

```kdl
Layout secret-bypass name="A hidden way between two rooms" tags="secret, bypass, shortcut" source="drawn from maps 1 and 2"
Part role=near width="15-20" length="15-20"
Part role=far width="15-20" length="15-20"
Part role=bypass shape=hall width="25-40" length="5"
Tie a=near b=bypass kind=door
Tie a=bypass b=far kind=door
Socket name=near-in part=near bearing=south width=5
Socket name=far-in part=far bearing=north width=5
```
