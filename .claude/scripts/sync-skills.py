#!/usr/bin/env python3
"""
Sync .claude/rules/skills.md when new skills are installed.
Run after: npx skills add <repo>
Appends any skills not yet in the registry to a "Newly Installed" section.
"""
import os
import re
import sys


SKILLS_DIR = ".claude/skills"
OUTPUT = ".claude/rules/skills.md"


def extract_description(skill_md_path):
    try:
        with open(skill_md_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return ""

    # Try multi-line block scalar (description: |)
    m = re.search(
        r"^description:\s*\|\s*\n((?:[ \t]+.+\n?)+)",
        content,
        re.MULTILINE,
    )
    if m:
        desc = re.sub(r"\s+", " ", m.group(1)).strip()
        return desc[:120]

    # Try inline value
    m = re.search(r"^description:\s*(.+)", content, re.MULTILINE)
    if m:
        desc = re.sub(r"\s+", " ", m.group(1)).strip()
        return desc[:120]

    return ""


def main():
    if not os.path.isdir(SKILLS_DIR):
        sys.exit(0)
    if not os.path.isfile(OUTPUT):
        sys.exit(0)

    with open(OUTPUT, "r", encoding="utf-8") as f:
        current = f.read()

    # Collect already-registered skill names from backtick entries like `/name`
    registered = set(re.findall(r"`/([^`\n]+)`", current))

    new_entries = []
    for name in sorted(os.listdir(SKILLS_DIR)):
        skill_md = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        if name in registered:
            continue
        desc = extract_description(skill_md) or "(no description)"
        new_entries.append((name, desc))

    if not new_entries:
        sys.exit(0)

    with open(OUTPUT, "a", encoding="utf-8") as f:
        f.write("\n## Newly Installed\n\n")
        f.write("| Skill | Purpose |\n")
        f.write("|-------|----------|\n")
        for name, desc in new_entries:
            f.write(f"| `/{name}` | {desc} |\n")

    print(f"sync-skills: added {len(new_entries)} skill(s) to {OUTPUT}")


if __name__ == "__main__":
    main()
