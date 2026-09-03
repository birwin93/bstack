#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
STATE_PATH = SKILL_DIR / "state.json"


class SyncError(RuntimeError):
    pass


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise SyncError(f"git {' '.join(args)} failed: {detail}")
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise SyncError(f"missing {path}") from error
    except json.JSONDecodeError as error:
        raise SyncError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise SyncError(f"expected an object in {path}")
    return value


def require_string(state: dict[str, Any], key: str) -> str:
    value = state.get(key)
    if not isinstance(value, str) or not value:
        raise SyncError(f"state field {key!r} must be a non-empty string")
    return value


def repository_root(candidate: str) -> Path:
    root = Path(candidate).resolve()
    result = run_git(root, "rev-parse", "--show-toplevel")
    actual = Path(result.stdout.strip()).resolve()
    if actual != root:
        raise SyncError(f"run from repository root {actual}")
    if not (root / "skills" / "poteto-mode" / "SKILL.md").is_file():
        raise SyncError(f"{root} does not look like the bstack repository")
    return root


def cache_repository(root: Path, upstream_url: str, branch: str) -> Path:
    cache = root / ".bstack" / "pstack-sync" / "upstream"
    if cache.exists() and not (cache / ".git").is_dir():
        raise SyncError(f"cache path exists but is not a git repository: {cache}")

    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                "--branch",
                branch,
                upstream_url,
                str(cache),
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise SyncError(f"git clone failed: {detail}")
    else:
        cached_url = run_git(cache, "remote", "get-url", "origin").stdout.strip()
        if cached_url != upstream_url:
            raise SyncError(
                f"cache origin is {cached_url!r}, expected {upstream_url!r}; "
                "move the cache aside and retry"
            )

    run_git(
        cache,
        "fetch",
        "--prune",
        "origin",
        f"+refs/heads/{branch}:refs/remotes/origin/{branch}",
    )
    return cache


def ensure_commit(cache: Path, commit: str) -> None:
    exists = run_git(cache, "cat-file", "-e", f"{commit}^{{commit}}", check=False)
    if exists.returncode == 0:
        return
    run_git(cache, "fetch", "origin", commit)
    exists = run_git(cache, "cat-file", "-e", f"{commit}^{{commit}}", check=False)
    if exists.returncode != 0:
        raise SyncError(f"saved upstream commit is unavailable: {commit}")


def inspect(root: Path) -> None:
    state = load_json(STATE_PATH)
    upstream_url = require_string(state, "upstream_url")
    branch = require_string(state, "upstream_branch")
    upstream_path = require_string(state, "upstream_path")
    base = require_string(state, "last_checked_commit")

    cache = cache_repository(root, upstream_url, branch)
    ensure_commit(cache, base)
    head = run_git(cache, "rev-parse", f"refs/remotes/origin/{branch}").stdout.strip()

    ancestor = run_git(cache, "merge-base", "--is-ancestor", base, head, check=False)
    if ancestor.returncode != 0:
        raise SyncError(
            f"saved commit {base} is not an ancestor of upstream {branch} at {head}"
        )

    observed_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )
    commit_lines = run_git(
        cache,
        "log",
        "--reverse",
        "--format=%H%x09%aI%x09%s",
        f"{base}..{head}",
        "--",
        upstream_path,
    ).stdout.splitlines()
    changed_lines = run_git(
        cache,
        "diff",
        "--name-status",
        "--find-renames",
        f"{base}..{head}",
        "--",
        upstream_path,
    ).stdout.splitlines()
    diff_stat = run_git(
        cache,
        "diff",
        "--stat",
        f"{base}..{head}",
        "--",
        upstream_path,
    ).stdout.rstrip()

    pending = {
        "base_commit": base,
        "head_commit": head,
        "observed_at": observed_at,
        "upstream_url": upstream_url,
        "upstream_branch": branch,
        "upstream_path": upstream_path,
    }
    pending_path = root / ".bstack" / "pstack-sync" / "pending.json"
    pending_path.parent.mkdir(parents=True, exist_ok=True)
    pending_path.write_text(json.dumps(pending, indent=2) + "\n", encoding="utf-8")

    report = {
        **pending,
        "previous_check_at": state.get("last_checked_at"),
        "cache_path": str(cache),
        "pending_path": str(pending_path),
        "commits_touching_pstack": commit_lines,
        "changed_files": changed_lines,
        "diff_stat": diff_stat,
    }
    print(json.dumps(report, indent=2))


def mark(root: Path) -> None:
    state = load_json(STATE_PATH)
    pending_path = root / ".bstack" / "pstack-sync" / "pending.json"
    pending = load_json(pending_path)

    current = require_string(state, "last_checked_commit")
    base = require_string(pending, "base_commit")
    head = require_string(pending, "head_commit")
    for key in ("upstream_url", "upstream_branch", "upstream_path"):
        if state.get(key) != pending.get(key):
            raise SyncError(f"pending {key} no longer matches state; inspect again")
    if current != base:
        raise SyncError(
            f"state moved from pending base {base} to {current}; inspect again"
        )

    state["last_checked_commit"] = head
    state["last_checked_at"] = datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    ).replace("+00:00", "Z")
    temporary = STATE_PATH.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE_PATH)
    pending_path.unlink()
    print(
        json.dumps(
            {
                "last_checked_commit": state["last_checked_commit"],
                "last_checked_at": state["last_checked_at"],
            },
            indent=2,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect and mark the upstream pstack review cursor."
    )
    parser.add_argument(
        "command",
        choices=("inspect", "mark"),
        help="inspect upstream without moving the cursor, or mark the pending range reviewed",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="bstack repository root, defaults to the current directory",
    )
    args = parser.parse_args()

    try:
        root = repository_root(args.repo_root)
        if args.command == "inspect":
            inspect(root)
        else:
            mark(root)
    except SyncError as error:
        print(f"pstack-sync: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
