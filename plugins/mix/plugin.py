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
    tts_audio = tts_info.get("audio")
    bgm = ctx["scene"].get("bgm")

    # 检查输入
    if not tts_audio or not os.path.exists(tts_audio):
        log("❌ mix: no valid TTS audio found.")
        return {"mix": None}

    if not bgm or not os.path.exists(bgm):
        log("⚠️ BGM missing or invalid, using TTS only.")
        final_audio = os.path.join(out_dir, "mixed_audio.wav")
        subprocess.run(["cp", tts_audio, final_audio])
        return {"mix": {"audio": final_audio}}

    # 获取 TTS 时长（秒）
    try:
        tts_duration = float(
            subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", tts_audio]
            ).decode().strip()
        )
        log(f"[mix] detected TTS duration = {tts_duration:.2f}s")
    except Exception:
        tts_duration = None

    out_file = os.path.join(out_dir, "mixed_audio.wav")

    # 先裁剪 BGM 到 TTS 同步时长
    trimmed_bgm = os.path.join(out_dir, "bgm_trimmed.wav")
    if tts_duration:
        subprocess.run([
            "ffmpeg", "-y", "-i", bgm,
            "-ss", "0", "-t", str(tts_duration),
            "-c:a", "pcm_s16le", trimmed_bgm
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        log("[mix] ⚠️ cannot detect TTS duration, using full BGM.")
        trimmed_bgm = bgm

    # 混音，保证输出总长与 TTS 一致
    cmd = [
        "ffmpeg", "-y",
        "-i", trimmed_bgm,
        "-i", tts_audio,
        "-filter_complex",
        "[0:a]volume=0.3[a0];[1:a]volume=1.0[a1];"
        "[a0][a1]amix=inputs=2:duration=shortest",
        "-c:a", "pcm_s16le",
        out_file
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log(f"[mix] output → {out_file}")

    return {"mix": {"audio": out_file}}
