---
globs: "**/*.test.ts, **/*.test.tsx, **/*.spec.ts, **/*_test.go, **/test_*.py, **/__tests__/**"
---
# 테스트 규칙

## 공통
- 테스트는 실제 동작을 검증. 구현 내부 로직 테스트 금지.
- 테스트 이름: "should [행동] when [조건]" 형식.
- 하나의 테스트 = 하나의 검증. 여러 assert 지양.

## TypeScript (Vitest / Jest)
- 컴포넌트 테스트: React Testing Library 사용.
- 사용자 관점으로 테스트 (getByRole, getByText 우선).
- API 호출 mock은 msw 사용.

## Go
- 테이블 드리븐 테스트 패턴 사용.
- DB 테스트는 실제 DB 사용 (mock 금지).
- 테스트 헬퍼는 testutils/ 패키지로 분리.

## Python (pytest)
- fixture로 공통 설정 관리.
- DB 테스트는 트랜잭션 롤백으로 격리.
- async 테스트는 pytest-asyncio 사용.
