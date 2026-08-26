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

from harness import LEDGER, REGION, Sandbox  # noqa: E402

import common  # noqa: E402
import ledger as ledger_mod  # noqa: E402
import roll  # noqa: E402

EMPTY = ("setting", "state", "STATE.md")


def scaffold_a_setting(sandbox: Sandbox) -> None:
    """One setting, all 24 tables, one region of each type, one location each."""
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
            sandbox.run("scaffold.py", "location", "--code", "R03-L11", "--name", "Mere Tier",
                        "--tags", "open,cold,deep", "--container", "drowned-tier",
                        "--weight", "LOW")
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
            sandbox.run("ledger.py", "built", "R03-L07", "R03-L03")
            sandbox.run("ledger.py", "built", "R03-L07")
            self.assertEqual(json.loads(sandbox.read(LEDGER))["built"],
                             ["R03-L03", "R03-L07"])

    def test_state_is_regenerated_on_every_write(self) -> None:
        with Sandbox() as sandbox:
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

    def test_slug_and_diagram_names(self) -> None:
        self.assertEqual(common.slugify("The Drowned Tier"), "the-drowned-tier")
        self.assertEqual(common.diagram_name(4, "R03", "drowned-tier"),
                         "T4_R03_DROWNED_TIER.md")
        self.assertEqual(common.diagram_name(1, "SETTING"), "T1_SETTING.md")

    def test_edges_read_their_one_way_column(self) -> None:
        with Sandbox() as sandbox:
            doc = common.read_doc(sandbox.path("setting/regions/R03-ashen-fen/connections.md"),
                                  "connections")
            edges = common.edges_from(doc)
            self.assertEqual(len(edges), 1)
            self.assertEqual((edges[0].source, edges[0].target, edges[0].one_way),
                             ("R03-L03", "R03-L07", False))


if __name__ == "__main__":
    unittest.main()
