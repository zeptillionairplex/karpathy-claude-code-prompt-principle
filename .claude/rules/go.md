---
globs: "**/*.go"
---
# Go / Gin 규칙

## 레이어 구조
- handler → service → repository 순서. 역방향 금지.
- handler: HTTP 파싱, 유효성 검사, 응답 직렬화만.
- service: 비즈니스 로직만. DB 직접 접근 금지.
- repository: DB 쿼리만. 비즈니스 로직 금지.

## 에러 처리
- 에러는 상위로 전파. 로그는 handler에서만 출력.
- fmt.Errorf("...: %w", err) 로 컨텍스트 추가.
- panic 금지 — 초기화 코드 제외.

## API 응답 형식
```go
// 성공
{"data": ..., "message": "ok"}
// 실패
{"error": "...", "code": "ERROR_CODE"}
```

## 기타
- goroutine 생성 시 반드시 종료 조건 명시.
- context.Context는 항상 첫 번째 인자.
- 구조체 필드 태그: json, db, validate 순서.
