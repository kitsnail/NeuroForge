# plugins/d2/plugin.py

import os
import subprocess
from core.logger import log
from core.io import IOManager

def run(ctx):
    plugin = "d2"
    scene_dir = ctx["scene_dir"]
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)

    log(f"[{plugin}] generating D2 diagram...")

    d2_text = ctx["scene"].get("d2_text", "box: Hello D2")

    d2_file = os.path.join(out_dir, "diagram.d2")
    with open(d2_file, "w") as f:
        f.write(d2_text)

    output_png = os.path.join(out_dir, "diagram.png")

    # 调用系统 d2 渲染
    subprocess.run(["d2", d2_file, output_png], check=False)

    log(f"[d2] output → {output_png}")

    return {"d2": {"file": output_png}}
