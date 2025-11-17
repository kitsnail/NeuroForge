class Pipeline:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def run(self, meta, scenes):
        print("🚀 NeuroForge Pipeline started!")
        results = []

        for scene in scenes:
            result = self.scheduler.run_scene(scene)
            results.append(result)

        print("✨ Pipeline finished!")
        return results
