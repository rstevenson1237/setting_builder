# Intake - wild maps: a WILD or SAFE block's map shows the place

## The request, verbatim

> We can design 6.

## How it is read

Review item 6. `spec.md` numbers each proposal for approval; none is built.

## What the maps show today

- **A, the buried city**: nine marks on bare sand over 2,400 feet. The seed's "gridded city", "drifted streets"
  and the pyramid's tip are not drawn. Grass, forest and a river stand at the sheet's edge, in a desert the
  genre cuts off from the world: `maps.py place` asks artgen for the region's `ground` inside its area and lets
  it fill the rest.
- **B, the lake city**: eight boxes and an ellipse on rock. No cavern wall, no quay, no street.
- Neither region has a `design` line, so `Street` and `Tie`, which the schema holds for them, are unused.
- `Map_Judgement_Check.md` reviews DANGEROUS blocks only: nobody is asked whether these two maps read.

## What the history holds

| Commit | What it decided or found | Here |
|---|---|---|
| a2ac2d1 (F14) | Most "landmark" entries in the source corpus "are not locations at all - they are terrain quality, which in a point crawl is connective texture the referee narrates from the region fields". Only what can be "named, revisited and connected to" is a Landmark. | Why "ground is never a location". W3 draws that texture; it keys none of it. |
| 346b373 (D16) | "Each rating has its own connection topology - SAFE a shallow hub ..., WILD a forest of trees, DANGEROUS a dense graph with few entrances." | A WILD region's places hanging off its way in is the design, not a gap. |
| 0df4b9f (#71) | "WILD Landmarks and Routes are reached from the region itself"; an edge between two is an error. | |
| `archive/plans/b2-friction/intake.md` item 2, closed in 778ff41 | "Landmarks are still not joined" was raised for the Borderlands build and declined. | Not proposed again here. |
| 6b64172 (#92) | Region maps and location cuts paused, "to restore later". | |
| `archive/plans/visual-design/spike-settlement.md` | The dungeon solver cannot lay out a settlement: places 360 to 1,000 feet apart, and "a street is not a way". It led to the settlement layout `tools/design.py` drives. | That path stands and is not yet used on a region. |

## Out of scope

Hex or point crawls between a region's places (the play-structure plan), and terrain art.
