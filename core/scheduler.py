# ===========================================================
# NeuroForge v1.3 Core: Scheduler
# -----------------------------------------------------------
# 功能：
#   项目的全局调度器，加载 Timeline 并执行全流程。
# ===========================================================

from core.logger import log
from core.timeline import Timeline

class Scheduler:
    def __init__(self, meta=None, scenes=None, output_dir="output"):
        self.meta = meta or {}
        self.scenes = scenes or []
        self.output_dir = output_dir

    def run(self):
        """执行完整时间线调度"""
        log("🚀 NeuroForge v1.3 Scheduler Initialized")
        timeline = Timeline(self.meta, self.scenes, self.output_dir)
        timeline.execute()
        log("✅ All scenes executed successfully.")
