# Context Management: /clear vs /compact

## The Rule

| Situation | Command |
|---|---|
| Current task is fully done, moving to a different task | `/clear` |
| Mid-task milestone — research done before implementation, debugging done before next feature | `/compact` |
| **Never** mid-implementation (loses variable names, file paths, partial state) | ❌ `/compact` banned |

## Why

Context accumulation degrades Claude performance over long sessions (Context Rot):
- Old instructions conflict with new ones
- Unrelated file contents dilute attention
- Token budget shrinks, causing important information to be missed

## /clear
- Wipes context completely
- Free, instant
- Forgets everything — only appropriate when switching to a new task

## /compact
- Summarizes and compresses current context
- Preserves key state (variable names, file paths, progress)
- Use only at milestones between distinct work phases

## Signal: When to Act

The `context-monitor` Stop hook detects usage and fires a desktop notification:
- **60%** → Consider `/compact` (if you're at a milestone, now is the time)
- **80%** → Run `/clear` or `/compact` immediately
