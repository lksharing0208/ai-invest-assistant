#!/usr/bin/env python3
"""Validate Skill directories and required SKILL.md front matter using stdlib."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
EXPECTED_SKILLS = {
    "ai-invest-workflow", "intent-router", "market-data", "macro-analysis",
    "market-analysis", "industry-analysis", "stock-research", "stock-screening",
    "strategy-analysis", "fund-etf-analysis", "portfolio-management",
    "risk-management", "trading-plan", "trade-journal", "performance-analysis",
    "investment-report",
}


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("front matter is not closed")
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = FIELD_RE.match(line)
        if match:
            key, value = match.groups()
            values[key] = value.strip().strip("\"'")
    return values


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print("ERROR: skills/ directory not found")
        return 2

    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    found = {path.parent.name for path in skill_files}
    errors: list[str] = []

    missing = EXPECTED_SKILLS - found
    extra = found - EXPECTED_SKILLS
    if missing:
        errors.append(f"missing expected Skills: {sorted(missing)}")
    if extra:
        errors.append(f"unexpected Skill directories: {sorted(extra)}")

    seen: set[str] = set()
    for path in skill_files:
        folder = path.parent.name
        try:
            metadata = parse_front_matter(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if not NAME_RE.fullmatch(folder):
            errors.append(f"{path.relative_to(ROOT)}: invalid folder name")
        if name != folder:
            errors.append(f"{path.relative_to(ROOT)}: name does not match folder")
        if not description:
            errors.append(f"{path.relative_to(ROOT)}: empty description")
        if name in seen:
            errors.append(f"{path.relative_to(ROOT)}: duplicate Skill name {name}")
        seen.add(name)

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Skill validation passed: {len(skill_files)} Skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
