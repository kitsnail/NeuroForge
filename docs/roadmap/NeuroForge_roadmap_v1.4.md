非常好 👍。以下是为 **NeuroForge v1.4** 精心设计的 ——

# 🧭 《NeuroForge v1.4 精简版开发计划书》

---

## 🚀 一、版本定位

**版本代号**：`NeuroForge v1.4 — Minimal Core, Clear Boundaries`
**发布日期**：预计 2026 Q1
**核心目标**：

> ✳️ 在保持功能完整的前提下，重构核心架构，使其更加**轻量、纯净、可扩展**，
> 让 NeuroForge 真正成为一个“AI 驱动的视频编排引擎内核”，而非一个“多功能应用容器”。

---

## 🧩 二、核心哲学（v1.4 指导原则）

| 原则                        | 说明                                       |
| ------------------------- | ---------------------------------------- |
| **Minimal Core**          | Core 只负责 orchestrate（编排），不负责 create（生成）。 |
| **Plugin First**          | 所有可变逻辑、AI 生成、合成、特效、转场均通过插件体系实现。          |
| **Unified Context**       | 所有核心模块共享统一上下文结构 `ctx`，使插件间天然解耦。          |
| **Timeline Driven**       | 一切执行均由时间线驱动，而非顺序逻辑硬编码。                   |
| **Predictable Evolution** | 每个版本小步快跑、渐进演化，不引入复杂概念。                   |

---

## 🧱 三、版本目标概述

| 目标模块                | 关键变更     | 意图                    |
| ------------------- | -------- | --------------------- |
| `core.scene_runner` | 精简为纯执行单元 | 仅负责插件执行，不含业务逻辑        |
| `core.timeline`     | 转为时间调度器  | 管理场景顺序与时长汇总           |
| `core`              | 不新增模块    | 保持极简与稳定               |
| 插件体系                | 保持兼容     | 支持 v1.3 规范的返回结构       |
| 配置结构                | 不变       | 保持 YAML 兼容性，向下兼容 v1.3 |
| Transition 模块       | 延期       | 未来以插件形式实现（非 core 模块）  |

---

## ⚙️ 四、系统架构（v1.4 精简版）

```
NeuroForge/
├── core/
│   ├── scheduler.py      ← 项目入口调度器
│   ├── timeline.py       ← 时间驱动执行控制器（仅调度）
│   ├── scene_runner.py   ← 场景执行引擎（仅执行插件）
│   ├── io.py             ← IO 路径管理
│   ├── loader.py         ← 插件加载器
│   └── logger.py         ← 全局日志
│
├── plugins/
│   ├── canvas/
│   ├── tts/
│   ├── mix/
│   ├── compose/
│   └── ...               ← 后续扩展（如 transition、vision 等）
│
├── configs/
│   └── demo_v1_4.yaml    ← v1.4 示例配置（兼容 v1.3）
│
└── output/
    └── scene_x/          ← 各场景独立输出目录
```

---

## 🧠 五、核心模块设计

### 1️⃣ `core.scene_runner`

**职责**：

> 仅负责“顺序执行插件”，维护上下文状态，不关心时间线或时长。

**主要变化：**

* 移除时长检测逻辑（由 timeline 统一汇总）
* 简化执行流程
* 保持 ctx 的生命周期一致性

**接口定义：**

```python
class SceneRunner:
    def __init__(self, scene_id, meta, scene_data, output_dir):
        ...

    def execute(self) -> dict:
        """执行场景并返回 ctx"""
```

---

### 2️⃣ `core.timeline`

**职责**：

> Timeline 作为“导演”，SceneRunner 是“演员”。
> Timeline 决定何时、以何顺序执行场景，并收集时长。

**主要变化：**

* 从 `ctx` 中自动提取时长信息（由 mix/tts/compose 插件提供）
* 汇总 timeline 数据结构
* 为未来 transition 插件预留钩子（不内置实现）

**接口定义：**

```python
class Timeline:
    def __init__(self, meta, scenes, output_dir="output"):
        ...

    def run(self) -> list:
        """顺序执行所有场景，返回 timeline 数据结构"""
```

**执行结果示例：**

```yaml
timeline:
  - scene_id: 1
    title: "Intro"
    start: 0.00
    duration: 6.80
    end: 6.80
  - scene_id: 2
    title: "AI Narrative"
    start: 6.80
    duration: 7.25
    end: 14.05
```

---

### 3️⃣ `core.scheduler`

**职责**：

> 项目入口，加载配置，实例化 Timeline 并启动执行。

**输出示例日志：**

```
🚀 NeuroForge v1.4 Scheduler Started
🎞️ Executing Scene 1: Intro
⏳ Duration: 6.80s
🎞️ Executing Scene 2: AI Narrative
⏳ Duration: 7.25s
✅ All scenes executed successfully.
```

---

## 🧩 六、向后兼容性

| 兼容对象       | 状态      | 说明                            |
| ---------- | ------- | ----------------------------- |
| v1.3 配置结构  | ✅ 完全兼容  | 不需要修改配置文件                     |
| v1.3 插件接口  | ✅ 完全兼容  | 支持相同的 `ctx` 与返回格式             |
| v1.3 输出路径  | ✅ 完全兼容  | 输出目录结构一致                      |
| v1.2 及更早版本 | ⚠️ 部分兼容 | 需统一字段命名（scene_id、narration 等） |

---

## 🧰 七、测试与验证计划

| 测试类型    | 内容             | 预期结果                 |
| ------- | -------------- | -------------------- |
| 单场景测试   | 单一 pipeline 执行 | 各插件输出正确              |
| 多场景串联测试 | Timeline 调度多场景 | 时间线顺序正确，时长叠加正确       |
| 插件兼容性测试 | v1.3 插件执行      | 返回结构可正常解析            |
| 异常处理    | 插件缺失 / 错误中断    | Scheduler 可捕获错误并安全退出 |

---

## 🌱 八、延后功能（延期到 v1.5+）

| 功能                            | 原计划版本 | 调整后             |
| ----------------------------- | ----- | --------------- |
| Transition 模块（转场动画）           | v1.4  | **v1.5**，插件形式实现 |
| AI Scene Generator（AI 场景自动生成） | v1.4  | v1.6            |
| Video Merger（全局合成器）           | v1.4  | v1.5            |
| Metrics & Profiling（性能监控）     | v1.4  | v1.6            |
| Web 控制台（UI 前端）                | v1.5+ | v1.7+           |

---

## 🧭 九、里程碑与任务拆解

| 阶段       | 任务                            | 负责人    | 状态 |
| -------- | ----------------------------- | ------ | -- |
| 1️⃣ 核心解耦 | 拆分 SceneRunner / Timeline 职责  | ✅ 完成草案 |    |
| 2️⃣ 测试重构 | 更新单元测试、验证 ctx 一致性             | ⏳ 进行中  |    |
| 3️⃣ 插件验证 | 确认 canvas/tts/mix/compose 全兼容 | ⏳ 进行中  |    |
| 4️⃣ 文档更新 | v1.4 开发指南、API 参考              | ⏳ 待编写  |    |
| 5️⃣ 稳定发布 | 生成 v1.4.0 release 版本          | ⏳ 计划中  |    |

---

## 🔮 十、未来演进方向（2026+）

| 版本   | 目标                 | 关键词                        |
| ---- | ------------------ | -------------------------- |
| v1.5 | Timeline Plugins   | `transition`、`video merge` |
| v1.6 | AI Scene Authoring | 自动生成场景、AI 脚本引擎             |
| v1.7 | Realtime Mode      | 实时生成 / 流式播放                |
| v1.8 | Web Studio         | 基于 Web 的神经视频创作空间           |
| v2.0 | AI-Driven Director | 完整的 AI 视频导演系统架构            |

---

## 💡 总结：v1.4 的核心价值

> v1.4 不新增复杂特性，不追求炫技，而是**一次向内收敛的重构**。
> 它让 NeuroForge 从一个“AI 视频生成系统”，
> 真正过渡为一个 **AI 视频创作内核（Neural Video Engine Core）**。

**一句话总结：**

> 🧠 v1.3 让它工作，
> 🧩 v1.4 让它优雅。

---

是否希望我帮你基于这个计划书，生成对应的项目结构与代码模板（v1.4 精简实现版，包括新的 `core/timeline.py` 与 `core/scene_runner.py`）？
这样可以直接成为你下一版本开发分支的基础。
