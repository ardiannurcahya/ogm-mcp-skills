# Google Antigravity Setup

Install from PyPI with `uv tool install ogm-mcp-skills`, or run directly with `uvx ogm-mcp-skills==0.2.2`.

## 1. Skill Installation

Antigravity discovers skills in `.agents/skills/<name>/SKILL.md` (workspace project) or `~/.gemini/config/skills/<name>/SKILL.md` (global).

You can auto-install the skill and MCP configuration using:
```bash
ogm-mcp-skills setup
```
Or copy `src/ogm_mcp_skills/resources/SKILL.md` directly into `.agents/skills/ogm/SKILL.md`.

## 2. MCP Server Configuration

Merge `examples/antigravity/mcp_config.json.example` into `~/.gemini/antigravity-cli/mcp_config.json`:

```json
{
  "mcpServers": {
    "ogm": {
      "command": "uvx",
      "args": ["ogm-mcp-skills==0.2.2"],
      "env": {
        "OGM_BASE_URL": "${OGM_BASE_URL}",
        "OGM_API_KEY": "${OGM_API_KEY}",
        "OGM_PROJECT_ID": "${OGM_PROJECT_ID}",
        "OGM_PERMISSION_PROFILE": "read-only"
      }
    }
  }
}
```

## 3. Project Rule Directive (`GEMINI.md` / `AGENTS.md`)

Add the snippet from `examples/antigravity/GEMINI.md.example` to your project's `GEMINI.md` or `AGENTS.md`. This instructs Antigravity to activate the `ogm` skill during pair-programming workflows:
- Recall memory before attempting fixes (`ogm_recall_code_memory`).
- Query Hybrid RAG for architecture context (`ogm_retrieval_query`).
- Trace call graphs before refactoring (`ogm_get_code_call_graph`).
- Record verified solutions after tests pass (`ogm_record_code_fix`).

Expected 22 tools: `ogm_health`, `ogm_list_datasets`, `ogm_search_entities`, `ogm_get_entity`, `ogm_get_neighbors`, `ogm_find_path`, `ogm_get_subgraph`, `ogm_get_graph`, `ogm_get_evidence`, `ogm_get_relation_evidence`, `ogm_retrieval_query`, `ogm_upload_document`, `ogm_memory_list_episodes`, `ogm_memory_get_episode`, `ogm_memory_search`, `ogm_memory_create_episode`, `ogm_memory_append_attempt`, `ogm_memory_record_outcome`, `ogm_memory_feedback_episode`, `ogm_memory_supersede_episode`, `ogm_memory_feedback_pattern`, `ogm_memory_supersede_pattern`.
