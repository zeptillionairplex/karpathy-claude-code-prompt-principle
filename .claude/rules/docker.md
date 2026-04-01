---
globs: "**/Dockerfile*, **/docker-compose*, **/.dockerignore"
---
# Docker / Docker Compose 규칙

## Dockerfile
- 멀티스테이지 빌드 사용 (builder → runner).
- 최종 이미지는 최소 베이스 (alpine, distroless).
- RUN 명령은 레이어 최소화를 위해 && 로 체이닝.
- 민감 정보(API 키, 비밀번호) ARG/ENV에 하드코딩 금지.

## Docker Compose
- 서비스별 healthcheck 필수.
- 볼륨 마운트로 데이터 영속성 보장 (PostgreSQL, MinIO).
- 환경변수는 .env 파일 참조. 직접 값 입력 금지.
- 네트워크는 명시적으로 정의.

## 공통
- .dockerignore에 node_modules, __pycache__, .env 반드시 포함.
- 프로덕션/개발 compose 파일 분리:
  docker-compose.yml (공통) + docker-compose.dev.yml + docker-compose.prod.yml
