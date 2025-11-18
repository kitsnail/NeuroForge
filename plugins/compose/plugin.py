# plugins/compose/plugin.py

import os
import subprocess
from core.logger import log
from core.io import IOManager

def run(ctx):
    plugin = "compose"
    scene_dir = ctx["scene_dir"]
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)

    log(f"[{plugin}] composing final video...")

    # 获取文件路径
    canvas = ctx.get("canvas", {}).get("file")
    diagram = ctx.get("d2", {}).get("file")
    audio = ctx.get("mix", {}).get("audio")

    # 检查每个文件是否存在
    if not all([canvas, diagram, audio]):
        log(f"❌ Missing files: canvas={canvas}, diagram={diagram}, audio={audio}")
        return {"compose": None, "error": "Missing files for composition."}

    output_mp4 = os.path.join(out_dir, "final.mp4")

    # 使用 FFmpeg 将图像叠加 + 音频合成
    cmd = [
        "ffmpeg", "-y",
        "-i", canvas,
        "-i", diagram,
        "-filter_complex", "[0:v][1:v]overlay=W-w-50:H-h-50",  # 将 diagram 放置在 canvas 上
        "-i", audio,
        "-map", "0:v",  # 使用画布视频流
        "-map", "2:a",  # 使用混音音频
        "-shortest",  # 保持音频时长最短
        output_mp4
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log(f"[compose] successfully created final video → {output_mp4}")
    except subprocess.CalledProcessError as e:
        log(f"🔥 FFmpeg error: {e}")
        return {"compose": None, "error": f"FFmpeg failed: {e}"}

    return {"compose": {"file": output_mp4}}
