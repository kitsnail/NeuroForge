# 🧠 NeuroForge v1.4.0 — “Minimal Core Stable”

**发布日期**：2025-11-19
**作者**：wh
**代号**：*Minimal Core, Strong Plugins, Harmony Timeline*

---

## 🧩 概述

NeuroForge v1.4.0 是一次具有里程碑意义的版本更新。
该版本正式确立了 **“最小核心 + 插件驱动 + 自动时间线”** 的系统架构哲学，标志着项目从实验性阶段进入到稳定可扩展阶段。

核心思想保持不变：

> **Core 只负责编排与协调，所有智能与生成逻辑由插件负责。**

这一版本优化了系统结构、插件接口一致性、上下文数据标准化，并全面重构了执行调度流程，使整个 AI 视频生成管线更加模块化、可控、可扩展。

---

## 🧱 核心更新摘要

### 1️⃣ Core 架构

| 模块                     | 状态     | 更新说明                                                    |
| ---------------------- | ------ | ------------------------------------------------------- |
| `core/scheduler.py`    | ✅ 稳定   | 新版启动日志标识 `Minimal Core Mode`；仅负责启动与调度。                  |
| `core/timeline.py`     | ✅ 精简化  | 自动推断场景时长、维护时间游标、统一日志格式。                                 |
| `core/scene_runner.py` | ✅ 重构   | 移除冗余逻辑；支持上下文链式传递；自动收集 TTS 或混音结果时长。                      |
| `core/io.py`           | ✅ 统一   | 提供通用 I/O 管理接口：`prepare_scene_dir()`、`get_plugin_dir()`。 |
| `core/loader.py`       | ✅ 稳定   | 动态加载插件模块，确保每次执行自动扫描 `plugins/`。                         |
| `core/logger.py`       | ✅ 保持简洁 | 统一日志输出样式 `[NeuroForge YYYY-MM-DD HH:MM:SS]`。            |

> 🧩 **设计哲学：**
>
> * Core 只负责任务编排与上下文传递；
> * 无插件耦合；
> * 无全局状态；
> * 代码结构清晰，单文件职责明确。

---

### 2️⃣ 插件系统（Plugins）

统一的插件接口标准在本版本中正式确立。

#### 🧩 插件返回规范

所有插件必须返回：

```python
{
  "<plugin_name>": {
    "<main_output>": "<path_or_value>",
    "meta": {"duration": float, ...}
  }
}
```

#### 插件更新详情：

| 插件             | 状态     | 说明                                                 |
| -------------- | ------ | -------------------------------------------------- |
| 🖼️ **canvas** | ✅ 完全重写 | 标准化输出键名为 `image_out`；生成统一画布。                       |
| 🧩 **d2**      | ✅ 优化   | 输出键名统一为 `diagram_out`；支持 D2 结构图自动渲染。               |
| 🗣️ **tts**    | ✅ 重构   | 使用 Edge-TTS 生成语音与字幕；输出 `audio_out`、`subtitle_out`。 |
| 🎧 **mix**     | ✅ 稳定   | 自动检测音频长度；统一输出 `audio_out`；支持无 BGM 模式。              |
| 🎬 **compose** | ✅ 重写   | 标准化输入输出；自动叠加画面 + 音频 + 字幕；输出 `video_out`。           |

> 所有插件均遵循统一数据上下文（Context）接口规范，可任意组合执行。

---

### 3️⃣ 场景系统（Scenes）

#### ✅ 新版场景配置结构

```yaml
scenes:
  - id: 1
    title: "Introduction"
    narration: "Welcome to NeuroForge."
    pipeline: [canvas, d2, tts, mix, compose]
```

#### ✅ 命名规范确立

* `title`：场景标题
* `narration`：叙述文本（语音生成来源）
* `pipeline`：插件执行顺序

> 💡 统一弃用旧字段 `text`、`tts` 等冗余命名。

---

### 4️⃣ 时间线系统（Timeline）

#### ✨ 自动时间线模式（Auto Timeline）

无需手动定义时间点：

* 每个场景的时长自动由 TTS 或混音结果推断；
* `timeline` 自动推进；
* 自动生成 Summary 日志：

  ```
  🧭 Auto-Timeline Summary:
    • Scene 1: 0.00s → 7.10s
    • Scene 2: 7.10s → 14.52s
  ```

---

## ⚙️ 内部改进

* 🧠 上下文传递 (`ctx`) 统一标准化，避免层级混乱；
* 🧩 插件执行异常安全隔离，不影响主流程；
* 🧰 统一路径规范：`output/scene_{id}/{plugin}/...`；
* 💬 日志输出更简洁一致；
* 🎛️ 支持场景复用与多阶段执行；
* 🚦 保留向后兼容性：旧版配置仍可运行。

---

## 🧠 设计哲学演化

| 核心理念                      | v1.3 → v1.4 变化        |
| ------------------------- | --------------------- |
| **Core 负责 orchestration** | 完全剥离业务逻辑，仅负责任务控制与上下文。 |
| **Plugins 负责 creation**   | 插件自由组合形成完整视频管线。       |
| **Timeline 负责 harmony**   | 自动同步音画与场景时长，无需人工控制。   |

---

## 🧭 路线图（v1.4.x → v1.5+）

| 版本         | 类型      | 核心目标                                        |
| ---------- | ------- | ------------------------------------------- |
| **v1.4.1** | 🧩 稳定维护 | 增加日志级别控制（INFO/WARN/ERROR）。                  |
| **v1.4.2** | 🎞️ 新插件 | `plugins/transition`：淡入淡出场景衔接（保持 core 无变化）。 |
| **v1.4.3** | 🧠 智能增强 | AI Scene Generator（文本→配置自动生成）。              |
| **v1.5.0** | 🚀 架构扩展 | 多模态 AI 接入：图像生成 / Prompt 控制 / 动态 Timeline。   |

---

## 🧩 文件结构（v1.4）

```
NeuroForge/
 ├── core/
 │   ├── scheduler.py
 │   ├── timeline.py
 │   ├── scene_runner.py
 │   ├── loader.py
 │   ├── io.py
 │   └── logger.py
 ├── plugins/
 │   ├── canvas/
 │   ├── d2/
 │   ├── tts/
 │   ├── mix/
 │   └── compose/
 ├── configs/
 │   └── demo_v1_4.yaml
 ├── output/
 ├── README.md
 └── CHANGELOG_v1.4.md
```

---

## 🧩 升级指引

```bash
git pull origin main
pip install -r requirements.txt
python3 neuroforge.py configs/demo_v1_4.yaml
```

---

## ✨ 开发者须知

* 所有插件必须返回标准化字典结构；
* 禁止在 core 层使用全局变量；
* 插件必须具备容错性；
* Scene ID 必须唯一；
* 输出目录结构需保持一致。

---

## ❤️ 致谢

> 感谢所有参与 NeuroForge 架构演进、测试与反馈的开发者。
> NeuroForge 仍在构建中 —— 一个面向未来的 AI 视频编排引擎。

---

## 🏁 版本信息

| 项目                  | 版本     | 状态      |
| ------------------- | ------ | ------- |
| **NeuroForge Core** | v1.4.0 | ✅ 稳定    |
| **Plugin System**   | v1.4.0 | ✅ 稳定    |
| **Timeline Engine** | v1.4.0 | ✅ 自动化完成 |
| **Compatibility**   | v1.3+  | ✅ 向后兼容  |

---

> 🧩 *“Minimal Core. Strong Plugins. Harmony Timeline.”*
> — NeuroForge Project, 2025
