# 🎬 **NeuroForge · AI 视频结构化生产框架（MVP v1.0）**

NeuroForge 是一个 **面向 AI 时代的视频生产框架**，
采用 **插件化 + 声明式 Pipeline + 结构化 IO 隔离** 的方式，
用最小的系统实现 **灵活、高扩展、可插拔的 AI 视频生成流程**。

它不是一个“工具集合”，
而是一个 **AI 驱动的视频编排引擎（Video Orchestrator）**。

---

# 🚀 Features（特性）

### 🧱 1. 极简核心（Minimal Core）

核心只负责四件事：

* 插件加载（PluginLoader）
* 顺序执行（Pipeline）
* 调度控制（Scheduler）
* 输入/输出管理（IOManager）

没有复杂状态、没有共享副作用、没有过度设计。

---

### 🔌 2. 完全插件化（Plugin as Unit）

每个插件都是一个独立模块，可以随时：

* 增加
* 移除
* 替换
* 单独运行

插件开发只需要实现一个函数：

```python
def run(context):
    ...
```

---

### 🎛 3. 声明式视频编排（YAML Pipeline）

通过 YAML 定义整个视频结构：

```yaml
scenes:
  - id: 1
    pipeline:
      - canvas
      - d2
      - tts
      - mix
      - compose
```

未来可轻松扩展成 **DAG + 并行执行**。

---

### 📁 4. 统一 IO 隔离

核心自动为每个场景与插件生成目录结构：

```
output/
  scene_1/
    canvas/
    d2/
    tts/
    mix/
    compose/
```

避免插件互相污染，保持结果可追踪与可复现。

---

### 🔮 5. 构建未来 AI 视频创作架构

基于第一性原理：视频 = 信息结构化表达
NeuroForge 是一个：

* 结构驱动（Structure-First）
* 插件可组合（Composable）
* 模型可切换（Model-Agnostic）
* 可扩展到 Agent / DAG / 并行

的视频生成系统。

---

# 📦 项目结构

```
NeuroForge/
│
├── neuroforge.py
│
├── core/
│   ├── loader.py
│   ├── pipeline.py
│   ├── scheduler.py
│   ├── io.py
│   └── logger.py
│
├── plugins/
│   ├── canvas/
│   │   └── plugin.py
│   ├── d2/
│   │   └── plugin.py
│   ├── tts/
│   │   └── plugin.py
│   ├── mix/
│   │   └── plugin.py
│   └── compose/
│       └── plugin.py
│
├── configs/
│   └── demo.yaml
│
└── output/
```

---

# 🧠 核心组件介绍

## 🔹 PluginLoader

自动扫描并加载 plugins/ 下的插件。

## 🔹 Pipeline

按 YAML 定义顺序执行插件
（未来可扩展成 DAG）

## 🔹 Scheduler

调度整个项目生命周期：
加载插件 → 执行 pipeline

## 🔹 IOManager

为每个插件生成标准输出目录，保证插件自治性。

## 🔹 Logger

统一日志输出。

---

# 🔌 开发你的第一个插件

在 `plugins/myplugin/plugin.py` 中编写：

```python
from core.io import IOManager
from core.logger import log
import os

def run(ctx):
    plugin_name = os.path.basename(os.path.dirname(__file__))
    out_dir = IOManager.get_plugin_dir(ctx["scene_dir"], plugin_name)

    log(f"[{plugin_name}] running...")

    output_file = os.path.join(out_dir, "result.txt")
    with open(output_file, "w") as f:
        f.write("Hello from my plugin!")

    return {
        plugin_name: {
            "output": output_file
        }
    }
```

插件无需注册，会自动被加载。

---

# 📜 示例配置文件（configs/demo.yaml）

```yaml
meta:
  title: Demo Project

scenes:
  - id: 1
    title: Scene One
    pipeline:
      - canvas
      - d2
      - tts
      - mix
      - compose
```

---

# ▶️ 运行项目

```bash
python neuroforge.py
```

NeuroForge 会基于 demo.yaml 执行整个视频生产流程。

---

# 🧩 插件生态（示例）

你可以将下面这些通用处理步骤实现为插件：

* AI 绘图（canvas）
* 结构图生成（d2）
* 文本转语音（tts）
* 背景音乐混合（mix）
* 视频合成（compose）
* Manim 动画（manim）
* AI 配音（voice）
* 文字排版（layout）
* 镜头切分（shot）
* 角色生成（avatar）
* RAG 信息生成（knowledge）

所有插件均可互相组合。

---

# 🌱 开发路线（Roadmap）

### ✅ v1.0 — MVP 版本（当前）

* 最小核心
* 顺序式 Pipeline
* 插件可插拔
* 统一 IO
* 独立插件执行

---

### 🚧 v1.5 — 插件参数化

* 每个插件可配置参数
* 插件执行缓存

---

### 🚀 v2.0 — DAG 调度（突破）

* DAG Pipeline
* 并行执行
* 插件依赖系统
* 自动重试
* 中间结果复用

---

### 🔮 v3.0 — AI 智能编排

* 大模型自动规划 Pipeline
* 智能镜头生成
* 智能节奏控制
* 多 Agent 协同

---

### 🪐 v4.0 — 完整视频 AI 操作系统

* 插件生态平台
* 分布式执行（K8s 风格）
* 高度自动化
* 结构化视频标准

---

# ❤️ 贡献

欢迎提交 Issue / PR，一起把 NeuroForge 打造成
**AI 视频时代最优雅、最模块化、最结构化的生成框架。**

---

# 📄 License

MIT License

---

如果你需要，我可以继续提供：

### ✔ 项目 Logo

### ✔ 项目架构图（D2）

### ✔ 插件开发文档（Plugin Dev Guide）

### ✔ Pipeline 语法规范

### ✔ 项目网站 README（更商业版）

