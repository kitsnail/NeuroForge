# 🚀 NeuroForge

### **结构化·插件化·可扩展的 AI 视频自动化创作平台**

*Structure-Driven, Plugin-Powered, Future-Proof.*

---

## 🌌 项目简介

**NeuroForge** 是一个为 **AI 视频创作、结构化内容生产、自动化媒体流水线** 而设计的
**插件化 + 模块化 + 可扩展** 的开源系统。

核心目标：

* 🧠 让创作者只关注 **结构（Structure）**
* 🔌 所有素材处理（图片、TTS、字幕、动画、合成）全部由 **插件负责**
* 🔁 项目核心永远保持轻量、可维护
* 🛠️ 简单、通用、像 Linux 一样可无限扩展
* 🎬 一键从 Markdown → 完整视频

NeuroForge **不直接做生成**，
它是一个 **调度系统 / 视频 OS / 插件运行时（Runtime）**。

未来你可以像装“插件 App”一样扩展整个能力宇宙。

---

# ✨ 功能特性（v1.0）

### 📦 1. Markdown 一键生成结构化场景

解析器自动解析视频脚本：

* 元信息（title / author / bgm / fps…）
* 多场景结构
* narration（旁白）
* visual（D2 或动画代码）
* subtitle（字幕格式）

生成统一结构数据交给插件。

---

### 🔌 2. 插件系统（NeuroForge 的灵魂）

所有功能都以插件形式存在，例如：

| 插件类型        | 功能                          |
| ----------- | --------------------------- |
| `tts`       | 文本转语音 (支持停顿语法 `((⏱️=800))`) |
| `d2`        | 将 `.d2` 图生成 SVG/PNG         |
| `manim`     | 数学或结构动画                     |
| `ffmpeg`    | 最终视频合成                      |
| `bgm`       | 背景音乐混音                      |
| `caption`   | 字幕生成                        |
| `imagegen`  | AI 图片生成插件                   |
| `inference` | 各类模型推理（未来可接 openai/vllm）    |

---

### 🔁 3. Pipeline（流水线调度）

每个场景自动进入流水线：

```
Parse → Plugin Run → Material → Assemble → Video
```

你可以定制自己的 pipeline。

---

### 🧱 4. 模块化项目结构

核心和插件完全解耦，不会产生“巨石工程”。

---

### 🎬 5. 可扩展的未来

NeuroForge 未来将发展为：

* 视频 OS
* 动态结构动画引擎
* 结构化 AI 创作 IDE
* 模型路由 × 创作工具链的统一平台

---

# 📁 项目结构

```
neuroforge/
│
├── core/               # 核心系统（不处理任何素材）
│   ├── parser.py       # Markdown → Scene
│   ├── registry.py     # 插件注册中心
│   ├── scheduler.py    # 调度器
│   ├── pipeline.py     # 运行流水线
│   └── config.py
│
├── plugins/            # 插件目录
│   └── echo_plugin/    
│       ├── plugin.yaml
│       └── plugin.py
│
├── cli/
│   └── main.py         # neuroforge CLI
│
├── examples/
│   └── demo.md
│
└── neuroforge.py       # 项目入口
```

---

# 🧪 快速开始（Quick Start）

### 1. 克隆项目

```
git clone https://github.com/xxx/NeuroForge.git
cd NeuroForge
```

### 2. 安装依赖

```
pip install -r requirements.txt
```

### 3. 运行 Demo

```
python3 neuroforge.py run examples/demo.md
```

你将看到：

```
🚀 NeuroForge Pipeline started!
[NeuroForge] Running scene: Scene 1
🔧 [echo plugin] received:
{ ... }
✨ Pipeline finished!
```

（说明插件系统、解析系统、调度系统全都正常运行。）

---

# 🔌 如何编写一个插件？

只需要两个文件：

## 1) plugin.yaml

```yaml
name: d2_renderer
type: visual
entry: plugin.py:render
```

## 2) plugin.py

```python
def render(input_data):
    d2_code = input_data["visual"]
    # 调用 d2 生成 SVG
    return {"svg_path": "xxx.svg"}
```

NeuroForge 会自动加载，无需修改核心代码。

---

# 🎨 视频脚本格式（Markdown）

```
---
title: 什么是结构？
author: wh
fps: 30
---

## 开场——为什么要讲结构？
### narration
- “你有没有一种感觉…”
- “有些人，看问题总是更快、更准、更深？”

### visual
A: "信息"
B: "结构"
A -> B

### subtitle
color: "#00ffff"
```

---

# 🛠️ Roadmap（未来路线）

### 🚧 v1.1（开发中）

* D2 渲染插件
* TTS 插件（带停顿）
* FFmpeg 合成插件
* 视频模板系统（结构动画模板库）

### 🚀 v2.0

* 全自动 AI 视频工厂
* “结构动画引擎”
* 大模型推理插件（OpenAI、vLLM、SGLang）
* 流程可视化 UI

### 🌌 v3.0

* NeuroForge OS（结构化内容的生产操作系统）
* 模型互联网 × 创作链路
* 行业级 Pipeline 编辑器（像 AfterEffects 但用结构驱动）

---

# 🤝 贡献（Contributing）

欢迎提交：

* 插件
* 动画模板
* 文档
* Bug 修复
* 示例脚本

提交 issue / PR 即可。

---

# 📜 许可证（License）

MIT License
完全开源，商用友好。

---

# ⭐ 你觉得 NeuroForge 有潜力吗？

如果你喜欢这个项目，欢迎 **Star ⭐️** 支持一下！

---

# 🌐 English Version (Short)

## NeuroForge

*A plugin-based, structure-driven automation OS for AI video creation.*

### Features

* Markdown → structured scenes
* Full plugin runtime (TTS, D2, FFmpeg, etc.)
* Modular pipeline
* Extendable like a mini-Linux
* Supports animation, diagrams, narration & final video assembly

### Quick Start

```bash
git clone xxx
pip install -r requirements.txt
python3 neuroforge.py run examples/demo.md
```