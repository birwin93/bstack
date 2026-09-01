#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_KEYS = {
    "name",
    "description",
    "license",
    "metadata",
    "allowed-tools",
}
FORBIDDEN = {
    "Cursor Task API": re.compile(r"\bTask\b"),
    "Cursor question API": re.compile(r"\bAskQuestion\b"),
    "Cursor subagent field": re.compile(r"subagent_type"),
    "Cursor background field": re.compile(r"run_in_background"),
    "Cursor home path": re.compile(r"~/\.cursor|\.cursor/"),
    "Cursor transcript path": re.compile(r"agent-transcripts"),
    "Cursor team kit": re.compile(r"cursor-team-kit"),
    "hardcoded Grok model": re.compile(r"grok-4\.6"),
    "hardcoded Claude model": re.compile(r"claude-(?:fable|opus)"),
    "hardcoded OpenAI model": re.compile(r"gpt-5\.6-sol-max"),
}
REMOVED_RUNTIME = {
    "removed bstack executor wrapper": re.compile(r"\bbstack_exec(?:\.py)?\b"),
}


def frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}, ["missing opening frontmatter delimiter"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, ["missing closing frontmatter delimiter"]

    values: dict[str, str] = {}
    errors: list[str] = []
    for line in lines[1:end]:
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key] = value.strip().strip('"')
        if key not in ALLOWED_KEYS:
            errors.append(f"unsupported frontmatter key {key!r}")
    return values, errors


def validate_skill(path: Path) -> list[str]:
    values, errors = frontmatter(path)
    directory_name = path.parent.name
    name = values.get("name", "")
    description = values.get("description", "")

    if not name:
        errors.append("missing name")
    elif not NAME_RE.fullmatch(name):
        errors.append(f"invalid name {name!r}")
    elif name != directory_name:
        errors.append(f"name {name!r} does not match directory {directory_name!r}")

    if not description:
        errors.append("missing description")
    elif len(description) > 1024:
        errors.append("description exceeds 1024 characters")

    return errors


def validate_portability(path: Path) -> list[str]:
    if "references/adapters" in path.as_posix():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    return [label for label, pattern in FORBIDDEN.items() if pattern.search(text)]


def is_vendored(path: Path) -> bool:
    return any(part in {"node_modules", ".git"} for part in path.parts)


def main() -> int:
    failures: list[str] = []
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    if not skill_files:
        failures.append("no skills found")

    for skill_file in skill_files:
        for error in validate_skill(skill_file):
            failures.append(f"{skill_file.relative_to(ROOT)}: {error}")

    for path in sorted(SKILLS.rglob("*")):
        if (
            path.is_file()
            and not is_vendored(path)
            and path.suffix in {".md", ".ts", ".mjs", ".sh"}
        ):
            for error in validate_portability(path):
                failures.append(f"{path.relative_to(ROOT)}: {error}")
            text = path.read_text(encoding="utf-8", errors="replace")
            for label, pattern in REMOVED_RUNTIME.items():
                if pattern.search(text):
                    failures.append(f"{path.relative_to(ROOT)}: {label}")

    if failures:
        print("bstack validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"bstack validation passed for {len(skill_files)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
