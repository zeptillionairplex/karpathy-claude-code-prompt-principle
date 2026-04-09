

각 Phase를 독립적으로 복붙할 수 있게, 이전 Phase의 맥락을 간략히 포함시켜서 작성하겠습니다.

---

# Phase 0: 브랜치 정리

```
이 프로젝트는 Claude Code 환경 자동 설정 저장소입니다.
v2 리팩토링을 시작합니다. 먼저 현재 main을 보존용 브랜치로 복사합니다.

## 작업

1. 현재 main 브랜치의 전체 내용을 `v1-full-stack` 브랜치로 복사합니다:
   git checkout -b v1-full-stack
   git push origin v1-full-stack

2. main으로 돌아옵니다:
   git checkout main

3. 확인:
   - git branch로 v1-full-stack 브랜치가 존재하는지 확인
   - git log --oneline -3으로 main과 v1-full-stack이 동일 커밋인지 확인

완료 후 결과를 알려주세요.
```

---

# Phase 1: Rules 파일 통합 (7개 → 3개)

```
v2 리팩토링 Phase 1입니다.
.claude/rules/ 내 7개 파일을 3개로 통합하여 토큰을 줄입니다.

## 작업

먼저 아래 7개 파일을 모두 읽어주세요:
- .claude/rules/behavior.md
- .claude/rules/architecture.md
- .claude/rules/code-style.md
- .claude/rules/codex.md
- .claude/rules/context-hygiene.md
- .claude/rules/context-management.md
- .claude/rules/qmd.md

읽은 후, 아래 병합 계획에 따라 작업합니다.

### (A) coding-principles.md 생성
behavior.md + code-style.md + architecture.md → .claude/rules/coding-principles.md
- Karpathy 4원칙(Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution)을 최상단에 배치
- 아키텍처 규칙(FSD, Clean Architecture 등)을 그 아래에 간결하게 병합
- 코드스타일(네이밍, 커밋, 문서화)을 마지막 섹션으로
- 3개 파일 간 중복되는 문장은 완전히 제거
- 목표: 원본 3개 합계 대비 40% 이상 토큰 감소

### (B) context-rules.md 생성
context-hygiene.md + context-management.md → .claude/rules/context-rules.md
- 금지 경로 목록(node_modules, dist, lock files 등)을 상단에
- /clear vs /compact 사용 규칙을 하단에
- 중복 제거

### (C) tools-rules.md 생성
codex.md + qmd.md → .claude/rules/tools-rules.md
- Codex 검증 규칙(언제 실행, 분류 기준 HIGH/WARN/INFO)
- QMD 검색 규칙(Glob/Grep 전에 QMD 먼저)
- 아래 Gemini CLI 규칙을 신규 추가:

"""
## Gemini CLI
- Gemini CLI는 UI/UX 리뷰, 대용량 컨텍스트 분석, 문서 요약에 활용
- omc team N:gemini 명령으로 병렬 실행 가능
- CCG 모드(/ccg)로 Codex+Gemini 결과를 Claude가 종합
"""

- 아래 OMC 도구 규칙도 신규 추가:

"""
## OMC (oh-my-claudecode)
- 멀티에이전트 오케스트레이션은 OMC를 통해 수행
- 간단한 작업은 OMC가 Haiku 에이전트에 자동 위임 (비용 절감)
- 병렬 실행이 필요하면 ultrawork 또는 team 키워드 사용
- 계획 수립은 /oh-my-claudecode:omc-plan 사용
"""

### (D) 원본 7개 파일 삭제
병합 완료 후 아래 파일을 삭제합니다:
- behavior.md, architecture.md, code-style.md
- codex.md, context-hygiene.md, context-management.md, qmd.md

### 진행 방식
1. 먼저 7개 파일을 읽고 중복 분석 결과를 보여주세요
2. 각 통합 파일의 초안 목차를 보여주세요
3. 확인하면 파일 생성 및 원본 삭제를 실행합니다
```

---

# Phase 2: Skills 정리 및 구조 변경

```
v2 리팩토링 Phase 2입니다.
Phase 1에서 rules를 7개→3개로 통합했습니다.
이번에는 스킬을 정리합니다.

## 2-1. 불필요한 스킬 폴더 삭제

.claude/skills/ 에서 아래 폴더를 삭제합니다:

| 삭제 대상 | 이유 |
|---|---|
| gstack/ | OMC의 architect/planner 에이전트로 대체 |
| gsd/ | OMC의 project-memory 훅으로 대체 |
| humanizer/ | 코딩 직접 기여 낮음 |
| installing-essential-skills/ | setup 스킬이 이미 처리 |
| evolving-docs/ | 우선순위 낮음 |
| new-domain/ | 상시 로드 불필요 |

삭제 전에 각 폴더의 존재 여부를 먼저 확인하고 목록을 보여주세요.

## 2-2. 언어별 스킬 → optional 디렉토리로 이동

.claude/skills/optional/ 디렉토리를 생성하고, 아래 스킬들을 이동합니다:

| 원래 위치 | 이동 위치 |
|---|---|
| vercel-react-best-practices/ | optional/react/ |
| n8n-workflow-patterns/ | optional/n8n/ |
| async-python-patterns/ | optional/python/ |
| python-project-structure/ | optional/python-structure/ |
| supabase-postgres-best-practices/ | optional/supabase/ |
| golang-best-practices/ | optional/golang/ |
| ui-ux-pro-max/ | optional/ui-ux/ |

이동 후, optional/ 안에 README.md를 생성합니다:

"""
# Optional Skills

프로젝트 기술 스택에 맞는 스킬만 선택적으로 활성화합니다.
/setup 실행 시 자동 감지되며, 수동으로 활성화하려면:

1. 원하는 스킬 폴더를 .claude/skills/ 루트로 복사 또는 심링크
2. Claude Code 재시작

| 폴더 | 대상 프로젝트 | 감지 파일 |
|---|---|---|
| react/ | React/Next.js | package.json 내 react |
| python/ | Python 비동기 | requirements.txt, pyproject.toml |
| python-structure/ | Python 프로젝트 구조 | requirements.txt, pyproject.toml |
| golang/ | Go | go.mod |
| supabase/ | Supabase | supabase/ 디렉토리, .env 내 SUPABASE |
| n8n/ | n8n 워크플로우 | n8n 관련 설정 파일 |
| ui-ux/ | UI/UX 집중 | 프론트엔드 프로젝트 |
"""

## 2-3. 최종 확인

정리 후 .claude/skills/ 루트에 남아있는 폴더 목록을 보여주세요.
아래 6개만 남아야 합니다:
- setup/
- power-stack/
- explore/
- implement/
- fix-bug/
- refactor/
- optional/ (하위에 7개 언어별 스킬)
```

---

# Phase 3: /setup 스킬 리팩토링

```
v2 리팩토링 Phase 3입니다.
Phase 1에서 rules 통합, Phase 2에서 스킬 정리를 완료했습니다.
이번에는 /setup 스킬의 SKILL.md를 v2 구조로 재작성합니다.

## 작업

.claude/skills/setup/SKILL.md를 읽은 후, 아래 내용으로 재작성합니다.
기존 파일의 유용한 에러 처리/안내 로직은 살리되, 설치 대상을 v2로 변경합니다.

### 새 /setup SKILL.md 내용 (아래를 기반으로 작성):

---
name: setup
description: v2 환경 설치 — OMC + Superpowers + Codex + Gemini CLI + QMD
---

# Environment Setup (v2)

원커맨드로 Claude Code 개발 환경을 구성합니다.

## Step 1: 시스템 요구사항 확인
아래가 설치되어 있는지 확인합니다. 없으면 안내 메시지 출력 후 중단:
- Node.js 18.18+ (`node --version`)
- Python 3.10+ (`python3 --version` 또는 `python --version`)
- Git (`git --version`)
- tmux (`tmux -V`) — OMC team 모드에 필요, 없으면 경고만 출력하고 계속 진행

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

```
# 1. OMC (멀티에이전트 오케스트레이션 — 핵심)
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode

# 2. Superpowers (TDD 및 실행 규율)
/plugin install superpowers@claude-plugins-official

# 3. Codex 플러그인 (이중 검증)
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex

# 4. commit-commands (커밋 자동화)
/plugin install commit-commands@claude-plugins-official

# 5. skill-creator (스킬 생성 도구)
/plugin install skill-creator@claude-plugins-official
```

## Step 4: 프로젝트 언어 감지 → 선택적 스킬 활성화
프로젝트 루트에서 아래 파일 존재 여부를 확인하고,
감지된 언어의 스킬만 .claude/skills/optional/에서 .claude/skills/로 심링크합니다:

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
qmd collection add . --name "$DIR" --mask "**/*.{ts,tsx,js,jsx,py,go,rs,md,json,yaml,yml,toml}"
qmd collection add .claude/rules --name rules --mask "**/*.md"
qmd update && qmd embed --chunk-strategy auto
```

## Step 7: API 키 및 인증 안내
아래를 순서대로 확인합니다:
- OPENAI_API_KEY 환경변수 미설정 시:
  "Codex 이중 검증을 사용하려면 OPENAI_API_KEY를 설정하세요.
   발급: https://platform.openai.com/api-keys
   설정: export OPENAI_API_KEY=sk-... 를 쉘 프로필에 추가"
- Gemini 인증 미완료 시:
  "Gemini CLI를 사용하려면 `gemini` 명령을 실행하여 OAuth 인증을 완료하세요."
- codex 인증 미완료 시:
  "codex login 을 실행하여 인증을 완료하세요."

## Step 8: 최종 확인
/context를 실행하여 결과를 보여줍니다.
목표 기준:
- Skills: 800 토큰 이하
- Memory files: 2,000 토큰 이하
- 총 고정 오버헤드: 15K 이하

기준 초과 시 원인을 분석하여 추가 최적화를 제안합니다.

---

### 기존 /setup에서 제거하는 항목:
- npx skills add ctsstc/get-shit-done-skills@gsd (OMC로 대체됨)
- npx skills add garrytan/gstack@gstack (OMC로 대체됨)
- frontend-design 플러그인 무조건 설치 (→ 프로젝트 감지 시에만)
- LSP 플러그인 3개 무조건 설치 (→ 프로젝트 감지 시에만)

작성 전에 기존 SKILL.md 내용을 보여주고,
v2 버전과의 차이점을 정리한 뒤 확인 후 작성합니다.
```

---

# Phase 4: power-stack 스킬 OMC 버전으로 재작성

```
v2 리팩토링 Phase 4입니다.
Phase 1~3에서 rules 통합, 스킬 정리, /setup 리팩토링을 완료했습니다.
이번에는 /power-stack 스킬을 OMC 기반으로 재작성합니다.

## 작업

.claude/skills/power-stack/SKILL.md를 읽은 후, 아래 구조로 재작성합니다.

### 기존 v1 파이프라인 (참고용):
Session 1: /gstack:autoplan → .planning/PROJECT.md
Session 2: /gsd:new-project → phase plans
Session 3+: superpowers:tdd + parallel agents → /codex:review
Final: /gstack:qa + /gstack:cso + /gstack:ship

### 새 v2 파이프라인:

---
name: power-stack
description: OMC 기반 Plan→Build→Verify 파이프라인
---

# Power Stack v2 (OMC Edition)

프로젝트의 전체 라이프사이클을 오케스트레이션합니다.
상태는 .omc/ 디렉토리에서 관리됩니다.

## Stage 1: 기획 (Deep Interview)
요구사항이 모호하면:
```
/oh-my-claudecode:deep-interview "프로젝트 설명"
```
→ 소크라테스식 질문으로 요구사항을 구체화
→ 결과: .omc/specs/deep-interview-{slug}.md

요구사항이 명확하면 Stage 2로 바로 진행합니다.

## Stage 2: 계획 (Consensus Plan)
```
/oh-my-claudecode:omc-plan --consensus "구체화된 요구사항"
```
→ 여러 에이전트가 합의 기반으로 계획 수립
→ 복잡한 프로젝트: /oh-my-claudecode:ralplan (반복 합의)

## Stage 3: 구현 (Parallel Execution + TDD)
규모에 따라 선택:

소규모 (파일 1~3개):
```
/oh-my-claudecode:autopilot "구현 작업"
```

중규모 (파일 4~10개):
```
/oh-my-claudecode:ultrawork "구현 작업"
```
→ 각 에이전트가 Superpowers의 TDD 절차를 따름
   (test-driven-development 스킬 자동 적용)

대규모 (파일 10개+):
```
/oh-my-claudecode:team 3:executor "구현 작업"
```
→ N개 에이전트 병렬 실행

멀티모델 검증이 필요하면:
```
/ccg "구현한 기능 리뷰"
```
→ Codex(아키텍처) + Gemini(UI/UX) + Claude(종합)

## Stage 4: 이중 검증 (Codex Review)
각 구현 wave 완료 후:
```
/codex:review
```
→ 분류: HIGH(즉시 수정), WARN(QA 전 수정), INFO(선택)

## Stage 5: QA (Autonomous Cycling)
```
/oh-my-claudecode:ultraqa "모든 기능이 정상 동작하는지 확인"
```
→ 목표 달성까지 자동 순환

## Stage 6: 최종 완료
```
Superpowers의 verification-before-completion 적용
Superpowers의 finishing-a-development-branch 적용
/commit-commands:commit-push-pr
```

## 컨텍스트 관리 원칙
- 각 Stage 시작 전 컨텍스트 50% 미만인지 확인
- 50% 이상이면 /compact 실행 후 진행
- Stage 간 전환 시 .omc/ 상태 파일로 맥락 유지

---

작성 전에 기존 power-stack SKILL.md를 보여주고,
v1→v2 변경 사항을 정리한 뒤 확인 후 작성합니다.
```

---

# Phase 5: Hooks 충돌 확인 및 정리

```
v2 리팩토링 Phase 5입니다.
Phase 1~4에서 rules, skills, setup, power-stack을 모두 정리했습니다.
이번에는 기존 Python 훅과 OMC 훅 간 충돌을 확인합니다.

## 작업

### 5-1. 현재 훅 설정 확인
.claude/settings.json을 읽고, 등록된 모든 훅을 나열해주세요.
각 훅의 이벤트(PreToolUse, PostToolUse, Stop 등)와 스크립트 경로를 표로 정리합니다.

### 5-2. OMC 훅과의 충돌 분석
OMC는 아래 훅을 자동 등록합니다. 기존 훅과 겹치는 이벤트가 있는지 확인합니다:

| OMC 훅 | 이벤트 |
|---|---|
| keyword-detector.mjs | UserPromptSubmit |
| skill-injector.mjs | UserPromptSubmit |
| session-start.mjs | SessionStart |
| project-memory-session.mjs | SessionStart |
| pre-tool-enforcer.mjs | PreToolUse |
| post-tool-verifier.mjs | PostToolUse |
| project-memory-posttool.mjs | PostToolUse |
| context-guard-stop.mjs | Stop |
| persistent-mode.cjs | Stop |
| pre-compact.mjs | PreCompact |
| session-end.mjs | SessionEnd |

### 5-3. 판정 기준에 따라 처리

유지 (OMC에 없는 고유 기능):
- guard-file-read.py (PreToolUse/Read — OMC의 pre-tool-enforcer와 이벤트는 같지만 기능이 다름. 금지 경로 차단)
- guard-bash.py (PreToolUse/Bash — 위험 명령 차단)
- doc-guardian.py (Stop — CLAUDE.md 드리프트 감지)
- qmd-worktree-sync.py (PostToolUse/Bash:git worktree — QMD 인덱스 동기화)

충돌 확인 후 제거 판단:
- context-monitor.py (Stop) ↔ OMC의 context-guard-stop.mjs (Stop)
  → 두 스크립트의 내용을 비교하여 기능이 겹치면 context-monitor.py 제거
  → 기능이 다르면(예: 경고 임계값이 다름) 둘 다 유지 가능한지 확인

- notify.py (SessionEnd) ↔ OMC의 session-end.mjs + Telegram/Discord 알림
  → OMC 알림 설정을 사용할 예정이면 notify.py 제거
  → 데스크톱 알림(notify.py)이 별도로 필요하면 유지

- skill-hook-analyzer.py (PostToolUse/Write)
  → 스킬 수가 47→12개로 줄었으므로 필요성 재평가
  → 불필요하면 제거

- sync-skills.py
  → v2 구조에서 스킬이 고정되므로 동적 동기화 불필요할 가능성 높음
  → 확인 후 판단

### 5-4. settings.json 업데이트
판정 결과에 따라 .claude/settings.json의 훅 목록을 수정합니다.
수정 전에 변경 계획을 보여주고 확인받습니다.

### 5-5. 제거된 스크립트 파일 삭제
settings.json에서 제거된 훅의 Python 스크립트를
.claude/scripts/에서도 삭제합니다.
```

---

# Phase 6: CLAUDE.md 업데이트

```
v2 리팩토링 Phase 6입니다.
Phase 1~5에서 rules, skills, setup, power-stack, hooks를 모두 정리했습니다.
이번에는 CLAUDE.md를 v2 구조에 맞게 업데이트합니다.

## 작업

프로젝트 루트의 CLAUDE.md를 읽은 후, 아래 기준으로 수정합니다.

### 변경 사항

1. rules 파일 포인터 수정:
   - 기존 7개 파일 참조 → 새 3개 파일로 변경
   - .claude/rules/coding-principles.md (Karpathy 원칙 + 아키텍처 + 코드스타일)
   - .claude/rules/context-rules.md (컨텍스트 위생 + 관리)
   - .claude/rules/tools-rules.md (Codex + QMD + Gemini + OMC)

2. OMC 관련 안내 추가:
   """
   ## Multi-Agent Orchestration
   이 프로젝트는 oh-my-claudecode(OMC)를 사용합니다.
   - 병렬 실행: ultrawork 또는 team 키워드 사용
   - 계획 수립: /oh-my-claudecode:omc-plan
   - 자율 실행: autopilot 키워드
   - 멀티모델: /ccg (Claude + Codex + Gemini)
   """

3. power-stack v2 파이프라인 간략 안내:
   """
   ## Development Pipeline
   /power-stack으로 전체 파이프라인 실행:
   deep-interview → omc-plan → ultrawork/team + TDD → codex:review → ultraqa → ship
   """

4. 기존 참조 제거:
   - gstack 관련 모든 참조 삭제
   - GSD 관련 모든 참조 삭제
   - "Power Stack pipeline — Plan → Manage → Build → Verify using gstack, GSD, and Superpowers TDD"
     → "Power Stack pipeline — Plan → Build → Verify using OMC orchestration + Superpowers TDD"

5. CLAUDE.md는 포인터 파일로서 최대한 간결하게 유지합니다.
   상세 내용은 rules 파일에 위임합니다.

수정 전에 현재 CLAUDE.md 내용과 변경 계획을 보여주고 확인받습니다.
```

---

# Phase 7: README.md 업데이트

```
v2 리팩토링 Phase 7입니다.
Phase 1~6에서 모든 내부 구조 변경이 완료되었습니다.
이번에는 README.md를 v2에 맞게 전면 재작성합니다.

## 작업

README.md를 읽은 후, 아래 구조로 재작성합니다.

### README.md v2 구조:

# Claude Code Prompt Principles v2

Karpathy의 4가지 코딩 원칙 기반 Claude Code 워크스페이스 설정.
OMC 멀티에이전트 오케스트레이션 + Superpowers TDD + 삼중 모델 검증.

## What You Get
- OMC 멀티에이전트 — 29개 전문 에이전트, 병렬 실행, 스마트 모델 라우팅(30~50% 비용 절감)
- Superpowers TDD — 테스트 먼저 → 구현 → 검증 엄격한 실행 루프
- 삼중 모델 검증 — Claude(구현) + Codex(리뷰) + Gemini(UI/대용량 분석)
- 컨텍스트 최적화 — v1 대비 44% 고정 오버헤드 감소 (21.5K → ~12K)
- Karpathy 4원칙 — rules로 자동 적용
- QMD 시맨틱 검색 — Glob/Grep 대신 BM25 + 벡터 검색
- 원커맨드 설치 — /setup으로 환경 자동 구성

## Requirements
- Claude Code CLI
- Node.js 18.18+
- Python 3.10+
- Git
- tmux (OMC team 모드용, 선택)
- OpenAI API key (Codex 검증용)
- Google 계정 (Gemini CLI OAuth 인증용)

## Quick Start
git clone https://github.com/zeptillionairplex/karpathy-claude-code-prompt-principle.git
cd karpathy-claude-code-prompt-principle
→ Claude Code 실행 후: /setup

## Project Structure
v2 디렉토리 구조를 반영합니다:
- .claude/rules/ (3개 파일)
- .claude/skills/ (핵심 6개 + optional/ 하위에 언어별)
- .claude/scripts/ (정리된 훅 스크립트)

## How It Works
5개 레이어 설명 (v2 기준):
- Layer 1: Rules (3개 파일)
- Layer 2: Skills (핵심 + 선택적)
- Layer 3: Hooks (기존 + OMC 훅)
- Layer 4: OMC 멀티에이전트 오케스트레이션 (NEW)
- Layer 5: 삼중 모델 검증 (Claude + Codex + Gemini)
- Layer 6: QMD 시맨틱 검색

## The Power Stack Pipeline v2
deep-interview → omc-plan → ultrawork/team + TDD → codex:review → ultraqa → ship

## v1에서 마이그레이션
기존 v1 전체 스택(gstack + GSD + Superpowers 모두 포함)이 필요하면:
git checkout v1-full-stack

## Manual Setup
v2 수동 설치 명령어 전체 나열

## Principles
Karpathy 4원칙 설명 (기존과 동일)

## License
MIT

---

작성 전에 현재 README.md와 v2 버전의 주요 차이점을 정리하여 보여주고,
확인 후 작성합니다.
```

---

# Phase 8: 커밋 & 검증

```
v2 리팩토링 최종 Phase입니다.
Phase 1~7에서 모든 변경이 완료되었습니다.
커밋하고 검증합니다.

## 작업

### 8-1. 변경 사항 전체 확인
git status와 git diff --stat으로 모든 변경 파일을 보여주세요.
의도하지 않은 변경이 없는지 확인합니다.

### 8-2. 커밋
git add -A
git commit -m "refactor: v2 lean setup — OMC-based, 44% context reduction

- Replace gstack+GSD with oh-my-claudecode multi-agent orchestration
- Add Gemini CLI + OMC plugin installation to /setup
- Merge 7 rules files into 3 (coding-principles, context-rules, tools-rules)
- Move 7 language-specific skills to optional/ with auto-detect on /setup
- Remove 6 redundant skills (gstack, gsd, humanizer, etc.)
- Rewrite power-stack pipeline for OMC (deep-interview → omc-plan → ultrawork → codex:review → ultraqa)
- Review hooks for OMC compatibility, remove conflicts
- Update CLAUDE.md pointers and README.md for v2
- Target: session startup overhead ~12K tokens (was ~21.5K)"

### 8-3. Push
git push origin main

### 8-4. 최종 검증
/context를 실행하여 결과를 보여주세요.

목표 기준:
| 항목 | 목표 |
|---|---|
| Skills 토큰 | ≤ 800 |
| Memory files 토큰 | ≤ 2,000 |
| 총 고정 오버헤드 | ≤ 15,000 |
| Free space | ≥ 152,000 |

기준을 초과하는 항목이 있으면 원인을 분석하고 추가 최적화를 제안합니다.

### 8-5. 결과 요약
아래 형식으로 v1 vs v2 비교표를 출력합니다:

| 항목 | v1 | v2 | 변화 |
|---|---|---|---|
| Rules 파일 | 7개 | 3개 | |
| Skills (상시) | 47개 | ~12개 | |
| Skills 토큰 | 2,800 | ? | |
| Memory 토큰 | 3,900 | ? | |
| 총 오버헤드 | 21,500 | ? | |
| Free space | 145,500 | ? | |
| 오케스트레이션 | 없음 | OMC | |
| 모델 | Claude+Codex | Claude+Codex+Gemini | |
```

---

총 9개 프롬프트(Phase 0~8)입니다. 각 Phase 실행 후 컨텍스트가 50%를 넘으면 `/compact`를 한 번 해주시고 다음 Phase로 넘어가시면 됩니다. 특히 **Phase 1(rules 읽기)과 Phase 3(setup 리팩토링)에서 컨텍스트가 많이 찰 수 있으니** 그 직후에 `/compact` 하는 것을 추천합니다.