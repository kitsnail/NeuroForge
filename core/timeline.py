# ===========================================================
# NeuroForge v1.3 Core: Timeline
# -----------------------------------------------------------
# 功能：
#   统一管理场景顺序与时间线，顺序执行所有 SceneRunner。
# 输出：
#   summary 列表，包含每个场景的开始/结束时间。
# ===========================================================

from core.logger import log
from core.scene_runner import SceneRunner

class Timeline:
    def __init__(self, meta, scenes, output_dir="output"):
        self.meta = meta
        self.scenes = scenes or []
        self.output_dir = output_dir

    def execute(self):
        """按顺序执行所有场景"""
        cursor = 0.0
        summary = []

        for idx, scene in enumerate(self.scenes, start=1):
            sid = scene.get("id", idx)
            title = scene.get("title", f"Scene {sid}")
            log(f"\n🎞️ Executing Scene {sid}: {title}")
            log(f"⏱️ Start Time: {cursor:.2f}s")

            runner = SceneRunner(self.meta, scene, self.output_dir)
            result = runner.run()

            dur = float(result.get("duration", 0.0))
            summary.append({
                "scene_id": sid,
                "title": title,
                "start": cursor,
                "duration": dur,
                "end": cursor + dur
            })

            log(f"⏳ Scene {sid} Duration: {dur:.2f}s")
            cursor += dur

        log("\n🧭 Auto-Timeline Summary:")
        for s in summary:
            log(f"  • Scene {s['scene_id']}: {s['start']:.2f}s → {s['end']:.2f}s")

        log("🎬 All scenes processed, auto timeline complete.")
        return summary
