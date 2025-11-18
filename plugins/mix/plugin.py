# ===========================================================
# NeuroForge v1.3 Plugin: mix
# -----------------------------------------------------------
# 功能：
#   将 TTS 输出语音与背景音乐混音并同步时长。
# 输出：
#   {"mix": {"status": "ok", "audio_out": "...", "duration": float}}
# ===========================================================

import os
import subprocess
from core.logger import log
from core.io import IOManager

def _probe_duration(path):
    if not path or not os.path.exists(path):
        return None
    try:
        return float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", path
        ]).decode().strip())
    except Exception:
        return None

def run(ctx):
    plugin = "mix"
    scene_dir = ctx["scene_dir"]
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)
    os.makedirs(out_dir, exist_ok=True)

    log(f"[{plugin}] mixing audio...")

    tts_audio = (ctx.get("tts", {}) or {}).get("audio_out")
    bgm = ctx.get("scene", {}).get("bgm") or ctx.get("meta", {}).get("bgm")

    if not tts_audio or not os.path.exists(tts_audio):
        log("❌ [mix] no valid TTS audio found.")
        return {"mix": {"status": "skip"}}

    tts_dur = _probe_duration(tts_audio)
    if not bgm or not os.path.exists(bgm):
        log("[mix] No valid BGM, using TTS only.")
        out_file = os.path.join(out_dir, "mixed_audio.wav")
        subprocess.run(["cp", tts_audio, out_file])
        return {"mix": {"status": "ok", "audio_out": out_file, "duration": tts_dur}}

    trimmed_bgm = os.path.join(out_dir, "bgm_trimmed.wav")
    subprocess.run([
        "ffmpeg", "-y", "-i", bgm, "-t", str(tts_dur), "-c:a", "pcm_s16le", trimmed_bgm
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out_file = os.path.join(out_dir, "mixed_audio.wav")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", trimmed_bgm,
        "-i", tts_audio,
        "-filter_complex", "[0:a]volume=0.3[a0];[1:a]volume=1.0[a1];[a0][a1]amix=inputs=2:duration=shortest",
        "-c:a", "pcm_s16le", out_file
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    log(f"[{plugin}] output → {out_file}")
    return {"mix": {"status": "ok", "audio_out": out_file, "duration": tts_dur}}
