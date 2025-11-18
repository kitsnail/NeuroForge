# ===========================================================
# NeuroForge v1.3 Entry Point
# -----------------------------------------------------------
# 加载配置 → 启动 Scheduler → 执行时间线。
# ===========================================================

import yaml
from core.scheduler import Scheduler

def main(config_path="configs/demo_v1_3.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    scheduler = Scheduler(
        meta=cfg.get("meta", {}),
        scenes=cfg.get("scenes", []),
        output_dir=cfg.get("output_dir", "output")
    )
    scheduler.run()

if __name__ == "__main__":
    main()
