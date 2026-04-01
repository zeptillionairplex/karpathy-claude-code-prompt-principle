---
globs: "**/migrations/**, **/repository*, **/*_repository*, **/db/**, **/*.sql"
---
# Database / PostgreSQL / MinIO 규칙

## PostgreSQL
- 마이그레이션은 반드시 up/down 쌍으로 작성.
- DROP, TRUNCATE, DELETE (WHERE 없는) 실행 전 반드시 사용자 확인.
- 인덱스는 쿼리 작성 후 EXPLAIN ANALYZE 확인 후 추가.
- N+1 쿼리 금지 — JOIN 또는 batch 로딩 사용.

## 트랜잭션
- 여러 테이블 변경은 트랜잭션으로 묶음.
- 트랜잭션 내부에서 외부 API 호출 금지.

## MinIO
- 파일 업로드는 presigned URL 방식 사용.
- 버킷 이름은 환경변수로 관리. 하드코딩 금지.
- 객체 삭제 전 존재 여부 확인.

## 공통
- 민감 데이터(개인정보, 비밀번호)는 로그 출력 금지.
- 비밀번호는 반드시 bcrypt/argon2 해시 저장.
