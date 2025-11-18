# core/timeline.py (v1.4)
from core.logger import log
from core.scene_runner import SceneRunner

class Timeline:
    """
    NeuroForge v1.4 Timeline
    ------------------------
    职责：负责时间线调度与时长汇总。
    - 不直接执行插件逻辑
    - 从 ctx 中读取场景时长信息
    """

    def __init__(self, meta, scenes, output_dir="output"):
        self.meta = meta
        self.scenes = scenes
        self.output_dir = output_dir

    def run(self):
        cursor = 0.0
        summary = []

        for idx, scene_data in enumerate(self.scenes, start=1):
            sid = scene_data.get("id", idx)
            title = scene_data.get("title", f"Scene {sid}")
            log(f"\n🎞️ Executing Scene {sid}: {title}")
            log(f"⏱️ Start Time: {cursor:.2f}s")

            runner = SceneRunner(self.meta, scene_data, self.output_dir)
            ctx = runner.execute()

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
            meta = block.get("meta", {})
            if "duration" in meta:
                return float(meta["duration"])
        return 5.0  # fallback
