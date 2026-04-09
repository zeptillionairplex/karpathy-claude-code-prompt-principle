---
name: power-stack
description: Use when starting any non-trivial software project from scratch, or resuming one across sessions. Routes to gstack (planning), GSD (project management), Superpowers TDD (implementation), and gstack QA (verification) based on current lifecycle stage.
---

# Power Stack v2 (OMC Edition)

프로젝트의 전체 라이프사이클을 오케스트레이션합니다.
상태는 `.omc/` 디렉토리에서 관리됩니다.

## Step 0: 상태 확인 (매 세션 시작 시)

```bash
ls .omc/ 2>/dev/null || echo "No state — starting Stage 1"
```

- `.omc/` 없음 → Stage 1부터 시작
- `.omc/` 있음 → 마지막 상태 파일 확인 후 "계속할까요, 재시작할까요?" 질문

---

## Stage 1: 기획 (Deep Interview)

요구사항이 모호하면:
```
/oh-my-claudecode:deep-interview "프로젝트 설명"
```
→ 소크라테스식 질문으로 요구사항을 구체화
→ 결과: `.omc/specs/deep-interview-{slug}.md`

요구사항이 명확하면 Stage 2로 바로 진행.

## Stage 2: 계획 (Consensus Plan)

```
/oh-my-claudecode:omc-plan --consensus "구체화된 요구사항"
```
→ 여러 에이전트가 합의 기반으로 계획 수립
→ 복잡한 프로젝트: `/oh-my-claudecode:ralplan` (반복 합의)

## Stage 3: 구현 (Parallel Execution + TDD)

각 에이전트는 `superpowers:test-driven-development` 절차를 따름.

규모에 따라 선택:

**소규모** (파일 1~3개):
```
/oh-my-claudecode:autopilot "구현 작업"
```

**중규모** (파일 4~10개):
```
/oh-my-claudecode:ultrawork "구현 작업"
```

**대규모** (파일 10개+):
```
/oh-my-claudecode:team 3:executor "구현 작업"
```

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
→ HIGH → 즉시 수정 · WARN → QA 전 수정 · INFO → 선택

## Stage 5: QA (Autonomous Cycling)

```
/oh-my-claudecode:ultraqa "모든 기능이 정상 동작하는지 확인"
```
→ 목표 달성까지 자동 순환

## Stage 6: 최종 완료

```
superpowers:verification-before-completion
superpowers:finishing-a-development-branch
/commit-commands:commit-push-pr
```

---

## 규칙

- 이 스킬은 라우팅만 함 — 직접 구현하지 않음
- 각 Stage 진입 전 컨텍스트 50% 미만 확인. 50% 이상이면 `/compact` 후 진행
- QMD를 모든 코드베이스 쿼리에 우선 사용
- 서브에이전트는 해당 작업 컨텍스트만 전달, 전체 히스토리 전달 금지
- 문서/포매팅/주석 작업은 Haiku 에이전트에 위임
