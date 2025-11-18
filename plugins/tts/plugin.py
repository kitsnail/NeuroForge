# plugins/tts/plugin.py
import os
import asyncio
import uuid
import re
from pydub import AudioSegment
import edge_tts

from core.logger import log
from core.io import IOManager

# =============================
# 配置
# =============================
CHUNK_MAX = 300  # 每段最大字符数
VOICE = "zh-CN-XiaoxiaoNeural"
FRAME_RATE = 24000  # 最终音频 24kHz
CHANNELS = 1        # 单声道

# =============================
# 文本切片
# =============================
def _split_into_chunks(text, max_chars=CHUNK_MAX):
    paras = [p.strip() for p in re.split(r'\n+', text) if p.strip()]
    chunks = []
    for p in paras:
        if len(p) <= max_chars:
            chunks.append(p)
        else:
            parts = re.split(r'([，,。\.；;！!\?:\?])', p)
            cur = ""
            for piece in parts:
                if not piece:
                    continue
                if len(cur) + len(piece) <= max_chars:
                    cur += piece
                else:
                    if cur:
                        chunks.append(cur.strip())
                    cur = piece
            if cur:
                chunks.append(cur.strip())
    return [c for c in chunks if c]

# =============================
# edge-tts 合成单段
# =============================
async def _synthesize_to_mp3(text, out_mp3, voice=VOICE):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(out_mp3)

# =============================
# SRT 时间格式
# =============================
def _format_srt_time(seconds_float):
    ms = int(round(seconds_float * 1000))
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

# =============================
# 写 SRT 文件
# =============================
def _write_srt(items, out_srt):
    lines = []
    for idx, start, end, text in items:
        lines.append(str(idx))
        lines.append(f"{_format_srt_time(start)} --> {_format_srt_time(end)}")
        lines.append(text.replace("\n", "\\n"))
        lines.append("")
    with open(out_srt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# =============================
# NeuroForge 插件入口
# =============================
def run(ctx):
    plugin = "tts"
    scene_dir = ctx["scene_dir"]
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)

    narration = (ctx.get("scene", {}).get("tts") or "").strip()

    if not narration:
        log("[tts] No narration text. Skip.")
        return {"tts": None}

    log(f"[tts] Generating speech... len={len(narration)} chars")

    chunks = _split_into_chunks(narration)
    if not chunks:
        return {"tts": None, "warning": "text empty after split"}

    # 临时存储切片
    tmpdir = os.path.join(out_dir, "chunks")
    os.makedirs(tmpdir, exist_ok=True)
    mp3_list = []

    async def synth_all():
        for idx, chunk in enumerate(chunks):
            out_mp3 = os.path.join(tmpdir, f"{idx}_{uuid.uuid4().hex}.mp3")
            try:
                await _synthesize_to_mp3(chunk, out_mp3)
            except Exception:
                # 重试一次
                await _synthesize_to_mp3(chunk, out_mp3)
            mp3_list.append((out_mp3, chunk))

    # 异步合成
    try:
        asyncio.run(synth_all())
    except Exception as e:
        return {"status": "error", "error": f"edge-tts failed: {e}"}

    # =============================
    # 音频拼接
    # =============================
    try:
        segments = []
        srt_items = []
        cursor = 0.0

        for idx, (mp3path, text) in enumerate(mp3_list, start=1):
            seg = AudioSegment.from_file(mp3path)
            seg = seg.set_frame_rate(FRAME_RATE).set_channels(CHANNELS)
            segments.append(seg)

            dur = seg.duration_seconds
            start = cursor
            end = cursor + dur
            srt_items.append((idx, start, end, text))
            cursor = end

        # 合并 WAV
        final_seg = segments[0]
        for seg in segments[1:]:
            final_seg += seg

        out_wav = os.path.join(out_dir, "tts.wav")
        final_seg.export(out_wav, format="wav", parameters=["-ar", str(FRAME_RATE), "-ac", "1"])

        # 写入 SRT
        out_srt = os.path.join(out_dir, "subtitle.srt")
        _write_srt(srt_items, out_srt)

    except Exception as e:
        return {"status": 'error', "error": f"concat failed: {e}"}

    log(f"[tts] Audio → {out_wav}")
    log(f"[tts] Subtitle → {out_srt}")

    return {
        "tts": {
            "audio": out_wav,
            "subtitle": out_srt
        }
    }
