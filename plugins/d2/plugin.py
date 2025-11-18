# ===========================================================
# NeuroForge v1.3 Plugin: d2
# -----------------------------------------------------------
# 功能：
#   根据场景定义生成 D2 结构图。
# 输出：
#   {"d2": {"status": "ok", "file": "diagram.png"}}
# ===========================================================

import os
import subprocess
from core.logger import log
from core.io import IOManager

def run(ctx):
    plugin = "d2"
    scene_dir = ctx["scene_dir"]
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)
    os.makedirs(out_dir, exist_ok=True)

    log(f"[{plugin}] generating D2 diagram...")

    d2_text = ctx["scene"].get("d2_text", "box: NeuroForge D2 Diagram")
    d2_file = os.path.join(out_dir, "diagram.d2")
    with open(d2_file, "w", encoding="utf-8") as f:
        f.write(d2_text)

    output_png = os.path.join(out_dir, "diagram.png")
    subprocess.run(["d2", d2_file, output_png], check=False)

    log(f"[{plugin}] output → {output_png}")

    return {
        "d2": {
            "status": "ok",
            "file": output_png
        }
    }
