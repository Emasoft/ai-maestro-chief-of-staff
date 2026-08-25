"""Real (non-mocked) guard tests for the resource-check alert output shape.

TRDD-23C5566E item C: the alert path must carry a `terminalSequence` cue
(Claude Code 2.1.141+ hook output field) alongside the systemMessage warning,
and must stay non-blocking. Tested via the pure builder so no real resource
threshold has to be exceeded.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from amcos_resource_check import (  # noqa: E402
    ALERT_TERMINAL_SEQUENCE,
    build_alert_output,
)

_ALERTS = [{"resource": "CPU", "current": 93.2, "threshold": 80}]


def test_alert_output_carries_terminal_sequence() -> None:
    """Alert output includes the bell/title terminalSequence cue verbatim."""
    out = build_alert_output(_ALERTS)
    assert out["terminalSequence"] == ALERT_TERMINAL_SEQUENCE
    assert "\x07" in out["terminalSequence"], "no BEL — the cue would be silent"


def test_alert_output_warns_without_blocking() -> None:
    """Alert output keeps the warn-only contract: continue=True + the warning text."""
    out = build_alert_output(_ALERTS)
    assert out["continue"] is True
    assert "RESOURCE WARNING" in out["systemMessage"]
    assert "CPU" in out["systemMessage"]
