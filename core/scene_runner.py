# ===========================================================
# NeuroForge v1.3 Core: SceneRunner
# -----------------------------------------------------------
# 功能：
#   执行单个场景的完整插件管线。
#   管理上下文 ctx 并将结果回传 Timeline。
# 输出：
#   dict {
#     "scene_id": int,
#     "title": str,
#     "duration": float,
#     "ctx": {...}
#   }
# ===========================================================

import os
import subprocess
from core.logger import log
from core.loader import PluginLoader
from core.io import IOManager

class SceneRunner:
    def __init__(self, meta, scene, output_dir="output"):
        self.meta = meta
        self.scene = scene
        self.output_dir = output_dir

    def run(self):
        PluginLoader.load_plugins("plugins")

        sid = self.scene.get("id", "unknown")
        title = self.scene.get("title", f"Scene {sid}")
        log(f"🚀 SceneRunner → {title}")

        scene_dir = IOManager.prepare_scene_dir(self.output_dir, sid)
        ctx = {
            "meta": self.meta,
            "scene": self.scene,
            "scene_id": sid,
            "scene_dir": scene_dir,
        }

        # 执行场景插件管线
        for plugin_name in self.scene.get("pipeline", []):
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

        # 自动探测音频时长
        duration = self._detect_audio_duration(ctx)
        return {
            "scene_id": sid,
            "title": title,
            "duration": duration,
            "ctx": ctx
        }

    # ===========================================================
    # 辅助：探测音频时长
    # ===========================================================
    @staticmethod
    def _detect_audio_duration(ctx):
        """优先从 mix 或 tts 输出中检测音频时长"""
        for key in ["mix", "tts"]:
            block = ctx.get(key, {})
            for field in ["audio_out", "mix_out"]:
                audio_file = block.get(field)
                if audio_file and os.path.exists(audio_file):
                    return SceneRunner._probe_duration(audio_file)
        log("⚠️ No valid audio found for duration detection.")
        return 0.0

    @staticmethod
    def _probe_duration(path):
        """调用 ffprobe 获取音频时长"""
        try:
            out = subprocess.check_output([
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                path
            ]).decode().strip()
            return float(out)
        except Exception:
            return 0.0
