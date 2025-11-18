# plugins/canvas/plugin.py

import os
from PIL import Image, ImageDraw
from core.logger import log
from core.io import IOManager

def run(ctx):
    plugin = "canvas"
    scene_dir = ctx["scene_dir"]
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)

    log(f"[{plugin}] creating base canvas...")

    # 创建白色背景 1920x1080
    img = Image.new("RGB", (1920, 1080), (245, 245, 245))
    draw = ImageDraw.Draw(img)
    draw.text((50, 50), f"Scene {ctx['scene_id']} Canvas", fill=(80, 80, 80))

    output_file = os.path.join(out_dir, "canvas.png")
    img.save(output_file)

    log(f"[canvas] output → {output_file}")

    return {"canvas": {"file": output_file}}
