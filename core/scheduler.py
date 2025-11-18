# core/scheduler.py
from core.loader import PluginLoader
from core.pipeline import Pipeline

class Scheduler:
    """极简调度器：加载插件 → 执行 Pipeline"""

    def __init__(self, meta, scenes, output_dir="output"):
        self.meta = meta
        self.scenes = scenes
        self.output_dir = output_dir

    def run(self):
        PluginLoader.load_plugins()
        pipeline = Pipeline(self.meta, self.scenes, self.output_dir)
        pipeline.run()
