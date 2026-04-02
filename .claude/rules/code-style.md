# Global Code Style
<!-- No condition — always loaded -->

## Naming
- Variables/functions: camelCase
- Constants: UPPER_SNAKE_CASE
- Files: kebab-case
- Classes/Types/Interfaces: PascalCase

## Commit Messages
- Conventional Commits: `type(scope): message`
- Types: feat, fix, refactor, test, docs, chore

## Documentation Writing
- Always apply `/humanizer` when writing or editing any user-facing text:
  CLAUDE.md files, PR descriptions, README, comments intended for humans.
- Do not apply to inline code comments that describe logic.

## General
- Single responsibility per function. Split if over 20 lines.
- No magic numbers — extract to named constants.
- Comments explain "why", not "what". Code explains itself.
