#!/usr/bin/env python3
"""
Hook: auto-sync git worktrees with QMD.
- git worktree add  → register collection + qmd update (BM25 only, no embed)
- git worktree remove → deregister collection
Reads PostToolUse JSON from stdin. Fails silently if QMD is unavailable.
"""
import json
import sys
import subprocess
import shlex
import os


def parse_worktree_path(parts: list[str], subcommand: str) -> str | None:
    """Extract worktree path from parsed git worktree command."""
    try:
        idx = parts.index("worktree")
        if parts[idx - 1] != "git" or parts[idx + 1] != subcommand:
            return None
        for arg in parts[idx + 2:]:
            if not arg.startswith("-"):
                return os.path.abspath(arg)
    except (ValueError, IndexError):
        pass
    return None


def run(cmd: list[str], timeout: int = 60) -> bool:
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=timeout)
        return True
    except Exception:
        return False


def register(worktree_path: str) -> None:
    name = f"worktree-{os.path.basename(worktree_path)}"
    mask = "**/*.{ts,tsx,js,jsx,py,go,rs,md,json,yaml,yml,toml}"
    if run(["qmd", "collection", "add", worktree_path, "--name", name, "--mask", mask], timeout=30):
        if run(["qmd", "update"], timeout=60):
            print(f"QMD: registered '{name}' (BM25, no embed)", file=sys.stderr)


def deregister(worktree_path: str) -> None:
    name = f"worktree-{os.path.basename(worktree_path)}"
    if run(["qmd", "collection", "remove", name], timeout=30):
        print(f"QMD: removed '{name}'", file=sys.stderr)


def main() -> None:
    try:
        data = json.load(sys.stdin)
        command = data.get("tool_input", {}).get("command", "")
        parts = shlex.split(command)
    except Exception:
        return

    if "worktree" not in parts:
        return

    if "add" in parts:
        path = parse_worktree_path(parts, "add")
        if path:
            register(path)
    elif "remove" in parts:
        path = parse_worktree_path(parts, "remove")
        if path:
            deregister(path)


if __name__ == "__main__":
    main()
