#!/usr/bin/env python3
import json
import os
import stat
import tempfile
import time
import unittest
from pathlib import Path

import bstack_exec


class FakeRunner:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = []

    def run(self, argv, **kwargs):
        self.calls.append((list(argv), kwargs))
        if self.error:
            raise self.error
        return self.result


class DispatcherTests(unittest.TestCase):
    def setUp(self):
        self.cwd = tempfile.TemporaryDirectory()
        self.path = self.cwd.name

    def tearDown(self):
        self.cwd.cleanup()

    def test_exact_codex_argv_and_auto_omits_model(self):
        self.assertEqual(
            bstack_exec.build_argv("codex", "auto", self.path, "read-only"),
            ["codex", "exec", "--ephemeral", "--sandbox", "read-only", "-C", self.path, "--json", "-"],
        )
        self.assertEqual(
            bstack_exec.build_argv("codex", "gpt-5.6-luna", self.path, "workspace-write")[-3:],
            ["-m", "gpt-5.6-luna", "-"],
        )

    def test_exact_claude_argv(self):
        self.assertEqual(
            bstack_exec.build_argv("claude", "fable", self.path, "read-only"),
            ["claude", "-p", "--restricted", "--strict-mcp-config", "--permission-mode", "plan", "--output-format", "json", "--no-session-persistence", "--model", "fable"],
        )
        self.assertEqual(
            bstack_exec.build_argv("claude", "auto", self.path, "workspace-write"),
            ["claude", "-p", "--restricted", "--strict-mcp-config", "--permission-mode", "acceptEdits", "--output-format", "json", "--no-session-persistence"],
        )

    def test_claude_routes_keep_restrictions_and_no_bypass_flags(self):
        for access in ("read-only", "workspace-write"):
            argv = bstack_exec.build_argv("claude", "fable", self.path, access)
            self.assertIn("--restricted", argv)
            self.assertIn("--strict-mcp-config", argv)
            self.assertNotIn("--dangerously-skip-permissions", argv)
            self.assertNotIn("--bare", argv)

    def test_validation_does_not_run_process(self):
        runner = FakeRunner()
        for kwargs in (
            {"cwd": "relative"},
            {"cwd": "/definitely/missing"},
            {"prompt": "  "},
            {"model": "--unexpected-flag"},
        ):
            values = {"executor": "codex", "model": "auto", "cwd": self.path, "access": "read-only", "prompt": "hello"}
            values.update(kwargs)
            result = bstack_exec.dispatch(**values, runner=runner)
            self.assertEqual(result["error"]["code"], "invalid_request")
        self.assertEqual(runner.calls, [])

    def test_codex_jsonl_result_and_bounded_metadata(self):
        raw = b'{"type":"thread.started","thread_id":"do-not-leak"}\n{"type":"item.completed","item":{"type":"agent_message","text":"done"},"usage":{"input_tokens":3}}\n'
        runner = FakeRunner(bstack_exec.ProcessResult(raw, b"warning", 0))
        result = bstack_exec.dispatch(executor="codex", model="auto", cwd=self.path, access="read-only", prompt="secret", runner=runner)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["final_text"], "done")
        self.assertNotIn("secret", json.dumps(result))
        self.assertNotIn("do-not-leak", json.dumps(result))
        self.assertEqual(runner.calls[0][1]["stdin"], b"secret")

    def test_claude_result_and_metadata(self):
        raw = json.dumps({"type": "result", "subtype": "success", "result": "fable says hi", "session_id": "abc", "usage": {"input_tokens": 4}}).encode()
        result = bstack_exec.dispatch(executor="claude", model="fable", cwd=self.path, access="read-only", prompt="hello", runner=FakeRunner(bstack_exec.ProcessResult(raw, b"", 0)))
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["final_text"], "fable says hi")
        self.assertEqual(result["metadata"]["session_id"], "abc")

    def test_nonzero_exit_preserves_bounded_stderr(self):
        result = bstack_exec.dispatch(executor="claude", model="fable", cwd=self.path, access="read-only", prompt="hello", runner=FakeRunner(bstack_exec.ProcessResult(b"", b"failure", 7)))
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["error"]["code"], "exit_nonzero")
        self.assertEqual(result["exit_code"], 7)
        self.assertEqual(result["stderr"], "failure")

    def test_malformed_output(self):
        result = bstack_exec.dispatch(executor="codex", model="auto", cwd=self.path, access="read-only", prompt="hello", runner=FakeRunner(bstack_exec.ProcessResult(b"not json\n", b"", 0)))
        self.assertEqual(result["error"]["code"], "malformed_output")

    def test_missing_binary(self):
        result = bstack_exec.dispatch(executor="codex", model="auto", cwd=self.path, access="read-only", prompt="hello", runner=FakeRunner(error=FileNotFoundError()))
        self.assertEqual(result["error"]["code"], "missing_binary")

    def test_timeout_and_caps(self):
        result = bstack_exec.dispatch(executor="codex", model="auto", cwd=self.path, access="read-only", prompt="hello", timeout=1, runner=FakeRunner(bstack_exec.ProcessResult(b"", b"", -9, timed_out=True)))
        self.assertEqual(result["status"], "timed_out")
        self.assertEqual(result["error"]["code"], "timeout")
        capped = bstack_exec.dispatch(executor="codex", model="auto", cwd=self.path, access="read-only", prompt="hello", stdout_limit=2, stderr_limit=2, runner=FakeRunner(bstack_exec.ProcessResult(b"123", b"456", 0, stdout_truncated=True, stderr_truncated=True)))
        self.assertTrue(capped["stdout_truncated"])
        self.assertTrue(capped["stderr_truncated"])

    def test_real_runner_passes_prompt_via_stdin(self):
        script = Path(self.path) / "codex"
        script.write_text("#!/bin/sh\nread value\nprintf '%s' '{\"type\":\"item.completed\",\"item\":{\"type\":\"agent_message\",\"text\":\"ok\"}}'\nprintf '%s' \"$value\" >&2\n")
        script.chmod(script.stat().st_mode | stat.S_IXUSR)
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{self.path}:{old_path}"
        try:
            result = bstack_exec.dispatch(executor="codex", model="auto", cwd=self.path, access="read-only", prompt="stdin-marker", timeout=2)
        finally:
            os.environ["PATH"] = old_path
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["final_text"], "ok")
        self.assertEqual(result["stderr"], "[prompt redacted]")

    def test_real_runner_kills_timed_out_process_group(self):
        script = Path(self.path) / "codex"
        script.write_text("#!/usr/bin/env python3\nimport time\ntime.sleep(10)\n")
        script.chmod(script.stat().st_mode | stat.S_IXUSR)
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{self.path}:{old_path}"
        started = time.monotonic()
        try:
            result = bstack_exec.dispatch(executor="codex", model="auto", cwd=self.path, access="read-only", prompt="timeout-marker", timeout=0.1)
        finally:
            os.environ["PATH"] = old_path
        self.assertLess(time.monotonic() - started, 3)
        self.assertEqual(result["status"], "timed_out")
        self.assertEqual(result["error"]["code"], "timeout")

    def test_real_runner_caps_provider_output(self):
        script = Path(self.path) / "codex"
        script.write_text("#!/bin/sh\nprintf '%s' '{\"type\":\"item.completed\",\"item\":{\"type\":\"agent_message\",\"text\":\"xxxxxxxxxxxxxxxx\"}}'\nprintf '%s' 'yyyyyyyyyyyy' >&2\n")
        script.chmod(script.stat().st_mode | stat.S_IXUSR)
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{self.path}:{old_path}"
        try:
            result = bstack_exec.dispatch(executor="codex", model="auto", cwd=self.path, access="read-only", prompt="cap-marker", stdout_limit=8, stderr_limit=4)
        finally:
            os.environ["PATH"] = old_path
        self.assertTrue(result["stdout_truncated"])
        self.assertTrue(result["stderr_truncated"])
        self.assertLessEqual(len(result["stderr"].encode()), 4)


class ProbeTests(unittest.TestCase):
    def test_probe_uses_version_and_normalizes(self):
        runner = FakeRunner(bstack_exec.ProcessResult(b"codex-cli 1.2\n", b"", 0))
        result = bstack_exec.probe("codex", runner)
        self.assertEqual(result["status"], "available")
        self.assertEqual(runner.calls[0][0], ["codex", "--version"])


if __name__ == "__main__":
    unittest.main()
