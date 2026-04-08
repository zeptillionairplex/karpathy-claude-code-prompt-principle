# Doc Guardian Hook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stop 훅에서 세션 중 변경된 파일을 분석해 FSD/Clean Arch 폴더에 `CLAUDE.md`가 누락됐거나 오래됐을 때 Claude에게 알림을 출력하는 `doc-guardian.py` 스크립트를 작성하고 `settings.json`에 등록한다.

**Architecture:** Stop 이벤트 발생 시 `git diff --name-only`로 세션 변경 파일 목록을 수집하고, FSD/Clean Arch 폴더 패턴에 매칭되는 폴더들의 `CLAUDE.md` 존재 여부 및 파일 목록 일치 여부를 검사한다. 누락/오래된 폴더가 있으면 stdout으로 안내 메시지를 출력해 다음 응답에서 Claude가 인지하게 한다. 코딩 중 끼어들지 않으므로 작업 흐름을 방해하지 않는다.

**Tech Stack:** Python 3.10+, git CLI, Claude Code Stop hook (stdin JSON)

---

## File Structure

| File | 역할 |
|------|------|
| `.claude/scripts/doc-guardian.py` | 신규 생성 — Stop 훅 스크립트 본체 |
| `.claude/settings.json` | 수정 — Stop 훅에 doc-guardian 등록 |
| `.claude/rules/architecture.md` | 수정 — 경로 오류 수정 + hook 자동화 언급 추가 |

---

### Task 1: `doc-guardian.py` 작성

**Files:**
- Create: `.claude/scripts/doc-guardian.py`

- [ ] **Step 1: 스크립트 작성**

```python
#!/usr/bin/env python3
"""
Stop hook: 세션 변경 파일 분석 → FSD/Clean Arch 폴더 CLAUDE.md 누락 감지.

동작:
  1. stdin JSON에서 session_id, transcript_path 수신 (사용 안 해도 됨)
  2. git diff --name-only HEAD로 uncommitted 변경 파일 수집
     + git diff --name-only HEAD~1..HEAD 로 최근 커밋도 포함 (실패해도 무시)
  3. 변경 파일 경로에서 FSD / Clean Arch 폴더 감지
  4. 각 폴더의 CLAUDE.md 존재 여부 + 파일 목록 변화 검사
  5. 누락/오래된 폴더가 있으면 stdout에 안내 출력 → Claude가 다음 응답에서 인지
"""
import json
import os
import subprocess
import sys
from pathlib import Path

# ── 아키텍처 폴더 패턴 ────────────────────────────────────────────────────────

# FSD 레이어 (경로에 이 세그먼트가 포함된 폴더)
FSD_LAYERS = {"app", "pages", "widgets", "features", "entities", "shared"}

# Clean Architecture 레이어 (경로에 이 세그먼트가 포함된 폴더)
CLEAN_LAYERS = {"use_cases", "infrastructure", "interfaces"}
# entities는 FSD와 겹치므로 별도 처리 없이 FSD_LAYERS에서 커버

ARCH_LAYERS = FSD_LAYERS | CLEAN_LAYERS

# 무시할 경로 패턴 (context-hygiene 준수)
IGNORE_PREFIXES = (
    "node_modules/", "vendor/", ".venv/", "venv/", "__pycache__/",
    "dist/", "build/", ".next/", "coverage/",
    ".claude/", "docs/",  # 설정/문서 폴더는 아키텍처 폴더 아님
)

IGNORE_SUFFIXES = (
    ".min.js", ".min.css", ".map", ".lock",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
)


def get_changed_files(repo_root: Path) -> list[str]:
    """git으로 변경된 파일 목록 수집 (uncommitted + 최근 커밋)."""
    files: set[str] = set()

    def run(cmd: list[str]) -> list[str]:
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                cwd=str(repo_root), timeout=10,
            )
            return [l.strip() for l in result.stdout.splitlines() if l.strip()]
        except Exception:
            return []

    files.update(run(["git", "diff", "--name-only", "HEAD"]))
    files.update(run(["git", "diff", "--name-only", "--cached"]))
    # 최근 커밋도 포함 (새 파일이 바로 커밋된 경우)
    files.update(run(["git", "diff", "--name-only", "HEAD~1..HEAD"]))
    return list(files)


def should_ignore(path: str) -> bool:
    for prefix in IGNORE_PREFIXES:
        if path.startswith(prefix) or f"/{prefix.rstrip('/')}" in path:
            return True
    for suffix in IGNORE_SUFFIXES:
        if path.endswith(suffix):
            return True
    return False


def extract_arch_folders(files: list[str], repo_root: Path) -> set[Path]:
    """변경 파일 목록에서 FSD/Clean Arch 해당 폴더(슬라이스 직접 부모) 추출."""
    folders: set[Path] = set()
    for f in files:
        if should_ignore(f):
            continue
        parts = Path(f).parts
        for i, part in enumerate(parts[:-1]):  # 마지막은 파일명
            if part in ARCH_LAYERS:
                # 레이어 폴더 자체보다 한 단계 아래(슬라이스) 폴더가 목표
                # 예: features/auth/api.ts → features/auth/
                slice_depth = i + 1
                if slice_depth < len(parts) - 1:
                    folder = repo_root / Path(*parts[:slice_depth + 1])
                else:
                    folder = repo_root / Path(*parts[:slice_depth])
                if folder.is_dir():
                    folders.add(folder)
                break
    return folders


def files_in_folder(folder: Path) -> list[str]:
    """폴더 내 소스 파일 목록 (테스트 파일 제외, 재귀 없이 1단계)."""
    skip_names = {"CLAUDE.md", "__init__.py"}
    skip_dirs = {"__tests__", "node_modules", "__pycache__"}
    result = []
    try:
        for p in sorted(folder.iterdir()):
            if p.name in skip_names or p.name.startswith("."):
                continue
            if p.is_dir() and p.name in skip_dirs:
                continue
            if p.is_file() and not (
                p.name.endswith("_test.go")
                or p.name.endswith(".test.ts")
                or p.name.endswith(".test.tsx")
                or p.name.endswith(".spec.ts")
                or p.name.startswith("test_")
            ):
                result.append(p.name)
    except Exception:
        pass
    return result


def check_claude_md(folder: Path) -> tuple[bool, bool]:
    """(exists, is_stale) 반환.

    is_stale: CLAUDE.md의 Files 섹션에 없는 파일이 폴더에 생겼을 때 True.
    """
    claude_md = folder / "CLAUDE.md"
    if not claude_md.exists():
        return False, False

    try:
        content = claude_md.read_text(encoding="utf-8")
    except Exception:
        return True, False

    current_files = set(files_in_folder(folder))
    # Files 섹션에 언급된 파일명 추출 (파이프 테이블 첫 번째 열)
    mentioned: set[str] = set()
    in_files_section = False
    for line in content.splitlines():
        if line.strip().startswith("## Files"):
            in_files_section = True
            continue
        if in_files_section and line.strip().startswith("## "):
            in_files_section = False
        if in_files_section and "|" in line:
            cell = line.split("|")[1].strip().strip("`")
            if cell and not cell.startswith("-") and cell != "File":
                mentioned.add(cell)

    new_files = current_files - mentioned
    is_stale = bool(new_files)
    return True, is_stale


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    repo_root = Path(
        data.get("cwd") or
        subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True,
        ).stdout.strip() or
        os.getcwd()
    )

    changed = get_changed_files(repo_root)
    if not changed:
        sys.exit(0)

    folders = extract_arch_folders(changed, repo_root)
    if not folders:
        sys.exit(0)

    missing: list[str] = []
    stale: list[str] = []

    for folder in sorted(folders):
        exists, is_stale = check_claude_md(folder)
        rel = relative(folder, repo_root)
        if not exists:
            missing.append(rel)
        elif is_stale:
            stale.append(rel)

    if not missing and not stale:
        sys.exit(0)

    print("\n" + "=" * 60)
    print("📄 DOC GUARDIAN — CLAUDE.md 점검 필요")
    print("=" * 60)
    if missing:
        print("\n[누락] CLAUDE.md 없음 — /evolving-docs 실행 필요:")
        for f in missing:
            print(f"  • {f}")
    if stale:
        print("\n[오래됨] 새 파일이 추가됐으나 CLAUDE.md 미반영:")
        for f in stale:
            print(f"  • {f}")
    print("\n→ 각 폴더에 대해 `/evolving-docs <folder>` 를 실행하세요.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 실행 가능 확인**

```bash
echo '{}' | python .claude/scripts/doc-guardian.py
```

Expected: 변경 파일이 없으면 아무 출력 없이 exit 0. 오류 없음.

- [ ] **Step 3: 동작 테스트 (더미 폴더 생성)**

```bash
mkdir -p features/auth && touch features/auth/api.ts
echo '{}' | python .claude/scripts/doc-guardian.py
```

Expected: `DOC GUARDIAN — CLAUDE.md 점검 필요` 메시지와 `features/auth` 출력.

- [ ] **Step 4: 정리**

```bash
rm -rf features/
```

---

### Task 2: `settings.json` Stop 훅에 등록

**Files:**
- Modify: `.claude/settings.json`

- [ ] **Step 1: Stop 훅 배열에 doc-guardian 추가**

`settings.json`의 `"Stop"` 배열에 아래 항목을 추가한다 (기존 notify, context-monitor 뒤에):

```json
{
  "type": "command",
  "command": "python \"$(git rev-parse --show-toplevel)/.claude/scripts/doc-guardian.py\"",
  "timeout": 20,
  "async": true
}
```

최종 Stop 배열:

```json
"Stop": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "python \"$(git rev-parse --show-toplevel)/.claude/scripts/notify.py\"",
        "timeout": 15,
        "async": true
      },
      {
        "type": "command",
        "command": "python \"$(git rev-parse --show-toplevel)/.claude/scripts/context-monitor.py\"",
        "timeout": 15,
        "async": true
      },
      {
        "type": "command",
        "command": "python \"$(git rev-parse --show-toplevel)/.claude/scripts/doc-guardian.py\"",
        "timeout": 20,
        "async": true
      }
    ]
  }
]
```

- [ ] **Step 2: JSON 유효성 확인**

```bash
python -c "import json; json.load(open('.claude/settings.json'))" && echo "OK"
```

Expected: `OK`

---

### Task 3: `architecture.md` 경로 수정 및 hook 자동화 언급 추가

**Files:**
- Modify: `.claude/rules/architecture.md`

- [ ] **Step 1: 파일 수정**

현재 내용의 두 곳을 수정한다:

1. FSD 섹션 참조 경로:
   - `→ See .claude/rules/react.md` → `→ See docs/rules/react.md`

2. Backend 섹션 참조 경로:
   - `→ See .claude/rules/go.md or .claude/rules/python.md` → `→ See docs/rules/go.md or docs/rules/python.md`

3. Self-Describing Folders 섹션에 hook 자동화 추가:

변경 전:
```markdown
## Self-Describing Folders
Every domain/feature folder has a `CLAUDE.md` (auto-loaded by Claude Code).
→ Run `/evolving-docs` to create or update a folder's `CLAUDE.md`.
```

변경 후:
```markdown
## Self-Describing Folders
Every domain/feature folder has a `CLAUDE.md` (auto-loaded by Claude Code).
→ Run `/evolving-docs` to create or update a folder's `CLAUDE.md`.
→ **Automated:** `doc-guardian.py` (Stop hook) detects missing/stale `CLAUDE.md`
  after each session and prompts you to run `/evolving-docs`.
```

- [ ] **Step 2: 변경 확인**

```bash
grep -n "docs/rules\|doc-guardian" .claude/rules/architecture.md
```

Expected: 3줄 출력 (react.md, go.md/python.md, doc-guardian).

---

### Task 4: 커밋

**Files:** 위 3개 파일 모두

- [ ] **Step 1: 스테이징 및 커밋**

```bash
git add .claude/scripts/doc-guardian.py .claude/settings.json .claude/rules/architecture.md docs/superpowers/plans/2026-04-07-doc-guardian-hook.md
git commit -m "feat(hooks): add doc-guardian Stop hook for CLAUDE.md drift detection"
```

Expected: 4 files changed 커밋 성공.

- [ ] **Step 2: 푸시**

```bash
git push origin feat/claude-skills-setup
```
