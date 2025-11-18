# plugins/mix/plugin.py

import os
import subprocess
from core.logger import log
from core.io import IOManager

def run(ctx):
    plugin = "mix"
    scene_dir = ctx["scene_dir"]
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)

    log(f"[{plugin}] mixing audio...")

    tts_info = ctx.get("tts", {})

    # 修复点：读取正确字段
    tts_audio = tts_info.get("audio")

    if not tts_audio:
        log("❌ mix: no TTS audio found in ctx['tts']['audio']")
        return {"mix": None}

    bgm = ctx["scene"].get("bgm")

    if not bgm or not os.path.exists(bgm):
        log("⚠️ BGM missing or invalid, mixing TTS only.")
        final_audio = os.path.join(out_dir, "mixed_audio.wav")
        # 直接复制
        subprocess.run(["cp", tts_audio, final_audio])
        return {"mix": {"audio": final_audio}}

    # 输出文件
    out_file = os.path.join(out_dir, "mixed_audio.wav")

    # ffmpeg 混音：TTS 主音 + BGM 降低音量
    cmd = [
        "ffmpeg", "-y",
        "-i", bgm,
        "-i", tts_audio,
        "-filter_complex",
        "[0:a]volume=0.3[a0];[1:a]volume=1.0[a1];[a0][a1]amix=inputs=2:duration=longest",
        "-c:a", "pcm_s16le",
        out_file
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    log(f"[mix] output → {out_file}")

    return {"mix": {"audio": out_file}}
