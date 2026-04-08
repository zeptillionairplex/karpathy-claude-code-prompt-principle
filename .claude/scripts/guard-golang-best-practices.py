#!/usr/bin/env python3
"""Hook: enforce Go best practices on Bash tool calls."""
import json
import re
import sys

def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool = payload.get("tool_name", "")
    if tool != "Bash":
        sys.exit(0)

    command = payload.get("tool_input", {}).get("command", "")

    # Only inspect commands that write/run Go files or go toolchain
    is_go_related = bool(
        re.search(r"\.go\b", command) or
        re.search(r"\bgo\s+(run|build|test|generate)\b", command)
    )
    if not is_go_related:
        sys.exit(0)

    violations = []

    # db-parameterized / sec-sql-injection
    # Detect fmt.Sprintf / fmt.Fprintf used to build SQL strings
    if re.search(r'fmt\.Sprintf[^)]*(?:SELECT|INSERT|UPDATE|DELETE|FROM|WHERE)', command, re.IGNORECASE):
        violations.append(
            "[db-parameterized] Never interpolate user input into SQL strings. "
            "Use parameterized queries instead of fmt.Sprintf."
        )

    # gin-no-global: block gin.Default()
    if re.search(r'gin\.Default\(\)', command):
        violations.append(
            "[gin-no-global] Never use gin.Default() in production. "
            "Use gin.New() with explicit middleware instead."
        )

    # gin-bind-should: block c.BindJSON
    if re.search(r'\.BindJSON\(', command):
        violations.append(
            "[gin-bind-should] Never use BindJSON (it hijacks error handling). "
            "Use ShouldBindJSON instead."
        )

    # err-no-panic: block panic() outside of main/init context
    # Heuristic: flag bare panic() calls in go run/build of non-main files
    if re.search(r'\bpanic\(', command) and not re.search(r'\bfunc\s+(?:main|init)\b', command):
        violations.append(
            "[err-no-panic] Never call panic() in library/service code. "
            "Return errors instead; panic only in main() or init()."
        )

    if violations:
        print("Go best-practices violations detected:\n", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        print(
            "\nFix these issues before running the command.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
