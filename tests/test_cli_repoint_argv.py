"""Argv contract tests for the TRDD-8E8D6618 frozen-CLI repoints.

Pin the EXACT argv each repointed path hands the frozen CLI, by running the
real code against a stub CLI (env-overridable AIMAESTRO_AGENT_CLI /
AIMAESTRO_GOVERNANCE_CLI) that records its argv and answers JSON. No mocks of
the code under test — the subprocess really runs; only the CLI binary is
substituted. These exist because "the old suite passed" says nothing about a
brand-new CLI call: the verbs were read from the deployed source
(agent-commands.sh cmd_create; aimaestro-governance.sh approve/reject AID
path), and these tests keep the constructed argv pinned to that read.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def _stub_cli(tmp_path: Path) -> tuple[Path, Path]:
    """A fake CLI that records its argv to a file and prints a JSON object."""
    log = tmp_path / "argv.log"
    stub = tmp_path / "stub-cli.sh"
    stub.write_text(f'#!/bin/sh\necho "$@" >> "{log}"\necho \'{{"ok":true}}\'\n')
    stub.chmod(0o755)
    return stub, log


def _run(code: str, env_var: str, stub: Path) -> str:
    env = dict(os.environ, **{env_var: str(stub)})
    out = subprocess.run(
        [sys.executable, "-c", f"import sys; sys.path.insert(0, {str(SCRIPTS)!r}); {code}"],
        capture_output=True, text=True, env=env, cwd=REPO_ROOT,
    )
    assert out.returncode == 0, out.stderr
    return out.stdout


def test_add_agent_argv_matches_deployed_create_surface(tmp_path: Path) -> None:
    """add_agent hands the agent CLI exactly: create <name> --no-session --team <uuid> --title <gov-role> --plugin <plugin>."""
    stub, log = _stub_cli(tmp_path)
    out = _run(
        "import amcos_team_registry as r; import json;"
        "print(json.dumps(r.add_agent('TEAM-UUID','agent-x','programmer',"
        "'ai-maestro-programmer-agent','host')))",
        "AIMAESTRO_AGENT_CLI", stub,
    )
    assert json.loads(out)["success"] is True
    assert log.read_text().strip() == (
        "create agent-x --no-session --team TEAM-UUID "
        "--title member --plugin ai-maestro-programmer-agent"
    )


def test_decide_argv_matches_aid_approve_reject_surface(tmp_path: Path) -> None:
    """decide() hands the governance CLI exactly: 'approve <id>' / 'reject <id> --reason <r>' — never --password, never --approver/--rejector."""
    stub, log = _stub_cli(tmp_path)
    _run(
        "import amcos_approval_manager as m;"
        "api = m.GovernanceAPI();"
        "assert api.decide('REQ-1', 'rejected', 'nope') is not None;"
        "assert api.decide('REQ-2', 'approved') is not None",
        "AIMAESTRO_GOVERNANCE_CLI", stub,
    )
    assert log.read_text().splitlines() == [
        "reject REQ-1 --reason nope",
        "approve REQ-2",
    ]
