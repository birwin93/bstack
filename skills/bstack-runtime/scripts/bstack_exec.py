#!/usr/bin/env python3
"""Run a bounded bstack worker through one of the supported CLI executors.

This is deliberately dependency-free.  Configuration parsing belongs to the
host/runtime layer; this module accepts one already-resolved route.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import selectors
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = 1
DEFAULT_TIMEOUT_SECONDS = 300.0
DEFAULT_STDOUT_LIMIT = 1_048_576
DEFAULT_STDERR_LIMIT = 262_144
MAX_METADATA_DEPTH = 3
MAX_METADATA_ITEMS = 32
MAX_METADATA_STRING = 4_096


class RequestError(ValueError):
    """A caller supplied an invalid dispatch request."""


@dataclass(frozen=True)
class ProcessResult:
    stdout: bytes
    stderr: bytes
    exit_code: int | None
    timed_out: bool = False
    stdout_truncated: bool = False
    stderr_truncated: bool = False


def _bounded_text(value: Any, limit: int = MAX_METADATA_STRING) -> str:
    text = value if isinstance(value, str) else str(value)
    return text[:limit]


def _bounded_metadata(value: Any, depth: int = 0) -> Any:
    """Keep provider metadata useful without copying arbitrary provider data."""

    if depth >= MAX_METADATA_DEPTH:
        return _bounded_text(value)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return _bounded_text(value)
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in list(value.items())[:MAX_METADATA_ITEMS]:
            result[_bounded_text(key, 128)] = _bounded_metadata(item, depth + 1)
        return result
    if isinstance(value, (list, tuple)):
        return [_bounded_metadata(item, depth + 1) for item in value[:MAX_METADATA_ITEMS]]
    return _bounded_text(value)


def _redact_prompt(value: Any, prompt: str) -> Any:
    """Prevent an executor that echoes stdin from reflecting it in results."""

    if isinstance(value, str):
        return value.replace(prompt, "[prompt redacted]")
    if isinstance(value, Mapping):
        return {str(key): _redact_prompt(item, prompt) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_prompt(item, prompt) for item in value]
    return value


def _append_bounded(buffer: bytearray, data: bytes, limit: int) -> bool:
    remaining = limit - len(buffer)
    if remaining <= 0:
        return bool(data)
    buffer.extend(data[:remaining])
    return len(data) > remaining


class ProcessRunner:
    """Subprocess runner with bounded pipes and process-group timeouts."""

    def run(
        self,
        argv: Sequence[str],
        *,
        cwd: str,
        stdin: bytes,
        timeout: float,
        stdout_limit: int,
        stderr_limit: int,
    ) -> ProcessResult:
        try:
            process = subprocess.Popen(
                list(argv),
                cwd=cwd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )
        except FileNotFoundError as exc:
            raise FileNotFoundError(str(argv[0])) from exc

        assert process.stdin is not None
        assert process.stdout is not None
        assert process.stderr is not None
        try:
            process.stdin.write(stdin)
        except BrokenPipeError:
            pass
        finally:
            process.stdin.close()

        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ, "stdout")
        selector.register(process.stderr, selectors.EVENT_READ, "stderr")
        stdout = bytearray()
        stderr = bytearray()
        stdout_truncated = False
        stderr_truncated = False
        deadline = time.monotonic() + timeout
        timed_out = False

        try:
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    timed_out = True
                    self._kill_group(process)
                    remaining = 0.5
                events = selector.select(min(max(remaining, 0.0), 0.25))
                for key, _ in events:
                    chunk = os.read(key.fileobj.fileno(), 65_536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
                        continue
                    if key.data == "stdout":
                        stdout_truncated |= _append_bounded(stdout, chunk, stdout_limit)
                    else:
                        stderr_truncated |= _append_bounded(stderr, chunk, stderr_limit)
                if timed_out and process.poll() is not None and not events:
                    # Once the process is gone, do not wait on a pipe held by a
                    # detached descendant forever.
                    break
        finally:
            selector.close()
            if process.poll() is None:
                self._kill_group(process)
            try:
                process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

        return ProcessResult(
            stdout=bytes(stdout),
            stderr=bytes(stderr),
            exit_code=process.returncode,
            timed_out=timed_out,
            stdout_truncated=stdout_truncated,
            stderr_truncated=stderr_truncated,
        )

    @staticmethod
    def _kill_group(process: subprocess.Popen[bytes]) -> None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            try:
                process.kill()
            except ProcessLookupError:
                pass


def _validate_request(executor: str, model: str, cwd: str, prompt: str) -> str:
    if executor not in ("codex", "claude"):
        raise RequestError("executor must be codex or claude")
    if not model.strip():
        raise RequestError("model must be nonempty or auto")
    if model.startswith("-") or any(character in model for character in "\x00\r\n"):
        raise RequestError("model must be a single provider identifier")
    if not prompt.strip():
        raise RequestError("prompt must be nonempty")
    path = Path(cwd)
    if not path.is_absolute():
        raise RequestError("cwd must be an absolute directory")
    if not path.is_dir():
        raise RequestError("cwd must be an existing directory")
    return str(path)


def build_argv(executor: str, model: str, cwd: str, access: str) -> list[str]:
    if executor not in ("codex", "claude"):
        raise RequestError("executor must be codex or claude")
    if access not in ("read-only", "workspace-write"):
        raise RequestError("access must be read-only or workspace-write")
    if executor == "codex":
        argv = [
            "codex",
            "exec",
            "--ephemeral",
            "--sandbox",
            access,
            "-C",
            cwd,
            "--json",
        ]
        if model != "auto":
            argv.extend(["-m", model])
        argv.append("-")
        return argv
    if access == "read-only":
        argv = [
            "claude",
            "-p",
            "--restricted",
            "--strict-mcp-config",
            "--permission-mode",
            "plan",
            "--output-format",
            "json",
            "--no-session-persistence",
        ]
    else:
        argv = [
            "claude",
            "-p",
            "--restricted",
            "--strict-mcp-config",
            "--permission-mode",
            "acceptEdits",
            "--output-format",
            "json",
            "--no-session-persistence",
        ]
    if model != "auto":
        argv.extend(["--model", model])
    return argv


def _json_lines(raw: bytes) -> list[Mapping[str, Any]]:
    events: list[Mapping[str, Any]] = []
    for line in raw.decode("utf-8", errors="replace").splitlines():
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, Mapping):
            events.append(parsed)
    return events


def _message_text(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        for key in ("text", "content", "message"):
            result = _message_text(value.get(key))
            if result is not None:
                return result
    if isinstance(value, list):
        parts = [_message_text(item) for item in value]
        joined = "".join(part for part in parts if part is not None)
        return joined or None
    return None


def parse_codex(raw: bytes) -> tuple[str | None, dict[str, Any]]:
    events = _json_lines(raw)
    event_types: dict[str, int] = {}
    final_text: str | None = None
    usage: Any = None
    for event in events:
        event_type = event.get("type")
        if isinstance(event_type, str):
            event_types[event_type] = min(event_types.get(event_type, 0) + 1, 999)
        if "usage" in event and usage is None:
            usage = event["usage"]
        item = event.get("item")
        if isinstance(item, Mapping) and item.get("type") in ("agent_message", "message"):
            final_text = _message_text(item) or final_text
        if event_type in ("agent_message", "message", "assistant"):
            final_text = _message_text(event) or final_text
        if event_type == "response.output_text.done":
            final_text = _message_text(event) or final_text
    metadata: dict[str, Any] = {"event_types": _bounded_metadata(event_types)}
    if usage is not None:
        metadata["usage"] = _bounded_metadata(usage)
    return final_text, metadata


def parse_claude(raw: bytes) -> tuple[str | None, dict[str, Any], bool]:
    try:
        parsed = json.loads(raw.decode("utf-8", errors="replace"))
    except json.JSONDecodeError:
        return None, {}, False
    if not isinstance(parsed, Mapping):
        return None, {}, False
    metadata: dict[str, Any] = {}
    for key in ("subtype", "is_error", "session_id", "usage", "duration_ms"):
        if key in parsed:
            metadata[key] = _bounded_metadata(parsed[key])
    result = _message_text(parsed.get("result"))
    return result, metadata, True


def _error(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": _bounded_text(message)}


def dispatch(
    *,
    executor: str,
    model: str,
    cwd: str,
    access: str,
    prompt: str,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    stdout_limit: int = DEFAULT_STDOUT_LIMIT,
    stderr_limit: int = DEFAULT_STDERR_LIMIT,
    runner: ProcessRunner | None = None,
) -> dict[str, Any]:
    try:
        validated_cwd = _validate_request(executor, model, cwd, prompt)
        if not math.isfinite(timeout) or timeout <= 0 or stdout_limit <= 0 or stderr_limit <= 0:
            raise RequestError("timeout and output caps must be positive")
        argv = build_argv(executor, model, validated_cwd, access)
    except RequestError as exc:
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "failed",
            "executor": executor,
            "model": model,
            "exit_code": None,
            "final_text": None,
            "metadata": {},
            "stderr": "",
            "stderr_truncated": False,
            "stdout_truncated": False,
            "error": _error("invalid_request", str(exc)),
        }

    try:
        result = (runner or ProcessRunner()).run(
            argv,
            cwd=validated_cwd,
            stdin=prompt.encode("utf-8"),
            timeout=timeout,
            stdout_limit=stdout_limit,
            stderr_limit=stderr_limit,
        )
    except FileNotFoundError:
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "failed",
            "executor": executor,
            "model": model,
            "exit_code": None,
            "final_text": None,
            "metadata": {},
            "stderr": "",
            "stderr_truncated": False,
            "stdout_truncated": False,
            "error": _error("missing_binary", f"{argv[0]} was not found on PATH"),
        }

    stderr = _redact_prompt(result.stderr.decode("utf-8", errors="replace"), prompt)
    base: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "status": "timed_out" if result.timed_out else ("completed" if result.exit_code == 0 else "failed"),
        "executor": executor,
        "model": model,
        "exit_code": result.exit_code,
        "final_text": None,
        "metadata": {},
        "stderr": stderr,
        "stderr_truncated": result.stderr_truncated,
        "stdout_truncated": result.stdout_truncated,
        "error": None,
    }
    if result.timed_out:
        base["error"] = _error("timeout", f"executor exceeded {timeout:g} seconds")
        return base

    if executor == "codex":
        final_text, metadata = parse_codex(result.stdout)
        parsed = final_text is not None
    else:
        final_text, metadata, parsed = parse_claude(result.stdout)
    base["final_text"] = _redact_prompt(final_text, prompt)
    base["metadata"] = _redact_prompt(metadata, prompt)
    if result.exit_code != 0:
        base["error"] = _error("exit_nonzero", f"executor exited with status {result.exit_code}")
    elif metadata.get("is_error") is True:
        base["status"] = "failed"
        base["error"] = _error("provider_error", "provider reported an error")
    elif not parsed:
        base["status"] = "failed"
        base["error"] = _error("malformed_output", f"{executor} did not emit a parseable result")
    return base


def probe(executor: str, runner: ProcessRunner | None = None) -> dict[str, Any]:
    if executor not in ("codex", "claude"):
        return {"schema_version": SCHEMA_VERSION, "status": "failed", "executor": executor, "error": _error("invalid_request", "executor must be codex or claude")}
    try:
        result = (runner or ProcessRunner()).run(
            [executor, "--version"],
            cwd=os.getcwd(),
            stdin=b"",
            timeout=10,
            stdout_limit=16_384,
            stderr_limit=16_384,
        )
    except FileNotFoundError:
        return {"schema_version": SCHEMA_VERSION, "status": "failed", "executor": executor, "error": _error("missing_binary", f"{executor} was not found on PATH")}
    output = result.stdout.decode("utf-8", errors="replace").strip()
    if result.exit_code != 0:
        return {"schema_version": SCHEMA_VERSION, "status": "failed", "executor": executor, "exit_code": result.exit_code, "version": output or None, "stderr": result.stderr.decode("utf-8", errors="replace"), "error": _error("exit_nonzero", f"executor exited with status {result.exit_code}")}
    return {"schema_version": SCHEMA_VERSION, "status": "available", "executor": executor, "exit_code": 0, "version": _bounded_text(output), "stderr": ""}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    plan = subparsers.add_parser("plan", help="print the resolved argv without executing it")
    probe_parser = subparsers.add_parser("probe", help="check one executor binary")
    run = subparsers.add_parser("run", help="execute a prompt and print one JSON result")
    for command in (plan, run):
        command.add_argument("--executor", choices=("codex", "claude"), required=True)
        command.add_argument("--model", default="auto")
    plan.add_argument("--cwd", required=True)
    plan.add_argument("--access", choices=("read-only", "workspace-write"), default="read-only")
    probe_parser.add_argument("--executor", choices=("codex", "claude"), required=True)
    run.add_argument("--cwd", required=True)
    run.add_argument("--access", choices=("read-only", "workspace-write"), default="read-only")
    run.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    run.add_argument("--stdout-limit", type=int, default=DEFAULT_STDOUT_LIMIT)
    run.add_argument("--stderr-limit", type=int, default=DEFAULT_STDERR_LIMIT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "probe":
        result = probe(args.executor)
    elif args.command == "plan":
        try:
            cwd = _validate_request(args.executor, args.model, args.cwd, "plan")
            result = {"schema_version": SCHEMA_VERSION, "status": "planned", "executor": args.executor, "model": args.model, "access": args.access, "cwd": cwd, "argv": build_argv(args.executor, args.model, cwd, args.access)}
        except RequestError as exc:
            result = {"schema_version": SCHEMA_VERSION, "status": "failed", "executor": args.executor, "model": args.model, "error": _error("invalid_request", str(exc))}
    else:
        result = dispatch(executor=args.executor, model=args.model, cwd=args.cwd, access=args.access, prompt=sys.stdin.read(), timeout=args.timeout, stdout_limit=args.stdout_limit, stderr_limit=args.stderr_limit)
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0 if result.get("status") in ("available", "planned", "completed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
