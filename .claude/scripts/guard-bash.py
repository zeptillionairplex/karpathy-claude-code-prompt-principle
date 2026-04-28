#!/usr/bin/env python3
"""
PreToolUse / Bash: block dangerous commands unconditionally.
Exit 2 = block. Exit 0 = allow.

Rules enforced (from behavior.md, database.md, git safety):
- No force push to main/master
- No --no-verify (hook bypass)
- No git reset --hard
- No git clean -f/-fd/-fx
- No git branch -D main/master
- No DROP TABLE / TRUNCATE without explicit confirmation
- No DELETE FROM without WHERE
- No rm -rf targeting root or project root
- No .env file staging in git
"""
import json
import re
import sys

# (pattern, explanation)
BLOCKED: list[tuple[str, str]] = [
    # Git: force push to protected branches
    (
        r'git\s+push\s+.*--force(-with-lease)?\b.*\b(main|master|HEAD)\b',
        "Force push to main/master is blocked. Use a feature branch.",
    ),
    (
        r'git\s+push\s+.*\b(main|master)\b.*--force(-with-lease)?\b',
        "Force push to main/master is blocked. Use a feature branch.",
    ),
    (
        r'git\s+push\s+(-f)\b.*\b(main|master)\b',
        "Force push to main/master is blocked. Use a feature branch.",
    ),
    # Git: hook bypass
    (
        r'git\s+.*--no-verify',
        "--no-verify skips pre-commit hooks. Fix the underlying issue instead.",
    ),
    # Git: destructive resets
    (
        r'git\s+reset\s+--hard',
        "git reset --hard destroys uncommitted work. Ask the user to confirm first.",
    ),
    # Git: untracked file deletion
    (
        r'git\s+clean\s+.*-[a-zA-Z]*f',
        "git clean -f deletes untracked files permanently. Ask the user to confirm first.",
    ),
    # Git: delete protected branch
    (
        r'git\s+branch\s+(-D|-d\s+--force)\s+(main|master)\b',
        "Deleting main/master branch is blocked.",
    ),
    # Git: staging .env files
    (
        r'git\s+(add|stage)\s+.*\.env\b',
        ".env contains secrets. Never stage it. Check .gitignore.",
    ),
    # SQL: destructive without WHERE
    (
        r'\bDROP\s+TABLE\b',
        "DROP TABLE requires explicit user confirmation. Ask first.",
    ),
    (
        r'\bTRUNCATE\s+(TABLE\s+)?\w+',
        "TRUNCATE requires explicit user confirmation. Ask first.",
    ),
    (
        r'\bDELETE\s+FROM\s+\w+\s*;',
        "DELETE without WHERE clause detected. Add WHERE or ask the user to confirm.",
    ),
    # Shell: rm -rf on dangerous targets
    (
        r'rm\s+-[a-zA-Z]*r[a-zA-Z]*f\s+/',
        "rm -rf on root path is blocked unconditionally.",
    ),
    (
        r'rm\s+-[a-zA-Z]*r[a-zA-Z]*f\s+\.\s*$',
        "rm -rf . (current directory) is blocked. Specify exact paths.",
    ),
]


def main() -> None:
    try:
        data = json.load(sys.stdin)
        command = data.get("tool_input", {}).get("command", "")
    except Exception:
        sys.exit(0)

    for pattern, reason in BLOCKED:
        if re.search(pattern, command, re.IGNORECASE):
            print(f"[guard-bash] BLOCKED\n{reason}\n\nCommand was:\n  {command}")
            sys.exit(2)


if __name__ == "__main__":
    main()
