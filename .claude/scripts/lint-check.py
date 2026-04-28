#!/usr/bin/env python3
"""
Stop hook: 세션 종료 시 변경된 파일 유형을 감지하여 린트/타입체크 실행 안내.

원리:
  - git diff --name-only로 변경 파일 목록 확인
  - 파일 확장자에 따라 해당 린트 명령어 안내 메시지 출력
  - 실제 린트 실행은 하지 않음 (프로젝트마다 설정이 다르므로 안내만)
  - Go / Python / TypeScript 지원
"""
import json
import subprocess
import sys
from pathlib import Path


def get_changed_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, timeout=10
        )
        staged = subprocess.run(
            ["git", "diff", "--name-only", "--cached"],
            capture_output=True, text=True, timeout=10
        )
        files = result.stdout.splitlines() + staged.stdout.splitlines()
        return list(set(files))
    except Exception:
        return []


def classify(files: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {"go": [], "py": [], "ts": []}
    for f in files:
        p = Path(f)
        if p.suffix == ".go":
            groups["go"].append(f)
        elif p.suffix == ".py":
            groups["py"].append(f)
        elif p.suffix in (".ts", ".tsx"):
            groups["ts"].append(f)
    return {k: v for k, v in groups.items() if v}


def build_hint(groups: dict[str, list[str]]) -> str:
    lines = ["[lint-check] 변경된 파일이 감지되었습니다. 린트를 실행하세요:"]
    if "go" in groups:
        lines.append(f"  Go ({len(groups['go'])}개 파일): go vet ./... && go build ./...")
    if "py" in groups:
        lines.append(f"  Python ({len(groups['py'])}개 파일): ruff check . && mypy .")
    if "ts" in groups:
        lines.append(f"  TypeScript ({len(groups['ts'])}개 파일): tsc --noEmit && eslint .")
    return "\n".join(lines)


def main() -> None:
    try:
        json.load(sys.stdin)  # Stop hook stdin 소비 (무시)
    except Exception:
        pass

    files = get_changed_files()
    if not files:
        return

    groups = classify(files)
    if not groups:
        return

    print(build_hint(groups), flush=True)


if __name__ == "__main__":
    main()
