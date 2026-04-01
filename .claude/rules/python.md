---
globs: "**/*.py"
---
# Python / FastAPI 규칙

## 구조
- router → service → repository 레이어 분리.
- Pydantic 모델로 요청/응답 타입 강제.
- 의존성 주입은 FastAPI Depends() 사용.

## 비동기
- async/await 일관되게 사용. sync 함수 혼용 금지.
- DB 작업은 반드시 async (asyncpg / SQLAlchemy async).

## 에러 처리
- HTTPException으로 명시적 상태 코드 반환.
- 예상 가능한 에러는 커스텀 Exception 클래스 정의.

## 타입
- 모든 함수에 타입 힌트 필수.
- Optional[X] 대신 X | None (Python 3.10+).

## 기타
- 환경변수는 pydantic-settings BaseSettings로 관리.
- n8n API 호출은 별도 service 레이어에서만.
