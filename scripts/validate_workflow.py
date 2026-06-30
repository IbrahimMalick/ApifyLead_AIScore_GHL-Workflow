#!/usr/bin/env python3
"""Validate the n8n workflow JSON and scan the repo for leaked secrets.

Usage:
    python3 scripts/validate_workflow.py

Exit code 0 = all checks passed, 1 = a problem was found.
Used by CI (.github/workflows/validate.yml) and safe to run locally before commits.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_DIR = ROOT / "workflows"

# Patterns for credentials that must never be committed.
SECRET_PATTERNS = {
    "Apify API token": r"apify_api_[A-Za-z0-9]{20,}",
    "GHL private token": r"pit-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}",
    "OpenAI key": r"sk-[A-Za-z0-9]{20,}",
    "Google OAuth secret": r"GOCSPX-[A-Za-z0-9_-]{10,}",
}

# Placeholder substrings that are allowed to match the patterns above.
ALLOWED_PLACEHOLDERS = ("xxxx", "your_", "your-", "example")

# Files scanned for secrets (text files only).
SCAN_GLOBS = ("*.json", "*.md", "*.example", "*.yml", "*.yaml")


def fail(msg: str) -> None:
    print(f"  ✗ {msg}")


def validate_workflows() -> bool:
    ok = True
    files = sorted(WORKFLOW_DIR.glob("*.json")) if WORKFLOW_DIR.exists() else []
    if not files:
        fail("no workflow JSON files found under workflows/")
        return False

    for f in files:
        rel = f.relative_to(ROOT)
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(f"{rel}: invalid JSON — {e}")
            ok = False
            continue

        nodes = data.get("nodes")
        if not isinstance(nodes, list) or not nodes:
            fail(f"{rel}: missing or empty 'nodes' array")
            ok = False
            continue
        if "connections" not in data:
            fail(f"{rel}: missing 'connections' object")
            ok = False
            continue

        names = [n.get("name") for n in nodes]
        for n in nodes:
            for key in ("name", "type", "id"):
                if not n.get(key):
                    fail(f"{rel}: a node is missing required field '{key}'")
                    ok = False
        # Connections must reference real nodes.
        for src, conn in data.get("connections", {}).items():
            if src not in names:
                fail(f"{rel}: connection source '{src}' is not a known node")
                ok = False

        if ok:
            print(f"  ✓ {rel}: valid JSON, {len(nodes)} nodes, "
                  f"{len(data.get('connections', {}))} connection groups")
    return ok


def scan_secrets() -> bool:
    ok = True
    for pattern_glob in SCAN_GLOBS:
        for f in ROOT.rglob(pattern_glob):
            if ".git" in f.parts:
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for label, pattern in SECRET_PATTERNS.items():
                for m in re.finditer(pattern, text):
                    hit = m.group(0)
                    if any(p in hit.lower() for p in ALLOWED_PLACEHOLDERS):
                        continue
                    fail(f"{f.relative_to(ROOT)}: possible {label} → {hit[:18]}…")
                    ok = False
    if ok:
        print("  ✓ no leaked secrets detected")
    return ok


def main() -> int:
    print("Validating workflow JSON…")
    a = validate_workflows()
    print("Scanning for secrets…")
    b = scan_secrets()
    if a and b:
        print("\nAll checks passed ✅")
        return 0
    print("\nChecks FAILED ❌")
    return 1


if __name__ == "__main__":
    sys.exit(main())
