#!/usr/bin/env python3
"""Gitignore-aware file filtering for plugin validation.

Provides a GitignoreFilter class that loads .gitignore patterns once
and exposes helpers to filter os.walk, rglob, and iterdir results.
All validators should use this to skip gitignored files/directories.

Usage:
    gi = GitignoreFilter(plugin_root)
    for path in gi.walk_files(plugin_root, skip_dirs={"__pycache__"}):
        # path is a Path object, gitignored files are excluded
        ...

    for path in gi.rglob(plugin_root, "*.pyc"):
        # gitignored matches excluded
        ...
"""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path

# parse_gitignore / is_path_gitignored were inlined verbatim from the removed
# cpv_validation_common.py (local validator suite retired in favor of the
# remote CPV plugin — only these two pattern helpers were load-bearing here).


def parse_gitignore(gitignore_path: Path) -> list[str]:
    """Parse a .gitignore file and return list of patterns.

    Args:
        gitignore_path: Path to .gitignore file

    Returns:
        List of gitignore patterns (comments and empty lines stripped)
    """
    patterns: list[str] = []
    try:
        with open(gitignore_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue
                patterns.append(line)
    except (OSError, UnicodeDecodeError):
        pass
    return patterns


def is_path_gitignored(rel_path: str, patterns: list[str]) -> bool:
    """Check if a relative path matches any gitignore pattern.

    Args:
        rel_path: Relative path to check
        patterns: List of gitignore patterns

    Returns:
        True if path matches any pattern
    """
    # Normalize path separators
    rel_path = rel_path.replace("\\", "/")
    path_parts = rel_path.split("/")

    for pattern in patterns:
        # Handle negation (!) - un-ignore previously matched paths
        if pattern.startswith("!"):
            neg_pattern = pattern[1:]
            # If the path matches the negation pattern, it should NOT be ignored
            if fnmatch.fnmatch(rel_path, neg_pattern) or fnmatch.fnmatch(str(Path(rel_path).name), neg_pattern):
                return False
            continue

        # Handle directory-only patterns (ending with /)
        is_dir_pattern = pattern.endswith("/")
        if is_dir_pattern:
            pattern = pattern[:-1]

        # Handle patterns starting with /
        is_anchored = pattern.startswith("/")
        if is_anchored:
            pattern = pattern[1:]

        # Handle ** patterns properly for recursive directory matching
        if "**" in pattern:
            if pattern.startswith("**/"):
                # **/foo matches foo at any depth
                suffix = pattern[3:]  # e.g., "dist" from "**/dist"
                if (
                    fnmatch.fnmatch(rel_path, suffix)
                    or fnmatch.fnmatch(rel_path, f"*/{suffix}")
                    or f"/{suffix}" in f"/{rel_path}"
                ):
                    return True
                continue
            elif pattern.endswith("/**"):
                # build/** matches any file under the prefix directory
                prefix = pattern[:-3]  # e.g., "build" from "build/**"
                if rel_path.startswith(prefix + "/") or rel_path == prefix:
                    return True
                continue
            else:
                # General ** — replace with regex-like matching
                regex = pattern.replace(".", r"\.").replace("**", ".*").replace("*", "[^/]*").replace("?", "[^/]")
                if re.match(regex + "$", rel_path):
                    return True
                continue

        # Check if pattern matches any component or the full path
        if is_anchored:
            # Anchored patterns only match from root
            if fnmatch.fnmatch(rel_path, pattern):
                return True
        else:
            # Non-anchored patterns can match any component
            if fnmatch.fnmatch(rel_path, pattern):
                return True
            # Also check if any path component matches
            for part in path_parts:
                if fnmatch.fnmatch(part, pattern):
                    return True

    return False


class GitignoreFilter:
    """Gitignore-aware file filter — loads patterns once, reuses for all scans.

    Uses pathlib exclusively for cross-platform compatibility.
    """

    def __init__(self, plugin_root: Path) -> None:
        self.root = plugin_root.resolve()
        gitignore_path = self.root / ".gitignore"
        self.patterns = parse_gitignore(gitignore_path) if gitignore_path.is_file() else []

    def is_ignored(self, path: Path) -> bool:
        """Check if a path should be skipped based on .gitignore patterns."""
        if not self.patterns:
            return False
        try:
            # Use PurePosixPath-style forward slashes for gitignore matching
            rel = path.relative_to(self.root).as_posix()
        except ValueError:
            return False
        return is_path_gitignored(rel, self.patterns)

    def is_dir_ignored(self, dirpath: Path) -> bool:
        """Check if a directory should be skipped — appends trailing / for dir-only patterns."""
        if not self.patterns:
            return False
        try:
            rel = dirpath.relative_to(self.root).as_posix()
        except ValueError:
            return False
        # Check both with and without trailing slash (gitignore treats dir/ specially)
        return is_path_gitignored(rel, self.patterns) or is_path_gitignored(rel + "/", self.patterns)

    def _walk_pathlib(
        self,
        directory: Path,
        skip_dirs: set[str],
        skip_hidden: bool,
    ):
        """Recursive directory walk using pathlib only (cross-platform).

        Yields (dirpath: Path, subdirs: list[str], files: list[str]).
        Compatible with os.walk() return signature but uses Path objects.
        """
        subdirs: list[str] = []
        files: list[str] = []

        try:
            entries = sorted(directory.iterdir())
        except PermissionError:
            return

        for entry in entries:
            if entry.is_dir():
                if skip_hidden and entry.name.startswith("."):
                    continue
                if entry.name in skip_dirs:
                    continue
                if self.is_dir_ignored(entry):
                    continue
                subdirs.append(entry.name)
            elif entry.is_file():
                if not self.is_ignored(entry):
                    files.append(entry.name)

        yield str(directory), subdirs, files

        # Recurse into non-ignored subdirectories
        for subdir_name in subdirs:
            yield from self._walk_pathlib(directory / subdir_name, skip_dirs, skip_hidden)

    def walk(
        self,
        root: Path | None = None,
        skip_dirs: set[str] | None = None,
        skip_hidden: bool = True,
    ):
        """Gitignore-aware directory walk using pathlib (cross-platform).

        Yields (dirpath: str, dirnames: list[str], filenames: list[str]).
        Automatically prunes gitignored directories and files.
        """
        root = root or self.root
        extra_skip = skip_dirs or set()
        yield from self._walk_pathlib(root, extra_skip, skip_hidden)

    def rglob(self, pattern: str, root: Path | None = None):
        """Gitignore-aware rglob — yields Path objects that are not gitignored."""
        root = root or self.root
        for path in root.rglob(pattern):
            if not self.is_ignored(path):
                yield path

    def iterdir(self, directory: Path | None = None, skip_hidden: bool = False):
        """Gitignore-aware iterdir — yields Path objects that are not gitignored."""
        directory = directory or self.root
        for item in directory.iterdir():
            if skip_hidden and item.name.startswith("."):
                continue
            if not self.is_ignored(item):
                yield item
