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

An earlier spike (`archive/plans/visual-design/spike-settlement.md`) found the dungeon solver unfit for a
settlement: places 360 to 1,000 feet apart, and a street is not a way between two rooms. It led to the
settlement layout `tools/design.py` now drives. That path stands and is not yet used on a region.

## Out of scope

Hex or point crawls between a region's places (the play-structure plan), and terrain art.
