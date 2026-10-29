# -*- coding: utf-8 -*-
"""
git 自动同步：后台每次保存/删除内容后，把改动提交并推送到 GitHub。

用途：云端部署管理后台时，形成「后台保存 → 仓库更新 → Netlify 自动重新构建 → 线上生效」的闭环。
本地开发默认也开启（保存即同步，方便联调）；设环境变量 AUTO_GIT_SYNC=0 可关闭。
"""
import os
import subprocess
import threading
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]  # portfolio/

# 是否启用自动同步（默认开启）
ENABLED = os.environ.get("AUTO_GIT_SYNC", "1") != "0"

_LOCK = threading.Lock()


def _git(args: list, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
        timeout=timeout,
        encoding="utf-8",
        errors="replace",
    )


def sync_now(reason: str = "content update via admin") -> tuple:
    """
    同步执行一次 commit + push（后台管理只改 src/data 与 src/content）。
    返回 (ok: bool, message: str)。
    """
    if not ENABLED:
        return True, "auto git sync disabled"
    try:
        r = _git(["add", "-A", "src/data", "src/content"])
        if r.returncode != 0:
            return False, f"git add 失败: {r.stderr.strip()[:200]}"

        # 无内容变化时不提交
        r = _git(["diff", "--cached", "--quiet"])
        if r.returncode == 0:
            return True, "no changes"

        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        r = _git(["commit", "-m", f"{reason} ({ts})"])
        if r.returncode != 0:
            return False, f"git commit 失败: {r.stderr.strip()[:200]}"

        r = _git(["push", "origin", "HEAD"])
        if r.returncode != 0:
            return False, f"git push 失败: {r.stderr.strip()[:200]}"
        return True, "pushed to github"
    except Exception as e:  # noqa: BLE001
        return False, f"git sync 异常: {e}"


def sync_async(reason: str = "content update via admin") -> None:
    """后台线程执行同步（不阻塞保存接口）。"""
    if not ENABLED:
        return

    def _run() -> None:
        with _LOCK:
            sync_now(reason)

    threading.Thread(target=_run, daemon=True).start()
