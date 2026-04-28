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

ARCH_LAYERS = FSD_LAYERS | CLEAN_LAYERS

# 무시할 경로 패턴
IGNORE_PREFIXES = (
    "node_modules/", "vendor/", ".venv/", "venv/", "__pycache__/",
    "dist/", "build/", ".next/", "coverage/",
    ".claude/", "docs/",
)

IGNORE_SUFFIXES = (
    ".min.js", ".min.css", ".map", ".lock",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
)


def run_git(cmd: list[str]) -> list[str]:
    """Run git command and return list of lines."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return []
    except Exception:
        return []


def get_changed_files() -> list[str]:
    """git으로 변경된 파일 목록 수집."""
    files: set[str] = set()
    files.update(run_git(["git", "diff", "--name-only", "HEAD"]))
    files.update(run_git(["git", "diff", "--name-only", "--cached"]))
    files.update(run_git(["git", "diff", "--name-only", "HEAD~1..HEAD"]))
    return list(files)


def should_ignore(path: str) -> bool:
    for prefix in IGNORE_PREFIXES:
        if path.startswith(prefix):
            return True
    for suffix in IGNORE_SUFFIXES:
        if path.endswith(suffix):
            return True
    return False


def extract_arch_folders(files: list[str]) -> set[str]:
    """변경 파일 목록에서 FSD/Clean Arch 폴더 추출."""
    folders: set[str] = set()
    for f in files:
        if should_ignore(f):
            continue
        parts = Path(f).parts
        for i, part in enumerate(parts[:-1]):
            if part in ARCH_LAYERS:
                slice_depth = i + 1
                if slice_depth < len(parts) - 1:
                    folder = "/".join(parts[:slice_depth + 1])
                else:
                    folder = "/".join(parts[:slice_depth])
                folder_path = Path(folder)
                if folder_path.is_dir():
                    folders.add(folder)
                break
    return folders


def files_in_folder(folder: Path) -> set[str]:
    """폴더 내 소스 파일 목록 (테스트 파일 제외, 재귀 탐색)."""
    skip_names = {"CLAUDE.md", "__init__.py"}
    skip_dirs = {"__tests__", "node_modules", "__pycache__"}
    result: set[str] = set()
    try:
        for p in folder.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(folder)
            if any(part in skip_dirs for part in rel.parts[:-1]):
                continue
            if p.name in skip_names or p.name.startswith("."):
                continue
            if p.name.endswith(("_test.go", ".test.ts", ".test.tsx", ".spec.ts")) or p.name.startswith("test_"):
                continue
            result.add(str(rel))
    except Exception:
        pass
    return result


def check_claude_md(folder: Path) -> tuple[bool, bool]:
    """Return (exists, is_stale)."""
    claude_md = folder / "CLAUDE.md"
    if not claude_md.exists():
        return False, False

    try:
        content = claude_md.read_text(encoding="utf-8")
    except Exception:
        return True, False

    current_files = files_in_folder(folder)
    mentioned: set[str] = set()
    in_files_section = False

    for line in content.splitlines():
        if line.strip().lower().startswith("## files"):
            in_files_section = True
            continue
        if in_files_section and line.strip().startswith("## "):
            in_files_section = False
        if in_files_section and "|" in line:
            cell = line.split("|")[1].strip().strip("`")
            if cell and not cell.startswith("-") and cell != "File":
                mentioned.add(cell)

    is_stale = bool(current_files - mentioned)
    return True, is_stale


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    changed = get_changed_files()
    if not changed:
        return

    folders = extract_arch_folders(changed)
    if not folders:
        return

    missing: list[str] = []
    stale: list[str] = []

    for folder_str in sorted(folders):
        folder = Path(folder_str)
        exists, is_stale = check_claude_md(folder)
        if not exists:
            missing.append(folder_str)
        elif is_stale:
            stale.append(folder_str)

    if not missing and not stale:
        return

    print("\n" + "=" * 60)
    print("DOC GUARDIAN -- CLAUDE.md 점검 필요")
    print("=" * 60)
    if missing:
        print("\n[누락] CLAUDE.md 없음 -- /evolving-docs 실행 필요:")
        for f in missing:
            print(f"  - {f}")
    if stale:
        print("\n[오래됨] 새 파일이 추가됐으나 CLAUDE.md 미반영:")
        for f in stale:
            print(f"  - {f}")
    print("\n→ 각 폴더에 대해 `/evolving-docs <folder>` 를 실행하세요.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
