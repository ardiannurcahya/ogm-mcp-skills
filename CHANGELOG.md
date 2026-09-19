# Changelog

All notable changes follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.3] - 2026-09-19

### Added

- **Hybrid RAG MCP Tool (`ogm_retrieval_query`)**:
  - Connects to OpenGraphMemory v0.3.0 `POST /v1/retrieval/query` fusing dense vector search (`pgvector`) and knowledge graph traversal via Reciprocal Rank Fusion (RRF).
- **Multi-Agent Harness Support**:
  - **Cursor**: Workspace MCP config (`.cursor/mcp.json`) and MDC rule (`.cursor/rules/ogm.mdc`).
  - **Google Antigravity**: Workspace project skills (`.agents/skills/ogm/SKILL.md`) and global MCP config (`~/.gemini/antigravity-cli/mcp_config.json`).
  - **OpenClaw**: MCP server configuration (`openclaw.json`) and agent prompt template.
  - **OpenAI Codex**: System instructions template for OpenAI Assistant and Codex workflows.
  - **Claude Code**: Project directive (`CLAUDE.md`) for autonomous pair-programming memory recall and persistence.
- **Agent Lifecycle Trigger Matrix**:
  - 4-phase operational protocol in `SKILL.md`: *Phase 1: Inception/Recall* ➡️ *Phase 2: Navigation/Blast Radius* ➡️ *Phase 3: Live Code Sync* ➡️ *Phase 4: Persistence/Closure*.
- **Enhanced Auto-Installer (`ogm-mcp-skills setup`)**:
  - Detects and automatically configures Cursor, Antigravity, Claude Desktop, and OpenClaw.

### Changed

- Updated harness documentation and examples across all supported agents.

---

## [0.1.8] - 2026-08-11

### Added

- `ogm_index_codebase` MCP tool for batch recursive AST symbol extraction and call-graph ingestion across codebases.
- Token Economics & Benchmark Analysis documentation in `README.md` detailing token savings for recurring bugs and AST subgraphs.

### Changed

- Updated skill manifest and tool docs (`docs/tools.md`, `tests/test_docs.py`) to cover all 24 MCP tools.

### Fixed

- Synced MCP registration and unit test fixtures for codebase tools and verified all 33 unit tests pass.

---

## [0.1.7] - 2026-08-02

### Added

- Rebranded repository, package, and MCP server from `ogm-agent-bridge` to `ogm-mcp-skills`.
- Production-grade `.agents/skills/ogm-mcp-skills/SKILL.md` for autonomous AI coding agents.
- Codebase Knowledge Graph MCP tools (`ogm_search_code_symbols`, `ogm_get_code_call_graph`, `ogm_get_code_chunks`, `ogm_recall_code_memory`, `ogm_record_code_fix`, `ogm_sync_code_file`).
- Ten Agent Memory MCP tools aligned with the OpenGraphMemory core `v0.1.0` source-level HTTP contract.
- Contract coverage for MCP registration, HTTP routes, payloads, redirects, ambiguous writes, and secure uploads.

### Changed

- Rebranded Python package to `ogm_mcp_skills` and CLI entrypoint to `ogm-mcp-skills` / `ogm-mcp`.
- Default permission profile is `read-only`; write and curator capabilities require explicit opt-in.
- All documented `uvx` harness examples pin `ogm-mcp-skills==0.1.7`.
- Upload roots are explicit allowlists and are empty by default.

### Fixed

- Sanitize upstream failures, reject every non-2xx response, correctly classify audited HTTP statuses, and bound safe-request retries.
- Reject non-finite or excessive timeout/retry configuration and malformed or unknown tool arguments.
- Preserve no-retry ambiguous-outcome protection for all write operations, including uploads.
- Validate uploads through descriptor-anchored, symlink-resistant file handling and close every descriptor/response.

### Security

- Raw upstream error details are no longer exposed to MCP callers.
- A missing `OGM_UPLOAD_ROOTS` no longer falls back to exposing the process working directory.

## [0.1.6] - 2026-07-18

### Fixed

- Install the pinned PyPI publisher inside the isolated publish job.

## [0.1.5] - 2026-07-18

### Changed

- Prefer PyPI install and `uvx` usage in README, harness docs, and examples.

### Fixed

- Exclude `SHA256SUMS` from PyPI publish input.
- Align harness example tests with PyPI `uvx` examples.
- Read package version test from `pyproject.toml`.
- Publish to PyPI with `twine==6.1.0` directly.

## [0.1.0] - 2026-07-18

### Added

- Compatibility target: OpenGraphMemory core `7703d3994b49272bef7b0d38caf896cde4338f13`.
- Four graph/community read MCP tools; bridge now exposes eleven tools.
- Query modes `graph_local` and `graph_global`; valid modes are `vector_only`, `graph_only`, `graph_local`, `graph_global`, `hybrid`. No `auto`.
- Query `include_communities` and `community_level` 0..2.
- `.json` upload MIME auto-detection as `application/json`; core validates malformed JSON.
- MCP read and write tools for OpenGraphMemory.
- Claude Code, OpenCode, and Hermes setup docs.
- Typed package marker, package metadata, CI package validation, and tag-gated release workflow.
