# neuroforge.py
import yaml
from core.scheduler import Scheduler

def main(config_path="configs/demo.yaml"):
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
