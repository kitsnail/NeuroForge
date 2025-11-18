# ===========================================================
# NeuroForge v1.3 Plugin: tts
# -----------------------------------------------------------
# 功能：
#   将场景叙述文本 narration 转换为语音 + 字幕。
# 输出：
#   {"tts": {"status": "ok", "audio_out": "...", "subtitle_out": "...", "duration": float}}
# ===========================================================

import os
import asyncio
import uuid
import re
from pydub import AudioSegment
import edge_tts
from core.logger import log
from core.io import IOManager

CHUNK_MAX = 300
VOICE = "zh-CN-XiaoxiaoNeural"
FRAME_RATE = 24000
CHANNELS = 1

def _split_text(text, max_len=CHUNK_MAX):
    paras = [p.strip() for p in re.split(r'\n+', text) if p.strip()]
    chunks = []
    for p in paras:
        if len(p) <= max_len:
            chunks.append(p)
        else:
            parts = re.split(r'([，,。\.；;！!\?:\?])', p)
            cur = ""
            for piece in parts:
                if len(cur) + len(piece) <= max_len:
                    cur += piece
                else:
                    if cur:
                        chunks.append(cur.strip())
                    cur = piece
            if cur:
                chunks.append(cur.strip())
    return chunks

async def _tts_chunk(text, out_mp3, voice=VOICE):
    await edge_tts.Communicate(text, voice=voice).save(out_mp3)

def _format_srt_time(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def _write_srt(items, out_srt):
    lines = []
    for idx, start, end, text in items:
        lines.append(str(idx))
        lines.append(f"{_format_srt_time(start)} --> {_format_srt_time(end)}")
        lines.append(text)
        lines.append("")
    with open(out_srt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def run(ctx):
    plugin = "tts"
    scene_dir = ctx["scene_dir"]
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)
    os.makedirs(out_dir, exist_ok=True)

    narration = (ctx.get("scene", {}).get("narration") or "").strip()
    if not narration:
        log("[tts] No narration text, skip.")
        return {"tts": {"status": "skip"}}

    log(f"[{plugin}] Generating TTS audio, len={len(narration)} chars")

    chunks = _split_text(narration)
    tmpdir = os.path.join(out_dir, "chunks")
    os.makedirs(tmpdir, exist_ok=True)
    mp3_files = []

    async def synth_all():
        for idx, chunk in enumerate(chunks):
            out_mp3 = os.path.join(tmpdir, f"{idx}_{uuid.uuid4().hex}.mp3")
            await _tts_chunk(chunk, out_mp3)
            mp3_files.append((out_mp3, chunk))

    asyncio.run(synth_all())

    # 拼接音频并生成字幕
    audio_segments = []
    srt_items = []
    cursor = 0.0

    for idx, (path, text) in enumerate(mp3_files, start=1):
        seg = AudioSegment.from_file(path).set_frame_rate(FRAME_RATE).set_channels(CHANNELS)
        dur = seg.duration_seconds
        srt_items.append((idx, cursor, cursor + dur, text))
        cursor += dur
        audio_segments.append(seg)

    final_audio = sum(audio_segments)
    out_wav = os.path.join(out_dir, "tts.wav")
    out_srt = os.path.join(out_dir, "subtitle.srt")
    final_audio.export(out_wav, format="wav")
    _write_srt(srt_items, out_srt)

    log(f"[{plugin}] Audio → {out_wav}")
    log(f"[{plugin}] Subtitle → {out_srt}")

    return {
        "tts": {
            "status": "ok",
            "audio_out": out_wav,
            "subtitle_out": out_srt,
            "duration": cursor
        }
    }
