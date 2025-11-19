# tests/test_plugins_analyze.py
import os
import tempfile
from plugins.analyze import plugin as analyze

def test_analyze_writes_file(tmp_path):
    scene_dir = str(tmp_path / "scene_10")
    os.makedirs(scene_dir, exist_ok=True)
    ctx = {
        "scene_id": 10,
        "scene_dir": scene_dir,
        "scene": {"id": 10, "narration": "今天天气很好。我们去散步吧！"}
    }
    res = analyze.run(ctx)
    assert "analyze" in res
    assert res["analyze"]["status"] == "ok"
    path = res["analyze"]["analysis_file"]
    assert os.path.exists(path)
    # load and check
    import json
    j = json.load(open(path, "r", encoding="utf-8"))
    assert j["sentence_count"] >= 1
