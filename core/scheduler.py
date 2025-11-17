class Scheduler:
    def __init__(self, registry):
        self.registry = registry

    def run_scene(self, scene):
        print(f"[NeuroForge] Running scene: {scene.title}")

        # 目前 Demo：只调用 echo 插件
        out = self.registry.run("echo", {
            "title": scene.title,
            "narration": scene.narration,
            "visual": scene.visual,
            "subtitle": scene.subtitle
        })

        return out
