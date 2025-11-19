# plugins/analyze/plugin.py
"""
Analyze plugin (v1.5.1)
- 规则版的 narration 分句、停顿建议、情绪关键词提取
- 输出 JSON 到插件目录，并返回 {"analyze": {...}} 到 ctx
"""

import os
import re
import json
from datetime import datetime
from core.io import IOManager
from core.logger import log

POSITIVE = {"快乐", "高兴", "喜悦", "兴奋", "满意", "美好"}
NEGATIVE = {"悲伤", "难过", "愤怒", "失望", "痛苦"}

def _split_sentences(text: str):
    parts = re.split(r'([。！？\n])', text)
    segs = []
    buf = ""
    for p in parts:
        if p is None:
            continue
        buf += p
        if p in "。！？\n":
            s = buf.strip()
            if s:
                segs.append(s)
            buf = ""
    if buf.strip():
        segs.append(buf.strip())
    return segs

def _suggest_pauses(segs):
    out = []
    for i, s in enumerate(segs):
        ln = len(s)
        if ln <= 6:
            pause = 0.12
        elif ln <= 14:
            pause = 0.25
        else:
            pause = 0.4
        out.append({"index": i, "text": s, "suggested_pause_after": pause})
    return out

def _extract_emotions(text):
    pos = [w for w in POSITIVE if w in text]
    neg = [w for w in NEGATIVE if w in text]
    return {"positive": pos, "negative": neg}

def run(ctx):
    plugin = "analyze"
    scene_id = ctx.get("scene_id")
    scene = ctx.get("scene", {}) or {}
    narration = (scene.get("narration") or "").strip()

    scene_dir = ctx.get("scene_dir")
    out_dir = IOManager.get_plugin_dir(scene_dir, plugin)
    os.makedirs(out_dir, exist_ok=True)

    if not narration:
        log(f"[{plugin}] skip (no narration)")
        return {plugin: {"status": "skip", "reason": "no_narration"}}

    sentences = _split_sentences(narration)
    pauses = _suggest_pauses(sentences)
    emotions = _extract_emotions(narration)

    out = {
        "scene_id": scene_id,
        "narration_length": len(narration),
        "sentence_count": len(sentences),
        "sentences": sentences,
        "pauses": pauses,
        "emotions": emotions,
        "generated_at": datetime.utcnow().isoformat()
    }

    out_path = os.path.join(out_dir, f"analyze_{scene_id}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    log(f"[{plugin}] analysis → {out_path}")
    return {plugin: {"status": "ok", "analysis_file": out_path, "sentence_count": len(sentences)}}
