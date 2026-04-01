---
globs: "**/*.tsx, **/*.ts, **/components/**, **/pages/**, **/hooks/**"
---
# React / TypeScript 규칙

## 컴포넌트
- 함수형 컴포넌트 + hooks만 사용. 클래스 컴포넌트 금지.
- 컴포넌트 파일 1개 = 컴포넌트 1개 원칙.
- Props 타입은 interface로 선언, 파일 상단에 위치.

## 상태 관리
- 로컬 상태: useState / useReducer
- 서버 상태: React Query (useQuery, useMutation)
- 전역 상태: Zustand — 도메인당 store 1개

## 스타일
- Tailwind CSS 사용. 인라인 style 금지.
- 조건부 클래스는 clsx 또는 cn() 유틸 사용.

## 타입
- any 금지. unknown 사용 후 타입 가드.
- API 응답 타입은 반드시 정의.
- non-null assertion(!) 최소화 — 타입 가드로 대체.
