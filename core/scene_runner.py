# core/scene_runner.py (v1.5.1 debug-hardened)
from core.logger import log
from core.loader import PluginLoader
from core.io import IOManager
import os
import traceback

class SceneRunner:
    """
    SceneRunner (debug-hardened)
    - Load plugins once per SceneRunner construction (avoids repeated clears).
    - Print pipeline debug: pipeline list, available plugins, mapping results.
    - Execute plugins in order; if plugin not found, log a clear warning and continue.
    """

    def __init__(self, meta, scene_data, output_dir="output", prev_ctx=None):
        self.meta = meta
        self.scene_data = scene_data
        self.output_dir = output_dir
        self.prev_ctx = prev_ctx

        # Load plugins once for this runner and capture snapshot of available plugins
        try:
            PluginLoader.load_plugins("plugins")
        except Exception:
            # non-fatal: ensure we still have plugins dict
            log("[SceneRunner] Warning: PluginLoader.load_plugins() threw exception:")
            log(traceback.format_exc())
        self.available_plugins = dict(PluginLoader.plugins)  # snapshot

    def _collect_outputs_from_ctx(self, ctx):
        outputs = {}
        if not ctx:
            return outputs

        candidate_keys = ["compose", "mix", "tts"]
        for k in candidate_keys:
            blk = ctx.get(k)
            if isinstance(blk, dict):
                if "video_out" in blk:
                    outputs["video"] = outputs.get("video") or blk.get("video_out")
                if "audio_out" in blk:
                    outputs["audio"] = outputs.get("audio") or blk.get("audio_out")
                if "subtitle_out" in blk:
                    outputs["subtitle"] = outputs.get("subtitle") or blk.get("subtitle_out")

        # fallback mapping
        for k, v in ctx.items():
            if isinstance(v, dict) and v.get("status") == "ok":
                if "video_out" in v and "video" not in outputs:
                    outputs["video"] = v.get("video_out")
                if "audio_out" in v and "audio" not in outputs:
                    outputs["audio"] = v.get("audio_out")
        return outputs

    def execute(self) -> dict:
        scene_id = self.scene_data.get("id")
        title = self.scene_data.get("title", f"Scene {scene_id}")

        log(f"🚀 SceneRunner → {title}")

        # prepare scene dir
        scene_dir = IOManager.prepare_scene_dir(self.output_dir, scene_id)

        # prepare prev_scene info
        prev_scene_info = None
        if self.prev_ctx:
            prev_scene_id = self.prev_ctx.get("scene_id") or self.prev_ctx.get("scene", {}).get("id")
            outputs = self._collect_outputs_from_ctx(self.prev_ctx)
            prev_scene_info = {
                "scene_id": prev_scene_id,
                "outputs": outputs,
                "raw_ctx": self.prev_ctx
            }

        # build ctx
        ctx = {
            "meta": self.meta,
            "scene": self.scene_data,
            "scene_id": scene_id,
            "scene_dir": scene_dir,
        }
        if prev_scene_info:
            ctx["prev_scene"] = prev_scene_info

        # DEBUG: print requested pipeline and available plugins
        pipeline = self.scene_data.get("pipeline", [])
        log(f"[SceneRunner] pipeline for scene {scene_id}: {pipeline}")
        log(f"[SceneRunner] available plugins: {sorted(list(self.available_plugins.keys()))}")

        # execute plugins in pipeline order
        for plugin_name in pipeline:
            fn = PluginLoader.get(plugin_name)
            if not fn:
                # plugin not found — try simple heuristics: lower/strip
                alt = plugin_name.strip().lower()
                fn_alt = PluginLoader.get(alt)
                if fn_alt:
                    fn = fn_alt
                    log(f"[SceneRunner] plugin name normalized: '{plugin_name}' -> '{alt}'")
                else:
                    log(f"⚠️ Plugin not found: '{plugin_name}' for scene {scene_id}")
                    log(f"   → Available plugin names: {sorted(list(self.available_plugins.keys()))}")
                    # continue to next plugin (do not crash)
                    continue

            log(f"  🔧 Running plugin: {plugin_name}")
            try:
                result = fn(ctx)
                if isinstance(result, dict):
                    # Merge result into ctx gently (don't overwrite top-level reserved keys)
                    for k, v in result.items():
                        # best-effort merge: if existing key is dict, update; else replace
                        if isinstance(v, dict) and isinstance(ctx.get(k), dict):
                            ctx[k].update(v)
                        else:
                            ctx[k] = v
            except Exception as e:
                log(f"🔥 Plugin {plugin_name} failed with exception: {e}")
                log(traceback.format_exc())
                ctx.setdefault("errors", []).append({"plugin": plugin_name, "error": str(e)})
                # stop executing further plugins for this scene to avoid cascading failures
                break

        # mark and return ctx
        ctx["scene_id"] = scene_id
        return ctx
