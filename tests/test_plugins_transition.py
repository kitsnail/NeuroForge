# tests/test_plugins_transition.py
import os
import shutil
import tempfile
from plugins.transition import plugin as transition
from core.io import IOManager

class DummyCtx:
    def __init__(self, base_dir):
        self.base = base_dir

def test_transition_metadata_creation(tmp_path, monkeypatch):
    # 准备两个 fake video files
    prev_video = tmp_path / "prev.mp4"
    curr_video = tmp_path / "curr.mp4"
    prev_video.write_text("dummy")
    curr_video.write_text("dummy")

    # 构造 prev_ctx with compose.video_out
    prev_ctx = {"scene_id": 1, "compose": {"video_out": str(prev_video)}}

    # current scene ctx skeleton
    scene_dir = str(tmp_path / "scene_2")
    os.makedirs(scene_dir, exist_ok=True)
    ctx = {
        "scene_id": 2,
        "scene_dir": scene_dir,
        "scene": {"id": 2, "title": "S2"},
        "compose": {"video_out": str(curr_video)},
        "prev_scene": {"scene_id": 1, "outputs": {"video": str(prev_video)}, "raw_ctx": prev_ctx}
    }

    res = transition.run(ctx)
    assert isinstance(res, dict)
    assert "transition" in res
    assert res["transition"]["status"] == "ok"
    tf = res["transition"]["transition_file"]
    assert os.path.exists(tf)
    # metadata json should exist
    assert os.path.exists(tf + ".json")
