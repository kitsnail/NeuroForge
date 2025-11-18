# plugins/compose/plugin.py
import os
import subprocess
from core.logger import log
from core.io import IOManager

def run(ctx):
    plugin = "compose"
    scene_dir = ctx["scene_dir"]
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)
    os.makedirs(out_dir, exist_ok=True)

    log(f"[{plugin}] composing final video...")

    canvas = ctx.get("canvas", {}).get("file")
    diagram = ctx.get("d2", {}).get("file")
    audio = ctx.get("mix", {}).get("audio")
    subtitle = ctx.get("tts", {}).get("subtitle")

    if not all([canvas, diagram, audio]):
        log(f"❌ Missing compose inputs: canvas={canvas}, diagram={diagram}, audio={audio}")
        return {"compose": None}

    # 获取音频长度
    try:
        audio_duration = float(
            subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", audio]
            ).decode().strip()
        )
    except Exception:
        audio_duration = 5.0  # fallback

    # 合成输出路径
    tmp_bg_video = os.path.join(out_dir, "background.mp4")
    output_video = os.path.join(out_dir, "final.mp4")

    # Step 1: 让背景图片持续整个音频时长
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1",  # 循环单帧
        "-i", canvas,
        "-t", str(audio_duration),
        "-vf", "scale=1280:720",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        tmp_bg_video
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Step 2: 叠加 diagram 图片到右下角
    overlayed_video = os.path.join(out_dir, "overlay.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", tmp_bg_video,
        "-i", diagram,
        "-filter_complex", "[0:v][1:v]overlay=W-w-50:H-h-50",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        overlayed_video
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Step 3: 添加音频并保持与音频对齐
    cmd = [
        "ffmpeg", "-y",
        "-i", overlayed_video,
        "-i", audio,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",  # 对齐音频长度
        output_video
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Step 4: 可选字幕嵌入
    if subtitle and os.path.exists(subtitle):
        final_with_sub = os.path.join(out_dir, "final_with_sub.mp4")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", output_video,
            "-vf", f"subtitles={subtitle}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF&'",
            "-c:a", "copy",
            final_with_sub
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_video = final_with_sub
        log(f"[compose] subtitles embedded.")

    log(f"[compose] successfully created final video → {output_video}")

    return {"compose": {"file": output_video}}
