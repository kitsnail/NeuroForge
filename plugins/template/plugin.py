# plugins/<plugin_name>/plugin.py

import os
from core.logger import log
from core.io import IOManager

def run(ctx):
    plugin_name = os.path.basename(os.path.dirname(__file__))
    scene_dir = ctx["scene_dir"]
    output_dir = IOManager.get_plugin_dir(scene_dir, plugin_name)

    log(f"[{plugin_name}] started")

    # 写入示例文件
    output_file = os.path.join(output_dir, "result.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{plugin_name} executed.\n")

    log(f"[{plugin_name}] completed → {output_file}")

    return {
        plugin_name: {
            "output": output_file
        }
    }
