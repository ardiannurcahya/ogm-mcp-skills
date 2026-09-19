# OpenClaw Setup

Install from PyPI with `uv tool install ogm-mcp-skills`, or run directly with `uvx ogm-mcp-skills==0.2.2`.

## 1. MCP Configuration

Merge `examples/openclaw/openclaw.json.example` into your OpenClaw agent configuration:

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

## 2. Agent Prompt Directive

Add the following instructions to your OpenClaw agent prompt template:

```text
You have access to OpenGraphMemory (OGM) tools (`ogm_*`).
1. Before modifying code or diagnosing an issue, call `ogm_recall_code_memory` or `ogm_memory_search` to check prior fixes.
2. Query Hybrid RAG with `ogm_retrieval_query` for architecture and documentation context.
3. Trace symbol call graphs with `ogm_get_code_call_graph` before refactoring.
4. After tests pass and the bug is resolved, record the solution with `ogm_record_code_fix`.
```

Expected 22 tools: `ogm_health`, `ogm_list_datasets`, `ogm_search_entities`, `ogm_get_entity`, `ogm_get_neighbors`, `ogm_find_path`, `ogm_get_subgraph`, `ogm_get_graph`, `ogm_get_evidence`, `ogm_get_relation_evidence`, `ogm_retrieval_query`, `ogm_upload_document`, `ogm_memory_list_episodes`, `ogm_memory_get_episode`, `ogm_memory_search`, `ogm_memory_create_episode`, `ogm_memory_append_attempt`, `ogm_memory_record_outcome`, `ogm_memory_feedback_episode`, `ogm_memory_supersede_episode`, `ogm_memory_feedback_pattern`, `ogm_memory_supersede_pattern`.
