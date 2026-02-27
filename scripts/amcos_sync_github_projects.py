#!/usr/bin/env python3
"""
ecos_sync_github_projects.py - Sync local project state with GitHub Projects boards.

Reads .emasoft/projects.json for local project state and uses the `gh` CLI tool
to interact with GitHub Projects API. Supports pull (fetch remote state), push
(update remote from local), and bidirectional sync with conflict detection.

Absorbs the functionality of ecos_compare_projects.py (--compare-only) and
ecos_verify_sync.py (--verify).

Dependencies: Python 3.8+ stdlib only (requires `gh` CLI installed and authenticated)

Usage:
    ecos_sync_github_projects.py [--project-root PATH] [--repo OWNER/REPO]
        [--direction pull|push|both] [--compare-only] [--verify] [--dry-run]

Exit codes:
    0 - Success
    1 - Error (gh not found, API error, sync conflict, file error)
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECTS_FILE = ".emasoft/projects.json"
DEFAULT_DIRECTION = "pull"
VALID_DIRECTIONS = ("pull", "push", "both")

# GitHub Projects v2 field names we care about
GH_STATUS_FIELD = "Status"
GH_PRIORITY_FIELD = "Priority"


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def log(msg: str, verbose: bool = True) -> None:
    """Print a log message to stderr if verbose is enabled."""
    if verbose:
        print(f"[sync] {msg}", file=sys.stderr)


def fail(msg: str) -> int:
    """Print an error and return exit code 1."""
    result = {"success": False, "error": msg}
    print(json.dumps(result, indent=2))
    return 1


def ensure_gh_cli() -> bool:
    """Check that `gh` CLI is available on PATH."""
    return shutil.which("gh") is not None


def run_gh(args: list[str], capture: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a `gh` CLI command and return the result.

    Args:
        args: Arguments to pass after `gh`.
        capture: Whether to capture stdout/stderr.

    Returns:
        CompletedProcess result.

    Raises:
        RuntimeError: If the command exits with a non-zero code.
    """
    cmd = ["gh"] + args
    result = subprocess.run(
        cmd,
        capture_output=capture,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        stderr_text = result.stderr.strip() if result.stderr else "(no stderr)"
        raise RuntimeError(
            f"gh command failed (exit {result.returncode}): {' '.join(cmd)}\n{stderr_text}"
        )
    return result


# ---------------------------------------------------------------------------
# Local state I/O
# ---------------------------------------------------------------------------


def get_projects_path(project_root: Path) -> Path:
    """Return the path to the local projects.json file."""
    return project_root / PROJECTS_FILE


def read_local_projects(project_root: Path) -> dict[str, Any]:
    """Read .emasoft/projects.json and return its contents.

    Args:
        project_root: Root directory of the project.

    Returns:
        Parsed JSON dict. If the file does not exist, returns a skeleton.
    """
    path = get_projects_path(project_root)
    if not path.exists():
        return {"projects": [], "last_synced": None, "schema_version": 1}
    content = path.read_text(encoding="utf-8")
    return json.loads(content)  # type: ignore[no-any-return]


def write_local_projects(project_root: Path, data: dict[str, Any]) -> None:
    """Write project data to .emasoft/projects.json.

    Creates parent directories if they do not exist.

    Args:
        project_root: Root directory of the project.
        data: Project data dictionary.
    """
    path = get_projects_path(project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    data["last_synced"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(data, indent=2, default=str) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# GitHub Projects v2 interaction via `gh` CLI
# ---------------------------------------------------------------------------


def detect_repo(project_root: Path, repo_override: str | None) -> str:
    """Detect the OWNER/REPO for the current repository.

    Args:
        project_root: Root directory to look for .git.
        repo_override: Explicit OWNER/REPO from CLI args.

    Returns:
        OWNER/REPO string.

    Raises:
        RuntimeError: If detection fails.
    """
    if repo_override:
        return repo_override
    # Try to get from gh, running from the project root directory
    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
            capture_output=True, text=True, timeout=30, cwd=str(project_root),
        )
        repo = result.stdout.strip()
        if repo:
            return repo
    except RuntimeError:
        pass
    raise RuntimeError(
        "Could not detect repository. Use --repo OWNER/REPO or run from a git repo."
    )


def list_gh_projects(repo: str) -> list[dict[str, Any]]:
    """List all GitHub Projects v2 associated with the repository.

    Args:
        repo: OWNER/REPO string.

    Returns:
        List of project dicts with at minimum 'number' and 'title'.
    """
    try:
        result = run_gh([
            "project", "list",
            "--owner", repo.split("/")[0],
            "--format", "json",
        ])
        data = json.loads(result.stdout)
        # gh project list --format json returns {"projects": [...]}
        projects = data.get("projects", [])
        return projects  # type: ignore[no-any-return]
    except (RuntimeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Failed to list GitHub Projects: {exc}") from exc


def fetch_gh_project_items(owner: str, project_number: int) -> list[dict[str, Any]]:
    """Fetch all items from a GitHub Project v2 board.

    Args:
        owner: GitHub organization or user that owns the project.
        project_number: The project number.

    Returns:
        List of item dicts.
    """
    try:
        result = run_gh([
            "project", "item-list", str(project_number),
            "--owner", owner,
            "--format", "json",
        ])
        data = json.loads(result.stdout)
        items = data.get("items", [])
        return items  # type: ignore[no-any-return]
    except (RuntimeError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"Failed to fetch items for project #{project_number}: {exc}"
        ) from exc


def create_gh_project_item(
    owner: str,
    project_number: int,
    title: str,
    body: str | None = None,
) -> dict[str, Any]:
    """Create a draft issue item in a GitHub Project v2.

    Args:
        owner: GitHub org/user owning the project.
        project_number: The project number.
        title: Item title.
        body: Optional item body text.

    Returns:
        Created item data.
    """
    cmd = [
        "project", "item-create", str(project_number),
        "--owner", owner,
        "--title", title,
        "--format", "json",
    ]
    if body:
        cmd.extend(["--body", body])
    result = run_gh(cmd)
    return json.loads(result.stdout)  # type: ignore[no-any-return]


# ---------------------------------------------------------------------------
# Comparison / diff logic
# ---------------------------------------------------------------------------


def normalize_title(title: str) -> str:
    """Normalize a project item title for comparison (lowercase, strip whitespace)."""
    return title.strip().lower()


def compare_local_remote(
    local_projects: dict[str, Any],
    remote_projects: list[dict[str, Any]],
    remote_items_by_project: dict[int, list[dict[str, Any]]],
) -> dict[str, Any]:
    """Compare local project state with remote GitHub Projects state.

    Args:
        local_projects: Parsed local projects.json data.
        remote_projects: List of remote project dicts from GitHub.
        remote_items_by_project: Map of project_number -> list of items.

    Returns:
        Diff dict with 'local_only', 'remote_only', 'common', and 'conflicts'.
    """
    diff: dict[str, Any] = {
        "local_only_projects": [],
        "remote_only_projects": [],
        "matched_projects": [],
        "item_diffs": [],
    }

    # Build lookup maps
    local_list = local_projects.get("projects", [])
    local_by_number: dict[int, dict[str, Any]] = {}
    for proj in local_list:
        num = proj.get("github_project_number")
        if num is not None:
            local_by_number[int(num)] = proj

    remote_by_number: dict[int, dict[str, Any]] = {}
    for proj in remote_projects:
        num = proj.get("number")
        if num is not None:
            remote_by_number[int(num)] = proj

    # Find local-only and remote-only projects
    local_nums = set(local_by_number.keys())
    remote_nums = set(remote_by_number.keys())

    for num in local_nums - remote_nums:
        diff["local_only_projects"].append(local_by_number[num])
    for num in remote_nums - local_nums:
        diff["remote_only_projects"].append(remote_by_number[num])

    # Compare items in matched projects
    for num in local_nums & remote_nums:
        match_info: dict[str, Any] = {
            "project_number": num,
            "title": remote_by_number[num].get("title", ""),
            "local_item_count": 0,
            "remote_item_count": 0,
            "local_only_items": [],
            "remote_only_items": [],
        }
        diff["matched_projects"].append(match_info)

        local_proj = local_by_number[num]
        local_items = local_proj.get("items", [])
        remote_items = remote_items_by_project.get(num, [])

        match_info["local_item_count"] = len(local_items)
        match_info["remote_item_count"] = len(remote_items)

        # Compare by normalized title
        local_titles = {normalize_title(it.get("title", "")): it for it in local_items}
        remote_titles = {normalize_title(it.get("title", "")): it for it in remote_items}

        for title in set(local_titles.keys()) - set(remote_titles.keys()):
            match_info["local_only_items"].append(local_titles[title])
        for title in set(remote_titles.keys()) - set(local_titles.keys()):
            match_info["remote_only_items"].append(remote_titles[title])

    return diff


# ---------------------------------------------------------------------------
# Sync operations
# ---------------------------------------------------------------------------


def sync_pull(
    project_root: Path,
    repo: str,
    dry_run: bool,
    verbose: bool,
) -> dict[str, Any]:
    """Pull remote GitHub Projects state into local projects.json.

    Args:
        project_root: Root directory of the project.
        repo: OWNER/REPO string.
        dry_run: If True, do not write changes.
        verbose: If True, print progress to stderr.

    Returns:
        Result dict with sync details.
    """
    owner = repo.split("/")[0]
    log(f"Fetching GitHub Projects for {repo}...", verbose)

    remote_projects = list_gh_projects(repo)
    log(f"Found {len(remote_projects)} remote project(s)", verbose)

    local_data = read_local_projects(project_root)
    updated_projects: list[dict[str, Any]] = []

    for rp in remote_projects:
        number = rp.get("number")
        if not isinstance(number, int):
            log(f"  Skipping project with non-integer number: {number}", verbose)
            continue
        title = rp.get("title", "")
        log(f"  Fetching items for project #{number}: {title}", verbose)

        items = fetch_gh_project_items(owner, number)
        log(f"    {len(items)} item(s)", verbose)

        project_entry: dict[str, Any] = {
            "github_project_number": number,
            "title": title,
            "description": rp.get("description", ""),
            "url": rp.get("url", ""),
            "items": items,
            "synced_at": datetime.now(timezone.utc).isoformat(),
        }
        updated_projects.append(project_entry)

    local_data["projects"] = updated_projects

    if not dry_run:
        write_local_projects(project_root, local_data)
        log(f"Wrote {len(updated_projects)} project(s) to {get_projects_path(project_root)}", verbose)
    else:
        log("[DRY RUN] Would write updated projects.json", verbose)

    return {
        "direction": "pull",
        "projects_synced": len(updated_projects),
        "dry_run": dry_run,
    }


def sync_push(
    project_root: Path,
    repo: str,
    dry_run: bool,
    verbose: bool,
) -> dict[str, Any]:
    """Push local project state changes to GitHub Projects board.

    Only creates items that exist locally but not remotely.

    Args:
        project_root: Root directory of the project.
        repo: OWNER/REPO string.
        dry_run: If True, do not create items.
        verbose: If True, print progress to stderr.

    Returns:
        Result dict with push details.
    """
    owner = repo.split("/")[0]
    local_data = read_local_projects(project_root)
    local_list = local_data.get("projects", [])

    if not local_list:
        return {"direction": "push", "error": "No local projects to push", "items_created": 0}

    items_created = 0

    for local_proj in local_list:
        number = local_proj.get("github_project_number")
        if number is None:
            log(f"  Skipping project without github_project_number: {local_proj.get('title', '?')}", verbose)
            continue

        log(f"Checking project #{number} for items to push...", verbose)

        # Fetch current remote items
        remote_items = fetch_gh_project_items(owner, number)
        remote_titles = {normalize_title(it.get("title", "")) for it in remote_items}

        local_items = local_proj.get("items", [])
        for item in local_items:
            title = item.get("title", "")
            if normalize_title(title) not in remote_titles:
                body = item.get("body", "")
                if dry_run:
                    log(f"  [DRY RUN] Would create item: {title}", verbose)
                else:
                    log(f"  Creating item: {title}", verbose)
                    create_gh_project_item(owner, number, title, body or None)
                items_created += 1

    return {
        "direction": "push",
        "items_created": items_created,
        "dry_run": dry_run,
    }


def sync_both(
    project_root: Path,
    repo: str,
    dry_run: bool,
    verbose: bool,
) -> dict[str, Any]:
    """Bidirectional sync with conflict detection.

    First pulls remote state, detects conflicts with local state, then pushes
    local-only items. Conflicts are reported but NOT auto-resolved (user must
    resolve manually).

    Args:
        project_root: Root directory of the project.
        repo: OWNER/REPO string.
        dry_run: If True, do not write or create anything.
        verbose: If True, print progress to stderr.

    Returns:
        Result dict with sync details and any conflicts.
    """
    owner = repo.split("/")[0]
    log("Starting bidirectional sync...", verbose)

    # Step 1: Read current local state
    local_data = read_local_projects(project_root)

    # Step 2: Fetch remote state
    remote_projects = list_gh_projects(repo)
    remote_items_by_project: dict[int, list[dict[str, Any]]] = {}
    for rp in remote_projects:
        number = rp.get("number")
        if number is not None:
            remote_items_by_project[number] = fetch_gh_project_items(owner, number)

    # Step 3: Compare
    diff = compare_local_remote(local_data, remote_projects, remote_items_by_project)

    conflicts: list[str] = []

    # Check for project-level conflicts (projects that exist only on one side)
    if diff["local_only_projects"]:
        for proj in diff["local_only_projects"]:
            conflicts.append(
                f"Project #{proj.get('github_project_number')} exists locally but not remotely"
            )
    if diff["remote_only_projects"]:
        for proj in diff["remote_only_projects"]:
            conflicts.append(
                f"Project #{proj.get('number')} exists remotely but not locally"
            )

    if conflicts:
        log(f"Found {len(conflicts)} conflict(s) - manual resolution required", verbose)
        return {
            "direction": "both",
            "conflicts": conflicts,
            "conflict_count": len(conflicts),
            "dry_run": dry_run,
            "synced": False,
        }

    # Step 4: No conflicts - do pull then push
    pull_result = sync_pull(project_root, repo, dry_run, verbose)
    push_result = sync_push(project_root, repo, dry_run, verbose)

    return {
        "direction": "both",
        "pull": pull_result,
        "push": push_result,
        "conflicts": [],
        "conflict_count": 0,
        "dry_run": dry_run,
        "synced": True,
    }


# ---------------------------------------------------------------------------
# Compare-only mode
# ---------------------------------------------------------------------------


def run_compare(
    project_root: Path,
    repo: str,
    verbose: bool,
) -> dict[str, Any]:
    """Compare local and remote state without syncing.

    Replaces the functionality of the former ecos_compare_projects.py script.

    Args:
        project_root: Root directory of the project.
        repo: OWNER/REPO string.
        verbose: If True, print progress to stderr.

    Returns:
        Comparison diff dict.
    """
    owner = repo.split("/")[0]
    log("Comparing local and remote project state...", verbose)

    local_data = read_local_projects(project_root)
    remote_projects = list_gh_projects(repo)

    remote_items_by_project: dict[int, list[dict[str, Any]]] = {}
    for rp in remote_projects:
        number = rp.get("number")
        if number is not None:
            log(f"  Fetching items for project #{number}...", verbose)
            remote_items_by_project[number] = fetch_gh_project_items(owner, number)

    diff = compare_local_remote(local_data, remote_projects, remote_items_by_project)
    diff["mode"] = "compare-only"
    return diff


# ---------------------------------------------------------------------------
# Verify mode
# ---------------------------------------------------------------------------


def run_verify(
    project_root: Path,
    repo: str,
    verbose: bool,
) -> dict[str, Any]:
    """Verify that local and remote state are in sync.

    Replaces the functionality of the former ecos_verify_sync.py script.

    Args:
        project_root: Root directory of the project.
        repo: OWNER/REPO string.
        verbose: If True, print progress to stderr.

    Returns:
        Verification result dict with 'in_sync' boolean.
    """
    diff = run_compare(project_root, repo, verbose)

    local_only = diff.get("local_only_projects", [])
    remote_only = diff.get("remote_only_projects", [])

    item_diffs_exist = False
    for matched in diff.get("matched_projects", []):
        if matched.get("local_only_items") or matched.get("remote_only_items"):
            item_diffs_exist = True
            break

    in_sync = (not local_only) and (not remote_only) and (not item_diffs_exist)

    return {
        "mode": "verify",
        "in_sync": in_sync,
        "local_only_project_count": len(local_only),
        "remote_only_project_count": len(remote_only),
        "item_diffs_exist": item_diffs_exist,
        "details": diff if not in_sync else None,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 for success, 1 for error.
    """
    parser = argparse.ArgumentParser(
        description="Sync local project state with GitHub Projects boards"
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=None,
        help="Project root directory (defaults to current directory)",
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=None,
        help="GitHub repository in OWNER/REPO format (auto-detected if omitted)",
    )
    parser.add_argument(
        "--direction",
        type=str,
        choices=VALID_DIRECTIONS,
        default=DEFAULT_DIRECTION,
        help=f"Sync direction: pull (remote->local), push (local->remote), both (default: {DEFAULT_DIRECTION})",
    )
    parser.add_argument(
        "--compare-only",
        action="store_true",
        help="Show differences without syncing (replaces ecos_compare_projects.py)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify sync state after operation (replaces ecos_verify_sync.py)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print progress messages to stderr",
    )

    args = parser.parse_args()

    # Resolve project root
    project_root = Path(args.project_root) if args.project_root else Path.cwd()
    if not project_root.is_dir():
        return fail(f"Project root is not a directory: {project_root}")

    # Check gh CLI
    if not ensure_gh_cli():
        return fail(
            "The `gh` CLI tool is not installed or not on PATH. "
            "Install it from https://cli.github.com/ and run `gh auth login`."
        )

    # Detect repo
    try:
        repo = detect_repo(project_root, args.repo)
    except RuntimeError as exc:
        return fail(str(exc))

    # Dispatch to the requested mode
    try:
        if args.compare_only:
            result = run_compare(project_root, repo, args.verbose)
        elif args.verify:
            result = run_verify(project_root, repo, args.verbose)
        else:
            if args.direction == "pull":
                result = sync_pull(project_root, repo, args.dry_run, args.verbose)
            elif args.direction == "push":
                result = sync_push(project_root, repo, args.dry_run, args.verbose)
            else:
                result = sync_both(project_root, repo, args.dry_run, args.verbose)
    except RuntimeError as exc:
        return fail(str(exc))

    # Output
    output = {"success": True, "timestamp": datetime.now(timezone.utc).isoformat(), "repo": repo}
    output.update(result)
    print(json.dumps(output, indent=2, default=str))

    # For verify mode, exit 1 if not in sync
    if args.verify and not result.get("in_sync", True):
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
