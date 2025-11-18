# core/scheduler.py (v1.4)
from core.logger import log
from core.timeline import Timeline

class Scheduler:
    def __init__(self, meta=None, scenes=None, output_dir="output"):
        self.meta = meta or {}
        self.scenes = scenes or []
        self.output_dir = output_dir

    def run(self):
        log("🚀 NeuroForge v1.4 Scheduler Started (Minimal Core Mode)")
        timeline = Timeline(self.meta, self.scenes, self.output_dir)
        timeline.run()
        log("✅ All scenes executed successfully.")
