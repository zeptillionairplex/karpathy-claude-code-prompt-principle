# 전역 코딩 스타일 규칙
<!-- 조건 없음 — 항상 로드됨 -->

## 네이밍
- 변수/함수: camelCase
- 상수: UPPER_SNAKE_CASE
- 파일: kebab-case
- 클래스/타입/인터페이스: PascalCase

## 커밋 메시지
- Conventional Commits 형식: `type(scope): message`
- type: feat, fix, refactor, test, docs, chore

## 공통 원칙
- 함수는 단일 책임. 20줄 초과 시 분리 검토.
- 매직 넘버 금지 — 상수로 추출.
- 주석은 "왜"만. "무엇"은 코드가 설명.
