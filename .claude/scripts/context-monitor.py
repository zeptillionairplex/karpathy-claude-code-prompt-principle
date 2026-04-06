#!/usr/bin/env python3
"""
Stop hook: Windows 알림 — 컨텍스트 60% 도달 시 1회 경고.

원리:
  - Stop hook stdin에서 transcript_path 수신
  - JSONL 트랜스크립트 파일의 문자 수로 토큰 추정
  - 고정 오버헤드(시스템 프롬프트 + 툴 + 스킬 + 메모리) 합산
  - 120k(60%) 초과 시 알림 (세션당 1회)
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# ── 상수 ────────────────────────────────────────────────────────────────────

CONTEXT_LIMIT   = 200_000
THRESHOLD       = 0.60
THRESHOLD_TOKENS = int(CONTEXT_LIMIT * THRESHOLD)   # 120_000

# 고정 오버헤드: 시스템 프롬프트 + 툴 정의 + 스킬 메타데이터 + 메모리 파일
# (/context 출력 기준: 6.4k + 6.7k + 2.6k + 5.4k ≈ 21k)
FIXED_OVERHEAD  = 21_000

STATE_FILE = Path(__file__).parent / ".context-monitor-state.json"
MAX_STATE_AGE_DAYS = 3   # 오래된 세션 기록 자동 정리


# ── 헬퍼 ────────────────────────────────────────────────────────────────────

def tokens(chars: int) -> int:
    """문자 수 → 토큰 추정 (1 token ≈ 4 chars)."""
    return chars // 4


def estimate_from_transcript(path: str) -> int:
    """JSONL 트랜스크립트에서 메시지 문자 수 합산 → 토큰 추정."""
    total = 0
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    content = msg.get("content", "")
                    if isinstance(content, str):
                        total += len(content)
                    elif isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict):
                                total += len(str(block.get("text", "") or ""))
                except Exception:
                    total += len(line)
    except Exception:
        pass
    return tokens(total)


def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state: dict) -> None:
    # 오래된 세션 정리
    cutoff = time.time() - MAX_STATE_AGE_DAYS * 86400
    state = {k: v for k, v in state.items() if v.get("ts", 0) > cutoff}
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def notify(title: str, body: str) -> None:
    ps = f"""
Add-Type -AssemblyName System.Windows.Forms
$n = New-Object System.Windows.Forms.NotifyIcon
$n.Icon = [System.Drawing.SystemIcons]::Warning
$n.BalloonTipTitle = '{title}'
$n.BalloonTipText  = '{body}'
$n.Visible = $true
$n.ShowBalloonTip(8000)
Start-Sleep -Milliseconds 800
$n.Visible = $false
$n.Dispose()
"""
    subprocess.run(
        ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps],
        capture_output=True,
        timeout=15,
    )


# ── 메인 ────────────────────────────────────────────────────────────────────

def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    session_id      = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    # 토큰 추정
    transcript_tokens = (
        estimate_from_transcript(transcript_path)
        if transcript_path and os.path.exists(transcript_path)
        else 0
    )
    estimated = FIXED_OVERHEAD + transcript_tokens
    pct = estimated / CONTEXT_LIMIT * 100

    # 세션 상태 확인 (이미 알린 세션은 스킵)
    state = load_state()
    session = state.get(session_id, {"notified": False, "ts": time.time()})

    if not session["notified"] and estimated >= THRESHOLD_TOKENS:
        notify(
            "Claude Code — 컨텍스트 경고 ⚠",
            f"컨텍스트 {pct:.0f}% 사용 중\n"
            f"({estimated:,} / {CONTEXT_LIMIT:,} tokens 추정)\n"
            "세션 전환 또는 /compact 를 고려하세요.",
        )
        session["notified"] = True
        session["ts"] = time.time()
        state[session_id] = session
        save_state(state)


if __name__ == "__main__":
    main()
