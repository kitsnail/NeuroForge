# core/timeline.py (v1.5.1 adapted)
from core.logger import log
from core.scene_runner import SceneRunner

class Timeline:
    """
    NeuroForge v1.5.1 Timeline
    -------------------------
    - 在执行场景时，将上一个场景的 ctx 传递给当前 SceneRunner（用于 transition 插件）
    - 其余逻辑与 v1.4 保持一致（时长提取优先级：mix/tts/compose）
    """

    def __init__(self, meta, scenes, output_dir="output"):
        self.meta = meta
        self.scenes = scenes
        self.output_dir = output_dir

    def run(self):
        cursor = 0.0
        summary = []
        prev_ctx = None

        for idx, scene_data in enumerate(self.scenes, start=1):
            sid = scene_data.get("id", idx)
            title = scene_data.get("title", f"Scene {sid}")
            log(f"\n🎞️ Executing Scene {sid}: {title}")
            log(f"⏱️ Start Time: {cursor:.2f}s")

            # 将 prev_ctx 传给 SceneRunner，以便插件（如 transition）能访问上一场景输出
            runner = SceneRunner(self.meta, scene_data, self.output_dir, prev_ctx=prev_ctx)
            ctx = runner.execute()

            # 保存本次 ctx 以便下一个场景使用
            prev_ctx = ctx

            # 提取时长（优先从 mix/tts/compose meta）
            duration = self._extract_duration(ctx)
            end_time = cursor + duration
            log(f"⏳ Scene {sid} Duration: {duration:.2f}s")

            summary.append({
                "scene_id": sid,
                "title": title,
                "start": cursor,
                "duration": duration,
                "end": end_time,
            })
            cursor = end_time

        # 汇总日志
        log("\n🧭 Auto-Timeline Summary:")
        for s in summary:
            log(f"  • Scene {s['scene_id']}: {s['start']:.2f}s → {s['end']:.2f}s")
        log("🎬 All scenes processed, timeline complete.")
        return summary

    # 内部方法：提取场景时长
    def _extract_duration(self, ctx) -> float:
        for key in ["mix", "tts", "compose"]:
            block = ctx.get(key, {})
            meta = block if isinstance(block, dict) else {}
            if "duration" in meta:
                try:
                    return float(meta["duration"])
                except Exception:
                    continue
        return 5.0  # fallback
