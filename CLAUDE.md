# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is not a software project. There is no build, lint, or test tooling, and none should be added — it is a plain-text framework for authoring OSR (Old-School Renaissance) adventure settings as markdown (and a few `.mmd` mermaid diagrams). All "development" here is content generation following the templates and workflow below.

## Directory structure

- `GENRE.md` — the top-level thematic spine (1981 B/X D&D, Conan-esque, Low Magic, Points of Light, Mythic Underworld, situations not authored plots). Every template's Context section names this file explicitly and states what to check against it — re-read it at every generation step, don't just skim it once. Genre drift (an authored plot creeping in, magic becoming common, an implied central authority) is the main failure mode in this project; watch for it.
- `templates/` — one template per artifact type. Each is structured as **Purpose / Context / Instructions / Template**. Context always lists exactly which files to read before drafting (GENRE.md first) — do not pull in more than a template's Context section names. `templates/Location.md` is deliberately the narrowest: only GENRE.md, the parent region overview, and the location's own gazetteer stub — other setting files are consulted only to look up a name already referenced, never wholesale.
- `patterns/` — `Safe.md`, `Wild.md`, `Dangerous_Low.md`, `Dangerous_Medium.md`, `Dangerous_High.md`. Each is a reusable list of thematic location patterns, picked by a region's SAFE/WILD/DANGEROUS rating and (for DANGEROUS) a location's weight. The pattern for a given location is chosen at generation time (in `templates/Location.md`), not pinned earlier in the gazetteer. When a chosen pattern calls for treasure, a creature, or a trap, `patterns/Treasure.md`, `patterns/Creatures.md`, and `patterns/Traps.md` guide *which* content fits — patterns guide content, templates guide formatting, so how that content gets written into a Feature (treasure table citation, creature naming, trap resolution language) lives in `templates/Location.md`, not here.
- `setting/` — the actual generated content for the current setting, mirroring the template set: `Setting.md`, `History.md`, `Truths.md`, `Rumours.md`, `Bestiary.md`, `Factions.md`, `Treasure1.md` through `Treasure5.md` (Treasure Tables I-V), then `region/Regions.md` + `region/Connections.mmd`, then one `region/[Code].md` Region Overview per region, then one `region/[Code]/` folder per region holding that region's `Locations.md` gazetteer, `Connections.mmd`, and one `[LocationCode].md` per location.
- `STEPS.md` — the authoritative, sequential build log. Every artifact created follows a numbered step here (e.g. `4c`) naming its template and its context files. When adding a new step to the workflow, append/renumber here and keep the wording consistent with existing entries (what's created, what context it uses, which template it follows).

## Generation workflow

The build order is strict and each stage's Context section depends on the previous stages already existing:

1. `GENRE.md` (fixed, edited directly — not generated from a template)
2. Setting-level documents in order: `Setting.md` → `History.md` → `Truths.md` → `Rumours.md` → `Bestiary.md` → `Factions.md` → `Treasure1.md`-`Treasure5.md`
3. Region level: `region/Regions.md` (gazetteer) → `region/Connections.mmd` (region-to-region graph, existence only) → `region/[Code].md` (full Region Overview per region, including its d6 Events/Encounter/Danger table now, not deferred)
4. Location level, per region: `region/[Code]/Locations.md` (gazetteer stub — name, weight, tags only, no content, no pattern) → `region/[Code]/Connections.mmd` (directional, typed: normal `---`, hidden `-.-`, one-way `-->`) → `region/[Code]/[N].md` (full location entry)

See `STEPS.md` for the exact, current step numbering and per-artifact context lists — it is more current than any summary here.

## Location entry format (`templates/Location.md`)

This is the most detail-sensitive template, worth calling out directly:

- Header line: `[Region].[N] **Name** - *three, thematic, tags*`
- Player Summary (plain text, 2 sentences, **bold** any feature named in it)
- Referee Notes (*italicized*: shape, size, sounds/smells)
- One bolded line per **Feature**, labeled with the feature's own name — no leading article (`**Thorn Tangle:**`, not `**The Thorn Tangle:**`)
- **Exits:** comma-separated, mundane only, each as `[what indicates the exit] -> [Code] [Location Name]` (e.g. `door -> A.2 Salvage Market`)
- Any exit that needs a trigger to reveal or access (a secret door, a puzzle) is described inside a Feature line instead of listed under Exits — Exits is reserved for straightforward access.

## Regions and weights

Regions are rated SAFE, WILD, or DANGEROUS with a die size (d4–d12) indicating encounter danger, coded A, B, C... (AA, AB... past 26). SAFE/WILD locations are landmarks, roughly as many as the die type; DANGEROUS locations are one per room, roughly 3× the die type, each weighted low/medium/high (connective, one reactive element, or a central set-piece respectively) — this weight selects which `patterns/Dangerous_*.md` file a location draws from.
