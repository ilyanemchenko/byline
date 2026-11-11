from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
         ".codex-plugin/plugin.json", ".agents/plugins/marketplace.json"]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_claude_plugin_manifest():
    m = load(FILES[0])
    assert (m["name"], m["version"], m["license"]) == ("byline", "0.1.0", "Apache-2.0")
    assert m["author"]["name"] == "Ilya Nemchenko"
    assert m["repository"] == "https://github.com/ilyanemchenko/byline"


def test_claude_marketplace_points_at_root():
    m = load(FILES[1])
    assert m["name"] == "byline-skills"
    assert [(p["name"], p["source"]) for p in m["plugins"]] == [("byline", "./")]


def test_codex_manifests():
    p = load(FILES[2])
    assert (p["name"], p["version"], p["skills"]) == ("byline", "0.1.0", "./skills/")
    entry = load(FILES[3])["plugins"][0]
    assert entry["name"] == "byline" and entry["source"] == {"source": "url", "url": "./"}


def test_versions_agree():
    assert load(FILES[0])["version"] == load(FILES[2])["version"] == load(FILES[1])["plugins"][0]["version"]


def test_no_email_and_no_forbidden_folders():
    assert all("@" not in (ROOT / f).read_text(encoding="utf-8") for f in FILES)
    assert not any((ROOT / d).exists() for d in ("bin", "commands", "agents", "hooks"))
