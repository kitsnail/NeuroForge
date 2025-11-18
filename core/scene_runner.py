# core/scene_runner.py (v1.4)
from core.logger import log
from core.loader import PluginLoader
from core.io import IOManager
import os

class SceneRunner:
    """
    NeuroForge v1.4 SceneRunner
    ---------------------------
    职责：执行单个场景的插件序列。
    - 不再检测音频时长
    - 不包含时间线逻辑
    """

    def __init__(self, meta, scene_data, output_dir="output"):
        self.meta = meta
        self.scene_data = scene_data
        self.output_dir = output_dir

    def execute(self) -> dict:
        scene_id = self.scene_data.get("id")
        title = self.scene_data.get("title", f"Scene {scene_id}")

        log(f"🚀 SceneRunner → {title}")

        # 初始化目录
        scene_dir = IOManager.prepare_scene_dir(self.output_dir, scene_id)

        # 初始化上下文
        ctx = {
            "meta": self.meta,
            "scene": self.scene_data,
            "scene_id": scene_id,
            "scene_dir": scene_dir,
        }

        # 执行插件
        PluginLoader.load_plugins("plugins")
        for plugin_name in self.scene_data.get("pipeline", []):
            fn = PluginLoader.get(plugin_name)
            if not fn:
                log(f"⚠️ Plugin not found: {plugin_name}")
                continue

            log(f"  🔧 Running plugin: {plugin_name}")
            try:
                result = fn(ctx)
                if isinstance(result, dict):
                    ctx.update(result)
            except Exception as e:
                log(f"🔥 Plugin {plugin_name} failed: {e}")
                break

        return ctx
