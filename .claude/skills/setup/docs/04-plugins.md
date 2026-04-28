# Step 4: Claude Code Plugins

Skip any plugin already installed. Install order matters — OMC first:

```bash
# 1. OMC (multi-agent orchestration — core)
claude plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
claude plugin install oh-my-claudecode

# 2. Superpowers (TDD + execution discipline)
claude plugin install superpowers@claude-plugins-official

# 3. Codex plugin (dual-review)
claude plugin marketplace add openai/codex-plugin-cc
claude plugin install codex@openai-codex

# 4. commit-commands (commit automation)
claude plugin install commit-commands@claude-plugins-official

# 5. skill-creator (skill authoring)
claude plugin install skill-creator@claude-plugins-official
```
