"""The tools do what they claim, and scaffold.py and validate.py agree.

The most valuable case here is the round trip: a tree scaffolded from nothing
must pass the checks with no errors. `scaffold.py` fixes the body shape and
`validate.py` asserts it, and that claim is only true while this test passes.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import (  # noqa: E402
    GENRE, L03, LEDGER, PLAYBOOK, REGION, REGION_CONN, REPO, ROUTER, Sandbox,
)

import common  # noqa: E402
import ledger as ledger_mod  # noqa: E402
import roll  # noqa: E402
import validate  # noqa: E402

# A tree scaffolded from nothing starts without the content tree, the ledger and
# the derived build output. `build` is in the list because a diagram derived from
# the committed tree draws regions the new tree does not have.
EMPTY = ("setting", "state", "STATE.md", "build")


def scaffold_a_setting(sandbox: Sandbox) -> None:
    """One setting, all 24 tables, one region of each type, one location each.

    The diagram layer is derived at the end, because `scaffold.py` writes the
    markers and `mermaid_gen.py` writes the files they name. A tree with markers
    and no diagrams is half a step, not a finished one.
    """
    assert sandbox.run("ledger.py", "init", "--seed", "99").returncode == 0
    assert sandbox.run(
        "scaffold.py", "setting", "--name", "The Ashen Reach",
        "--tags", "drowned,ashen,covenant", "--seed", "99",
        "--container", "sunken-holds=The Sunken Holds",
    ).returncode == 0
    assert sandbox.run("scaffold.py", "tables").returncode == 0

    regions = [
        ("R01", "Bell Hold", "SAFE", "d10", "low", "upper-tier=Upper Tier"),
        ("R02", "Reed Mere", "WILD", "d8", "medium", "the-causeway=The Causeway"),
        ("R03", "Drowned Tier", "DANGEROUS", "d4", "high", "lower-tier=Lower Tier"),
    ]
    for code, name, kind, die, weight, sub in regions:
        assert sandbox.run(
            "scaffold.py", "region", "--code", code, "--name", name,
            "--tags", "cold,square,kept", "--type", kind, "--difficulty", die,
            "--weight", weight, "--container", "sunken-holds", "--sub", sub,
        ).returncode == 0
        assert sandbox.run(
            "scaffold.py", "location", "--code", f"{code}-L01", "--name", "Bell Frame",
            "--tags", "bare,seated,clean", "--container", sub.split("=")[0],
            "--weight", "HIGH",
        ).returncode == 0

    assert sandbox.run("mermaid_gen.py").returncode == 0


class TestScaffoldValidateRoundTrip(unittest.TestCase):
    def test_a_scaffolded_tree_passes_the_checks(self) -> None:
        with Sandbox(without=EMPTY) as sandbox:
            scaffold_a_setting(sandbox)
            result = sandbox.validate()
            self.assertEqual(
                result["errors"], 0,
                "\n".join(f"{f['check']} {f['code']}: {f['message']}"
                          for f in result["findings"] if f["severity"] == "ERROR"),
            )

    def test_every_catalogued_table_is_scaffolded(self) -> None:
        with Sandbox(without=EMPTY) as sandbox:
            scaffold_a_setting(sandbox)
            written = {p.name.split("-", 2)[0] + "-" + p.name.split("-", 2)[1]
                       for p in (sandbox.path("setting/tables")).glob("*.md")}
            self.assertEqual(written, set(common.S_TABLES) | set(common.T_TABLES))

    def test_the_referee_table_follows_the_region_type(self) -> None:
        with Sandbox(without=EMPTY) as sandbox:
            scaffold_a_setting(sandbox)
            expected = {"R01": ("Events", [1, 2, 3, 4, 5, 6]),
                        "R02": ("Encounters", [1, 2, 3, 4, 5, 6]),
                        "R03": ("Dangers", [6, 5, 4, 3, 2, 1])}
            for code, (heading, order) in expected.items():
                doc = common.read_doc(
                    next(sandbox.path("setting/regions").glob(f"{code}-*/region.md")), "region")
                section = doc.section("Tables")
                self.assertIsNotNone(section.subsection(heading), f"{code} wants {heading}")
                rows = common.parse_tables(section.subsection(heading).text)[0].rows
                self.assertEqual([int(r["Roll"]) for r in rows], order)


class TestScaffoldGuards(unittest.TestCase):
    """Overwrite discipline: SPEC.md section 8.1."""

    LOCATION = ("scaffold.py", "location", "--code", "R03-L07", "--name", "Drowned Shrine",
                "--tags", "flooded,votive,sinking", "--container", "drowned-tier",
                "--weight", "HIGH")

    def test_an_existing_file_needs_force(self) -> None:
        with Sandbox() as sandbox:
            refused = sandbox.run(*self.LOCATION)
            self.assertEqual(refused.returncode, 1)
            self.assertIn("--force", refused.stderr)
            self.assertEqual(sandbox.run(*self.LOCATION, "--force").returncode, 0)

    def test_force_does_not_override_a_built_target(self) -> None:
        """--force replaces a stub. Replacing content takes a booked step re-run."""
        with Sandbox() as sandbox:
            original = sandbox.read("setting/regions/R03-ashen-fen/locations/"
                                    "R03-L07-drowned-shrine.md")
            sandbox.mark("built", "R03-L07")

            refused = sandbox.run(*self.LOCATION, "--force")
            self.assertEqual(refused.returncode, 1)
            self.assertIn("--rerun", refused.stderr)
            self.assertEqual(sandbox.read("setting/regions/R03-ashen-fen/locations/"
                                          "R03-L07-drowned-shrine.md"), original)

            self.assertEqual(sandbox.run(*self.LOCATION, "--rerun").returncode, 0)

    def test_bad_arguments_are_refused(self) -> None:
        cases = [
            (("scaffold.py", "region", "--code", "R09", "--name", "X", "--tags", "a,b",
              "--type", "WILD", "--difficulty", "d8", "--weight", "medium",
              "--container", "sunken-holds", "--sub", "x=X"), "three tags"),
            (("scaffold.py", "region", "--code", "R09", "--name", "X", "--tags", "a,b,c",
              "--type", "WILD", "--difficulty", "d7", "--weight", "medium",
              "--container", "sunken-holds", "--sub", "x=X"), "d7"),
            (("scaffold.py", "region", "--code", "nine", "--name", "X", "--tags", "a,b,c",
              "--type", "WILD", "--difficulty", "d8", "--weight", "medium",
              "--container", "sunken-holds", "--sub", "x=X"), "region code"),
            (("scaffold.py", "location", "--code", "R03-L11", "--name", "Mere",
              "--tags", "a,b,c", "--container", "nope", "--weight", "LOW"), "not a container"),
            (("scaffold.py", "location", "--code", "R99-L01", "--name", "Mere",
              "--tags", "a,b,c", "--container", "nope", "--weight", "LOW"), "does not exist"),
            (("scaffold.py", "tables", "--only", "T-ZZZ"), "catalogue"),
        ]
        with Sandbox() as sandbox:
            for args, expected in cases:
                with self.subTest(args=args[1:3]):
                    result = sandbox.run(*args)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(expected, result.stderr)

    def test_the_cell_is_derived_from_the_region(self) -> None:
        """A location never states its own type. It inherits it, so M5 cannot fail."""
        with Sandbox() as sandbox:
            sandbox.unclaim("R03-L11")
            result = sandbox.run("scaffold.py", "location", "--code", "R03-L11",
                                 "--name", "Mere Tier", "--tags", "open,cold,deep",
                                 "--container", "drowned-tier", "--weight", "LOW")
            self.assertEqual(result.returncode, 0, result.stderr)
            doc = common.read_doc(sandbox.path("setting/regions/R03-ashen-fen/locations/"
                                               "R03-L11-mere-tier.md"), "location")
            self.assertEqual(doc.fm["cell"], "WILD_LOW")


class TestRoll(unittest.TestCase):
    """Seeded randomness: the same target rolls the same result on a rebuild."""

    def test_a_stream_is_reproducible(self) -> None:
        first = [roll.stream(4417, "R03-L07").randint(1, 6) for _ in range(20)]
        again = [roll.stream(4417, "R03-L07").randint(1, 6) for _ in range(20)]
        self.assertEqual(first, again)

    def test_targets_nonces_and_seeds_do_not_share_a_stream(self) -> None:
        def sample(seed: int, target: str, nonce: str = "") -> list[int]:
            rng = roll.stream(seed, target, nonce)
            return [rng.randint(1, 6) for _ in range(20)]

        base = sample(4417, "R03-L07")
        self.assertNotEqual(base, sample(4417, "R03-L03"))
        self.assertNotEqual(base, sample(4417, "R03-L07", "weather"))
        self.assertNotEqual(base, sample(4418, "R03-L07"))

    def test_dice_notation(self) -> None:
        self.assertEqual(roll.parse_dice("2d6+1"), (2, 6, 1))
        self.assertEqual(roll.parse_dice("d20"), (1, 20, 0))
        self.assertEqual(roll.parse_dice("3d8 - 2"), (3, 8, -2))
        for bad in ("d1", "0d6", "six", "2x6", ""):
            with self.subTest(bad=bad), self.assertRaises(roll.RollError):
                roll.parse_dice(bad)

    def test_a_roll_stays_within_its_bounds(self) -> None:
        rng = roll.stream(1, "t")
        for _ in range(200):
            result = roll.roll_dice("3d6+2", rng)
            self.assertEqual(len(result["rolls"]), 3)
            self.assertTrue(5 <= result["total"] <= 20)

    def test_unique_draws_do_not_repeat(self) -> None:
        rows = [{"ID": f"T-RUM-0{n}"} for n in range(1, 5)]
        drawn = roll.roll_table(rows, roll.stream(1, "t"), count=4, unique=True)
        self.assertEqual({r["ID"] for r in drawn}, {r["ID"] for r in rows})
        with self.assertRaises(roll.RollError):
            roll.roll_table(rows, roll.stream(1, "t"), count=5, unique=True)

    def test_a_zero_weight_is_never_drawn(self) -> None:
        rows = [{"ID": "a", "Weight": "0"}, {"ID": "b", "Weight": "3"}]
        drawn = roll.roll_table(rows, roll.stream(1, "t"), count=50, weight_column="Weight")
        self.assertEqual({r["ID"] for r in drawn}, {"b"})

    def test_a_bad_weight_is_refused(self) -> None:
        for weight in ("many", "-1"):
            with self.subTest(weight=weight), self.assertRaises(roll.RollError):
                roll.roll_table([{"ID": "a", "Weight": weight}], roll.stream(1, "t"),
                                weight_column="Weight")

    def test_the_cli_takes_its_seed_from_the_ledger(self) -> None:
        with Sandbox() as sandbox:
            first = sandbox.run("roll.py", "table", "T-RUM", "--target", "R03", "--count", "2")
            again = sandbox.run("roll.py", "table", "T-RUM", "--target", "R03", "--count", "2")
            self.assertEqual(first.returncode, 0)
            self.assertEqual(first.stdout, again.stdout)

            payload = json.loads(sandbox.run("roll.py", "dice", "2d6", "--target", "R03",
                                             "--json").stdout)
            self.assertEqual(payload["seed"], 4417)

    def test_a_missing_seed_is_an_error_not_a_guess(self) -> None:
        with Sandbox(without=("state", "setting")) as sandbox:
            result = sandbox.run("roll.py", "dice", "2d6", "--target", "R03")
            self.assertEqual(result.returncode, 1)
            self.assertIn("seed", result.stderr)


class TestLedger(unittest.TestCase):
    def test_complete_refuses_while_targets_are_pending(self) -> None:
        with Sandbox() as sandbox:
            sandbox.clear_step(9)
            sandbox.run("ledger.py", "start", "9", "--targets", "R03-L03", "R03-L07")
            refused = sandbox.run("ledger.py", "complete", "9")
            self.assertEqual(refused.returncode, 1)
            self.assertIn("R03-L03", refused.stderr)

            sandbox.run("ledger.py", "done", "9", "R03-L03", "R03-L07")
            self.assertEqual(sandbox.run("ledger.py", "complete", "9").returncode, 0)

            data = json.loads(sandbox.read(LEDGER))
            self.assertEqual(data["steps"]["9"]["status"], "complete")
            self.assertEqual(data["steps"]["9"]["targets"], 2)

    def test_progress_is_recorded_per_target(self) -> None:
        """Resumability: a step survives the end of a conversation."""
        with Sandbox() as sandbox:
            sandbox.run("ledger.py", "start", "11", "--targets", "R03-L03", "R03-L07",
                        "--pass", "HIGH")
            sandbox.run("ledger.py", "done", "11", "R03-L07")
            pending = sandbox.run("ledger.py", "pending", "11").stdout.split()
            self.assertEqual(pending, ["R03-L03"])
            self.assertEqual(json.loads(sandbox.read(LEDGER))["current_pass"], "HIGH")

    def test_guard_lists_deduplicate(self) -> None:
        with Sandbox() as sandbox:
            # From a fresh ledger, so the assertion states the whole list rather
            # than whatever the committed tree has built so far.
            sandbox.run("ledger.py", "init", "--seed", "4417", "--force")
            sandbox.run("ledger.py", "built", "R03-L07", "R03-L03")
            sandbox.run("ledger.py", "built", "R03-L07")
            self.assertEqual(json.loads(sandbox.read(LEDGER))["built"],
                             ["R03-L03", "R03-L07"])

    def test_state_is_regenerated_on_every_write(self) -> None:
        with Sandbox() as sandbox:
            sandbox.run("ledger.py", "init", "--seed", "4417", "--force")
            sandbox.path("STATE.md").write_text("stale", encoding="utf-8")
            sandbox.run("ledger.py", "built", "R03-L07")
            state = sandbox.read("STATE.md")
            self.assertNotIn("stale", state)
            self.assertIn("Built targets:** 1", state)

    def test_init_refuses_to_discard_a_ledger(self) -> None:
        with Sandbox() as sandbox:
            self.assertEqual(sandbox.run("ledger.py", "init", "--seed", "1").returncode, 1)
            self.assertEqual(sandbox.run("ledger.py", "init", "--seed", "1",
                                         "--force").returncode, 0)


class TestCommon(unittest.TestCase):
    """Parsing. Each case here is a bug that reached the tree once."""

    def test_only_an_escaped_pipe_is_an_escape(self) -> None:
        """Table cells carry regular expressions, so a lone backslash survives."""
        row = common._split_row(r"| `\b\d*d\d+\b` | a \| b |")
        self.assertEqual(row, [r"`\b\d*d\d+\b`", "a | b"])

    def test_the_mechanics_token_map_parses(self) -> None:
        tables = common.parse_tables((common.REPO_ROOT / common.MECHANICS_PATH)
                                     .read_text(encoding="utf-8"))
        vocabulary = next(t for t in tables if "Token" in t.headers)
        self.assertEqual({r["Token"].strip("`") for r in vocabulary.rows},
                         {"TEST", "WOUND", "CONDITION", "AD", "TYPE", "VALUE", "WT",
                          "QUALITY", "OUTCOME"})

    def test_a_heading_inside_a_fence_is_not_a_heading(self) -> None:
        sections = common.parse_sections("## Real\n\n```\n## Not a heading\n```\n\n## Also real\n")
        self.assertEqual([s.title for s in sections], ["Real", "Also real"])

    def test_subsections_belong_to_their_section(self) -> None:
        sections = common.parse_sections("## Features\n\n### One\na\n\n### Two\nb\n\n## Exits\nc\n")
        self.assertEqual([s.title for s in sections[0].subsections], ["One", "Two"])
        self.assertEqual(sections[1].text.strip(), "c")

    def test_frontmatter_must_be_present_and_closed(self) -> None:
        for bad in ("no frontmatter here", "---\ncode: R03\nstill open\n", "---\n- a list\n---\n"):
            with self.subTest(bad=bad[:12]), self.assertRaises(common.DocError):
                common.split_frontmatter(bad)

    def test_a_read_and_rewrite_changes_nothing(self) -> None:
        """Every tool reads a file and writes it back. That has to be a fixed point.

        A writer that reformats what it did not change turns every step into a
        diff nobody can read, and hides the one line the step meant to move.
        """
        with Sandbox() as sandbox:
            for path in sorted(sandbox.path("setting").rglob("*.md")):
                before = path.read_text(encoding="utf-8")
                doc = common.read_doc(path, "any")
                common.write_doc(path, doc.fm, doc.body)
                self.assertEqual(
                    path.read_text(encoding="utf-8"), before,
                    f"{path.name} came back different from how it went in",
                )

    def test_frontmatter_keeps_a_flat_list_inline_and_the_mapping_in_block(self) -> None:
        with Sandbox() as sandbox:
            path = sandbox.path("x.md")
            common.write_doc(
                path,
                {"code": "R01", "tags": ["a", "b", "c"],
                 "containers": [{"id": "one", "name": "One"}], "schema_version": 1},
                "## Overview",
            )
            text = path.read_text(encoding="utf-8")
            self.assertIn("\ncode: R01\n", text, "the frontmatter itself is block style")
            self.assertIn("tags: [a, b, c]", text, "a flat list stays on one line")
            self.assertIn("- {id: one, name: One}", text)

    def test_slug_and_diagram_names(self) -> None:
        self.assertEqual(common.slugify("The Drowned Tier"), "the-drowned-tier")
        self.assertEqual(common.diagram_name(4, "R03", "drowned-tier"),
                         "T4_R03_DROWNED_TIER.md")
        self.assertEqual(common.diagram_name(1, "SETTING"), "T1_SETTING.md")

    def test_edges_read_their_one_way_column(self) -> None:
        """The parser, stated against a table the test writes.

        Reading the region's own table would assert the build's current graph
        rather than the column's meaning, and would fail every time a location
        is added.
        """
        with Sandbox() as sandbox:
            sandbox.write(
                "setting/regions/R03-ashen-fen/connections.md",
                "---\ncode: R03\nscale: region\nschema_version: 1\n---\n\n"
                "| From | To | Type | One-way |\n| :--- | :--- | :--- | :--- |\n"
                "| R03-L03 | R03-L07 | sunk span | no |\n"
                "| R03-L07 | R03-L03 | fallen wall | yes |\n",
            )
            doc = common.read_doc(sandbox.path("setting/regions/R03-ashen-fen/connections.md"),
                                  "connections")
            edges = common.edges_from(doc)
            self.assertEqual(len(edges), 2)
            self.assertEqual((edges[0].source, edges[0].target, edges[0].one_way),
                             ("R03-L03", "R03-L07", False))
            self.assertEqual((edges[1].source, edges[1].target, edges[1].one_way),
                             ("R03-L07", "R03-L03", True))


# --------------------------------------------------------------------------
# Routing and dependency resolution
# --------------------------------------------------------------------------

PATTERN = """---
id: {id}
target: {target}
phase: {phase}
writes: [Features, Exits]
dependencies:
{dependencies}
schema_version: 1
---

## Patterns
Write the thing.

## Excluded patterns
Nothing that belongs to a neighbour.

## Design questions
What is here that is worth the walk?
"""

LOCATION_DEPENDENCIES = """  - table:T-ARC
  - region:${REGION_CODE}
  - container:${CONTAINER_ID}
  - siblings:location:${REGION_CODE}
  - cell:${CELL}
  - config"""

GENRE_TEXT = """# The Ashen Reach

Water over everything that was built, and nothing rotted.

## Constants
The water gives no sound back.
"""


def a_pattern(sandbox: Sandbox, name: str, *, id: str, target: str, phase: str = "builder",
              dependencies: str = "  - config") -> None:
    sandbox.write(f"patterns/{name}.md",
                  PATTERN.format(id=id, target=target, phase=phase,
                                 dependencies=dependencies))


def a_genre(sandbox: Sandbox, text: str = GENRE_TEXT) -> None:
    sandbox.write(GENRE, text)


def a_cell(sandbox: Sandbox, cell: str, line: str) -> None:
    sandbox.write(f"patterns/cells/{cell}.md", f"# {cell}\n\n{line}\n")


class TestRouter(unittest.TestCase):
    """The index is generated from frontmatter, and never hand-maintained."""

    def test_the_committed_index_is_current(self) -> None:
        """A pattern change that skipped the router is a stale router table."""
        with Sandbox() as sandbox:
            result = sandbox.run("router.py", "--check")
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_a_new_pattern_reaches_the_index(self) -> None:
        with Sandbox() as sandbox:
            a_pattern(sandbox, "location/builder", id="location.builder.fields",
                      target="location", dependencies=LOCATION_DEPENDENCIES)
            self.assertEqual(sandbox.run("router.py", "--check").returncode, 1)
            self.assertEqual(sandbox.run("router.py").returncode, 0)

            index = sandbox.read(ROUTER)
            self.assertIn("`location.builder.fields`", index)
            self.assertIn("| location | builder |", index)
            self.assertIn("`cell:${CELL}`", index)
            self.assertEqual(sandbox.run("router.py", "--check").returncode, 0)

    def test_a_broken_pattern_stops_the_write(self) -> None:
        """An index built from unchecked frontmatter routes calls that cannot resolve."""
        cases = [
            ("phase: builder", "phase: polisher", "phase"),
            ("  - config", "  - table:T-ZZZ", "catalogue"),
            ("## Design questions\n", "## Questions\n", "Design questions"),
            ("schema_version: 1", "schema_version: 2", "schema_version"),
        ]
        for old, new, expected in cases:
            with self.subTest(expected=expected), Sandbox() as sandbox:
                before = sandbox.read(ROUTER)
                a_pattern(sandbox, "region/builder", id="region.builder.fields",
                          target="region")
                sandbox.sub("patterns/region/builder.md", old, new)

                result = sandbox.run("router.py")
                self.assertEqual(result.returncode, 1)
                self.assertIn(expected, result.stderr)
                self.assertEqual(sandbox.read(ROUTER), before, "a broken pattern wrote an index")

    def test_a_duplicate_id_is_refused(self) -> None:
        with Sandbox() as sandbox:
            a_pattern(sandbox, "region/builder", id="region.builder.fields", target="region")
            a_pattern(sandbox, "region/builder-again", id="region.builder.fields",
                      target="region")
            result = sandbox.run("router.py")
            self.assertEqual(result.returncode, 1)
            self.assertIn("already used by", result.stderr)

    def test_cells_and_templates_are_not_routed(self) -> None:
        """A cell file carries no target or phase, so routing one would fail the run."""
        with Sandbox() as sandbox:
            a_cell(sandbox, "WILD_HIGH", "The arrival, and the thing worth leaving the road for.")
            sandbox.write("patterns/templates/location.md", "## Features\n")
            sandbox.path("patterns/cells/SAFE_LOW.md").unlink()
            self.assertEqual(sandbox.run("router.py").returncode, 0)

            index = sandbox.read(ROUTER)
            self.assertNotIn("templates/location.md", index)
            self.assertIn("| `WILD_HIGH` | `patterns/cells/WILD_HIGH.md` | yes |", index)
            self.assertIn("| `SAFE_LOW` | `patterns/cells/SAFE_LOW.md` | no |", index)


class TestCells(unittest.TestCase):
    """The nine cell files are the tuning surface, and a missing one stops a build."""

    SECTIONS = ["What belongs here", "Where the boundary falls", "Form",
                "Worked example", "Excluded patterns"]

    def cells(self) -> list[str]:
        weights = common.load_weights(REPO)
        return [f"{region_type}_{weight}"
                for region_type in weights["region_types"]
                for weight in weights["location_weights"]]

    def test_all_nine_are_written(self) -> None:
        missing = [cell for cell in self.cells()
                   if not (REPO / common.CELLS_DIR / f"{cell}.md").exists()]
        self.assertEqual(missing, [], "a cell:<TYPE>_<WEIGHT> selector cannot resolve")

    def test_each_states_its_own_discipline(self) -> None:
        """SPEC.md 9.4: what belongs in it, where the boundary falls, the form, examples."""
        for cell in self.cells():
            with self.subTest(cell=cell):
                text = (REPO / common.CELLS_DIR / f"{cell}.md").read_text(encoding="utf-8")
                self.assertTrue(text.startswith(f"# {cell}\n"), "a cell names itself first")
                missing = [s for s in self.SECTIONS if f"## {s}" not in text]
                self.assertEqual(missing, [], f"{cell} states no {missing}")

    def test_a_checked_count_is_cited_by_key(self) -> None:
        """SPEC.md 9.6: never write a checked count into a cell file. Cite the key."""
        for cell in self.cells():
            if not cell.endswith("_HIGH"):
                continue
            with self.subTest(cell=cell):
                text = (REPO / common.CELLS_DIR / f"{cell}.md").read_text(encoding="utf-8")
                self.assertTrue("region_weights" in text and common.WEIGHTS_PATH in text,
                                f"{cell} does not cite the config key holding its floor")


class TestResolveDeps(unittest.TestCase):
    """One bundle per generation call, and two rules a writer cannot talk past."""

    BUNDLE = "build/bundles/location.builder.fields-R03-L07.md"

    def a_location_call(self, sandbox: Sandbox) -> None:
        a_genre(sandbox)
        a_cell(sandbox, "WILD_HIGH", "A landmark is what a party leaves the road for.")
        a_cell(sandbox, "WILD_LOW", "Connective ground, and it should read as questionable.")
        a_pattern(sandbox, "location/builder", id="location.builder.fields",
                  target="location", dependencies=LOCATION_DEPENDENCIES)

    def test_a_bundle_carries_the_injected_and_the_declared(self) -> None:
        with Sandbox() as sandbox:
            self.a_location_call(sandbox)
            result = sandbox.run("resolve_deps.py", "--pattern", "location.builder.fields",
                                 "--target", "R03-L07")
            self.assertEqual(result.returncode, 0, result.stderr)

            bundle = sandbox.read(self.BUNDLE)
            # Injected without being declared (SPEC.md 7.3).
            self.assertIn("## Genre", bundle)
            self.assertIn("The water gives no sound back.", bundle)
            self.assertIn("## Mechanics", bundle)
            self.assertIn("{TEST: Sanity}", bundle)
            # Declared.
            self.assertIn("## Table T-ARC", bundle)
            self.assertIn("## Region R03", bundle)
            self.assertIn("## Container drowned-tier", bundle)
            self.assertIn("## Config", bundle)
            self.assertIn("locations_min", bundle)

    def test_exactly_one_cell_resolves(self) -> None:
        """A writer never carries the other eight (SPEC.md 7.5)."""
        with Sandbox() as sandbox:
            self.a_location_call(sandbox)
            sandbox.run("resolve_deps.py", "--pattern", "location.builder.fields",
                        "--target", "R03-L07")
            bundle = sandbox.read(self.BUNDLE)
            self.assertIn("A landmark is what a party leaves the road for.", bundle)
            self.assertNotIn("Connective ground", bundle)

    def test_siblings_carry_identity_and_no_content(self) -> None:
        with Sandbox() as sandbox:
            self.a_location_call(sandbox)
            sandbox.run("resolve_deps.py", "--pattern", "location.builder.fields",
                        "--target", "R03-L07")
            bundle = sandbox.read(self.BUNDLE)
            siblings = bundle.split("## Sibling locations in R03")[1].split("\n## ")[0]
            self.assertIn("R03-L03", siblings)
            self.assertNotIn("R03-L07", siblings, "a target is not its own sibling")

            body = sandbox.read(L03).split("## Player Overview")[1]
            sentence = next(line for line in body.split("\n") if len(line.split()) > 8)
            self.assertNotIn(sentence.strip(), bundle,
                             "a sibling's prose reached the bundle")

    def test_the_variables_come_from_the_target(self) -> None:
        with Sandbox() as sandbox:
            self.a_location_call(sandbox)
            sandbox.run("resolve_deps.py", "--pattern", "location.builder.fields",
                        "--target", "R03-L07")
            fm = common.split_frontmatter(sandbox.read(self.BUNDLE))[0]
            self.assertEqual(fm["dependencies"], [
                "table:T-ARC", "region:R03", "container:drowned-tier",
                "siblings:location:R03", "cell:WILD_HIGH", "config",
            ])

    def test_an_unfilled_variable_names_the_flag_that_fills_it(self) -> None:
        """A region target implies no cell, so the resolver asks rather than guesses."""
        with Sandbox() as sandbox:
            a_genre(sandbox)
            a_cell(sandbox, "WILD_HIGH", "A landmark.")
            a_pattern(sandbox, "region/builder", id="region.builder.fields", target="region",
                      dependencies="  - cell:${CELL}")

            refused = sandbox.run("resolve_deps.py", "--pattern", "region.builder.fields",
                                  "--target", "R03")
            self.assertEqual(refused.returncode, 1)
            self.assertIn("--var CELL=", refused.stderr)

            filled = sandbox.run("resolve_deps.py", "--pattern", "region.builder.fields",
                                 "--target", "R03", "--var", "CELL=WILD_HIGH")
            self.assertEqual(filled.returncode, 0, filled.stderr)

    def test_the_s_boundary_is_mechanical(self) -> None:
        """S content reaches a player through a T table, never directly (SPEC.md 7.4)."""
        with Sandbox() as sandbox:
            a_genre(sandbox)
            a_cell(sandbox, "WILD_HIGH", "A landmark.")
            a_pattern(sandbox, "location/builder", id="location.builder.fields",
                      target="location", dependencies="  - table:S-HIS")
            a_pattern(sandbox, "region/builder", id="region.builder.fields",
                      target="region", dependencies="  - table:S-HIS")

            refused = sandbox.run("resolve_deps.py", "--pattern", "location.builder.fields",
                                  "--target", "R03-L07")
            self.assertEqual(refused.returncode, 1)
            self.assertIn("S tables are referee-facing", refused.stderr)
            self.assertFalse(sandbox.path(self.BUNDLE).exists())

            allowed = sandbox.run("resolve_deps.py", "--pattern", "region.builder.fields",
                                  "--target", "R03")
            self.assertEqual(allowed.returncode, 0, allowed.stderr)

            self.assertEqual(sandbox.run("resolve_deps.py", "--check").returncode, 1)

    def test_the_genre_cap_is_enforced(self) -> None:
        """GENRE.md enters every bundle, so its size is a tax on every call."""
        with Sandbox() as sandbox:
            self.a_location_call(sandbox)
            cap = common.load_weights(sandbox.root)["genre"]["max_words"]
            a_genre(sandbox, GENRE_TEXT + "\n" + " ".join(["water"] * (cap + 1)))

            refused = sandbox.run("resolve_deps.py", "--pattern", "location.builder.fields",
                                  "--target", "R03-L07")
            self.assertEqual(refused.returncode, 1)
            self.assertIn(f"over the {cap} word cap", refused.stderr)
            self.assertEqual(sandbox.run("resolve_deps.py", "--check").returncode, 1)

    def test_a_missing_input_is_an_error_not_a_thinner_bundle(self) -> None:
        cases = [
            (lambda s: s.path(GENRE).unlink(), "GENRE.md does not exist"),
            (lambda s: s.path("patterns/cells/WILD_HIGH.md").unlink(), "Milestone 3"),
        ]
        for remove, expected in cases:
            with self.subTest(expected=expected), Sandbox() as sandbox:
                self.a_location_call(sandbox)
                remove(sandbox)
                result = sandbox.run("resolve_deps.py", "--pattern", "location.builder.fields",
                                     "--target", "R03-L07")
                self.assertEqual(result.returncode, 1)
                self.assertIn(expected, result.stderr)
                self.assertFalse(sandbox.path(self.BUNDLE).exists())

    def test_stdout_writes_no_bundle(self) -> None:
        """/generate samples a pattern without touching the tree (SPEC.md 12.1)."""
        with Sandbox() as sandbox:
            self.a_location_call(sandbox)
            result = sandbox.run("resolve_deps.py", "--pattern", "location.builder.fields",
                                 "--target", "R03-L07", "--stdout")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("# Bundle: location.builder.fields for R03-L07", result.stdout)
            self.assertFalse(sandbox.path(self.BUNDLE).exists())

    def test_an_output_template_reaches_the_bundle(self) -> None:
        with Sandbox() as sandbox:
            self.a_location_call(sandbox)
            sandbox.write("patterns/templates/location.md", "### <Feature name>\n")
            sandbox.sub("patterns/location/builder.md", "schema_version: 1",
                        "output_template: templates/location.md\nschema_version: 1")

            self.assertEqual(sandbox.run("resolve_deps.py", "--pattern",
                                         "location.builder.fields", "--target",
                                         "R03-L07").returncode, 0)
            self.assertIn("### <Feature name>", sandbox.read(self.BUNDLE))

            sandbox.path("patterns/templates/location.md").unlink()
            missing = sandbox.run("resolve_deps.py", "--pattern", "location.builder.fields",
                                  "--target", "R03-L07")
            self.assertEqual(missing.returncode, 1)
            self.assertIn("output_template", missing.stderr)

    def test_a_resolved_diagram_does_not_read_as_a_hand_drawn_one(self) -> None:
        """A bundle carries a copy of a derived diagram. M13 is about authored ones."""
        with Sandbox() as sandbox:
            self.a_location_call(sandbox)
            sandbox.write("build/diagrams/T4_R03_DROWNED_TIER.md",
                          "```mermaid\nflowchart TD\n  R03_L03 --> R03_L07\n```\n")
            sandbox.run("resolve_deps.py", "--pattern", "location.builder.fields",
                        "--target", "R03-L07")

            self.assertIn("flowchart TD", sandbox.read(self.BUNDLE))
            named = [f["code"] for f in sandbox.findings("M13")]
            self.assertFalse([code for code in named if "bundles" in code], named)

    def test_check_passes_on_the_committed_tree(self) -> None:
        with Sandbox() as sandbox:
            result = sandbox.run("resolve_deps.py", "--check")
            self.assertEqual(result.returncode, 0, result.stderr)


# --------------------------------------------------------------------------
# The diagram layer
# --------------------------------------------------------------------------


class TestMermaidGen(unittest.TestCase):
    """Every tier is a projection of a connections table, and only of that."""

    def derived(self, sandbox: Sandbox) -> dict[str, str]:
        directory = sandbox.path(common.DIAGRAMS_DIR)
        return {p.name: p.read_text(encoding="utf-8") for p in directory.glob("*.md")}

    def test_every_tier_the_tree_implies_is_derived(self) -> None:
        with Sandbox() as sandbox:
            self.assertEqual(sandbox.run("mermaid_gen.py").returncode, 0)
            names = set(self.derived(sandbox))
            self.assertIn("T1_SETTING.md", names)
            # One tier 2 per setting-level container, one tier 3 per region, one
            # tier 4 per region-level container.
            self.assertLessEqual(
                {"T2_CUT_WATER.md", "T2_COVENANT_GROUND.md", "T2_SUNKEN_HOLDS.md"}, names
            )
            self.assertIn("T3_R03.md", names)
            self.assertLessEqual(
                {"T4_R03_THE_CAUSEWAY.md", "T4_R03_DROWNED_TIER.md"}, names
            )
            self.assertEqual(
                [n for n in names if n.startswith("T5")], [],
                "a location is the leaf and has no diagram",
            )

    def test_type_is_drawn_at_tier_four_and_nowhere_else(self) -> None:
        with Sandbox() as sandbox:
            sandbox.run("mermaid_gen.py")
            derived = self.derived(sandbox)
            self.assertIn("|sunk span|", derived["T4_R03_THE_CAUSEWAY.md"])
            for name, text in derived.items():
                if name.startswith("T4"):
                    continue
                self.assertIsNone(
                    validate.RE_EDGE_LABEL.search(text),
                    f"{name} carries a labelled edge, and only tier 4 may",
                )

    def test_an_edge_leaving_the_container_draws_its_destination_outside(self) -> None:
        """Tier 4 is the tier a referee navigates from, so an exit shows where it goes."""
        with Sandbox() as sandbox:
            sandbox.run("mermaid_gen.py")
            text = self.derived(sandbox)["T4_R03_THE_CAUSEWAY.md"]
            frame = text.split("subgraph", 1)[1].split("\n    end", 1)
            self.assertIn("R03_L03", frame[0], "its own location is inside the frame")
            self.assertNotIn("R03_L07", frame[0], "the destination is not inside it")
            self.assertIn("R03_L07", frame[1], "and it is drawn outside it")

    def test_a_diagram_follows_the_table_it_draws(self) -> None:
        with Sandbox() as sandbox:
            sandbox.run("mermaid_gen.py")
            before = self.derived(sandbox)["T4_R03_DROWNED_TIER.md"]
            self.assertIn("|sunk span|", before)

            sandbox.sub(REGION_CONN, "| R03-L03 | R03-L07 | sunk span | no |",
                        "| R03-L03 | R03-L07 | flooded stair | yes |")
            sandbox.run("mermaid_gen.py")
            after = self.derived(sandbox)["T4_R03_DROWNED_TIER.md"]
            self.assertIn("|flooded stair|", after)
            self.assertIn("-->", after, "a one-way edge is drawn as an arrow")

    def test_derivation_is_stable(self) -> None:
        """A second run changes nothing, which is what makes M11 a usable check."""
        with Sandbox() as sandbox:
            sandbox.run("mermaid_gen.py")
            first = self.derived(sandbox)
            result = sandbox.run("mermaid_gen.py")
            self.assertEqual(self.derived(sandbox), first)
            self.assertIn("0 written", result.stdout)

    def test_a_diagram_of_nothing_is_removed(self) -> None:
        with Sandbox() as sandbox:
            sandbox.write(f"{common.DIAGRAMS_DIR}/T4_R03_OLD_NAME.md",
                          "```mermaid\nflowchart TD\n```\n")
            sandbox.run("mermaid_gen.py")
            self.assertNotIn("T4_R03_OLD_NAME.md", self.derived(sandbox))

    def test_check_reports_a_hand_edited_diagram(self) -> None:
        with Sandbox() as sandbox:
            self.assertEqual(sandbox.run("mermaid_gen.py", "--check").returncode, 0)
            sandbox.sub("build/diagrams/T3_R03.md", "The Causeway", "The Old Road")
            stale = sandbox.run("mermaid_gen.py", "--check")
            self.assertEqual(stale.returncode, 1)
            self.assertIn("T3_R03.md", stale.stderr)


# --------------------------------------------------------------------------
# The build
# --------------------------------------------------------------------------


class TestBuild(unittest.TestCase):
    """The playbook is a projection of the tree and holds nothing of its own."""

    def built(self, sandbox: Sandbox) -> str:
        sandbox.run("mermaid_gen.py")
        result = sandbox.run("build.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        return sandbox.read(PLAYBOOK)

    def test_every_marker_is_spliced(self) -> None:
        with Sandbox() as sandbox:
            markers = sum(
                len(common.RE_DIAGRAM_MARKER.findall(path.read_text(encoding="utf-8")))
                for path in sandbox.path("setting").rglob("*.md")
            )
            self.assertGreater(markers, 0, "the fixture carries markers to splice")

            playbook = self.built(sandbox)
            self.assertEqual(common.RE_DIAGRAM_MARKER.findall(playbook), [],
                             "no marker survives into the artifact")
            self.assertEqual(len(common.RE_MERMAID_BLOCK.findall(playbook)), markers)

    def test_a_section_mark_becomes_a_link_to_its_row(self) -> None:
        with Sandbox() as sandbox:
            playbook = self.built(sandbox)
            self.assertIn("[BESTIARY, Fen-wight](#t-bes-01)", playbook)
            self.assertIn('<a id="t-bes-01"></a>', playbook)

    def test_no_architect_note_survives(self) -> None:
        with Sandbox() as sandbox:
            sandbox.sub(L03, "## Exits", "## Exits\n\n[[ still open ]]")
            playbook = self.built(sandbox)
            self.assertEqual(common.RE_ARCHITECT_NOTE.findall(playbook), [],
                             "architect visibility does not survive into the artifact")

    def test_the_playbook_is_not_read_as_a_hand_drawn_diagram(self) -> None:
        """M13 catches mermaid somebody drew. The playbook's is spliced."""
        with Sandbox() as sandbox:
            self.built(sandbox)
            named = [f["code"] for f in sandbox.findings("M13")]
            self.assertNotIn(PLAYBOOK, named)
            self.assertEqual(sandbox.validate()["errors"], 0)

    def test_a_missing_diagram_stops_the_build(self) -> None:
        with Sandbox() as sandbox:
            sandbox.run("mermaid_gen.py")
            sandbox.path("build/diagrams/T3_R03.md").unlink()
            result = sandbox.run("build.py")
            self.assertEqual(result.returncode, 1)
            self.assertIn("T3_R03.md", result.stderr)

    def test_a_reference_that_resolves_to_nothing_stops_the_build(self) -> None:
        with Sandbox() as sandbox:
            sandbox.run("mermaid_gen.py")
            sandbox.sub(L03, "(BESTIARY,", "(BESTIARIES,")
            result = sandbox.run("build.py")
            self.assertEqual(result.returncode, 1)
            self.assertIn("names no table", result.stderr)

    def test_check_writes_nothing(self) -> None:
        with Sandbox() as sandbox:
            sandbox.run("mermaid_gen.py")
            sandbox.path(PLAYBOOK).unlink(missing_ok=True)
            result = sandbox.run("build.py", "--check")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(sandbox.path(PLAYBOOK).exists())


if __name__ == "__main__":
    unittest.main()
