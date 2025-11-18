# 🧠 NeuroForge — v1.0 (MVP Release)
**Release Date:** 2025-11-18  
**Codename:** *"Genesis of Cognitive Video"*

---

### 🚀 Highlights
- First complete run of the **NeuroForge AI video pipeline**  
- Achieved full modularization — each plugin can run standalone or via pipeline
- Implemented precise audio-video synchronization (4.63s verified)
- Full visual composition with diagram overlay + background music mix

---

### 🧩 Core System

**`core/`**
- `io.py`: Minimalist I/O and path manager ensuring deterministic structure
- `logger.py`: Structured event logging with timestamp & emoji tags
- `loader.py`: Dynamic plugin discovery system (auto-scan & hot-load)
- `pipeline.py`: Scene orchestrator — supports multi-stage plugin flow

**Philosophy:**  
> “Keep the core small, composable, and self-healing.”

---

### 🎛️ Plugins

| Plugin | Description | Status |
|---------|--------------|---------|
| 🎨 **canvas** | Generates base visual layer (PNG background) | ✅ |
| 🧭 **d2** | Integrates D2 diagrams via CLI | ✅ |
| 🗣️ **tts** | Edge-TTS powered text-to-speech with auto chunking + SRT subtitles | ✅ |
| 🎧 **mix** | Smart audio mixer — trims BGM to TTS length & volume balances | ✅ |
| 🎬 **compose** | Combines visuals + audio + subtitles → final MP4 | ✅ |

---

### ⚙️ Key Features
- Full **decoupling of plugin lifecycle**
- Automatic **audio length trimming**
- Deterministic **scene I/O routing**
- K8s-inspired **modular micro-pipeline**
- Supports **custom YAML pipelines**

---

### 🌱 Design Philosophy
> **“Minimal Complexity, Maximum Extensibility.”**  
> NeuroForge treats each creative step as a modular neuron —  
> composable, replaceable, and endlessly scalable.

---

### 🔮 Next Steps — v1.1 & Beyond
- 🧩 **Timeline System** — multi-scene composition
- 💬 **SubtitleOverlay Plugin** — stylized captions
- 🌈 **FX Layer** — motion graphics and visual filters
- 🪄 **Prompt2Scene Engine** — AI-driven narrative segmentation

---

### 🧾 Meta
- **Author:** wh  
- **Project Start:** Nov 2025  
- **Philosophy:**  Creativity through structural precision
