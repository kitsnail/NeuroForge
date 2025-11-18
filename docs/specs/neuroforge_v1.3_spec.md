# 🧭 NeuroForge v1.3 统一标准规范指南

**AI 驱动视频编排引擎的结构与命名哲学**

---

## 0. 引言

**NeuroForge** 致力于构建未来的 **AI 视频创作引擎**。
其核心目标是成为一个能够自动编排、组合、合成多模态内容的 **视频时间线系统（Video Timeline Engine）**。

在 v1.3 版本中，我们确立了整个系统的统一规范：

* 所有命名与设计均围绕 **“时间线（Timeline）” 与 “场景（Scene）”** 展开。
* 所有输入、输出与插件上下文必须具有一致的语义边界。
* 所有模块仅关注 “**AI 驱动的视频生成与合成**” 的主干逻辑。

---

## 1. 设计哲学

> 💡 **“AI 生成内容，系统负责编排。”**

NeuroForge 的核心思想是将复杂的 AI 生成任务抽象为
一个可以被时间轴调度的视频片段管线系统（Scene Pipeline）。

因此：

* 所有结构命名都以 **时间线与场景为中心**；
* 所有功能模块都可独立运行、组合与扩展；
* 系统始终保持 **结构性简单 + 语义一致性**；
* 不追求“功能大而全”，而追求“核心边界明确”。

---

## 2. 顶层结构：项目配置（Project Config）

NeuroForge 的项目配置文件采用 YAML 格式，定义视频生成工程的元信息、时间线、场景与插件编排。

### 基本结构

```yaml
meta:
  version: 1.3
  project: "NeuroForge Auto Timeline"
  author: "wh"
  bgm: "assets/bgm/soft_thinking.mp3"
  resolution: "1280x720"
  fps: 30
  mode: "auto"        # timeline mode

timeline:
  mode: auto          # 自动时间线模式

scenes:
  - id: 1
    title: "Scene One"
    narration: "Welcome to NeuroForge auto-timeline mode."
    pipeline: [canvas, d2, tts, mix, compose]

  - id: 2
    title: "Scene Two"
    narration: "This is the second scene, seamlessly connected."
    pipeline: [canvas, tts, mix, compose]
```

---

## 3. 命名与结构规范

### 3.1 核心命名边界

| 概念层级 | 名称         | 语义边界   | 说明         |
| ---- | ---------- | ------ | ---------- |
| 顶层配置 | `meta`     | 工程级元信息 | 视频生成全局参数   |
| 时间线层 | `timeline` | 时间序列控制 | 决定场景调度模式   |
| 场景层  | `scenes`   | 视频片段集合 | 每个片段独立生成   |
| 片段单元 | `scene`    | 单个视频片段 | 拥有叙述、素材、插件 |
| 插件层  | `plugins`  | 功能节点   | 组成场景执行流水线  |

---

### 3.2 Scene 场景结构规范

每个场景（Scene）代表时间线上的一个视频片段。

| 字段名         | 类型   | 说明            | 是否必填 |
| ----------- | ---- | ------------- | ---- |
| `id`        | int  | 场景编号          | ✅    |
| `title`     | str  | 场景标题          | ✅    |
| `narration` | str  | 叙述文本（TTS 输入源） | ✅    |
| `pipeline`  | list | 插件执行顺序        | ✅    |
| `assets`    | dict | 场景专属素材，如图片或音频 | ❌    |
| `meta`      | dict | 场景附加参数，如风格、语音 | ❌    |

> ✅ 采用 `narration` 作为叙述文本字段，而非 `text`。
> 理由：语义明确（用于语音叙述），贴合时间线逻辑，更便于扩展语音驱动特性。

---

### 3.3 插件执行上下文（Context）

所有插件共享相同的输入上下文结构：

```python
ctx = {
  "meta": {...},         # 全局配置信息（来自 meta）
  "scene": {...},        # 当前场景定义
  "scene_id": 1,
  "scene_dir": "output/scene_1",
  "timeline": {...},     # 当前时间线状态（可选）
}
```

> 所有上下文语义与时间线直接对应，不出现 `task`、`job` 等抽象名。

---

## 4. 插件设计规范（Plugin System）

### 4.1 插件职责

每个插件是一个“功能单元”，
执行视频生成过程中的一步（如生成画布、语音、合成等）。

### 4.2 插件命名规范

| 插件名       | 主要作用         | 输出内容                                    |
| --------- | ------------ | --------------------------------------- |
| `canvas`  | 生成基础画面底图     | `file`                                  |
| `d2`      | 渲染结构图        | `file`                                  |
| `tts`     | 文本转语音 + 字幕生成 | `audio_out`, `subtitle_out`, `duration` |
| `mix`     | 背景音乐与语音混音    | `audio_out`, `duration`                 |
| `compose` | 合成最终视频       | `video_out`, `duration`                 |

---

### 4.3 插件统一输入输出格式

#### 输入：

* 标准化上下文 `ctx`（见上节）。

#### 输出：

所有插件必须返回标准结构：

```python
return {
  "<plugin_name>": {
    "status": "ok",             # "ok" | "skip" | "error"
    "file": "xxx.png",          # 通用文件输出
    "audio_out": "xxx.wav",     # 音频输出（tts/mix）
    "video_out": "xxx.mp4",     # 视频输出（compose）
    "subtitle_out": "xxx.srt",  # 字幕输出（tts）
    "duration": 4.63,           # 输出时长（秒）
    "meta": {...}               # 插件内部状态数据
  }
}
```

#### 状态说明：

| 状态      | 含义                 |
| ------- | ------------------ |
| `ok`    | 成功执行               |
| `skip`  | 插件被跳过（输入缺失或场景条件不符） |
| `error` | 执行失败               |

---

### 4.4 插件目录结构规范

```
plugins/
 ├── canvas/
 │   └── plugin.py
 ├── d2/
 │   └── plugin.py
 ├── tts/
 │   └── plugin.py
 ├── mix/
 │   └── plugin.py
 └── compose/
     └── plugin.py
```

---

## 5. 输出命名标准化

| 输出类型 | 字段名            | 示例             | 说明         |
| ---- | -------------- | -------------- | ---------- |
| 图像输出 | `file`         | `canvas.png`   | 通用图像输出     |
| 音频输出 | `audio_out`    | `tts.wav`      | 音频文件路径     |
| 视频输出 | `video_out`    | `final.mp4`    | 视频输出路径     |
| 字幕输出 | `subtitle_out` | `subtitle.srt` | 字幕文件       |
| 时长   | `duration`     | `4.63`         | 音频或视频时长（秒） |

---

## 6. 系统执行层命名标准

| 模块                | 角色   | 命名规范           | 职责          |
| ----------------- | ---- | -------------- | ----------- |
| `scheduler.py`    | 调度层  | `Scheduler`    | 统一启动器       |
| `timeline.py`     | 编排层  | `Timeline`     | 统一调度所有场景    |
| `scene_runner.py` | 执行层  | `SceneRunner`  | 负责场景插件流水线执行 |
| `loader.py`       | 加载层  | `PluginLoader` | 动态加载所有插件    |
| `io.py`           | IO 层 | `IOManager`    | 路径与输出管理     |
| `logger.py`       | 日志层  | `log`          | 统一输出接口      |

---

## 7. 一致性验证表

| 范畴     | 命名边界                                        | 是否通过 |
| ------ | ------------------------------------------- | ---- |
| 时间线语义  | timeline / scene / narration                | ✅    |
| 输出语义   | file / audio_out / video_out / subtitle_out | ✅    |
| 上下文一致性 | meta / scene / scene_dir / timeline         | ✅    |
| 插件语义   | canvas / d2 / tts / mix / compose           | ✅    |
| 可扩展性   | AI 插件可无缝注册                                  | ✅    |
| 歧义性    | 所有字段语义唯一                                    | ✅    |

---

## 8. 未来扩展方向

| 模块           | 功能            | 状态     |
| ------------ | ------------- | ------ |
| `caption`    | 自动字幕/镜头描述     | 🚧 规划中 |
| `transition` | 场景过渡效果        | 🚧 规划中 |
| `ai-edit`    | 视频智能剪辑与布局     | 🚧 规划中 |
| `render`     | GPU/Cloud 渲染层 | 🚧 规划中 |

> 所有未来插件必须遵守本规范的输入输出标准与命名语义。

---

## 9. 版本声明

* **版本号**：NeuroForge v1.3
* **日期**：2025-11
* **作者**：wh
* **状态**：✅ 稳定规范版（建议所有后续开发遵循）

---

## 🔖 附录：架构概览图

```
NeuroForge Project
│
├── meta (project-level info)
│
├── timeline (temporal orchestration)
│     └── scenes[*]
│          ├── id / title
│          ├── narration
│          ├── pipeline[]
│          └── assets / meta
│
└── plugins
      ├── canvas   → file
      ├── d2       → file
      ├── tts      → audio_out + subtitle_out + duration
      ├── mix      → audio_out + duration
      └── compose  → video_out + duration
```

---

✅ **总结**：

> NeuroForge v1.3 是第一个具备完整“命名与结构统一性”的版本。
> 它确立了系统的语义边界、扩展规则与视频编排哲学。
> 所有后续版本（v2.x、v3.x）都将在此基础上演化。