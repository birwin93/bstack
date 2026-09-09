#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import posixpath
import re
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


def git(root: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True).stdout


def prose_and_blocks(text: str) -> tuple[list[tuple[int, str]], list[str]]:
    prose, blocks = [], []
    fence = None
    block = []
    frontmatter = text.startswith("---\n")
    for number, line in enumerate(text.splitlines(), 1):
        if frontmatter:
            if number > 1 and line == "---":
                frontmatter = False
            continue
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            block.append(line)
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                blocks.append("\n".join(block))
                block, fence = [], None
        elif match:
            fence, block = match[1], [line]
        elif not line.startswith(("    ", "\t")):
            prose.append((number, re.sub(r"(`+).*?\1", "", line)))
    if block:
        blocks.append("\n".join(block))
    return prose, blocks


def destinations(line: str) -> list[str]:
    result = []
    definition = re.match(r"^ {0,3}\[[^\]]+\]:\s*(.*)", line)
    starts = [m.end() for m in re.finditer(r"\]\(", line)]
    fragments = [line[start:] for start in starts]
    if definition:
        fragments.append(definition[1])
    for fragment in fragments:
        fragment = fragment.lstrip()
        if fragment.startswith("<"):
            if ">" in fragment:
                result.append(fragment[1:fragment.index(">")])
            continue
        depth, chars, escaped = 0, [], False
        for char in fragment:
            if escaped:
                chars.append(char)
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == "(":
                depth += 1
                chars.append(char)
            elif char == ")":
                if depth == 0:
                    break
                depth -= 1
                chars.append(char)
            elif char.isspace() and depth == 0:
                break
            else:
                chars.append(char)
        if chars:
            result.append("".join(chars))
    return result


def local_path(source: str, destination: str) -> str | None:
    try:
        parsed = urlsplit(destination)
    except ValueError:
        return None
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = unquote(parsed.path)
    if path.startswith("/"):
        return path.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(source), path))


def findings(documents: dict[str, str], exists) -> tuple[dict, dict]:
    errors, warnings = {}, {}
    for source, text in documents.items():
        prose, _ = prose_and_blocks(text)
        stack = []
        headings = Counter()
        for number, line in prose:
            if re.match(r"^(?:<{7}|\|{7}|={7}|>{7})(?: |$)", line):
                key = ("conflict", source, line)
                errors[key] = f"{source}:{number}: unresolved conflict marker"
            heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
            if heading:
                level, title = len(heading[1]), heading[2].strip().lower()
                while stack and stack[-1][0] >= level:
                    stack.pop()
                key = (source, tuple(stack), level, title)
                headings[key] += 1
                if headings[key] > 1:
                    warnings[(*key, headings[key])] = f"{source}:{number}: repeated heading {heading[2]!r} under the same parent; check for duplicated workflow steps"
                stack.append((level, title))
            for destination in destinations(line):
                target = local_path(source, destination)
                if target is not None and not exists(target):
                    key = ("link", source, destination)
                    errors[key] = f"{source}:{number}: broken local link {destination!r}"
    return errors, warnings


def check_markdown(root: Path, base: str = "HEAD") -> dict:
    commit = git(root, "rev-parse", "--verify", f"{base}^{{commit}}").decode().strip()
    old_paths = set(git(root, "ls-tree", "-r", "--name-only", "-z", commit).decode().split("\0")[:-1])
    paths = set(git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z").decode().split("\0")[:-1])
    old_docs = {p: git(root, "show", f"{commit}:{p}").decode(errors="replace") for p in old_paths if p.endswith(".md")}
    new_docs = {p: (root / p).read_text(errors="replace") for p in paths
                if p.endswith(".md") and (root / p).is_file() and not (root / p).is_symlink()}
    old_entries = old_paths | {str(parent) for p in old_paths for parent in Path(p).parents}
    old_errors, old_warnings = findings(old_docs, lambda p: p in old_entries)
    errors, warnings = findings(new_docs, lambda p: (root / p).exists())
    changed_blocks = [p for p in sorted(old_docs.keys() & new_docs.keys())
                      if prose_and_blocks(old_docs[p])[1] != prose_and_blocks(new_docs[p])[1]]
    return {"base_commit": commit, "markdown_files_checked": len(new_docs),
            "errors": [v for k, v in errors.items() if k not in old_errors],
            "warnings": [v for k, v in warnings.items() if k not in old_warnings],
            "existing_errors": len(errors.keys() & old_errors.keys()),
            "code_blocks_changed": changed_blocks}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Markdown regressions against a Git base; code changes and duplicate headings are review notices.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--base", default="HEAD")
    args = parser.parse_args()
    try:
        report = check_markdown(args.repo_root.resolve(), args.base)
    except (OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Markdown check failed: {error}\n")
    print(json.dumps(report, indent=2))
    return int(bool(report["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
