from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


CHECKER = Path(__file__).resolve().parents[2] / "skills/poteto-mode/scripts/check-plan.mjs"
PLAN = """# CSV export plan

Add stable CSV export for saved searches in PR 41. Operators review and land it.

## How to read this

One box is one unit of work. Every box names the evidence that checks it.
Check a box only when its evidence exists.
The program runs `skills/poteto-mode/playbooks/autopilot-stack.md`.
Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

## Program checklist

### Arm the program

- [ ] On the operator's go, record the durable objective in `export-objective.md`. Build PR 41, prove export parity, and deliver a verified branch for operator review.
- [ ] Read the playbook from the current installed bstack root at each audit.
- [ ] Arm the hourly runtime audit through the supported scheduler. If unavailable, checkpoint locally and report the monitoring gap.
- [ ] Send a status message only for new verdicts or blockers under host policy.
- [ ] Record the authorization boundary. Local changes and tests are allowed. Publication, merging, and deployment are not authorized.

### Spawn owners

- [ ] Give a fresh owner the export branch, consolidated directives, and prior report. Keep one writer on `src/export.py`.

### PR mechanics

- [ ] Prepare PR 41 locally and save its proposed body in `export-pr.md`.

### Verdict and merge

- [ ] Verify code-ready and changed-patch rounds with gates, live checks, perf, and at least two focused audit lanes. Audit quoting parity and data safety separately.
- [ ] Deliver only with all required evidence. Apply Shipping's verification reuse rule after branch movement.

### Boot recipe

- [ ] Start the CLI in an isolated checkout and load `fixtures/saved-search.json`.
- [ ] Capture the terminal with the available control driver at the reported SHA.

## Export saved searches (PR 41)

**Depends on.** None.

**Files.**

- [ ] Edit `src/export.py` and `tests/test_export.py`.

**Build.**

- [ ] Add RFC-compliant CSV quoting to the export command.

**You see.**

- [ ] `search export saved-1` prints the expected CSV rows in stable order.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Run `python -m unittest tests.test_export`. Compare quoted fields with literal CSV values.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `deep-code` at the PR head, per the boot recipe.

- [ ] Lane 1. Run the same saved search at trunk and head. Save `parity.png`. Pass when existing row order is preserved.
- [ ] Lane 2. Export an empty search. Save `empty.png`. Pass when only the header appears.
- [ ] Lane 3. Export a field containing a comma. Save `comma.png`. Pass when one quoted column contains the comma.
- [ ] Lane 4. Export a field containing quotes. Save `quotes.png`. Pass when each quote is doubled.
- [ ] Lane 5. Export a multiline field. Save `multiline.png`. Pass when a CSV reader returns one field.
- [ ] Lane 6. Export Unicode text. Save `unicode.png`. Pass when the original text survives a readback.
- [ ] Lane 7. Export a null field. Save `null.png`. Pass when the documented empty-cell representation appears.
- [ ] Lane 8. Export a missing search. Save `missing.png`. Pass when the CLI exits with its documented not-found error.
- [ ] Lane 9. Export to a read-only target. Save `readonly.png`. Pass when the command reports failure without replacing the target.
- [ ] Lane 10. Export 10000 rows. Save `large.png`. Pass when the last row and row count match the fixture.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Measure total time to export 10000 rows at trunk and head.
- [ ] Probe. Run five interleaved exports per SHA with identical fixtures and record each duration.
- [ ] Baseline. Record trunk's median duration before assessing the head.
- [ ] Rule. Fail if head median exceeds trunk by 10 percent.

**Review gate.** The operator reviews the changed CLI interaction before merge.

- [ ] Give the operator the screenshots and a video of the command and readback.

**Merge.**

- [ ] Save the clean verdict and exact SHA, and leave landing to the operator.

## Close the program

- [ ] Deliver the verified branch and receipts after every required box has evidence.

## Appendix A. Prototype evidence

A local CSV reader confirmed the quoting format. No external publication occurred.
"""


@unittest.skipUnless(shutil.which("node"), "Node is required to run the plan checker")
class PlanCheckerTests(unittest.TestCase):
    def run_plan(self, text):
        with tempfile.TemporaryDirectory() as temporary:
            plan = Path(temporary) / "plan.md"
            plan.write_text(text)
            return subprocess.run(
                ["node", str(CHECKER), str(plan)],
                capture_output=True,
                text=True,
                check=False,
            )

    def assert_rejected(self, text, diagnostic):
        result = self.run_plan(text)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("1 PR sections, 1 problems", result.stdout)
        self.assertIn(diagnostic, result.stderr)

    def test_filled_role_and_hourly_plan_pass(self):
        for role in ("deep-code", "critic", "judgment", "fast-code"):
            with self.subTest(role=role):
                result = self.run_plan(PLAN.replace("`deep-code`", f"`{role}`"))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("1 PR sections, 0 problems", result.stdout)
                self.assertEqual(result.stderr, "")

    def test_placeholder_and_provider_roles_fail(self):
        for role in ("<semantic worker role>", "deep-<role>", " ", "provider-default"):
            with self.subTest(role=role):
                self.assert_rejected(
                    PLAN.replace("`deep-code`", f"`{role}`"),
                    "with a supported role filled in",
                )

    def test_wrong_audit_cadence_fails(self):
        self.assert_rejected(
            PLAN.replace("hourly runtime audit", "30-minute runtime audit"),
            'lacks "hourly runtime audit"',
        )

    def test_missing_live_lane_fails(self):
        self.assert_rejected(
            "\n".join(line for line in PLAN.splitlines() if "Lane 10." not in line),
            "expected 1 to 10",
        )

    def test_missing_audit_lanes_fail(self):
        self.assert_rejected(
            PLAN.replace("at least two focused audit lanes", "one general review"),
            'lacks "at least two focused audit lanes"',
        )

    def test_missing_authority_evidence_fails(self):
        self.assert_rejected(
            "\n".join(line for line in PLAN.splitlines() if "authorization boundary" not in line),
            'lacks "authorization boundary"',
        )

    def test_durable_objective_and_installed_root_remain_required(self):
        for marker in ("record the durable objective", "current installed bstack root"):
            with self.subTest(marker=marker):
                self.assert_rejected(PLAN.replace(marker, "read local notes"), f'lacks "{marker}"')


if __name__ == "__main__":
    unittest.main()
