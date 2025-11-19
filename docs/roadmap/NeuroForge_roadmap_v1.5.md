# 🧭 NeuroForge v1.5 精准迭代开发计划书

**代号**：*“Smart Orchestration”*
**版本周期**：2025.11 → 2025.12
**目标原则**：

> **保持 Minimal Core，不增加复杂依赖；
> 扩展智能层，让引擎具备“自主感知”的基础。**

---

## 🎯 一、版本核心目标

v1.5 的目标不是“功能堆叠”，而是 **让 NeuroForge 具备初步的智能自编排能力**，
即让系统可以根据上下文（例如 narration、场景结构）**自动优化视频生成逻辑**。

换句话说：

> 从「人驱动的管线」 → 「AI 协同的管线」
> 从「配置文件描述流程」 → 「AI 理解意图生成配置」

---

## 🧩 二、主要改进方向

| 模块                       | 分类 | 改进内容                                     | 状态         |
| ------------------------ | -- | ---------------------------------------- | ---------- |
| 🧠 `core/scheduler`      | 优化 | 支持“任务回溯模式”，执行失败后可自动恢复现场                  | 🧩 计划中     |
| 🧩 `core/context` *(新增)* | 新增 | 全局上下文管理器，存储当前会话信息（meta、timeline、scene结果） | 🧠 新模块     |
| 🎞️ `core/timeline`      | 增强 | 支持外部 duration 提供器（如 AI 预测或前置估算）          | 🧩 可选扩展    |
| ⚙️ `plugins/transition`  | 新增 | 实现最简单的淡入淡出特效，输出短 transition clip         | 🧩 轻量实现    |
| 🧩 `plugins/analyze`     | 新增 | 负责自动分析 narration（节奏/停顿/情感），供 pipeline 参考 | 🧠 AI 模块雏形 |
| 🧱 插件系统                  | 稳定 | 保持接口一致性（v1.4 格式不变），允许异步执行（后续版本激活）        | ✅ 保持       |

---

## 🧠 三、架构调整图（v1.5 结构草图）

```
NeuroForge/
 ├── core/
 │   ├── scheduler.py     ← 调度控制（新增恢复机制）
 │   ├── timeline.py      ← 自动时长预测支持
 │   ├── context.py       ← 🧠 新增：统一上下文管理器
 │   ├── scene_runner.py
 │   ├── io.py
 │   ├── loader.py
 │   └── logger.py
 ├── plugins/
 │   ├── canvas/
 │   ├── d2/
 │   ├── tts/
 │   ├── mix/
 │   ├── compose/
 │   ├── transition/      ← 🎞️ 新增：淡入淡出
 │   └── analyze/         ← 🧠 新增：narration 语义分析
 ├── configs/
 │   └── demo_v1_5.yaml
 ├── output/
 ├── README.md
 └── CHANGELOG_v1.5.md
```

---

## ⚙️ 四、功能分阶段实现

### 🔹 v1.5.0 — “Context & Recovery”

🕐 **预计开发周期：5天**

* 新增 `core/context.py`

  * 管理全局上下文对象：meta、scenes、timeline_state、outputs。
  * 允许每个插件更新全局状态（非共享内存，而是注册树状结构）。
* Scheduler 新增：

  * **恢复机制**：若中途中断（崩溃/异常），下次启动可自动跳过已完成场景。
  * 配置项 `resume: true` 支持自动检测。

🧱 **核心输出**：

* 新增 `context.json` 自动记录在 `output/project_state/`；
* Timeline 可读取上次进度自动续跑。

---

### 🔹 v1.5.1 — “Transition & Analyze (Preview)”

🕐 **预计开发周期：7天**

* 新增插件：`plugins/transition`

  * 提供淡入、淡出两种过渡效果；
  * 输入上个视频和下个视频路径；
  * 输出带 transition 的片段；
  * 时长默认 0.5~1s；
  * 全局自动注入 pipeline 尾部（可配置关闭）。

* 新增插件：`plugins/analyze`

  * 解析 narration 文本；
  * 统计句子数、停顿点、情绪关键词；
  * 为后续情感 TTS 或镜头节奏控制提供元数据；
  * 输出 JSON 格式分析报告。

🧩 **核心目标**：AI 感知（Analyze）与 Timeline 调和（Transition）初步融合。

---

### 🔹 v1.5.2 — “Auto Pipeline Suggestion (Experimental)”

🕐 **预计开发周期：10天**

* 引入轻量 LLM 调度接口（可选调用）；
* 根据 narration 或 meta 自动建议 pipeline；
* 例如：

  ```
  narration: "The system evolves into harmony..."
  → pipeline: [canvas, d2, tts, mix, compose, transition]
  ```
* 自动生成临时 YAML 结构并执行。

> ⚙️ 这是 “AI 自编排” 的雏形，但不会引入复杂模型，只做 Prompt 级别智能。

---

## 📈 五、整体迭代原则

| 指标     | 原则                            |
| ------ | ----------------------------- |
| 核心保持最小 | Core 层不新增业务逻辑，只引入 Context 管理器 |
| 插件可选加载 | 所有新增插件都可独立关闭                  |
| 接口完全兼容 | v1.4 所有配置、返回结构继续可用            |
| 版本小步迭代 | 每个子版本控制在 500 行以内修改            |
| 可扩展性验证 | 为 v1.6 的 “智能镜头控制” 打基础         |

---

## 🧩 六、预期交付成果

| 模块            | 成果               | 指标     |
| ------------- | ---------------- | ------ |
| Core Context  | 全局状态记录/恢复        | ✅ 功能完成 |
| Transition 插件 | 可用淡入淡出视频段        | ✅ 可演示  |
| Analyze 插件    | narration 元信息提取  | ✅ 可调试  |
| 自动恢复机制        | 支持断点续跑           | ✅ 可用   |
| 兼容性测试         | v1.3/v1.4 配置均可运行 | ✅ 通过   |

---

## 🧭 七、版本号策略

| 版本     | 代号                   | 说明        |
| ------ | -------------------- | --------- |
| v1.5.0 | Context Launch       | 上下文核心上线   |
| v1.5.1 | Transition + Analyze | 插件扩展      |
| v1.5.2 | Smart Pipeline       | 智能编排实验功能  |
| v1.6.x | Vision Harmony       | 进入多模态镜头阶段 |

---

## 🧠 八、开发哲学总结

> **v1.4：人告诉系统“做什么”**
> **v1.5：系统开始理解“为什么这么做”**

NeuroForge 仍然是一个「AI 视频编排引擎」，而非全能生成器。
我们不追求巨大的功能堆叠，而是追求：

* 核心稳定；
* 插件强大；
* 时序和谐；
* 架构优雅。

---

## ✅ 九、下阶段任务分配建议（可选）

| 模块                   | 负责人               | 预计耗时  |
| -------------------- | ----------------- | ----- |
| `core/context.py`    | Core Lead (wh)    | 1~2 天 |
| `plugins/transition` | Media Dev         | 2~3 天 |
| `plugins/analyze`    | NLP Dev           | 3~5 天 |
| 文档 & 测试              | System Maintainer | 2 天   |
| Demo YAML + CI 测试    | 全体                | 1 天   |

---

## 🏁 十、总结

v1.5 是 NeuroForge 从 **“结构稳定”** 向 **“智能协同”** 迈出的第一步。
它不会推翻任何已有设计，而是让系统拥有了理解与记忆能力。
这一步虽小，却是通往真正 “AI 视频导演” 的开始。

---

是否希望我帮你继续生成
📄《CHANGELOG_v1.5.md（预发布版模板）》
以及
🧠《core/context.py》的设计草案（v1.5.0）？
这两个文件将是下一步实际开发的核心。
