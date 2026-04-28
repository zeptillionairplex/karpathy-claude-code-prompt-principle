#!/usr/bin/env python3
"""
PreToolUse / Read + Grep + Glob: context-hygiene enforcement.
Exit 2 = block the tool call.
Exit 0 = allow.
"""
import json
import re
import sys

FORBIDDEN = [
    # Dependency trees
    (r'node_modules[\\/]',        "node_modules — use package.json instead"),
    (r'\bvendor[\\/]',            "vendor/ — use go.mod instead"),
    (r'(\.venv|venv)[\\/]',       ".venv/venv — use pyproject.toml instead"),
    (r'__pycache__[\\/]',         "__pycache__ — compiled bytecode, no value"),
    (r'(dist|build|out)[\\/]',    "build output — read source files instead"),
    (r'(\.next|\.nuxt)[\\/]',     "framework build cache"),
    (r'\.min\.(js|css)$',         "minified file — read source instead"),
    (r'\.map$',                   "source map — no value in context"),
    # Lock files
    (r'package-lock\.json$',      "lock file — use package.json"),
    (r'yarn\.lock$',              "lock file — use package.json"),
    (r'pnpm-lock\.yaml$',         "lock file — use package.json"),
    (r'\bgo\.sum$',               "lock file — use go.mod"),
    (r'poetry\.lock$',            "lock file — use pyproject.toml"),
    # Secrets
    (r'(^|[\\/])\.env(\.[^.\\/]+)?$', ".env file — contains secrets"),
    (r'\.(pem|key|crt|p12|pfx)$',    "certificate/key file — contains secrets"),
    # OS / editor noise
    (r'(^|[\\/])\.git[\\/]',      ".git internals — use git commands instead"),
    (r'\.DS_Store$',              "macOS metadata"),
    (r'Thumbs\.db$',              "Windows thumbnail cache"),
    (r'(^|[\\/])\.(idea|vscode)[\\/]', ".idea/.vscode — editor config, not code"),
    (r'\.(log|tmp|swp)$',         "temp/log file — no value in context"),
    # Generated / binary
    (r'\bcoverage[\\/]',          "coverage report — run tests to regenerate"),
    (r'\.nyc_output[\\/]',        "coverage output"),
    (r'\.(png|jpg|jpeg|gif|ico|webp|woff2?|ttf|eot|otf)$', "binary asset"),
    (r'\.(sqlite|db)$',           "binary DB — read schema/migration files instead"),
    (r'\.(lcov)$',                "coverage data"),
]


def check_path(path: str) -> tuple[bool, str]:
    for pattern, reason in FORBIDDEN:
        if re.search(pattern, path, re.IGNORECASE):
            return True, reason
    return False, ""


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {})

    # Read and Edit use file_path; Grep uses path
    path = inp.get("file_path") or inp.get("path") or ""
    if not path:
        sys.exit(0)

    blocked, reason = check_path(path)
    if blocked:
        msg = f"[context-hygiene] BLOCKED — {path}\nReason: {reason}"
        print(msg)
        sys.exit(2)


if __name__ == "__main__":
    main()
