---
name: ogm
description: >-
  OpenGraphMemory (OGM) Hybrid RAG, Codebase AST Search, Knowledge Graph, and Persistent Agent Operational Memory.
  Trigger whenever investigating bugs, researching architecture, navigating code symbols/call-graphs,
  querying hybrid RAG evidence, syncing code files, or persisting verified bug fixes and operational lessons.
license: MIT
compatibility: Compatible with Antigravity, Cursor, Claude Code, OpenCode, Hermes Agent, OpenClaw, and Codex.
---

# OpenGraphMemory (OGM) Skill

This skill provides a comprehensive, unambiguous, production-grade operational guide for AI Agents interacting with OpenGraphMemory (OGM). It covers four core capabilities:
1. **Hybrid RAG & Semantic Retrieval** (Dense Vector pgvector + Knowledge Graph traversal via RRF).
2. **Codebase AST Call-Graphs & Centrality** (Tree-sitter continuous AST extraction).
3. **Document Knowledge Graphs & Evidence Citations** (LiteParse verbatim text & spatial bounding boxes).
4. **Persistent Failure-Driven Agent Operational Memory** (Bayesian confidence, closed-loop feedback, supersession).

---

## ⚡ Agent Lifecycle Trigger Matrix

Follow this 4-phase protocol during all pair-programming and engineering sessions:

| Phase | Agent State / Event | Mandatory Action | Primary MCP Tool |
| :--- | :--- | :--- | :--- |
| **1. Inception & Recall** | User asks to fix a bug, diagnose an error, refactor, or query system architecture. | **Search prior memory first** to check if a verified solution exists. Query Hybrid RAG for architecture context. | `ogm_recall_code_memory`<br>`ogm_memory_search`<br>`ogm_retrieval_query` |
| **2. Blast Radius & Navigation** | Agent explores codebase structure before modifying code. | Search AST symbols (functions/classes) and trace caller/callee relationships to evaluate impact. | `ogm_search_code_symbols`<br>`ogm_get_code_call_graph`<br>`ogm_get_code_chunks` |
| **3. Live Code Sync** | Agent edits or writes a code file during pair-programming. | **Sync single-file AST** into Knowledge Graph in real-time (<15ms). | `ogm_sync_code_file` |
| **4. Persistence & Closure** | Bug is fixed, tests pass, migration succeeds, or PR is merged. | **Record verified outcome & lesson** so future agent sessions don't repeat the error. | `ogm_record_code_fix`<br>`ogm_memory_record_outcome` |

---

## 🎯 Task Intent Routing (English & Indonesian Triggers)

### 🔍 Category 1: Hybrid RAG & Semantic Retrieval
**English Triggers:**
* *"How does the authentication / payment / storage service work?"*
* *"Query documentation and code using Hybrid RAG"*
* *"Find relevant evidence and quotes for architecture spec X"*

**Indonesian Triggers:**
* *"Bagaimana cara kerja modul autentikasi / pembayaran / storage?"*
* *"Cari dokumentasi dan kode pakai hybrid RAG"*
* *"Temukan kutipan dan bukti teknis untuk spesifikasi X"*

**Action Protocol:**
1. Call `ogm_retrieval_query` with `dataset_id`, `query`, and `mode="hybrid"` (combines vector and graph via RRF).
2. Inspect returned chunks and verbatim evidence citations.

---

### 💻 Category 2: Codebase AST Call-Graphs & Centrality
**English Triggers:**
* *"Extract/index this codebase into OpenGraphMemory / OGM"*
* *"Build AST call-graph for project Y"*
* *"Which symbols are most connected / have top degree in repo Z?"*
* *"Who calls function `process_payment`?"*

**Indonesian Triggers:**
* *"Tolong extract codebase ini ke dalam knowledge graph menggunakan ogm"*
* *"Index repo ini ke dalam OGM"*
* *"Simbol apa yang paling banyak keterhubungannya / urutkan degree terbanyak"*
* *"Siapa saja yang memanggil fungsi `process_payment`?"*

**Action Protocol:**
1. **Full Repo Onboarding (Oneshot)**: Call `ogm_index_codebase` with `dataset_id` and `path`.
2. **Incremental Single-File Edit**: Call `ogm_sync_code_file` when editing 1 file during pair programming.
3. **Symbol Search & Call Graphs**: Use `ogm_search_code_symbols` and `ogm_get_code_call_graph`.
4. **Degree Centrality Ranking**: Use `ogm_get_code_chunks` to fetch hub nodes sorted by degree.

---

### 📄 Category 3: Document Upload & Knowledge Extraction
**English Triggers:**
* *"Upload/index document spec.pdf or design.md into OGM"*
* *"Extract knowledge graph from document X"*
* *"Show evidence quotes for relation Y"*

**Indonesian Triggers:**
* *"Upload/index dokumen spec.pdf ke OGM"*
* *"Extract knowledge graph dari dokumen design.md"*
* *"Tampilkan bukti kutipan relasi Y"*

**Action Protocol:**
1. Identify dataset (`ogm_list_datasets`).
2. Upload document using `ogm_upload_document`.
3. Inspect relation evidence quotes using `ogm_get_evidence` or `ogm_get_relation_evidence`.

---

### 🧠 Category 4: Persistent Agent Operational Memory Workflow
**English Triggers:**
* *"Fix bug X", "Resolve error Y", "Failed test in Z"*
* *"Record verified fix for this issue"*
* *"Did we encounter this problem before?"*

**Indonesian Triggers:**
* *"Perbaiki error X", "Fix bug Y", "Test gagal di Z"*
* *"Catat solusi perbaikan ini ke memori"*
* *"Apakah masalah ini pernah terjadi sebelumnya?"*

**Action Protocol:**
1. **Recall**: Call `ogm_recall_code_memory` or `ogm_memory_search` before making edits.
2. **Reorient**: Search again only when initial hypothesis is disproven.
3. **Persist**: Call `ogm_record_code_fix` or `ogm_memory_record_outcome` after test/build passes.

---

## 🛠️ Complete 22-Tool MCP Cheat Sheet & Zero-Loop Rules

### Zero-Loop Policy & Direct Tool Execution
* **NEVER** run `curl` commands to `/v1/...` API endpoints manually.
* **NEVER** inspect OpenAPI schemas (`openapi.json`) or run custom regex/Node.js fallback scripts.
* **ALWAYS** call the matching `ogm_*` MCP tool directly in 1 single tool call (*oneshot*).

| Category | MCP Tool Name | Primary Parameters & Aliases | Purpose |
| :--- | :--- | :--- | :--- |
| **Hybrid RAG** | `ogm_retrieval_query` | `dataset_id`, `query`, `mode`, `top_k` | Query Hybrid RAG (pgvector + graph via RRF) with citations |
| **Codebase Ingestion** | `ogm_index_codebase` | `dataset_id`, `path` (or `directory_path`) | **Oneshot** index full codebase repository into OGM |
| **Codebase Sync** | `ogm_sync_code_file` | `dataset_id`, `file_path`, `code`, `language` | Live incremental AST sync for single edited file (<15ms) |
| **Symbol Search** | `ogm_search_code_symbols` | `dataset_id`, `q` (or `query`), `kind`, `limit` | Search codebase functions, classes, structs |
| **Call Graph** | `ogm_get_code_call_graph` | `entity_id` (or `symbol_id`), `limit` | Trace callers, calls, inheritance tree |
| **Degree & AST Chunks** | `ogm_get_code_chunks` | `dataset_id`, `file_path`, `limit` | Fetch top-degree hub nodes & AST chunk bounds |
| **Memory Recall** | `ogm_recall_code_memory` | `q` (or `query` / `file_path` / `function_name`) | Recall prior bugfixes & refactoring lessons |
| **Record Code Fix** | `ogm_record_code_fix` | `file_path`, `title`, `goal`, `root_cause`, `solution` | Record verified solution for future agent sessions |
| **Memory Search** | `ogm_memory_search` | `q` (or `query`), `problem_signature`, `repository` | Search verified agent operational memories |
| **Memory Create** | `ogm_memory_create_episode` | `goal`, `problem_signature`, `domain` | Start operational problem-solving episode |
| **Memory Attempt** | `ogm_memory_append_attempt` | `episode_id`, `hypothesis`, `action` | Log episode attempt & hypothesis |
| **Memory Outcome** | `ogm_memory_record_outcome` | `episode_id`, `status`, `lesson` | Finalize episode outcome with verifiers |
| **Memory Feedback** | `ogm_memory_feedback_episode` | `episode_id`, `score` (+1 / -1) | Calibrate Bayesian confidence score |
| **Memory Supersede** | `ogm_memory_supersede_episode` | `episode_id`, `superseding_episode_id` | Invalidate outdated memory episode |
| **Pattern Feedback** | `ogm_memory_feedback_pattern` | `pattern_key`, `score` (+1 / -1) | Calibrate pattern confidence score |
| **Pattern Supersede** | `ogm_memory_supersede_pattern` | `pattern_key`, `superseding_pattern_key` | Mark pattern superseded by newer pattern |
| **Document Upload** | `ogm_upload_document` | `dataset_id`, `path` (or `file_path`), `filename` | Upload PDF/MD/CSV document into Knowledge Graph |
| **Evidence & Quotes** | `ogm_get_evidence` | `evidence_id` | Inspect exact quote backing graph relation |
| **Relation Evidence** | `ogm_get_relation_evidence` | `dataset_id`, `relation_id` | Retrieve relation-specific quote evidence |
| **List Datasets** | `ogm_list_datasets` | *(None)* | List all isolated repository datasets |
| **Search Entities** | `ogm_search_entities` | `dataset_id`, `q` (or `query`), `entity_type` | Search canonical entities in Knowledge Graph |
| **Get Entity** | `ogm_get_entity` | `entity_id` | Read entity details by ID |
| **Get Neighbors** | `ogm_get_neighbors` | `entity_id` (or `symbol_id`), `limit` | Read 1-hop graph connections |
| **Find Path** | `ogm_find_path` | `dataset_id`, `source_entity_id`, `target_entity_id` | Calculate shortest path between two entities |
| **Get Subgraph** | `ogm_get_subgraph` | `dataset_id`, `entity_id` (or `root_entity_id`), `depth` | Extract clustered entity subgraphs |
| **Get Graph** | `ogm_get_graph` | `dataset_id`, `limit`, `depth` | Read dataset graph overview |

---

## 🛠️ MCP Tool Workflows & Examples

### 1. Hybrid RAG Query Workflow
```json
{
  "dataset_id": "core-backend",
  "query": "How does token validation and session expiration work?",
  "mode": "hybrid",
  "top_k": 10
}
```
*Tool: `ogm_retrieval_query`*

### 2. Recall Memory Before Bug Fix
```json
{
  "file_path": "apps/api/app/routers/retrieval.py",
  "q": "deadlock during bulk insert"
}
```
*Tool: `ogm_recall_code_memory` / `ogm_memory_search`*

### 3. Record Verified Fix After Passing Tests
```json
{
  "file_path": "apps/api/app/routers/retrieval.py",
  "title": "Fix database deadlock during batch insert",
  "goal": "Prevent concurrent transaction lock collisions",
  "root_cause": "Unordered bulk insert resulted in cross-table row lock deadlocks",
  "solution": "Sort batch rows by primary key before bulk insert and acquire advisory lock"
}
```
*Tool: `ogm_record_code_fix`*

### 4. Codebase Oneshot Indexing
```json
{
  "dataset_id": "ds_my_project",
  "path": "/workspace/my-project"
}
```
*Tool: `ogm_index_codebase`*

### 5. Live Incremental Code File Sync
```json
{
  "dataset_id": "ds_my_project",
  "file_path": "src/auth/jwt.py",
  "code": "def verify_token(token: str) -> bool:\n    ...",
  "language": "python"
}
```
*Tool: `ogm_sync_code_file`*
