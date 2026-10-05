from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/show-me-your-work/scripts/log.sh"
HEADER = "ts\tphase\tdecision\twhy\tevidence\tresult\n"


class DecisionLogTests(unittest.TestCase):
    def run_log(self, path: Path, cells: list[str], false_stat: bool = False) -> None:
        args = ["bash", str(SCRIPT), str(path), *cells]
        env = os.environ.copy()
        if false_stat:
            env["BSTACK_LOG_TEST_PATH"] = str(path)
            wrapper = """
function [ {
    if [[ "$1" == "!" && ( "$2" == "-f" || "$2" == "-s" ) && "$3" == "$BSTACK_LOG_TEST_PATH" ]]; then
        return 0
    fi
    builtin [ "$@"
}
source "$@"
"""
            args = ["bash", "-c", wrapper, "log-test", str(SCRIPT), str(path), *cells]
        result = subprocess.run(args, capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_empty_existing_log_receives_header(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "decisions.tsv"
            log.touch()
            self.run_log(log, ["build", "changed", "reason", "file", "pass"])
            lines = log.read_text().splitlines()
            self.assertEqual(lines[0], HEADER.rstrip("\n"))
            self.assertEqual(lines[1].split("\t")[1:], ["build", "changed", "reason", "file", "pass"])

    def test_existing_rows_survive_failed_file_stat(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "decisions.tsv"
            original = HEADER + "2026-01-01T00:00:00Z\tstart\told\twhy\told.txt\tpass\n"
            log.write_text(original)
            self.run_log(log, ["build", "new", "why", "new.txt", "pass"], false_stat=True)
            content = log.read_text()
            self.assertTrue(content.startswith(original))
            self.assertEqual(content.splitlines()[-1].split("\t")[1:], ["build", "new", "why", "new.txt", "pass"])

    def test_interleaved_runs_keep_their_own_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_a = Path(directory) / "task" / "run-a.tsv"
            run_b = Path(directory) / "task" / "run-b.tsv"
            self.run_log(run_a, ["start", "start A", "new run", "run-a", "open"])
            self.run_log(run_a, ["build", "A first", "why", "a.txt", "pass"])
            self.run_log(run_b, ["start", "start B", "new run", "run-b", "open"])
            self.run_log(run_b, ["build", "B first", "why", "b.txt", "pass"])
            prior_b = run_b.read_bytes()
            self.run_log(run_a, ["build", "A resumed", "why", "a2.txt", "pass"])
            decisions_a = [row.split("\t")[2] for row in run_a.read_text().splitlines()[1:]]
            decisions_b = [row.split("\t")[2] for row in run_b.read_text().splitlines()[1:]]
            self.assertEqual(decisions_a, ["start A", "A first", "A resumed"])
            self.assertEqual(decisions_b, ["start B", "B first"])
            self.assertEqual(run_b.read_bytes(), prior_b)

    def test_repeated_writes_preserve_rows_and_escape_cells(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "nested" / "decisions.tsv"
            self.run_log(log, ["start", "first", "why", "file", "pass"])
            original = log.read_text()
            self.run_log(log, ["=phase", "+decision", "-why", "@evidence", "a\tb\nc\rd"])
            content = log.read_text()
            self.assertTrue(content.startswith(original))
            self.assertEqual(content.count(HEADER), 1)
            self.assertEqual(content.splitlines()[-1].split("\t")[1:], ["'=phase", "'+decision", "'-why", "'@evidence", "a b c d"])


if __name__ == "__main__":
    unittest.main()
