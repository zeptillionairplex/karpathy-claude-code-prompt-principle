#!/usr/bin/env python3
"""
PreToolUse / Bash: limit command output to prevent context bloat.

updatedInput으로 실행 전 명령어를 래핑 → 출력이 MAX_LINES 초과 시
head + tail 만 남기고 중간을 자름. exit code는 원본 그대로 보존.

통과 (truncation 안 함):
  - 이미 head/tail/grep 으로 파이프된 명령
  - git diff, git show  (코드리뷰에 전체 필요)
  - echo, printf       (출력이 짧음)
"""
import json
import re
import sys

MAX_LINES  = 200   # 이 이상이면 자름
HEAD_LINES = 75    # 앞에서 보여줄 줄 수
TAIL_LINES = 75    # 뒤에서 보여줄 줄 수

PASSTHROUGH = re.compile(
    r"""
      \|\s*(head|tail|grep|less|more|wc)\b  # 이미 파이프로 제한됨
    | \b(head|tail)\s                        # 명시적 head/tail
    | \bgit\s+(diff|show)\b                  # 전체 diff 필요
    | \b(echo|printf)\b                      # 출력 짧음
    """,
    re.VERBOSE,
)


def should_passthrough(cmd: str) -> bool:
    return bool(PASSTHROUGH.search(cmd))


def wrap(command: str) -> str:
    """
    원본 명령어를 tmpfile에 캡처 → 줄 수 확인 → 초과 시 head+tail 출력.
    exit code는 원본 명령어의 것을 그대로 반환.
    """
    return (
        f"_t=$(mktemp) && "
        f"{{ {command}; }} > \"$_t\" 2>&1; _e=$?; "
        f"_n=$(wc -l < \"$_t\"); "
        f"if [ \"$_n\" -gt {MAX_LINES} ]; then "
        f"  printf '[출력 제한: %d줄 → 앞 {HEAD_LINES}줄 + 뒤 {TAIL_LINES}줄]\\n' \"$_n\"; "
        f"  head -{HEAD_LINES} \"$_t\"; "
        f"  printf '\\n[... %d줄 생략 ...]\\n\\n' \"$(( _n - {HEAD_LINES} - {TAIL_LINES} ))\"; "
        f"  tail -{TAIL_LINES} \"$_t\"; "
        f"else cat \"$_t\"; fi; "
        f"rm -f \"$_t\"; exit \"$_e\""
    )


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")
    if not command or should_passthrough(command):
        sys.exit(0)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "updatedInput": {"command": wrap(command)},
        }
    }))


if __name__ == "__main__":
    main()
