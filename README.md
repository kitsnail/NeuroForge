# 🧠 NeuroForge v1.3  
> **AI 驱动的视频时间线编排引擎**  
> —— 面向下一代智能视频创作架构

---

## 🚀 项目概述

**NeuroForge** 是一个由 AI 驱动的视频编排与合成引擎。  
它通过 **多插件流水线架构**，将文字叙述、语音合成、图像生成、音视频合成等 AI 模块整合为一个自动化视频生成系统。

v1.3 是首个实现 **统一规范化插件接口** 与 **自动时间线系统 (Auto-Timeline Engine)** 的版本。  
该版本正式确立了 **NeuroForge Core Architecture**：

```yaml
Text Narration → TTS → Audio Mix → Visual Compose → Timeline Output
```

---

## 🧩 核心特性

| 模块 | 功能 | 状态 |
|------|------|------|
| 🧠 **AI Narration Engine** | 支持基于文本或AI生成剧本 | ✅ |
| 🔊 **TTS Plugin** | 自动语音合成 + 字幕生成 | ✅ |
| 🎧 **Audio Mix Plugin** | 背景音乐混合与时长对齐 | ✅ |
| 🖼 **Canvas / D2 Plugins** | 自动生成视觉背景 / 结构图 | ✅ |
| 🎬 **Compose Plugin** | 合成最终视频并嵌入字幕 | ✅ |
| 🕰 **Auto Timeline Engine** | 动态计算场景时长，构建时间线 | ✅ |
| 🧩 **Plugin System** | 模块化执行，可扩展新插件 | ✅ |
| 📁 **IO Manager** | 统一输出路径与结构管理 | ✅ |

---

## 📁 项目结构

```sh

NeuroForge/
├── core/
│   ├── io.py              ← 输入/输出管理
│   ├── loader.py          ← 插件加载器
│   ├── logger.py          ← 统一日志系统
│   ├── scene_runner.py    ← 单场景执行单元
│   ├── timeline.py        ← 自动时间线系统
│   └── scheduler.py       ← 全局调度器
│
├── plugins/
│   ├── canvas/   ← 背景生成
│   ├── d2/       ← 结构图生成
│   ├── tts/      ← 文本语音合成
│   ├── mix/      ← 音频混合
│   ├── compose/  ← 视频合成
│   └── ...       ← 自定义插件扩展点
│
├── configs/
│   ├── demo_v1_3.yaml     ← 示例配置文件
│
├── assets/                ← 素材文件夹（如BGM）
│
├── output/                ← 输出结果（自动生成）
│   ├── scene_1/
│   ├── scene_2/
│   └── ...
│
└── neuroforge.py          ← 主入口

````

---

## ⚙️ 配置文件结构（YAML）

示例：`configs/demo_v1_3.yaml`

```yaml
meta:
  version: 1.3
  project: "NeuroForge Unified Standard"
  author: "wh"
  bgm: "assets/bgm/soft_thinking.mp3"

timeline:
  mode: auto  # 自动根据语音时长计算时间线

scenes:
  - id: 1
    title: "Introduction"
    narration: "Welcome to NeuroForge — an AI-driven video creation framework."
    pipeline: [canvas, d2, tts, mix, compose]

  - id: 2
    title: "AI Composed Story"
    narration: "In this scene, NeuroForge seamlessly connects AI narration with visuals and sound."
    pipeline: [canvas, tts, mix, compose]
````

---

## 🔄 执行示例

```bash
python3 neuroforge.py configs/demo_v1_3.yaml
```

**执行输出示例：**

```
[NeuroForge] 🚀 NeuroForge v1.3 Scheduler Initialized
🎞️ Executing Scene 1: Introduction
...
⏳ Scene 1 Duration: 7.10s
🎞️ Executing Scene 2: AI Composed Story
...
⏳ Scene 2 Duration: 7.42s
🧭 Auto-Timeline Summary:
  • Scene 1: 0.00s → 7.10s
  • Scene 2: 7.10s → 14.52s
🎬 All scenes processed, auto timeline complete.
✅ All scenes executed successfully.
```

---

## 🧱 插件开发规范（v1.3 标准）

每个插件必须：

* 位于 `plugins/<name>/plugin.py`
* 定义主函数：`def run(ctx):`
* 返回统一结构：

```python
return {
  "<plugin_name>": {
    "<output_key>": "path/to/output.file",
    "meta": { "duration": 7.1 }
  }
}
```

### 插件上下文 (ctx)

| 键名          | 类型       | 描述       |
| ----------- | -------- | -------- |
| `meta`      | dict     | 全局项目信息   |
| `scene`     | dict     | 当前场景配置   |
| `scene_id`  | int      | 场景编号     |
| `scene_dir` | str      | 当前场景输出目录 |
| `timeline`  | optional | 全局时间线数据  |

---

## 🔊 插件示例：TTS

```python
return {
  "tts": {
    "audio_out": "output/scene_1/tts/tts.wav",
    "subtitle_out": "output/scene_1/tts/subtitle.srt",
    "meta": {"duration": 4.63}
  }
}
```

## 🎧 插件示例：Mix

```python
return {
  "mix": {
    "audio_out": "output/scene_1/mix/mixed_audio.wav",
    "meta": {"duration": 4.63}
  }
}
```

## 🎬 插件示例：Compose

```python
return {
  "compose": {
    "video_out": "output/scene_1/compose/final_with_sub.mp4",
    "meta": {"duration": 7.10}
  }
}
```

---

## 🧭 输出结果结构

```
output/
├── scene_1/
│   ├── canvas/canvas.png
│   ├── tts/tts.wav
│   ├── tts/subtitle.srt
│   ├── mix/mixed_audio.wav
│   └── compose/final_with_sub.mp4
│
└── scene_2/
    ├── ...
```

---

## 💡 设计哲学

> **“AI 不是生成视频，而是编排叙事。”**

NeuroForge 的核心思想是：

> 将 AI 从“生成单一媒体”提升到“组织多模态时间序列”的层面。

这意味着：

* 文本、语音、图像、视频是“元素”；
* 时间线是“骨架”；
* NeuroForge 是“导演”。

---

## 🧭 未来规划（v1.4+）

| 模块                     | 目标功能                                |
| ---------------------- | ----------------------------------- |
| 🎞️ `timeline.merge()` | 自动拼接所有场景视频为完整影片                     |
| 🗣️ `ai.scriptgen`     | 自动剧本文案生成（LLM 接入）                    |
| 🎨 `ai.visual`         | 自动生成背景画面（Stable Diffusion / DALL·E） |
| 🧩 `plugin.registry`   | 在线插件注册与热加载                          |
| 🧰 `editor.gui`        | 图形化编排编辑器                            |

---

## 🧑‍💻 作者与版权

**Author:** wh
**Project:** NeuroForge
**Version:** 1.3 (Unified Plugin Standard + Auto Timeline Edition)
**License:** MIT

---

> *“In the future, AI will not just create — it will compose time.”*
> — **NeuroForge Philosophy**