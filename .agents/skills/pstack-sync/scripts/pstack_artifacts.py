from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import uuid
from pathlib import Path, PurePosixPath


class ArtifactError(RuntimeError):
    pass


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "--literal-pathspecs", "-C", str(repo), *args], capture_output=True)
    if result.returncode:
        raise ArtifactError(result.stderr.decode(errors="replace").strip())
    return result.stdout


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise ArtifactError(f"cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise ArtifactError(f"expected an object in {path}")
    return value


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def range_changes(cache: Path, base: str, head: str, prefix: str) -> list[dict]:
    for commit in (base, head):
        if not re.fullmatch(r"[0-9a-f]{40,64}", commit):
            raise ArtifactError("review commits must be full object IDs")
    parts = git(cache, "diff", "--name-status", "--no-renames", "-z", base, head,
                "--", prefix).decode().split("\0")[:-1]
    return [{"status": parts[i], "path": parts[i + 1]} for i in range(0, len(parts), 2)]


def blob(cache: Path, commit: str, path: str) -> tuple[str | None, bytes]:
    tree = git(cache, "ls-tree", "-z", commit, "--", path)
    if not tree:
        return None, b""
    metadata, actual = tree.rstrip(b"\0").split(b"\t", 1)
    mode, kind, oid = metadata.decode().split()
    if actual.decode() != path or kind != "blob":
        raise ArtifactError(f"expected a file at {path}")
    return mode, git(cache, "cat-file", "blob", oid)


def save_review(root: Path, cache: Path, pending: dict) -> Path:
    base, head, prefix = (pending[k] for k in ("base_commit", "head_commit", "upstream_path"))
    changes = range_changes(cache, base, head, prefix)
    review = root / ".bstack/pstack-sync/reviews" / f"{base}-{head}"
    if review.exists():
        saved = read_json(review / "range.json")
        if any(saved.get(k) != pending[k] for k in ("base_commit", "head_commit", "upstream_path", "upstream_url", "upstream_branch")):
            raise ArtifactError(f"review metadata differs at {review}")
        return review
    review.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=review.parent) as temporary:
        draft = Path(temporary) / "review"
        draft.mkdir()
        entries = []
        for index, change in enumerate(changes):
            source = change["path"]
            directory = draft / "files" / f"{index:04d}"
            directory.mkdir(parents=True)
            for label, commit in (("base", base), ("upstream", head)):
                _, content = blob(cache, commit, source)
                (directory / label).write_bytes(content)
            (directory / "change.diff").write_bytes(git(cache, "diff", "--no-ext-diff", "--no-textconv",
                                                       base, head, "--", source))
            relative = PurePosixPath(source).relative_to(prefix).as_posix()
            entries.append({**change, "disposition": "pending", "reason": "",
                            "target": relative if relative.startswith("skills/") else None,
                            "artifacts": f"files/{index:04d}"})
        write_json(draft / "range.json", pending)
        write_json(draft / "dispositions.json", {"base_commit": base, "head_commit": head, "entries": entries})
        draft.rename(review)
    return review


def coverage(cache: Path, review: Path) -> tuple[dict, list[dict]]:
    snapshot = read_json(review / "range.json")
    manifest = read_json(review / "dispositions.json")
    for key in ("base_commit", "head_commit"):
        if manifest.get(key) != snapshot.get(key):
            raise ArtifactError(f"manifest {key} does not match the inspected range")
    expected = {r["path"]: r["status"] for r in range_changes(cache, snapshot["base_commit"],
                snapshot["head_commit"], snapshot["upstream_path"])}
    entries = manifest.get("entries")
    if not isinstance(entries, list) or any(not isinstance(e, dict) for e in entries):
        raise ArtifactError("manifest entries must be a list of objects")
    paths = [e.get("path") for e in entries]
    if any(not isinstance(p, str) for p in paths) or len(set(paths)) != len(paths):
        raise ArtifactError("manifest has invalid or duplicate paths")
    if set(paths) != set(expected):
        raise ArtifactError(f"manifest coverage differs: missing={sorted(set(expected) - set(paths))}, "
                            f"extra={sorted(set(paths) - set(expected))}")
    for entry in entries:
        if entry.get("status") != expected[entry["path"]]:
            raise ArtifactError(f"changed status for {entry['path']}")
        if not isinstance(entry.get("disposition"), str) or entry["disposition"] not in {"port", "adapt", "covered", "skip"}:
            raise ArtifactError(f"unreviewed disposition for {entry['path']}")
    return snapshot, entries


def safe_target(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ArtifactError("target must be a repository-relative file path")
    parts = relative.split("/")
    if any(part in {"", ".", "..", ".git", ".bstack"} for part in parts):
        raise ArtifactError(f"unsafe target: {relative}")
    current = root
    for part in parts:
        current = current / part
        if current.is_symlink():
            raise ArtifactError(f"symlink in target: {relative}")
    if current.exists() and not current.is_file():
        raise ArtifactError(f"target is not a regular file: {relative}")
    return current


def fingerprint(path: Path) -> dict:
    if not path.exists():
        return {"sha256": None, "mode": None}
    return {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "mode": path.stat().st_mode & 0o777}


def conflict_markers(content: bytes) -> bool:
    return bool(re.search(rb"(?m)^(?:<{7}|\|{7}|={7}|>{7})(?: |$)", content))


def preview(root: Path, cache: Path, review: Path) -> Path:
    snapshot, entries = coverage(cache, review)
    preview_dir = review / "previews" / uuid.uuid4().hex
    preview_dir.mkdir(parents=True)
    plan = {"repository": str(root.resolve()), "range": snapshot, "entries": []}
    targets = set()
    for index, entry in enumerate(entries):
        if entry["disposition"] not in {"port", "adapt"}:
            continue
        source, target = entry["path"], entry.get("target")
        item = {"source": source, "target": target}
        if target is None:
            plan["entries"].append({**item, "status": "manual", "reason": "choose a target or adapt manually"})
            continue
        destination = safe_target(root, target)
        if target in targets:
            raise ArtifactError(f"multiple upstream paths target {target}; combine them manually")
        targets.add(target)
        base_mode, base = blob(cache, snapshot["base_commit"], source)
        upstream_mode, upstream = blob(cache, snapshot["head_commit"], source)
        if upstream_mode is None:
            plan["entries"].append({**item, "status": "deletion", "reason": "inspect and migrate callers before deleting manually"})
            continue
        if upstream_mode not in {"100644", "100755"} or base_mode not in {None, "100644", "100755"}:
            plan["entries"].append({**item, "status": "manual", "reason": "non-regular upstream file"})
            continue
        original = fingerprint(destination)
        local = destination.read_bytes() if original["sha256"] is not None else b""
        if b"\0" in base + upstream + local:
            plan["entries"].append({**item, "status": "manual", "reason": "binary content"})
            continue
        if original["sha256"] is None and base_mode is not None:
            plan["entries"].append({**item, "status": "manual", "reason": "local file is absent; decide whether to restore or remap it"})
            continue
        with tempfile.TemporaryDirectory(dir=preview_dir) as temporary:
            inputs = []
            for name, content in (("local", local), ("base", base), ("upstream", upstream)):
                path = Path(temporary) / name
                path.write_bytes(content)
                inputs.append(str(path))
            result = subprocess.run(["git", "merge-file", "-p", "--diff3", "-L", "bstack", "-L", "base",
                                     "-L", "upstream", *inputs], capture_output=True)
        if result.returncode < 0 or result.returncode > 127:
            raise ArtifactError(result.stderr.decode(errors="replace") or f"merge failed for {source}")
        candidate = f"candidate-{index:04d}"
        (preview_dir / candidate).write_bytes(result.stdout)
        plan["entries"].append({**item, "status": "conflict" if result.returncode else "ready",
                                "candidate": candidate, "original": original,
                                "mode": original["mode"] if original["mode"] is not None else int(upstream_mode[-3:], 8)})
    write_json(preview_dir / "plan.json", plan)
    return preview_dir


def apply_preview(root: Path, preview_dir: Path, selected: list[str]) -> dict:
    plan = read_json(preview_dir / "plan.json")
    if plan.get("repository") != str(root.resolve()):
        raise ArtifactError("preview belongs to another repository")
    if not selected or len(set(selected)) != len(selected):
        raise ArtifactError("select each reviewed target once with --path")
    items = {e["target"]: e for e in plan["entries"] if e.get("candidate")}
    if set(selected) - set(items):
        raise ArtifactError(f"no candidate for: {sorted(set(selected) - set(items))}")
    prepared = []
    for target in selected:
        item = items[target]
        destination = safe_target(root, target)
        candidate = item["candidate"]
        if not isinstance(candidate, str) or not re.fullmatch(r"candidate-[0-9]+", candidate):
            raise ArtifactError("invalid candidate filename")
        candidate_path = preview_dir / candidate
        if candidate_path.is_symlink():
            raise ArtifactError("candidate must not be a symlink")
        content = candidate_path.read_bytes()
        if conflict_markers(content):
            raise ArtifactError(f"resolve conflict markers in {candidate} before applying {target}")
        desired = {"sha256": hashlib.sha256(content).hexdigest(), "mode": item["mode"]}
        current = fingerprint(destination)
        if current != desired and current != item["original"]:
            raise ArtifactError(f"{target} changed since preview; make a new preview")
        prepared.append((target, destination, content, current, desired))
    applied, unchanged = [], []
    for target, destination, content, original, desired in prepared:
        safe_target(root, target)
        if fingerprint(destination) != original:
            raise ArtifactError(f"{target} changed during apply; already applied: {applied}")
        if original == desired:
            unchanged.append(target)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        fd, name = tempfile.mkstemp(prefix=".pstack-", dir=destination.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(content)
                os.fchmod(stream.fileno(), desired["mode"])
            os.replace(name, destination)
        finally:
            if os.path.exists(name):
                os.unlink(name)
        applied.append(target)
    return {"applied": applied, "already_applied": unchanged}
