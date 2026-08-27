"""Every mechanical check fires when the thing it guards is broken.

A validator that never complains is worth nothing, and a check can be disarmed
by an unrelated refactor without anyone noticing. Each case here breaks exactly
one thing in a copy of the repository and asserts that the matching check
reports it, at the severity SPEC.md section 14.1 assigns.

M11's case breaks a derived diagram rather than a content file, because that is
what the check guards: the diagram layer is derived in full, and a file edited
by hand is the one way it can disagree with the tables it draws.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import (  # noqa: E402
    DANGEROUS_REGION, DIAGRAM, L03, L07, LEDGER, REGION, REGION_CONN, SETTING_CONN,
    T_KEY, Sandbox,
)

# check -> (how to break it, steps that must be complete first, expected severity)
BREAKS: dict[str, tuple[object, tuple[int, ...], str]] = {
    "M1": (lambda s: s.sub(L03, "code: R03-L03", "code: R03-L07"), (), "ERROR"),
    "M2": (lambda s: s.rename(L03, "R03-L03-bell-road.md"), (), "ERROR"),
    "M3": (lambda s: s.sub(L03, "tags: [raised, exposed, tolling]",
                           "tags: [raised, exposed]"), (), "ERROR"),
    "M4": (lambda s: s.sub(REGION, "difficulty: d6", "difficulty: d7"), (), "ERROR"),
    "M5": (lambda s: s.sub(L07, "cell: WILD_HIGH", "cell: SAFE_HIGH"), (), "ERROR"),
    "M6": (lambda s: s.sub(L07, "cell: WILD_HIGH", "cell: WILD_LOW"), (9,), "ERROR"),
    "M7": (lambda s: s.sub(L03, "| R03-L07 | sunk span |", "| R03-L99 | sunk span |"),
           (), "ERROR"),
    "M8": (lambda s: s.sub(L07, "| R03-L03 | sunk span |", "| | |"), (10,), "ERROR"),
    "M9": (lambda s: s.sub(REGION_CONN, "| R03-L03 | R03-L07 | sunk span | no |", ""),
           (10,), "ERROR"),
    "M10": (lambda s: s.sub(L07, "container: drowned-tier", "container: no-such-tier"),
            (), "ERROR"),
    "M11": (lambda s: s.sub(DIAGRAM, 'C_DROWNED_TIER["The Drowned Tier"]',
                            'C_DROWNED_TIER["The Sunken Tier"]'), (), "ERROR"),
    "M12": (lambda s: s.sub(SETTING_CONN, "| From | To |\n| :--- | :--- |",
                            "| From | To | Type |\n| :--- | :--- | :--- |\n"
                            "| R03 | R03 | road |"), (), "ERROR"),
    "M13": (lambda s: s.sub(L03, "## Exits",
                            "## Exits\n\n```mermaid\nflowchart TD\n  A --> B\n```"),
            (), "ERROR"),
    "M14": (lambda s: s.sub(L03, "sources: [T-ARC-02", "sources: [S-HIS-01, T-ARC-02"),
            (), "ERROR"),
    "M15": (lambda s: s.sub(L03, "T-NAM-01, ", ""), (10,), "ERROR"),
    "M16": (lambda s: s.sub(L07, "(LORE, T-LOR-03)", "(LORE, T-LOR-99)"), (), "ERROR"),
    "M17": (lambda s: s.sub(L07, "is a **votive shelf**", "is a **brass altar**"),
            (), "ERROR"),
    "M18": (lambda s: s.sub(REGION, "name: Ashen Fen", "name: Zorbulax Fen"), (3,), "ERROR"),
    "M19": (lambda s: s.sub(REGION, "| 1 | Peat smoke from the west",
                            "| 4 | Peat smoke from the west"), (), "ERROR"),
    # M19 is checked twice: once for a roll column out of order, and once for a
    # Danger table that counts up. The second is the case the direction rule
    # exists for, and no ascending table can catch it.
    "M19d": (lambda s: s.sub(DANGEROUS_REGION, "| 6 | Wet rope", "| 1 | Wet rope"),
             (), "ERROR"),
    "M20": (lambda s: s.sub(T_KEY, "| R03-L03 | R03-L07 |", "|  |  |"), (10,), "ERROR"),
    "M21": (lambda s: s.sub(L07, "{WOUND: Frost}", "{WOUND: Sonic}"), (), "ERROR"),
    "M22": (lambda s: s.sub(L07, "**Terrain:** Dressed slab", "Dressed slab"), (), "ERROR"),
    "M23": (lambda s: s.sub(L07, "The reeds stop thirty yards",
                            "Water -> R03-L03. The reeds stop thirty yards"), (), "ERROR"),
    "M24": (lambda s: s.sub(L07, "a hand of still water", "a hand of still water, 2d6 of it"),
            (), "REPORT"),
    "M25": (lambda s: (s.sub(L07, "## Features", "## Features\n\n[[ still open ]]"),
                       s.mark("decorated", "R03-L07")), (), "REPORT"),
}


class TestBaseline(unittest.TestCase):
    """The repository as committed passes its own checks."""

    def test_no_errors(self) -> None:
        with Sandbox() as sandbox:
            result = sandbox.validate()
            self.assertEqual(
                result["errors"], 0,
                "\n".join(f"{f['check']} {f['code']}: {f['message']}"
                          for f in result["findings"] if f["severity"] == "ERROR"),
            )

    def test_every_report_is_a_declared_gate(self) -> None:
        """Nothing reports without a stated reason. A bare REPORT is a real finding."""
        with Sandbox() as sandbox:
            bare = [f for f in sandbox.validate()["findings"] if not f["deferred"]]
            self.assertEqual(bare, [], "unexplained findings in the committed tree")

    def test_exit_code_is_zero(self) -> None:
        with Sandbox() as sandbox:
            self.assertEqual(sandbox.run("validate.py").returncode, 0)


class TestChecksFire(unittest.TestCase):
    """Break one thing; the matching check reports it."""

    def test_each_check(self) -> None:
        for case, (mutate, gates, severity) in sorted(
            BREAKS.items(), key=lambda item: (int(item[0][1:].rstrip("abcd") or 0), item[0])
        ):
            check = "M" + case[1:].rstrip("abcd")
            with self.subTest(case=case), Sandbox() as sandbox:
                sandbox.complete_steps(*gates)
                mutate(sandbox)
                hits = [
                    f for f in sandbox.findings(check)
                    if f["severity"] == severity and not f["deferred"]
                ]
                raised = sorted({f["check"] for f in sandbox.validate()["findings"]})
                self.assertTrue(
                    hits, f"{case} did not fire at {severity}. Raised: {raised or 'nothing'}"
                )

    def test_every_check_has_a_case(self) -> None:
        """A new check must arrive with a case that proves it fires."""
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
        import validate  # noqa: PLC0415

        covered = {"M" + case[1:].rstrip("abcd") for case in BREAKS}
        missing = set(validate.CHECKS) - covered
        self.assertEqual(missing, set(), f"checks with no negative case: {sorted(missing)}")


class TestSeverity(unittest.TestCase):
    """Severity, gates and --final."""

    def test_gate_defers_until_its_step_closes(self) -> None:
        """M15 cannot be true before step 10 writes the citations."""
        with Sandbox() as sandbox:
            sandbox.reopen_steps(10)
            sandbox.sub(L03, "T-NAM-01, ", "")

            before = [f for f in sandbox.findings("M15") if f["code"] == "T-NAM"]
            self.assertEqual(len(before), 1)
            self.assertEqual(before[0]["severity"], "REPORT")
            self.assertTrue(before[0]["deferred"], "a deferred finding states why")

            sandbox.complete_steps(10)
            after = [f for f in sandbox.findings("M15") if f["code"] == "T-NAM"]
            self.assertEqual(after[0]["severity"], "ERROR")
            self.assertFalse(after[0]["deferred"])

    def test_setting_edges_defer_until_the_regions_are_stubbed(self) -> None:
        """M7's setting branch cannot be true between step 2 and step 5."""
        with Sandbox() as sandbox:
            sandbox.reopen_steps(5)
            sandbox.sub(SETTING_CONN, "| From | To |\n| :--- | :--- |",
                        "| From | To |\n| :--- | :--- |\n| R03 | R99 |")

            before = [f for f in sandbox.findings("M7") if "R99" in f["message"]]
            self.assertEqual(len(before), 1)
            self.assertEqual(before[0]["severity"], "REPORT")
            self.assertTrue(before[0]["deferred"], "a deferred finding states why")

            sandbox.complete_steps(5)
            after = [f for f in sandbox.findings("M7") if "R99" in f["message"]]
            self.assertEqual(after[0]["severity"], "ERROR")
            self.assertFalse(after[0]["deferred"])

    def test_final_ignores_gates_and_promotes_reports(self) -> None:
        with Sandbox() as sandbox:
            self.assertEqual(sandbox.validate()["errors"], 0)
            final = sandbox.validate("--final")
            self.assertGreater(final["errors"], 0, "--final holds an unfinished setting to account")
            self.assertEqual(final["reports"], 0, "--final leaves nothing at REPORT")
            self.assertEqual(sandbox.run("validate.py", "--final").returncode, 1)

    def test_report_alone_does_not_fail_the_run(self) -> None:
        with Sandbox() as sandbox:
            sandbox.sub(L07, "a hand of still water", "a hand of still water, 2d6 of it")
            self.assertEqual(sandbox.validate()["errors"], 0)
            self.assertEqual(sandbox.run("validate.py").returncode, 0)


class TestScope(unittest.TestCase):
    """--scope and --only narrow what is reported, not what is checked."""

    def test_scope_excludes_other_targets(self) -> None:
        with Sandbox() as sandbox:
            sandbox.sub(L03, "tags: [raised, exposed, tolling]", "tags: [raised, exposed]")
            self.assertTrue(sandbox.findings("M3", "--scope", "R03-L03"))
            self.assertFalse(sandbox.findings("M3", "--scope", "R03-L07"))

    def test_region_scope_covers_its_locations(self) -> None:
        with Sandbox() as sandbox:
            sandbox.sub(L07, "cell: WILD_HIGH", "cell: SAFE_HIGH")
            self.assertTrue(sandbox.findings("M5", "--scope", "R03"))

    def test_only_runs_the_named_checks(self) -> None:
        with Sandbox() as sandbox:
            sandbox.sub(L03, "tags: [raised, exposed, tolling]", "tags: [raised, exposed]")
            self.assertEqual(sandbox.validate("--only", "M17")["findings"], [])
            self.assertTrue(sandbox.validate("--only", "M3")["findings"])

    def test_unknown_check_is_refused(self) -> None:
        with Sandbox() as sandbox:
            self.assertEqual(sandbox.run("validate.py", "--only", "M99").returncode, 2)


class TestUnreadableFiles(unittest.TestCase):
    """A file that cannot be parsed is reported, not skipped."""

    def test_broken_frontmatter_is_an_error(self) -> None:
        with Sandbox() as sandbox:
            sandbox.sub(L07, "---\ncode: R03-L07", "code: R03-L07")
            result = sandbox.validate()
            self.assertGreater(result["errors"], 0)
            self.assertTrue(any("could not be read" in f["message"] for f in result["findings"]))


if __name__ == "__main__":
    unittest.main()
