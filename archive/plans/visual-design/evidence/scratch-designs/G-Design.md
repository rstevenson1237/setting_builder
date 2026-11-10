# Design of G

```kdl
Design G.a locations="G.1, G.2, G.3, G.4, G.5, G.6, G.7, G.8, G.9, G.10, G.11, G.12, G.13, G.14, G.15, G.16, G.17, G.18, G.19, G.20, G.21, G.22, G.23, G.24, G.25, G.26, G.27, G.28, G.29" outline="rect 240 240"
Use G.a id=axis layout=axis-of-halls params="halls=3"
Use G.a id=king layout=suite
Use G.a id=queen layout=suite
Use G.a id=byp layout=secret-bypass
Use G.a id=v1 layout=stair-vestibule
Use G.a id=v2 layout=stair-vestibule
Use G.a id=rows layout=cell-row params="per-row=2"
Bind G.a use=axis role=hall locations="G.2, G.13, G.22" type=Medium
Bind G.a use=king role=main locations="G.7" type=High
Bind G.a use=king role=sub locations="G.10" type=Medium
Bind G.a use=queen role=main locations="G.8" type=High
Bind G.a use=queen role=sub locations="G.9" type=High
Bind G.a use=byp role=near locations="G.20" type=High
Bind G.a use=byp role=far locations="G.14" type=Medium
Bind G.a use=byp role=bypass locations="G.21" type=Low
Bind G.a use=v1 role=vestibule locations="G.1" type=Low
Bind G.a use=v2 role=vestibule locations="G.19" type=Medium
Bind G.a use=rows role=hall locations="G.15" type=Medium
Bind G.a use=rows role=north-cell locations="G.16, G.17" type=Low
Bind G.a use=rows role=south-cell locations="G.12, G.18" type=Low
Fill G.a locations="G.3, G.4, G.5, G.11, G.25, G.27, G.28" type=Low width=20 length=20
Fill G.a locations="G.6, G.23, G.24, G.26, G.29" type=Medium width=30 length=20
Join G.a from="G.1" to="axis.first"
Join G.a from="G.2" to="G.3"
Join G.a from="G.2" to="G.4"
Join G.a from="G.3" to="G.11"
Join G.a from="G.4" to="G.15"
Join G.a from="G.4" to="G.28"
Join G.a from="G.5" to="G.13"
Join G.a from="G.5" to="G.18"
Join G.a from="G.5" to="G.22"
Join G.a from="G.6" to="G.13"
Join G.a from="G.6" to="G.7"
Join G.a from="G.6" to="G.8"
Join G.a from="G.6" to="G.27"
Join G.a from="G.8" to="G.19"
Join G.a from="G.11" to="G.24"
Join G.a from="G.17" to="G.19"
Join G.a from="G.15" to="G.20"
Join G.a from="G.20" to="G.28"
Join G.a from="G.21" to="G.29"
Join G.a from="G.22" to="G.23"
Join G.a from="G.23" to="G.24"
Join G.a from="G.24" to="G.25"
Join G.a from="G.26" to="G.27"
```
