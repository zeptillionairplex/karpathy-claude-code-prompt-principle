#!/usr/bin/env python3
"""
PostToolUse hook: auto-analyze skills for hookable patterns.

Triggers:
  - Write/Edit on .claude/skills/*/SKILL.md → analyze that skill
  - Bash(npx skills add *) → scan all unreviewed skills

For each skill, calls Claude CLI to determine if any instruction
can be mechanically enforced via a hook (PreToolUse/PostToolUse).
If yes: writes a guard script + updates settings.json.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # project root
SKILLS_DIR = ROOT / ".claude" / "skills"
SCRIPTS_DIR = ROOT / ".claude" / "scripts"
SETTINGS_PATH = ROOT / ".claude" / "settings.json"
REVIEWED_LOG = SCRIPTS_DIR / ".hook-reviewed-skills.json"

ANALYSIS_PROMPT = """\
You analyze a Claude Code skill to find instructions that can be \
mechanically enforced via Claude Code hooks instead of relying on LLM memory.

Hookable means the skill has rules like:
- "Always check X before reading/writing files" → PreToolUse hook
- "Never run command Y" / "Block Z" → PreToolUse hook, exit 2
- "After tool Y completes, run W" → PostToolUse hook

Skill name: {name}
---
{content}
---

Reply with ONLY valid JSON, no prose:

If hookable:
{{
  "hookable": true,
  "reason": "one sentence",
  "script_name": "guard-{slug}.py",
  "script_code": "#!/usr/bin/env python3\\n# complete runnable python hook script\\n...",
  "hook_event": "PreToolUse",
  "hook_matcher": "Bash",
  "hook_entry": {{
    "type": "command",
    "command": "python .claude/scripts/guard-{slug}.py",
    "timeout": 10
  }}
}}

If not hookable:
{{"hookable": false, "reason": "one sentence"}}
"""


# ── helpers ─────────────────────────────────────────────────────────────────

def load_reviewed() -> set[str]:
    try:
        return set(json.loads(REVIEWED_LOG.read_text()))
    except Exception:
        return set()


def save_reviewed(reviewed: set[str]) -> None:
    REVIEWED_LOG.write_text(json.dumps(sorted(reviewed), indent=2))


def extract_json(text: str) -> dict | None:
    """Try to extract first JSON object from text."""
    # Try code fence first
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
    # Try bare JSON
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except Exception:
            pass
    return None


def call_claude(prompt: str) -> dict | None:
    try:
        r = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True, text=True, timeout=120,
            cwd=str(ROOT),
        )
        if r.returncode != 0:
            return None
        return extract_json(r.stdout)
    except FileNotFoundError:
        print("[skill-hook-analyzer] claude CLI not found — skipping.", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("[skill-hook-analyzer] claude CLI timed out.", file=sys.stderr)
    except Exception as e:
        print(f"[skill-hook-analyzer] error: {e}", file=sys.stderr)
    return None


def update_settings(event: str, matcher: str, entry: dict) -> None:
    settings = json.loads(SETTINGS_PATH.read_text())
    hooks = settings.setdefault("hooks", {})
    event_list = hooks.setdefault(event, [])

    group = next((g for g in event_list if g.get("matcher") == matcher), None)
    if group:
        # Avoid duplicate entries
        existing_cmds = {h.get("command") for h in group["hooks"]}
        if entry.get("command") not in existing_cmds:
            group["hooks"].append(entry)
    else:
        event_list.append({"matcher": matcher, "hooks": [entry]})

    SETTINGS_PATH.write_text(json.dumps(settings, indent=2))


def analyze_skill(skill_dir: Path, reviewed: set[str]) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return

    name = skill_dir.name
    if name in reviewed:
        return

    content = skill_file.read_text(encoding="utf-8")[:4000]
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    prompt = ANALYSIS_PROMPT.format(name=name, content=content, slug=slug)
    print(f"[skill-hook-analyzer] Analyzing '{name}'...", file=sys.stderr)

    result = call_claude(prompt)

    # Always mark as reviewed (even on failure) to avoid re-analyzing repeatedly
    reviewed.add(name)

    if not result:
        print(f"[skill-hook-analyzer] '{name}': no response from Claude.", file=sys.stderr)
        return

    if not result.get("hookable"):
        print(f"[skill-hook-analyzer] '{name}': not hookable — {result.get('reason', '')}", file=sys.stderr)
        return

    # Write guard script
    script_path = SCRIPTS_DIR / result["script_name"]
    script_code = result.get("script_code", "")
    if not script_code.strip():
        print(f"[skill-hook-analyzer] '{name}': hookable but script_code is empty.", file=sys.stderr)
        return

    script_path.write_text(script_code, encoding="utf-8")

    # Update settings.json
    update_settings(
        event=result.get("hook_event", "PreToolUse"),
        matcher=result.get("hook_matcher", "Bash"),
        entry=result["hook_entry"],
    )

    print(
        f"[skill-hook-analyzer] ✓ '{name}' → hook registered: "
        f"{result['script_name']} ({result['hook_event']}/{result['hook_matcher']})",
        file=sys.stderr,
    )


# ── entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {})
    reviewed = load_reviewed()

    if tool in ("Write", "Edit"):
        # Triggered by a skill file being written/edited
        file_path = inp.get("file_path", "").replace("\\", "/")
        if ".claude/skills/" not in file_path or not file_path.endswith("SKILL.md"):
            return
        skill_dir = Path(inp["file_path"]).parent
        # Force re-analysis on explicit edits
        reviewed.discard(skill_dir.name)
        analyze_skill(skill_dir, reviewed)

    elif tool == "Bash":
        # Triggered by npx skills add — scan all unreviewed skills
        command = inp.get("command", "")
        if "npx skills" not in command:
            return
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            if skill_dir.is_dir():
                analyze_skill(skill_dir, reviewed)

    save_reviewed(reviewed)


if __name__ == "__main__":
    main()
