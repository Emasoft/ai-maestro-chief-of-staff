#!/usr/bin/env python3
"""
amcos_approval_manager.py - Dual-Authority Approval Manager for AMCOS

Manages GovernanceRequests using a dual-authority model:
  PRIMARY:   AI Maestro REST API (/api/v1/governance/requests) — source of truth
  SECONDARY: Local YAML files (.claude/approvals/) — audit trail and offline cache

When both are available, API state always wins. When the API is unreachable,
local YAML keeps working with degraded authority (warnings emitted).

Part of the ai-maestro-chief-of-staff plugin.

Usage:
  amcos_approval_manager.py create --type spawn --agent my-agent --reason "Need for task X"
  amcos_approval_manager.py status --id <uuid>
  amcos_approval_manager.py list [--status pending|all]
  amcos_approval_manager.py respond --id <uuid> --decision approved --comment "Go ahead"
  amcos_approval_manager.py wait --id <uuid> --timeout 120
  amcos_approval_manager.py sync
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

APPROVALS_DIR = ".claude/approvals"
PENDING_DIR = f"{APPROVALS_DIR}/pending"
COMPLETED_DIR = f"{APPROVALS_DIR}/completed"

DEFAULT_API_BASE = "http://localhost:23000"
GOVERNANCE_API_PATH = "/api/v1/governance/requests"
API_TIMEOUT = 10

# Extended status values matching GovernanceRequest state machine
VALID_STATUSES = frozenset({
    "pending",
    "local-approved",
    "remote-approved",
    "dual-approved",
    "executed",
    "rejected",
})

# Terminal statuses — no further transitions possible
TERMINAL_STATUSES = frozenset({"executed", "rejected"})

# Statuses that count as "approved" for backward compatibility
APPROVED_STATUSES = frozenset({"local-approved", "remote-approved", "dual-approved", "executed"})


# ---------------------------------------------------------------------------
# Governance REST API Client
# ---------------------------------------------------------------------------


class GovernanceAPI:
    """HTTP client for the AI Maestro GovernanceRequest REST API (stdlib-only)."""

    def __init__(self, api_base: Optional[str] = None):
        base = api_base or os.environ.get("AIMAESTRO_API", DEFAULT_API_BASE)
        self.base_url = base.rstrip("/") + GOVERNANCE_API_PATH
        self.available = True  # set to False on connection failure

    def _request(
        self, method: str, path: str = "", body: Optional[dict[str, Any]] = None,
        query: Optional[dict[str, str]] = None,
    ) -> Optional[dict[str, Any]]:
        """Send an HTTP request to the governance API. Returns parsed JSON or None on failure."""
        url = self.base_url + path
        if query:
            # Build query string from dict
            params = "&".join(f"{k}={urllib.parse.quote(v)}" for k, v in query.items() if v)
            if params:
                url += "?" + params

        data = json.dumps(body).encode("utf-8") if body else None
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=API_TIMEOUT) as resp:
                raw = resp.read().decode("utf-8")
                if not raw.strip():
                    return {}  # 204 No Content
                return json.loads(raw)
        except urllib.error.HTTPError as exc:
            # API returned an error status — still reachable
            self.available = True
            try:
                error_body = json.loads(exc.read().decode("utf-8"))
            except (json.JSONDecodeError, AttributeError):
                error_body = {"error": exc.reason, "status": exc.code}
            print(f"WARNING: API error {exc.code} on {method} {url}: {error_body}", file=sys.stderr)
            return None
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
            # API unreachable — degrade to YAML-only
            self.available = False
            print(f"WARNING: API unreachable ({exc}). Falling back to local YAML.", file=sys.stderr)
            return None

    def submit(self, request_data: dict[str, Any]) -> Optional[dict[str, Any]]:
        """POST a new GovernanceRequest to the API."""
        return self._request("POST", body=request_data)

    def get(self, request_id: str) -> Optional[dict[str, Any]]:
        """GET a GovernanceRequest by ID."""
        return self._request("GET", path=f"/{request_id}")

    def update(self, request_id: str, updates: dict[str, Any]) -> Optional[dict[str, Any]]:
        """PATCH a GovernanceRequest (e.g., to approve/reject)."""
        return self._request("PATCH", path=f"/{request_id}", body=updates)

    def list_requests(
        self, status: Optional[str] = None, requester: Optional[str] = None,
    ) -> Optional[list[dict[str, Any]]]:
        """GET GovernanceRequests with optional filters."""
        query: dict[str, str] = {}
        if status:
            query["status"] = status
        if requester:
            query["requester"] = requester

        result = self._request("GET", query=query)
        if result is None:
            return None
        # API may return a list directly or wrapped in {"requests": [...]}
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            return result.get("requests", result.get("data", []))
        return None


# ---------------------------------------------------------------------------
# Simple YAML serializer/parser (stdlib-only)
# ---------------------------------------------------------------------------


def dict_to_yaml(data: dict[str, Any], indent: int = 0) -> str:
    """Convert a dictionary to YAML format string (stdlib-only, basic types)."""
    lines = []
    prefix = "  " * indent

    for key, value in data.items():
        if key.startswith("_"):
            continue  # skip internal keys like _location
        if value is None:
            lines.append(f"{prefix}{key}: null")
        elif isinstance(value, bool):
            lines.append(f"{prefix}{key}: {str(value).lower()}")
        elif isinstance(value, (int, float)):
            lines.append(f"{prefix}{key}: {value}")
        elif isinstance(value, str):
            if "\n" in value:
                lines.append(f"{prefix}{key}: |")
                for line in value.split("\n"):
                    lines.append(f"{prefix}  {line}")
            elif any(c in value for c in [":", "#", "'", '"', "[", "]", "{", "}"]):
                escaped = value.replace('"', '\\"')
                lines.append(f'{prefix}{key}: "{escaped}"')
            else:
                lines.append(f"{prefix}{key}: {value}")
        elif isinstance(value, list):
            if not value:
                lines.append(f"{prefix}{key}: []")
            else:
                lines.append(f"{prefix}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        lines.append(f"{prefix}  -")
                        nested = dict_to_yaml(item, indent + 2)
                        lines.append(nested)
                    else:
                        lines.append(f"{prefix}  - {item}")
        elif isinstance(value, dict):
            if not value:
                lines.append(f"{prefix}{key}: {{}}")
            else:
                lines.append(f"{prefix}{key}:")
                nested = dict_to_yaml(value, indent + 1)
                lines.append(nested)
        else:
            lines.append(f"{prefix}{key}: {value}")

    return "\n".join(lines)


def parse_yaml_value(value: str) -> Any:
    """Parse a YAML value string to appropriate Python type."""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]

    if value.lower() == "null" or value == "~":
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass

    return value


def yaml_to_dict(yaml_str: str) -> dict[str, Any]:
    """Parse a simple YAML string to dictionary (stdlib-only, basic types)."""
    result: dict[str, Any] = {}
    current_indent = 0
    multiline_key: Optional[str] = None
    multiline_lines: list[str] = []
    list_key: Optional[str] = None
    list_items: list[Any] = []

    lines = yaml_str.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        # Handle multiline continuation
        if multiline_key is not None:
            line_indent = len(line) - len(line.lstrip())
            if line_indent > current_indent and stripped:
                multiline_lines.append(stripped)
                i += 1
                continue
            else:
                result[multiline_key] = "\n".join(multiline_lines)
                multiline_key = None
                multiline_lines = []

        # Handle list items
        if stripped.startswith("- "):
            if list_key is not None:
                item = stripped[2:].strip()
                list_items.append(parse_yaml_value(item))
            i += 1
            continue

        # End list if no longer in list items
        if list_key is not None and not stripped.startswith("-"):
            result[list_key] = list_items
            list_key = None
            list_items = []

        # Parse key: value pairs
        if ":" in stripped:
            colon_idx = stripped.index(":")
            key = stripped[:colon_idx].strip()
            value_part = stripped[colon_idx + 1:].strip()

            if value_part == "":
                list_key = key
                list_items = []
            elif value_part == "|":
                multiline_key = key
                current_indent = len(line) - len(line.lstrip())
            elif value_part == "[]":
                result[key] = []
            elif value_part == "{}":
                result[key] = {}
            else:
                result[key] = parse_yaml_value(value_part)

        i += 1

    if list_key is not None:
        result[list_key] = list_items
    if multiline_key is not None:
        result[multiline_key] = "\n".join(multiline_lines)

    return result


# ---------------------------------------------------------------------------
# Local YAML file operations
# ---------------------------------------------------------------------------


def get_project_root() -> Path:
    """Get the project root directory from environment or current directory."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    return Path(project_dir)


def ensure_directories() -> None:
    """Ensure approval directories exist."""
    root = get_project_root()
    (root / PENDING_DIR).mkdir(parents=True, exist_ok=True)
    (root / COMPLETED_DIR).mkdir(parents=True, exist_ok=True)


def generate_request_id() -> str:
    """Generate a GovernanceRequest ID in the GR-<timestamp>-<random> format."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    short_uuid = uuid.uuid4().hex[:8]
    return f"GR-{ts}-{short_uuid}"


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def save_yaml_mirror(request_id: str, data: dict[str, Any], pending: bool = True) -> Path:
    """Save an approval request to local YAML file (audit trail)."""
    ensure_directories()
    root = get_project_root()
    directory = PENDING_DIR if pending else COMPLETED_DIR
    filepath = root / directory / f"{request_id}.yaml"
    yaml_content = dict_to_yaml(data)
    filepath.write_text(yaml_content, encoding="utf-8")
    return filepath


def load_yaml_mirror(request_id: str) -> Optional[dict[str, Any]]:
    """Load an approval request from local YAML file."""
    root = get_project_root()
    for directory in [PENDING_DIR, COMPLETED_DIR]:
        filepath = root / directory / f"{request_id}.yaml"
        if filepath.exists():
            yaml_content = filepath.read_text(encoding="utf-8")
            data = yaml_to_dict(yaml_content)
            data["_location"] = "pending" if directory == PENDING_DIR else "completed"
            return data
    return None


def move_yaml_to_completed(request_id: str) -> None:
    """Move a YAML file from pending to completed directory."""
    root = get_project_root()
    pending_path = root / PENDING_DIR / f"{request_id}.yaml"
    if pending_path.exists():
        ensure_directories()
        completed_path = root / COMPLETED_DIR / f"{request_id}.yaml"
        pending_path.rename(completed_path)


def list_local_yaml(directory: str) -> list[dict[str, Any]]:
    """List all YAML files in a directory and parse them."""
    ensure_directories()
    root = get_project_root()
    target_dir = root / directory
    results = []
    for filepath in target_dir.glob("*.yaml"):
        try:
            yaml_content = filepath.read_text(encoding="utf-8")
            data = yaml_to_dict(yaml_content)
            results.append(data)
        except Exception as e:
            results.append({"request_id": filepath.stem, "error": str(e)})
    return results


# ---------------------------------------------------------------------------
# AMP messaging
# ---------------------------------------------------------------------------


def send_amp_message(
    to: str, subject: str, content: dict[str, Any], priority: str = "normal",
) -> bool:
    """Send a message via AMP CLI (amp-send)."""
    msg_type = content.get("type", "request") if isinstance(content, dict) else "request"
    message = (
        content.get("message", json.dumps(content))
        if isinstance(content, dict)
        else str(content)
    )

    try:
        result = subprocess.run(
            ["amp-send", to, subject, message, "--priority", priority, "--type", str(msg_type)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


# ---------------------------------------------------------------------------
# Merge logic: API state wins over local YAML
# ---------------------------------------------------------------------------


def merge_api_and_yaml(api_data: Optional[dict[str, Any]], yaml_data: Optional[dict[str, Any]]) -> dict[str, Any]:
    """Merge API and YAML data. API state takes priority for status/decision fields."""
    if api_data is None and yaml_data is None:
        return {}
    if api_data is None:
        # API unavailable — use YAML but flag it
        result = dict(yaml_data or {})
        result["_source"] = "local-only"
        return result
    if yaml_data is None:
        # No local copy — use API data
        result = dict(api_data)
        result["_source"] = "api-only"
        return result

    # Both exist — API wins for authoritative fields, YAML fills in extras
    result = dict(yaml_data)
    # API overwrites these authoritative fields
    for key in ("status", "decision", "decided_by", "decided_at", "decision_comment", "updated_at"):
        if key in api_data and api_data[key] is not None:
            result[key] = api_data[key]
    result["api_synced"] = True
    result["_source"] = "merged"
    return result


# ---------------------------------------------------------------------------
# Core operations (API-first with YAML fallback)
# ---------------------------------------------------------------------------


def create_request(
    api: GovernanceAPI,
    operation_type: str,
    agent_name: str,
    reason: str,
    requester: str,
    scope: str = "local",
    risk_level: str = "low",
    source_cos: Optional[str] = None,
    source_manager: Optional[str] = None,
    target_cos: Optional[str] = None,
    target_manager: Optional[str] = None,
) -> dict[str, Any]:
    """Create a new GovernanceRequest. Posts to API first, mirrors to local YAML."""
    request_id = generate_request_id()
    timestamp = get_timestamp()

    # Session name for COS identification
    session_name = os.environ.get("AIMAESTRO_AGENT", os.environ.get("SESSION_NAME", requester))

    # Build the GovernanceRequest payload (matches API contract)
    request_data: dict[str, Any] = {
        "request_id": request_id,
        "type": operation_type,
        "operation": {
            "action": operation_type,
            "target": agent_name,
            "parameters": {},
        },
        "justification": reason,
        "requester": requester,
        "source_cos": source_cos or session_name,
        "source_manager": source_manager or "",
        "target_cos": target_cos or "",
        "target_manager": target_manager or "",
        "scope": scope,
        "impact": {
            "scope": scope,
            "risk_level": risk_level,
        },
        "status": "pending",
        "created_at": timestamp,
        "updated_at": timestamp,
        "decision": None,
        "decision_comment": None,
        "decided_by": None,
        "decided_at": None,
        "api_synced": False,
        # Backward-compatible fields
        "operation_type": operation_type,
        "agent_name": agent_name,
        "reason": reason,
    }

    # Step 1: POST to API (primary authority)
    api_response = api.submit(request_data)
    if api_response is not None:
        request_data["api_synced"] = True
        # API may return a canonical ID — prefer it
        if "request_id" in api_response:
            request_data["request_id"] = api_response["request_id"]
            request_id = api_response["request_id"]

    # Step 2: Save local YAML mirror (audit trail)
    filepath = save_yaml_mirror(request_id, request_data, pending=True)

    # Step 3: Send AMP notification to manager for approval routing
    message_content = {
        "type": "governance_request",
        "message": (
            f"GovernanceRequest submitted for {operation_type}.\n\n"
            f"Request ID: {request_id}\n"
            f"Operation: {operation_type}\n"
            f"Agent/Resource: {agent_name}\n"
            f"Reason: {reason}\n"
            f"Scope: {scope}\n"
            f"Risk: {risk_level}\n"
            f"Requester: {requester}"
        ),
        "request_id": request_id,
    }
    message_sent = send_amp_message(
        to="ai-maestro-assistant-manager-agent",
        subject=f"[GOVERNANCE] {operation_type}: {agent_name}",
        content=message_content,
        priority="high" if risk_level in ("high", "critical") else "normal",
    )

    return {
        "success": True,
        "request_id": request_id,
        "status": "pending",
        "api_synced": request_data["api_synced"],
        "filepath": str(filepath),
        "message_sent": message_sent,
    }


def get_request(api: GovernanceAPI, request_id: str) -> dict[str, Any]:
    """Get a GovernanceRequest. Queries API first, merges with local YAML."""
    # Step 1: Try API (primary authority)
    api_data = api.get(request_id)

    # Step 2: Load local YAML (audit trail)
    yaml_data = load_yaml_mirror(request_id)

    # Step 3: Merge (API wins)
    merged = merge_api_and_yaml(api_data, yaml_data)

    if not merged:
        return {"success": False, "error": f"Request {request_id} not found", "status": "not_found"}

    # Update local YAML to reflect API state if needed
    if api_data is not None and yaml_data is not None:
        yaml_data.update({k: v for k, v in merged.items() if not k.startswith("_")})
        is_terminal = merged.get("status") in TERMINAL_STATUSES
        save_yaml_mirror(request_id, yaml_data, pending=not is_terminal)
        if is_terminal:
            move_yaml_to_completed(request_id)

    return {
        "success": True,
        "request_id": request_id,
        "status": merged.get("status", "unknown"),
        "operation_type": merged.get("operation_type", merged.get("type")),
        "agent_name": merged.get("agent_name", ""),
        "reason": merged.get("reason", merged.get("justification", "")),
        "requester": merged.get("requester"),
        "created_at": merged.get("created_at"),
        "decision": merged.get("decision"),
        "decision_comment": merged.get("decision_comment"),
        "decided_by": merged.get("decided_by"),
        "decided_at": merged.get("decided_at"),
        "scope": merged.get("scope", "local"),
        "api_synced": merged.get("api_synced", False),
        "_source": merged.get("_source", "unknown"),
    }


def list_requests(api: GovernanceAPI, status_filter: str = "pending") -> dict[str, Any]:
    """List GovernanceRequests. Queries API first, merges with local YAML."""
    api_requests: list[dict[str, Any]] = []
    local_requests: list[dict[str, Any]] = []

    # Step 1: Try API
    if status_filter == "pending":
        api_result = api.list_requests(status="pending")
    elif status_filter == "all":
        api_result = api.list_requests()
    else:
        api_result = api.list_requests(status=status_filter)

    if api_result is not None:
        api_requests = api_result

    # Step 2: Load local YAML
    if status_filter in ("pending", "all"):
        local_requests.extend(list_local_yaml(PENDING_DIR))
    if status_filter in ("all",):
        local_requests.extend(list_local_yaml(COMPLETED_DIR))

    # Step 3: Merge — API is authoritative, add any local-only requests
    api_ids = {r.get("request_id") for r in api_requests}
    merged: list[dict[str, Any]] = []

    for api_req in api_requests:
        merged.append({
            "request_id": api_req.get("request_id"),
            "operation_type": api_req.get("operation_type", api_req.get("type")),
            "agent_name": api_req.get("agent_name", ""),
            "status": api_req.get("status"),
            "requester": api_req.get("requester"),
            "created_at": api_req.get("created_at"),
            "decision": api_req.get("decision"),
            "decided_at": api_req.get("decided_at"),
            "api_synced": True,
            "_source": "api",
        })

    # Add local-only requests (not in API)
    for local_req in local_requests:
        req_id = local_req.get("request_id")
        if req_id and req_id not in api_ids:
            merged.append({
                "request_id": req_id,
                "operation_type": local_req.get("operation_type"),
                "agent_name": local_req.get("agent_name"),
                "status": local_req.get("status"),
                "requester": local_req.get("requester"),
                "created_at": local_req.get("created_at"),
                "decision": local_req.get("decision"),
                "decided_at": local_req.get("decided_at"),
                "api_synced": local_req.get("api_synced", False),
                "_source": "local-only",
            })

    # Sort by created_at (newest first)
    merged.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    pending_count = sum(1 for r in merged if r.get("status") == "pending")

    return {
        "success": True,
        "total_count": len(merged),
        "pending_count": pending_count,
        "api_available": api.available,
        "requests": merged,
    }


def respond_to_request(
    api: GovernanceAPI,
    request_id: str,
    decision: str,
    comment: str,
    decided_by: str = "user",
) -> dict[str, Any]:
    """Approve or reject a GovernanceRequest. Patches API first, mirrors to local YAML."""
    # Map simple decisions to GovernanceRequest state machine values
    # "approved" → "local-approved" (single-manager approval)
    # "rejected" → "rejected"
    if decision == "approved":
        api_status = "local-approved"
    elif decision == "rejected":
        api_status = "rejected"
    elif decision in VALID_STATUSES:
        api_status = decision
    else:
        return {"success": False, "error": f"Invalid decision: {decision}. Use 'approved' or 'rejected'."}

    timestamp = get_timestamp()
    update_payload = {
        "status": api_status,
        "decision": decision,
        "decision_comment": comment,
        "decided_by": decided_by,
        "decided_at": timestamp,
        "updated_at": timestamp,
    }

    # Step 1: PATCH API (primary authority)
    api_response = api.update(request_id, update_payload)
    api_synced = api_response is not None

    # Step 2: Update local YAML mirror
    yaml_data = load_yaml_mirror(request_id)
    if yaml_data:
        yaml_data.update(update_payload)
        yaml_data["api_synced"] = api_synced
        is_terminal = api_status in TERMINAL_STATUSES
        save_yaml_mirror(request_id, yaml_data, pending=not is_terminal)
        if is_terminal:
            move_yaml_to_completed(request_id)
    elif not api_synced:
        return {"success": False, "error": f"Request {request_id} not found (API unreachable, no local copy)"}

    # Step 3: Notify requester via AMP
    requester = (yaml_data or {}).get("requester", "unknown")
    operation_type = (yaml_data or {}).get("operation_type", "unknown")
    agent_name = (yaml_data or {}).get("agent_name", "unknown")

    notification_sent = send_amp_message(
        to=requester,
        subject=f"[GOVERNANCE {decision.upper()}] {operation_type}: {agent_name}",
        content={
            "type": "governance_response",
            "message": (
                f"GovernanceRequest {decision}.\n\n"
                f"Request ID: {request_id}\n"
                f"Decision: {decision.upper()}\n"
                f"Comment: {comment}\n"
                f"Decided by: {decided_by}"
            ),
            "request_id": request_id,
            "decision": decision,
        },
        priority="high",
    )

    return {
        "success": True,
        "request_id": request_id,
        "decision": decision,
        "api_status": api_status,
        "comment": comment,
        "decided_by": decided_by,
        "api_synced": api_synced,
        "notification_sent": notification_sent,
    }


def wait_for_decision(
    api: GovernanceAPI, request_id: str, timeout_seconds: int = 120,
) -> dict[str, Any]:
    """Poll for a GovernanceRequest decision. Checks API first, then local YAML."""
    start_time = time.time()
    poll_interval = 5

    # Verify request exists
    initial = get_request(api, request_id)
    if not initial.get("success"):
        return initial

    # Already decided?
    status = initial.get("status", "")
    if status in TERMINAL_STATUSES or status in APPROVED_STATUSES:
        return {
            "success": True,
            "request_id": request_id,
            "status": status,
            "decision": initial.get("decision"),
            "decision_comment": initial.get("decision_comment"),
            "decided_by": initial.get("decided_by"),
            "waited_seconds": 0,
        }

    while True:
        elapsed = time.time() - start_time
        if elapsed >= timeout_seconds:
            return {
                "success": False,
                "request_id": request_id,
                "status": "timeout",
                "waited_seconds": int(elapsed),
                "message": f"No decision within {timeout_seconds}s",
            }

        # Poll API first (authoritative)
        current = get_request(api, request_id)
        if current.get("success"):
            cur_status = current.get("status", "")
            if cur_status in TERMINAL_STATUSES or cur_status in APPROVED_STATUSES:
                return {
                    "success": True,
                    "request_id": request_id,
                    "status": cur_status,
                    "decision": current.get("decision"),
                    "decision_comment": current.get("decision_comment"),
                    "decided_by": current.get("decided_by"),
                    "waited_seconds": int(elapsed),
                }

        time.sleep(poll_interval)


def sync_local_to_api(api: GovernanceAPI) -> dict[str, Any]:
    """Sync all local-only (unsynced) YAML requests to the API."""
    if not api.available:
        # Test connectivity first
        api._request("GET", query={"limit": "1"})
        if not api.available:
            return {"success": False, "error": "API unreachable, cannot sync"}

    synced = 0
    failed = 0
    already_synced = 0

    for directory in [PENDING_DIR, COMPLETED_DIR]:
        for data in list_local_yaml(directory):
            req_id = data.get("request_id")
            if not req_id:
                continue

            if data.get("api_synced"):
                already_synced += 1
                continue

            # Check if it already exists in API
            existing = api.get(req_id)
            if existing is not None:
                # Already in API — just mark synced locally
                data["api_synced"] = True
                is_pending = directory == PENDING_DIR
                save_yaml_mirror(req_id, data, pending=is_pending)
                synced += 1
                continue

            # Submit to API
            result = api.submit(data)
            if result is not None:
                data["api_synced"] = True
                is_pending = directory == PENDING_DIR
                save_yaml_mirror(req_id, data, pending=is_pending)
                synced += 1
            else:
                failed += 1

    return {
        "success": failed == 0,
        "synced": synced,
        "failed": failed,
        "already_synced": already_synced,
        "api_available": api.available,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AMCOS Approval Manager - Dual-authority GovernanceRequest management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s create --type spawn --agent my-agent --reason "Need for task X" --requester amcos-chief-of-staff
  %(prog)s status --id GR-20260227-abcd1234
  %(prog)s list --status pending
  %(prog)s respond --id GR-20260227-abcd1234 --decision approved --comment "Go ahead"
  %(prog)s wait --id GR-20260227-abcd1234 --timeout 120
  %(prog)s sync
        """,
    )

    # Global flags
    parser.add_argument(
        "--api-only", action="store_true",
        help="Skip local YAML entirely (pure API mode)",
    )
    parser.add_argument(
        "--offline", action="store_true",
        help="Skip API entirely (pure YAML mode, for testing)",
    )
    parser.add_argument(
        "--api-url", type=str, default=None,
        help=f"AI Maestro API base URL (default: $AIMAESTRO_API or {DEFAULT_API_BASE})",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # create
    create_parser = subparsers.add_parser("create", help="Submit a new GovernanceRequest")
    create_parser.add_argument("--type", required=True, help="Operation type (spawn, deploy, terminate, etc.)")
    create_parser.add_argument("--agent", required=True, help="Agent or resource name")
    create_parser.add_argument("--reason", required=True, help="Justification for the request")
    create_parser.add_argument("--requester", default="amcos-chief-of-staff", help="Requesting agent")
    create_parser.add_argument("--scope", default="local", choices=["local", "cross-team"], help="Operation scope")
    create_parser.add_argument("--risk", default="low", choices=["low", "medium", "high", "critical"], help="Risk level")
    create_parser.add_argument("--source-cos", default=None, help="Source COS session name")
    create_parser.add_argument("--source-manager", default=None, help="Source manager session name")
    create_parser.add_argument("--target-cos", default=None, help="Target COS (cross-team)")
    create_parser.add_argument("--target-manager", default=None, help="Target manager (cross-team)")

    # status
    status_parser = subparsers.add_parser("status", help="Check GovernanceRequest status")
    status_parser.add_argument("--id", required=True, help="Request ID")

    # list
    list_parser = subparsers.add_parser("list", help="List GovernanceRequests")
    list_parser.add_argument("--status", default="pending", choices=["pending", "all"], help="Filter (default: pending)")

    # respond
    respond_parser = subparsers.add_parser("respond", help="Approve or reject a GovernanceRequest")
    respond_parser.add_argument("--id", required=True, help="Request ID")
    respond_parser.add_argument("--decision", required=True, choices=["approved", "rejected"], help="Decision")
    respond_parser.add_argument("--comment", required=True, help="Decision comment")
    respond_parser.add_argument("--decided-by", default="user", help="Who decided (default: user)")

    # wait
    wait_parser = subparsers.add_parser("wait", help="Wait for a decision on a GovernanceRequest")
    wait_parser.add_argument("--id", required=True, help="Request ID")
    wait_parser.add_argument("--timeout", type=int, default=120, help="Timeout in seconds (default: 120)")

    # sync
    subparsers.add_parser("sync", help="Sync local-only requests to the API")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # Initialize API client (disabled in offline mode)
    if args.offline:
        api = GovernanceAPI(api_base="http://0.0.0.0:0")  # will fail immediately
        api.available = False
    else:
        api = GovernanceAPI(api_base=args.api_url)

    result: dict[str, Any] = {}

    if args.command == "create":
        result = create_request(
            api=api,
            operation_type=args.type,
            agent_name=args.agent,
            reason=args.reason,
            requester=args.requester,
            scope=args.scope,
            risk_level=args.risk,
            source_cos=args.source_cos,
            source_manager=args.source_manager,
            target_cos=args.target_cos,
            target_manager=args.target_manager,
        )
    elif args.command == "status":
        result = get_request(api, args.id)
    elif args.command == "list":
        result = list_requests(api, status_filter=args.status)
    elif args.command == "respond":
        result = respond_to_request(
            api=api,
            request_id=args.id,
            decision=args.decision,
            comment=args.comment,
            decided_by=args.decided_by,
        )
    elif args.command == "wait":
        result = wait_for_decision(api, request_id=args.id, timeout_seconds=args.timeout)
    elif args.command == "sync":
        result = sync_local_to_api(api)

    # Output JSON
    print(json.dumps(result, indent=2, default=str))

    # Exit with appropriate code
    sys.exit(0 if result.get("success", True) else 1)


if __name__ == "__main__":
    main()
