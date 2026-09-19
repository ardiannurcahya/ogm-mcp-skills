"""Graph-first read-tool handlers and core input validation."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

from ogm_mcp_skills.client import OGMClient
from ogm_mcp_skills.errors import ValidationError
from ogm_mcp_skills.permissions import require_read
from ogm_mcp_skills.responses import envelope


async def list_datasets(client: OGMClient) -> dict[str, Any]:
    require_read("datasets:read")
    response = await client.request("GET", "/v1/datasets")
    return envelope(response.json(), provenance={"project_id": client.project_id})


async def search_entities(
    client: OGMClient, arguments: Mapping[str, Any]
) -> dict[str, Any]:
    _arguments(arguments, {"dataset_id", "q", "query", "entity_type", "limit"})
    dataset_id = _route_component(arguments.get("dataset_id"), "dataset_id", 1)
    query_val = str(arguments.get("q") or arguments.get("query") or "")[:200]
    if not query_val:
        raise ValidationError("Either 'q' or 'query' parameter is required.")
    params = {"q": query_val}
    _optional_string(arguments, params, "entity_type", 100)
    _integer(arguments, params, "limit", 1, 100)
    return await _get(
        client, f"/v1/datasets/{dataset_id}/entities/search", params, dataset_id
    )


async def get_entity(client: OGMClient, entity_id: str) -> dict[str, Any]:
    return await _get(
        client,
        f"/v1/entities/{_route_component(entity_id, 'entity_id', 1)}",
        {},
        None,
        entity_id,
    )


async def get_neighbors(
    client: OGMClient, arguments: Mapping[str, Any]
) -> dict[str, Any]:
    _arguments(arguments, {"entity_id", "symbol_id", "limit"})
    raw_id = arguments.get("entity_id") or arguments.get("symbol_id")
    entity_id = _route_component(raw_id, "entity_id", 1)
    params: dict[str, Any] = {}
    _integer(arguments, params, "limit", 1, 100)
    return await _get(
        client, f"/v1/entities/{entity_id}/neighbors", params, None, entity_id
    )


async def find_path(client: OGMClient, arguments: Mapping[str, Any]) -> dict[str, Any]:
    _arguments(
        arguments,
        {
            "dataset_id",
            "source_entity_id",
            "target_entity_id",
            "max_depth",
            "relation_limit",
        },
    )
    dataset_id = _route_component(arguments.get("dataset_id"), "dataset_id", 1)
    params = {
        "source_entity_id": _string(arguments, "source_entity_id", 1),
        "target_entity_id": _string(arguments, "target_entity_id", 1),
    }
    _integer(arguments, params, "max_depth", 1, 4)
    _integer(arguments, params, "relation_limit", 1, 200)
    return await _get(
        client, f"/v1/datasets/{dataset_id}/graph/path", params, dataset_id
    )


async def get_subgraph(
    client: OGMClient, arguments: Mapping[str, Any]
) -> dict[str, Any]:
    _arguments(
        arguments,
        {
            "dataset_id",
            "entity_id",
            "root_entity_id",
            "symbol_id",
            "depth",
            "node_limit",
            "relation_limit",
        },
    )
    dataset_id = _route_component(arguments.get("dataset_id"), "dataset_id", 1)
    raw_id = (
        arguments.get("entity_id")
        or arguments.get("root_entity_id")
        or arguments.get("symbol_id")
    )
    params = {"entity_id": _string({"entity_id": raw_id}, "entity_id", 1)}
    _integer(arguments, params, "depth", 0, 2)
    _integer(arguments, params, "node_limit", 1, 200)
    _integer(arguments, params, "relation_limit", 1, 400)
    return await _get(
        client, f"/v1/datasets/{dataset_id}/graph/subgraph", params, dataset_id
    )


async def get_graph(client: OGMClient, arguments: Mapping[str, Any]) -> dict[str, Any]:
    _arguments(arguments, {"dataset_id", "limit", "depth"})
    dataset_id = _route_component(arguments.get("dataset_id"), "dataset_id", 1)
    params: dict[str, Any] = {}
    _integer(arguments, params, "limit", 1, 200)
    _integer(arguments, params, "depth", 0, 1)
    return await _get(client, f"/v1/datasets/{dataset_id}/graph", params, dataset_id)


async def get_evidence(client: OGMClient, evidence_id: str) -> dict[str, Any]:
    return await _get(
        client,
        f"/v1/evidence/{_route_component(evidence_id, 'evidence_id', 1)}",
        {},
        None,
        None,
        evidence_id,
    )


async def get_relation_evidence(
    client: OGMClient, arguments: Mapping[str, Any]
) -> dict[str, Any]:
    _arguments(arguments, {"dataset_id", "relation_id", "limit"})
    dataset_id = _route_component(arguments.get("dataset_id"), "dataset_id", 1)
    relation_id = _route_component(arguments.get("relation_id"), "relation_id", 1)
    params: dict[str, Any] = {}
    _integer(arguments, params, "limit", 1, 100)
    return await _get(
        client,
        f"/v1/datasets/{dataset_id}/relations/{relation_id}/evidence",
        params,
        dataset_id,
        None,
        None,
        relation_id,
    )


def _validate_weight(name: str, value: Any) -> float:
    if type(value) not in (int, float) or isinstance(value, bool):
        raise ValidationError(f"{name} must be a number from 0.0 to 1.0")
    weight = float(value)
    if not math.isfinite(weight) or not 0.0 <= weight <= 1.0:
        raise ValidationError(f"{name} must be a number from 0.0 to 1.0")
    return weight


async def retrieval_query(
    client: OGMClient, arguments: Mapping[str, Any]
) -> dict[str, Any]:
    require_read("graph:read")
    _arguments(
        arguments,
        {
            "dataset_id",
            "query",
            "q",
            "mode",
            "top_k",
            "limit",
            "vector_weight",
            "graph_weight",
            "compare",
        },
    )
    dataset_id = _route_component(arguments.get("dataset_id"), "dataset_id", 1)
    query_val = str(arguments.get("query") or arguments.get("q") or "")[:500]
    if not query_val:
        raise ValidationError("Parameter 'query' or 'q' is required.")

    if "top_k" in arguments and arguments["top_k"] is not None:
        top_k = arguments["top_k"]
    elif "limit" in arguments and arguments["limit"] is not None:
        top_k = arguments["limit"]
    else:
        top_k = 10

    if type(top_k) is not int or isinstance(top_k, bool) or not 1 <= top_k <= 50:
        raise ValidationError("top_k must be an integer from 1 to 50")

    payload: dict[str, Any] = {
        "dataset_id": dataset_id,
        "query": query_val,
        "mode": str(arguments.get("mode") or "hybrid"),
        "top_k": top_k,
    }
    if "vector_weight" in arguments and arguments["vector_weight"] is not None:
        payload["vector_weight"] = _validate_weight(
            "vector_weight", arguments["vector_weight"]
        )
    if "graph_weight" in arguments and arguments["graph_weight"] is not None:
        payload["graph_weight"] = _validate_weight(
            "graph_weight", arguments["graph_weight"]
        )
    if "compare" in arguments and arguments["compare"] is not None:
        payload["compare"] = bool(arguments["compare"])

    response = await client.request("POST", "/v1/retrieval/query", json=payload)
    return envelope(
        response.json(),
        provenance={"project_id": client.project_id, "dataset_id": dataset_id},
    )


async def _get(
    client: OGMClient,
    path: str,
    params: Mapping[str, Any],
    dataset_id: str | None,
    entity_id: str | None = None,
    evidence_id: str | None = None,
    relation_id: str | None = None,
) -> dict[str, Any]:
    require_read("graph:read")
    response = await client.request("GET", path, params=params or None)
    provenance: dict[str, str] = {"project_id": client.project_id}
    for key, value in (
        ("dataset_id", dataset_id),
        ("entity_id", entity_id),
        ("evidence_id", evidence_id),
        ("relation_id", relation_id),
    ):
        if value is not None:
            provenance[key] = value
    return envelope(response.json(), provenance=provenance)


def _string(
    arguments: Mapping[str, Any], name: str, minimum: int, maximum: int | None = None
) -> str:
    return _value(arguments.get(name), name, minimum, maximum)


def _value(value: object, name: str, minimum: int, maximum: int | None = None) -> str:
    if (
        type(value) is not str
        or len(value) < minimum
        or (maximum is not None and len(value) > maximum)
    ):
        raise ValidationError(f"{name} has invalid length")
    return value


def _route_component(
    value: object, name: str, minimum: int, maximum: int | None = None
) -> str:
    """Validate a caller-provided value used as one literal URL path segment."""
    component = _value(value, name, minimum, maximum)
    if (
        any(ord(character) < 32 or ord(character) == 127 for character in component)
        or any(delimiter in component for delimiter in ("/", "\\", "?", "#", "%", "&"))
        or component in {".", ".."}
    ):
        raise ValidationError(f"{name} must be a safe route component")
    return component


def _arguments(arguments: Mapping[str, Any], allowed: set[str]) -> None:
    if set(arguments) - allowed:
        raise ValidationError("unknown argument")


def _integer(
    arguments: Mapping[str, Any],
    target: dict[str, Any],
    name: str,
    minimum: int,
    maximum: int,
) -> None:
    if name not in arguments:
        return
    value = arguments[name]
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValidationError(f"{name} must be an integer from {minimum} to {maximum}")
    target[name] = value


def _optional_string(
    arguments: Mapping[str, Any], target: dict[str, Any], name: str, maximum: int
) -> None:
    if name in arguments:
        target[name] = _value(arguments[name], name, 1, maximum)
