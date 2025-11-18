# ===========================================================
# NeuroForge v1.3 Plugin: canvas
# -----------------------------------------------------------
# 功能：
#   创建基础画布图像，作为场景背景。
# 输出：
#   {"canvas": {"status": "ok", "file": "canvas.png"}}
# ===========================================================

import os
from PIL import Image, ImageDraw, ImageFont
from core.logger import log
from core.io import IOManager

def run(ctx):
    plugin = "canvas"
    scene_dir = ctx["scene_dir"]
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)
    os.makedirs(out_dir, exist_ok=True)

    log(f"[{plugin}] generating base canvas...")

    # 基本参数
    width, height = 1280, 720
    bg_color = (245, 245, 245)
    text_color = (60, 60, 60)

    # 创建基础画布
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    title = ctx["scene"].get("title", f"Scene {ctx['scene_id']}")
    draw.text((50, 50), title, fill=text_color)

    output_file = os.path.join(out_dir, "canvas.png")
    img.save(output_file)
    log(f"[{plugin}] output → {output_file}")

    return {
        "canvas": {
            "status": "ok",
            "file": output_file
        }
    }
