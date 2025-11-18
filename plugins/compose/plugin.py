# ===========================================================
# NeuroForge v1.3 Plugin: compose
# -----------------------------------------------------------
# 功能：
#   将画面 (canvas + diagram) 与音频合成视频，自动嵌入字幕。
# 输出：
#   {"compose": {"status": "ok", "video_out": "...", "duration": float}}
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
    plugin = "compose"
    scene_dir = ctx["scene_dir"]
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)
    os.makedirs(out_dir, exist_ok=True)

    log(f"[{plugin}] composing video...")

    canvas = (ctx.get("canvas", {}) or {}).get("file")
    diagram = (ctx.get("d2", {}) or {}).get("file")
    audio = (ctx.get("mix", {}) or {}).get("audio_out") or (ctx.get("tts", {}) or {}).get("audio_out")
    subtitle = (ctx.get("tts", {}) or {}).get("subtitle_out")

    if not all([canvas, audio]):
        log(f"[compose] Missing inputs: canvas={canvas}, audio={audio}")
        return {"compose": {"status": "skip"}}

    dur = _probe_duration(audio) or 5.0
    bg_video = os.path.join(out_dir, "background.mp4")

    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", canvas, "-t", str(dur),
        "-vf", "scale=1280:720", "-c:v", "libx264", "-pix_fmt", "yuv420p", bg_video
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    overlay_video = os.path.join(out_dir, "overlay.mp4")
    if diagram and os.path.exists(diagram):
        subprocess.run([
            "ffmpeg", "-y", "-i", bg_video, "-i", diagram,
            "-filter_complex", "[0:v][1:v]overlay=W-w-50:H-h-50",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", overlay_video
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        overlay_video = bg_video

    out_video = os.path.join(out_dir, "final.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-i", overlay_video, "-i", audio,
        "-c:v", "copy", "-c:a", "aac", "-shortest", out_video
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if subtitle and os.path.exists(subtitle):
        sub_video = os.path.join(out_dir, "final_with_sub.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-i", out_video,
            "-vf", f"subtitles={subtitle}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF&'",
            "-c:a", "copy", sub_video
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_video = sub_video
        log(f"[compose] subtitles embedded.")

    log(f"[compose] output → {out_video}")
    return {"compose": {"status": "ok", "video_out": out_video, "duration": dur}}
