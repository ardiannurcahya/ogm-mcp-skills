# Cursor Setup

Install from PyPI with `uv tool install ogm-mcp-skills`, or run directly with `uvx ogm-mcp-skills==0.2.2`.

## 1. MCP Server Configuration

Merge `examples/cursor/.cursor/mcp.json.example` into your workspace `.cursor/mcp.json` or user `~/.cursor/mcp.json`:

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

For source development, replace command and args with:
```json
"command": "uv",
"args": ["run", "--project", "/absolute/path/ogm-mcp-skills", "ogm-mcp-skills"]
```

## 2. Agent Rule Configuration (`.cursor/rules/ogm.mdc`)

Copy `examples/cursor/.cursor/rules/ogm.mdc.example` into `.cursor/rules/ogm.mdc`. This instructs Cursor Composer and Chat to proactively invoke OGM tools:
- **Before coding**: Queries `ogm_recall_code_memory` and `ogm_retrieval_query`.
- **During navigation**: Queries `ogm_search_code_symbols` and `ogm_get_code_call_graph`.
- **After tests pass**: Persists the fix via `ogm_record_code_fix`.

Expected 22 tools: `ogm_health`, `ogm_list_datasets`, `ogm_search_entities`, `ogm_get_entity`, `ogm_get_neighbors`, `ogm_find_path`, `ogm_get_subgraph`, `ogm_get_graph`, `ogm_get_evidence`, `ogm_get_relation_evidence`, `ogm_retrieval_query`, `ogm_upload_document`, `ogm_memory_list_episodes`, `ogm_memory_get_episode`, `ogm_memory_search`, `ogm_memory_create_episode`, `ogm_memory_append_attempt`, `ogm_memory_record_outcome`, `ogm_memory_feedback_episode`, `ogm_memory_supersede_episode`, `ogm_memory_feedback_pattern`, `ogm_memory_supersede_pattern`.
