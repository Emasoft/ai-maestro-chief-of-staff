#!/usr/bin/env python3
"""Run the plugin's whole test suite and print a readable result table.

This is the contributor-facing runner. The publish pipeline
(`scripts/publish.py`) invokes pytest directly
(`uv run --with pytest pytest tests/ -x -q`); this runner wraps the SAME
pytest run, then renders a Unicode-bordered table of every test function with
its one-line docstring description and outcome, and exits 0 on all-pass /
non-zero on any failure (so CI and a human get the same verdict).

Usage:
    uv run --with pytest python tests/run-all-tests.py
    # or, if pytest is already on the interpreter:
    python tests/run-all-tests.py
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = TESTS_DIR.parent

# ANSI colors (no dependency on a TTY check failing the run — colors are cosmetic).
GREEN, RED, YELLOW, DIM, RESET = "\033[92m", "\033[91m", "\033[93m", "\033[2m", "\033[0m"
STATUS_COLOR = {"PASS": GREEN, "FAIL": RED, "ERROR": RED, "SKIP": YELLOW}
# pytest verbose verb -> our fixed-width 5-char status cell
VERB = {"PASSED": "PASS", "FAILED": "FAIL", "ERROR": "ERROR", "SKIPPED": "SKIP"}

LINE_RE = re.compile(r"^(tests/[^:]+\.py)::([^\s]+)\s+(PASSED|FAILED|ERROR|SKIPPED)")


def _docstrings(test_files: set[str]) -> dict[tuple[str, str], str]:
    """Map (file, base_test_name) -> first docstring line, by importing each module."""
    out: dict[tuple[str, str], str] = {}
    sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
    for rel in test_files:
        path = PLUGIN_ROOT / rel
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            continue  # an import error surfaces as a pytest ERROR anyway
        for attr in dir(module):
            if attr.startswith("test_"):
                fn = getattr(module, attr)
                doc = (fn.__doc__ or "").strip().splitlines()
                out[(rel, attr)] = doc[0] if doc else ""
    return out


def _render(rows: list[tuple[str, str, str]], docs: dict[tuple[str, str], str]) -> None:
    """rows = list of (file, test_id, STATUS). Print the bordered table."""
    table = []
    for rel, test_id, status in rows:
        base = test_id.split("[", 1)[0]  # strip parametrize suffix for docstring lookup
        desc = docs.get((rel, base), "")
        table.append((test_id, status, desc))

    w_name = min(max((len(r[0]) for r in table), default=4), 48)
    w_desc = min(max((len(r[2]) for r in table), default=11), 60)
    w_name = max(w_name, len("Test"))
    w_desc = max(w_desc, len("Description"))

    def bar(left: str, mid: str, right: str, fill: str) -> str:
        return f"{left}{fill * (w_name + 2)}{mid}{fill * 8}{mid}{fill * (w_desc + 2)}{right}"

    print(bar("┏", "┳", "┓", "━"))
    print(f"┃ {'Test':<{w_name}} ┃ {'Status':<6} ┃ {'Description':<{w_desc}} ┃")
    print(bar("┡", "╇", "┩", "━"))
    for name, status, desc in table:
        color = STATUS_COLOR.get(status, "")
        nm = name if len(name) <= w_name else name[: w_name - 1] + "…"
        ds = desc if len(desc) <= w_desc else desc[: w_desc - 1] + "…"
        print(f"│ {nm:<{w_name}} │ {color}{status:<6}{RESET} │ {ds:<{w_desc}} │")
    print(bar("└", "┴", "┘", "─"))


def main() -> int:
    proc = subprocess.run(
        ["python", "-m", "pytest", "tests/", "-v", "--tb=short", "-p", "no:cacheprovider"],
        cwd=PLUGIN_ROOT,
        capture_output=True,
        text=True,
    )
    rows: list[tuple[str, str, str]] = []
    files: set[str] = set()
    for line in proc.stdout.splitlines():
        m = LINE_RE.match(line)
        if m:
            rel, test_id, verb = m.group(1), m.group(2), m.group(3)
            rows.append((rel, test_id, VERB[verb]))
            files.add(rel)

    if not rows:
        # pytest failed to collect — surface its output and fail loudly.
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        print(f"{RED}No tests collected — see pytest output above.{RESET}")
        return proc.returncode or 1

    docs = _docstrings(files)
    _render(rows, docs)

    passed = sum(1 for _, _, s in rows if s == "PASS")
    failed = sum(1 for _, _, s in rows if s in ("FAIL", "ERROR"))
    skipped = sum(1 for _, _, s in rows if s == "SKIP")
    total = len(rows)
    verdict = f"{GREEN}All green.{RESET}" if failed == 0 else f"{RED}{failed} failing.{RESET}"
    print(f"\n{passed}/{total} passed"
          + (f", {skipped} skipped" if skipped else "")
          + (f", {failed} failed" if failed else "")
          + f".  {verdict}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
