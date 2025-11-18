# core/pipeline.py
from core.logger import log
from core.loader import PluginLoader
from core.io import IOManager

class Pipeline:

    def __init__(self, meta, scenes, output_dir="output"):
        self.meta = meta
        self.scenes = scenes
        self.output_dir = output_dir

    def run(self):
        log("🚀 NeuroForge Pipeline Started")

        for idx, scene in enumerate(self.scenes, start=1):
            log(f"\n🎬 Scene {idx}: {scene.get('title', 'Untitled')}")
            self.run_scene(idx, scene)

    def run_scene(self, scene_id, scene):
        scene_dir = IOManager.prepare_scene_dir(self.output_dir, scene_id)
        context = {
            "meta": self.meta,
            "scene": scene,
            "scene_id": scene_id,
            "scene_dir": scene_dir,
        }

        for plugin_name in scene.get("pipeline", []):
            fn = PluginLoader.get(plugin_name)
            if not fn:
                log(f"⚠️ Plugin not found: {plugin_name}")
                continue

            log(f"  🔧 Running plugin: {plugin_name}")
            try:
                result = fn(context)
                if isinstance(result, dict):
                    context.update(result)
            except Exception as e:
                log(f"🔥 Plugin {plugin_name} failed:", e)
                break
