# plugins/d2/plugin.py
# ===========================================================
# NeuroForge v1.5 Plugin: d2
# -----------------------------------------------------------
# 功能：
#   从 scene.diagram 字段读取 d2 文本，写入 .d2 文件并尝试调用 d2 CLI 渲染为 PNG。
# 输入：
#   ctx : dict（由 SceneRunner 注入）
# 输出：
#   { "d2": { "status": "ok" | "skip" | "error", "file": "<png_path>", "meta": {...} } }
# 规范：
#   - 遵循 plugin_dev_guide_v1.5.md 与 standards_v1.5.md
# ===========================================================

import os
import subprocess
from core.logger import log
from core.io import IOManager

def run(ctx):
    plugin = "d2"
    scene = ctx.get("scene", {}) or {}
    scene_id = scene.get("id", ctx.get("scene_id"))
    scene_dir = ctx.get("scene_dir")

    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)
    os.makedirs(out_dir, exist_ok=True)

    # 首先尝试读取 scene 中的 diagram 字段（v1.5 demo 使用该字段）
    diagram_text = scene.get("diagram")
    if not diagram_text:
        # 兼容旧字段命名（若曾用 d2_text）
        diagram_text = scene.get("d2_text")

    if not diagram_text:
        # 如果仍然没有，使用一个清晰的默认占位
        diagram_text = "box: NeuroForge D2 Diagram"

    d2_path = os.path.join(out_dir, "diagram.d2")
    png_path = os.path.join(out_dir, "diagram.png")

    # 写 .d2 文本文件
    try:
        with open(d2_path, "w", encoding="utf-8") as f:
            f.write(diagram_text)
    except Exception as e:
        log(f"[{plugin}] failed to write .d2 file: {e}")
        return {plugin: {"status": "error", "meta": {"error": str(e)}}}

    log(f"[{plugin}] generating D2 diagram...")

    # 调用 d2 CLI（如果系统安装了 d2）；失败时不抛出，只记录并返回 skip/error
    try:
        # subprocess.run 返回码非 0 会引发 CalledProcessError，如果 check=True
        # 我们用 check=False 来避免抛异常，同时检查 returncode
        proc = subprocess.run(["d2", d2_path, png_path], check=False,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            # 渲染失败：记录 stderr，并标记为 error（仍保留 .d2 文件供人工检查）
            stderr = proc.stderr.decode(errors="ignore") if proc.stderr else ""
            log(f"[{plugin}] d2 CLI failed (rc={proc.returncode}): {stderr.strip()}")
            # 仍返回文件路径（.d2 可用于调试），标记状态为 "error"
            return {
                plugin: {
                    "status": "error",
                    "file": d2_path,
                    "meta": {"rc": proc.returncode, "stderr": stderr}
                }
            }
    except FileNotFoundError:
        # d2 CLI 未安装：记录信息并返回 skip（或 error 取决于你希望的策略）
        log(f"[{plugin}] d2 CLI not found in PATH; skipping PNG render (d2 file written).")
        return {
            plugin: {
                "status": "skip",
                "file": d2_path,
                "meta": {"note": "d2 CLI not installed; .d2 file created"}
            }
        }
    except Exception as e:
        log(f"[{plugin}] unexpected error when running d2: {e}")
        return {plugin: {"status": "error", "meta": {"error": str(e)}}}

    # 成功渲染 PNG
    log(f"[{plugin}] output → {png_path}")
    return {
        plugin: {
            "status": "ok",
            "file": png_path,
            "meta": {"d2_source": d2_path}
        }
    }
