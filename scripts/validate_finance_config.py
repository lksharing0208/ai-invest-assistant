#!/usr/bin/env python3
"""Validate finance project manifests/configuration with PyYAML."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_mapping(relative: str, yaml_module, errors: list[str]) -> dict:
    path = ROOT / relative
    try:
        value = yaml_module.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            errors.append(f"{relative}: YAML root must be a mapping")
            return {}
        return value
    except (OSError, UnicodeError, yaml_module.YAMLError) as exc:
        errors.append(f"{relative}: {exc}")
        return {}


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
        "config/data-source-registry.yaml",
        "config/indicator-catalog.yaml",
        "config/strategy-config.yaml",
        "config/screening-config.yaml",
        "config/risk-config.yaml",
        "config/performance-metrics.yaml",
        "policies/financial-safety.yaml",
        "policies/data-quality.yaml",
        "policies/user-data-isolation.yaml",
        "tests/skill-routing-cases.yaml",
        "adapters/chatgpt/agents/openai.yaml",
    ]
    errors: list[str] = []
    loaded = {relative: load_mapping(relative, yaml, errors) for relative in required}

    routing_cases = loaded.get("tests/skill-routing-cases.yaml", {}).get("cases", [])
    if not isinstance(routing_cases, list) or not routing_cases:
        errors.append("tests/skill-routing-cases.yaml: cases must be a non-empty list")
    else:
        seen_ids: set[str] = set()
        for index, case in enumerate(routing_cases):
            if not isinstance(case, dict):
                errors.append(f"routing case #{index + 1}: must be a mapping")
                continue
            case_id = case.get("id")
            if not isinstance(case_id, str) or not case_id:
                errors.append(f"routing case #{index + 1}: missing id")
            elif case_id in seen_ids:
                errors.append(f"routing case #{index + 1}: duplicate id {case_id}")
            seen_ids.add(case_id)
            if not isinstance(case.get("input"), str) or not case["input"].strip():
                errors.append(f"routing case {case_id}: missing input")
            if case.get("level") not in {"S0", "S1", "S2", "S3"}:
                errors.append(f"routing case {case_id}: invalid task level")
            if "auxiliary" not in case or not isinstance(case["auxiliary"], list):
                errors.append(f"routing case {case_id}: auxiliary must be a list")

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
        if not isinstance(interface.get("capabilities"), list):
            errors.append("adapters/chatgpt/plugin.json: capabilities must be an array")
        if set(plugin) & {"skills", "mcpServers", "apps", "interface"}:
            errors.append("adapters/chatgpt/plugin.json: unsupported portable top-level field")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"adapters/chatgpt/plugin.json: {exc}")

    if errors:
        print("Finance configuration validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Finance configuration validation passed: {len(required)} YAML files, {len(routing_cases)} routing cases and plugin manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
