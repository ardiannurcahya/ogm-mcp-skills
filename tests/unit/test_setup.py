"""Unit tests for ogm_mcp_skills.setup module."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ogm_mcp_skills.setup import get_embedded_skill_content, setup_harnesses


def test_get_embedded_skill_content() -> None:
    content = get_embedded_skill_content()
    assert "OpenGraphMemory (OGM) Skill" in content
    assert "ogm_index_codebase" in content
    assert "ogm_retrieval_query" in content


def test_setup_harnesses(tmp_path: Path, monkeypatch: Any) -> None:
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    res = setup_harnesses("http://localhost:8000", "test_proj", "test_key")
    assert res["ok"] is True
    skill_file = tmp_path / ".gemini" / "config" / "skills" / "ogm" / "SKILL.md"
    assert skill_file.exists()
    assert "OpenGraphMemory (OGM) Skill" in skill_file.read_text(encoding="utf-8")
    mcp_file = tmp_path / ".gemini" / "antigravity-cli" / "mcp_config.json"
    assert mcp_file.exists()
    assert "mcpServers" in mcp_file.read_text(encoding="utf-8")
    cursor_mcp = tmp_path / ".cursor" / "mcp.json"
    assert cursor_mcp.exists()
    assert "mcpServers" in cursor_mcp.read_text(encoding="utf-8")
    cursor_rule = tmp_path / ".cursor" / "rules" / "ogm.mdc"
    assert cursor_rule.exists()


def test_merge_mcp_config_json_safely_skips_malformed(tmp_path: Path) -> None:
    from ogm_mcp_skills.setup import _merge_mcp_config_json

    broken_file = tmp_path / "broken.json"
    broken_file.write_text("{ broken json", encoding="utf-8")
    res = _merge_mcp_config_json(broken_file, "http://localhost:8000", None, None)
    assert res is False
    assert broken_file.read_text(encoding="utf-8") == "{ broken json"
