---
name: setup
description: v2 환경 설치 — OMC + Superpowers + Codex + Gemini CLI + QMD
---

# Environment Setup (v2)

원커맨드로 Claude Code 개발 환경을 구성합니다.

## Step 1: 시스템 요구사항 확인

아래가 설치되어 있는지 확인합니다. 없으면 안내 메시지 출력 후 중단:

```bash
node --version    # 18.18+ 필요
python3 --version || python --version   # 3.10+ 필요
git --version     # 필수
tmux -V           # OMC team 모드에 필요 — 없으면 경고만 출력하고 계속 진행
```

tmux 외 나머지가 하나라도 없으면 설치 안내 후 중단합니다.

## Step 2: CLI 도구 설치

각각 이미 설치되어 있으면 건너뜁니다:

```bash
# Codex CLI
which codex || npm install -g @openai/codex

# Gemini CLI
which gemini || npm install -g @google/gemini-cli

# QMD (코드베이스 검색)
which qmd || npm install -g @tobilu/qmd
```

## Step 3: Claude Code 플러그인 설치

이미 설치된 플러그인은 건너뜁니다.
설치 순서가 중요합니다 — OMC를 먼저 설치합니다:

```bash
# 1. OMC (멀티에이전트 오케스트레이션 — 핵심)
claude plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
claude plugin install oh-my-claudecode

# 2. Superpowers (TDD 및 실행 규율)
claude plugin install superpowers@claude-plugins-official

# 3. Codex 플러그인 (이중 검증)
claude plugin marketplace add openai/codex-plugin-cc
claude plugin install codex@openai-codex

# 4. commit-commands (커밋 자동화)
claude plugin install commit-commands@claude-plugins-official

# 5. skill-creator (스킬 생성 도구)
claude plugin install skill-creator@claude-plugins-official
```

## Step 4: 프로젝트 언어 감지 → 선택적 스킬 활성화

프로젝트 루트에서 아래 파일 존재 여부를 확인하고,
감지된 언어의 스킬만 `.claude/skills/optional/`에서 `.claude/skills/`로 심링크합니다:

| 감지 파일 | 활성화 스킬 | 추가 플러그인 |
|---|---|---|
| package.json 내 "react" 또는 tsconfig.json | optional/react/ | typescript-lsp 플러그인 |
| requirements.txt 또는 pyproject.toml | optional/python/, optional/python-structure/ | pyright-lsp 플러그인 |
| go.mod | optional/golang/ | gopls-lsp 플러그인 |
| supabase/ 디렉토리 또는 .env 내 SUPABASE | optional/supabase/ | — |
| n8n 관련 설정 파일 | optional/n8n/ | — |
| 프론트엔드 프로젝트 감지 시 | optional/ui-ux/ | frontend-design 플러그인 |

감지되지 않은 언어의 스킬은 건너뜁니다.
감지 결과를 사용자에게 보여주고 확인받습니다.

## Step 5: OMC 초기 설정

```
/oh-my-claudecode:omc-setup --local
```

## Step 6: QMD 인덱스 생성

```bash
DIR=$(basename "$PWD")
qmd collection add . --name "$DIR" --mask "**/*.{ts,tsx,js,jsx,py,go,rs,md,json,yaml,yml,toml}" 2>/dev/null || true
qmd collection add .claude/rules --name rules --mask "**/*.md" 2>/dev/null || true
qmd context add "qmd://$DIR" "Claude Code prompt engineering principles and workflow setup" 2>/dev/null || true
qmd context add "qmd://rules" "Claude Code behavioral and architecture rules" 2>/dev/null || true
qmd update && qmd embed --chunk-strategy auto
```

Note: `qmd embed`는 첫 실행 시 ~2GB 로컬 모델을 다운로드합니다. 정상입니다.

QMD MCP 서버 등록 (`~/.claude/.mcp.json`):

```json
{
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

등록 후 Claude Code를 재시작해야 MCP가 활성화됩니다.

## Step 7: API 키 및 인증 안내

아래를 순서대로 확인합니다:

- **OPENAI_API_KEY** 환경변수 미설정 시:
  > "Codex 이중 검증을 사용하려면 OPENAI_API_KEY를 설정하세요.
  > 발급: https://platform.openai.com/api-keys
  > 설정: `export OPENAI_API_KEY=sk-...` 를 쉘 프로필에 추가"

- **Gemini** 인증 미완료 시:
  > "`gemini` 명령을 실행하여 OAuth 인증을 완료하세요."

- **Codex** 인증 미완료 시:
  > "`codex login` 을 실행하여 인증을 완료하세요."

## Step 8: 최종 확인

`/context`를 실행하여 결과를 보여줍니다.
목표 기준:

- Skills: 800 토큰 이하
- Memory files: 2,000 토큰 이하
- 총 고정 오버헤드: 15K 이하

기준 초과 시 원인을 분석하여 추가 최적화를 제안합니다.
