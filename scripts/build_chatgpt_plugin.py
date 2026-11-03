#!/usr/bin/env python3
"""Build one ChatGPT Plugin ZIP from the unified Agent source and all Finance Skills."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
ADAPTER_DIR = ROOT / "adapters" / "chatgpt"


def run_validation() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/validate_skills.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/validate_finance_config.py")], cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    try:
        run_validation()
        manifest = json.loads((ADAPTER_DIR / "plugin.json").read_text(encoding="utf-8"))
        version = manifest["version"]
        output = (args.output or ROOT / "dist" / f"ai-invest-assistant-chatgpt-v{version}.zip").resolve()
        output.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(prefix="ai-invest-assistant-") as temporary:
            package = Path(temporary) / "package"
            package.mkdir()
            shutil.copy2(ADAPTER_DIR / "plugin.json", package / "plugin.json")
            (package / "agents").mkdir(parents=True, exist_ok=True)
            shutil.copy2(ADAPTER_DIR / "agents/openai.yaml", package / "agents/openai.yaml")
            shutil.copy2(ADAPTER_DIR / "README.md", package / "README.md")

            target_skills = package / "skills"
            target_skills.mkdir()
            skill_count = 0
            for source in sorted(SKILLS_DIR.iterdir()):
                if source.is_dir() and (source / "SKILL.md").is_file():
                    shutil.copytree(source, target_skills / source.name,
                                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", ".git"))
                    skill_count += 1

            if skill_count != 16:
                raise RuntimeError(f"expected 16 Skills, found {skill_count}")

            main_references = target_skills / "ai-invest-workflow/references"
            main_references.mkdir(parents=True, exist_ok=True)
            for directory in ["agent", "config", "policies", "references", "docs"]:
                shutil.copytree(ROOT / directory, main_references / directory)

            template_target = target_skills / "ai-invest-workflow/assets/templates"
            template_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(ROOT / "templates", template_target)

            with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                for path in sorted(package.rglob("*")):
                    if path.is_file():
                        archive.write(path, path.relative_to(package).as_posix())

        with zipfile.ZipFile(output, "r") as archive:
            if archive.testzip():
                raise RuntimeError("ZIP integrity check failed")
            names = set(archive.namelist())
            required = {"plugin.json", "agents/openai.yaml", "skills/ai-invest-workflow/SKILL.md"}
            if not required.issubset(names):
                raise RuntimeError(f"ZIP is missing required root entries: {sorted(required - names)}")
            skill_entries = {name.split("/")[1] for name in names if name.startswith("skills/") and name.endswith("/SKILL.md")}
            if len(skill_entries) != 16:
                raise RuntimeError(f"ZIP contains {len(skill_entries)} Skills instead of 16")
            if any(name.startswith("ai-invest-assistant/") for name in names):
                raise RuntimeError("ZIP must not include an extra enclosing directory")

        print(f"Built plugin: {manifest['extensions']['com.openai']['interface']['displayName']}")
        print(f"Version: {version}; Skills: {skill_count}; ZIP: {output}")
        return 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
