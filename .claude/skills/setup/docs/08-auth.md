# Step 8: API Keys & Auth

Check each in order; emit guidance for whichever is missing:

- **OPENAI_API_KEY** unset:
  > "Codex dual-review needs OPENAI_API_KEY.
  > Get one: https://platform.openai.com/api-keys
  > Set it: add `export OPENAI_API_KEY=sk-...` to your shell profile."

- **Gemini** not authenticated:
  > "Run `gemini` once to complete the OAuth flow."

- **Codex** not authenticated:
  > "Run `codex login` to authenticate."
