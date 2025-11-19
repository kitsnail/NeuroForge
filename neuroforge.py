# neuroforge.py (v1.5.1 CLI-fixed)
import sys
import yaml
from core.scheduler import Scheduler

def main():
    # 如果命令行给了参数，则使用该 YAML，否则使用默认 demo_v1_3.yaml
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = "configs/demo_v1_3.yaml"

    print(f"Loading config: {config_path}")

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
