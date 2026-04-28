#!/usr/bin/env python3
"""
Stop / SubagentStop hook: Windows balloon-tip notification when Claude finishes.
Reads hook event from stdin JSON (hook_event_name field).
"""
import json
import subprocess
import sys


def windows_notify(title: str, body: str) -> None:
    # Uses .NET System.Windows.Forms — available on all Windows versions
    ps = f"""
Add-Type -AssemblyName System.Windows.Forms
$n = New-Object System.Windows.Forms.NotifyIcon
$n.Icon = [System.Drawing.SystemIcons]::Information
$n.BalloonTipTitle = '{title}'
$n.BalloonTipText  = '{body}'
$n.Visible = $true
$n.ShowBalloonTip(5000)
Start-Sleep -Milliseconds 800
$n.Visible = $false
$n.Dispose()
"""
    subprocess.run(
        ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps],
        capture_output=True,
        timeout=15,
    )


def main() -> None:
    try:
        data = json.load(sys.stdin)
        event = data.get("hook_event_name", "Stop")
    except Exception:
        event = "Stop"

    if event == "SubagentStop":
        title = "Claude Code — 서브에이전트 완료"
        body  = "서브에이전트 작업이 완료됐습니다."
    else:
        title = "Claude Code — 응답 완료"
        body  = "작업이 완료됐습니다."

    windows_notify(title, body)


if __name__ == "__main__":
    main()
