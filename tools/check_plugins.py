# tools/check_plugins.py
import sys
import os
from core.loader import PluginLoader
from core.logger import log
import importlib

def list_plugins():
    PluginLoader.load_plugins("plugins")
    names = sorted(list(PluginLoader.plugins.keys()))
    log("Detected plugins:", names)
    return names

def try_call(name):
    fn = PluginLoader.get(name)
    if not fn:
        log(f"[check] plugin '{name}' not found.")
        return
    # prepare minimal ctx
    ctx = {
        "scene_id": 999,
        "scene_dir": os.path.join("output", "scene_999"),
        "scene": {"id": 999, "narration": "测试文本。"},
    }
    try:
        res = fn(ctx)
        log(f"[check] plugin '{name}' returned: {res}")
    except Exception as e:
        log(f"[check] plugin '{name}' call failed: {e}")

if __name__ == "__main__":
    names = list_plugins()
    # try typical suspects
    for suspect in ["analyze", "transition"]:
        if suspect in names:
            try_call(suspect)
        else:
            log(f"[check] '{suspect}' not in detected plugins.")
