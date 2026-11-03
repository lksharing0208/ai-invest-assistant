#!/usr/bin/env python3
"""Validate finance project manifests/configuration with PyYAML."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        import yaml
    except ImportError:
        print("ERROR: install development dependencies: pip install -r requirements-dev.txt")
        return 2

    required = [
        "agent/manifest.yaml",
        "config/skill-routing.yaml",
        "config/market-universe.yaml",
        "config/strategy-config.yaml",
        "config/screening-config.yaml",
        "config/risk-config.yaml",
        "config/performance-metrics.yaml",
        "policies/financial-safety.yaml",
        "policies/data-quality.yaml",
        "policies/user-data-isolation.yaml",
    ]
    errors: list[str] = []
    for relative in required:
        path = ROOT / relative
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                errors.append(f"{relative}: YAML root must be a mapping")
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            errors.append(f"{relative}: {exc}")

    plugin_path = ROOT / "adapters/chatgpt/plugin.json"
    try:
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        if plugin.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            errors.append("adapters/chatgpt/plugin.json: invalid Agent Plugins schema")
        if plugin.get("name") != "ai-invest-assistant":
            errors.append("adapters/chatgpt/plugin.json: invalid plugin name")
        interface = plugin.get("extensions", {}).get("com.openai", {}).get("interface", {})
        if interface.get("displayName") != "AI 金融助手":
            errors.append("adapters/chatgpt/plugin.json: invalid displayName")
        if len(interface.get("shortDescription", "")) > 30:
            errors.append("adapters/chatgpt/plugin.json: shortDescription exceeds 30 characters")
        if set(plugin) & {"skills", "mcpServers", "apps", "interface"}:
            errors.append("adapters/chatgpt/plugin.json: unsupported portable top-level field")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"adapters/chatgpt/plugin.json: {exc}")

    if errors:
        print("Finance configuration validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Finance configuration validation passed: {len(required)} YAML files and plugin manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
