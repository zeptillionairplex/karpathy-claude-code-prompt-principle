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
