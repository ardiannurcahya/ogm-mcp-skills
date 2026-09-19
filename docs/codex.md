# OpenAI Codex / Assistant Setup

Install from PyPI with `uv tool install ogm-mcp-skills`, or run directly with `uvx ogm-mcp-skills==0.2.2`.

## 1. Tool Integration

When integrating OpenGraphMemory with OpenAI Assistants or custom Codex workflows:
- Configure environment variables `OGM_BASE_URL`, `OGM_API_KEY`, `OGM_PROJECT_ID`, and `OGM_PERMISSION_PROFILE` (default `read-only`).
- Connect the `ogm-mcp-skills` FastMCP server via an MCP-to-OpenAPI proxy (e.g. `mcp-proxy`) or import the tool schemas directly into your Assistant's function definitions.

## 2. System Instructions

Paste the contents of `examples/codex/instructions.md.example` into your Assistant's system instructions prompt. This ensures Codex adheres to the 4-phase operational memory protocol:
- Recall memory before diagnosing errors (`ogm_recall_code_memory`).
- Query Hybrid RAG for architecture details (`ogm_retrieval_query`).
- Check call graphs before modifying symbols (`ogm_get_code_call_graph`).
- Persist verified bug fixes upon resolution (`ogm_record_code_fix`).

Expected 22 tools: `ogm_health`, `ogm_list_datasets`, `ogm_search_entities`, `ogm_get_entity`, `ogm_get_neighbors`, `ogm_find_path`, `ogm_get_subgraph`, `ogm_get_graph`, `ogm_get_evidence`, `ogm_get_relation_evidence`, `ogm_retrieval_query`, `ogm_upload_document`, `ogm_memory_list_episodes`, `ogm_memory_get_episode`, `ogm_memory_search`, `ogm_memory_create_episode`, `ogm_memory_append_attempt`, `ogm_memory_record_outcome`, `ogm_memory_feedback_episode`, `ogm_memory_supersede_episode`, `ogm_memory_feedback_pattern`, `ogm_memory_supersede_pattern`.
