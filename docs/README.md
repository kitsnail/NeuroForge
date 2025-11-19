# 🧱 NeuroForge 文档与版本治理体系（Docs & Version Governance System）

> 📂 文件所在目录：`docs/` + `tools/`
> 📖 版本：v1.5
> 🎯 目标：让项目的开发文档与规范**结构化、自动化、可追踪**

---

## 🗂️ 一、目录结构（标准布局）

```sh
NeuroForge/
├── docs/
│   ├── specs/
│   │   ├── standards_v1.3.md     # 历史版本
│   │   ├── standards_v1.4.md
│   │   └── standards_v1.5.md     # 当前生效版本
│   │
│   ├── roadmap/
│   │   ├── roadmap_v1.5.md       # 当前开发阶段路线图
│   │   └── roadmap_vNext.md      # 未来规划草案
│   │
│   ├── changelog/
│   │   ├── CHANGELOG_v1.4.md
│   │   └── CHANGELOG_v1.5.md
│   │
│   ├── README_docs.md            # 文档系统总览
│   └── governance.md             # 文档与版本管理规则
│
└── tools/
    ├── archive_spec.sh           # 自动归档标准文档
    ├── make_next_spec.sh         # 创建下一个标准版本模板
    ├── bump_version.py           # 自动更新项目版本号
    └── init_docs.sh              # 初始化整个 docs 目录结构
```

---

## 📘 二、文档职责说明

| 模块                   | 说明            | 更新策略          |
| -------------------- | ------------- | ------------- |
| `docs/specs`         | 存放所有版本的标准规范指南 | 每个版本独立文件，冻结   |
| `docs/roadmap`       | 阶段开发计划书       | 可覆盖、随版本更新     |
| `docs/changelog`     | 版本更新日志        | 按版本存档，不覆盖     |
| `docs/governance.md` | 管理策略          | 可长期维护         |
| `tools`              | 辅助脚本目录        | 每个版本可扩展，保持兼容性 |

---

## 🧭 三、版本规范归档工具（tools/archive_spec.sh）

```bash
#!/bin/bash
# ============================================================
# NeuroForge Spec Archiver v1.0
# 自动复制上一个标准规范为新版本模板
# ============================================================

set -e
DOCS_DIR="docs/specs"

if [ -z "$1" ]; then
  echo "Usage: ./tools/archive_spec.sh <next_version>"
  echo "Example: ./tools/archive_spec.sh v1.6"
  exit 1
fi

NEXT="$1"
LATEST=$(ls $DOCS_DIR | grep standards_v | sort -V | tail -1)
SRC="$DOCS_DIR/$LATEST"
DST="$DOCS_DIR/standards_$NEXT.md"

if [ -f "$DST" ]; then
  echo "⚠️ $DST already exists."
  exit 1
fi

cp "$SRC" "$DST"
sed -i '' "s/v[0-9]\+\.[0-9]\+/$(echo $NEXT)/g" "$DST"

echo "✅ Created new spec version:"
echo "    $DST"
```

---

## 🧩 四、快速模板创建工具（tools/make_next_spec.sh）

该脚本在创建新版本时，同时自动插入统一头部。

```bash
#!/bin/bash
# ============================================================
# NeuroForge Next Spec Creator
# 创建下一个标准版本模板，带自动头部
# ============================================================

set -e
DOCS_DIR="docs/specs"
NEXT="$1"

if [ -z "$NEXT" ]; then
  echo "Usage: ./tools/make_next_spec.sh v1.6"
  exit 1
fi

TARGET="$DOCS_DIR/standards_$NEXT.md"

if [ -f "$TARGET" ]; then
  echo "⚠️ $TARGET already exists"
  exit 1
fi

cat <<EOF > "$TARGET"
# 🧭 NeuroForge $NEXT 统一标准规范指南

> 📄 自动生成模板（由 tools/make_next_spec.sh 创建）
> 📅 创建日期：$(date '+%Y-%m-%d')
> 📦 状态：草案（Draft）
> ✍️ 作者：wh

---

## 引言

此文档为 NeuroForge $NEXT 版本的标准规范初稿。
它基于上一版本的统一结构 (v1.5)，将在后续版本中逐步完善。

---
EOF

echo "✅ New spec template created → $TARGET"
```

---

## ⚙️ 五、版本号自动更新工具（tools/bump_version.py）

当发布新版本时，可自动同步版本号到项目的：

* `meta.version`
* `README.md`
* `neuroforge.py`
* `docs/specs/latest` 指向

```python
#!/usr/bin/env python3
import re, sys, os

if len(sys.argv) < 2:
    print("Usage: python tools/bump_version.py v1.6")
    sys.exit(1)

new_version = sys.argv[1]

targets = [
    "README.md",
    "neuroforge.py",
    "docs/specs/standards_v1.5.md"
]

for path in targets:
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"v\d+\.\d+", new_version, text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Updated version in {path}")

print(f"\n🎯 NeuroForge version bumped to {new_version}")
```

---

## 🧱 六、文档初始化脚本（tools/init_docs.sh）

适合在新仓库初始化或重大重构后使用：

```bash
#!/bin/bash
# ============================================================
# NeuroForge Documentation Initializer
# 初始化标准 docs + tools 目录结构
# ============================================================

echo "🧩 Initializing NeuroForge Documentation..."

mkdir -p docs/{specs,roadmap,changelog}
mkdir -p tools

cat <<EOF > docs/README_docs.md
# 🧠 NeuroForge Documentation Overview

This directory contains all documentation for the NeuroForge AI Video Engine.

Structure:
- **specs/** → Core standards and design rules
- **roadmap/** → Version planning and evolution
- **changelog/** → Version updates and logs

Version evolution follows: v1.3 → v1.4 → v1.5 → v1.6 ...
EOF

echo "✅ Documentation directories initialized."
```

---

## 🧭 七、版本管理策略（governance.md）

```markdown
# NeuroForge 文档与版本治理规则

## 1️⃣ 版本编号策略
- 采用语义化命名：`v<major>.<minor>`
- 示例：`v1.5` → 表示兼容 v1.x 核心的次级更新
- 所有标准文件命名规则：
```

standards_vX.Y.md
CHANGELOG_vX.Y.md
roadmap_vX.Y.md

````

## 2️⃣ 版本冻结原则
- 每个标准版本发布后立即冻结
- 不允许直接编辑旧版文档
- 修改需通过新版本规范迭代

## 3️⃣ 目录清晰度
- 所有文档集中在 `/docs` 目录下
- 所有脚本集中在 `/tools` 目录下

## 4️⃣ 版本演进节奏
- 每次小版本迭代仅限 **3 项以内新增内容**
- 每次大版本（x.0）需更新架构层级

## 5️⃣ 文件引用规范
主仓库 README.md 永远指向最新稳定版本：
```markdown
[📘 最新规范文档 → standards_v1.5.md](docs/specs/standards_v1.5.md)
````

---

## ✅ 八、使用流程（简版）

| 操作 | 命令 | 功能 |
|------|------|------|
| 初始化文档目录 | `bash tools/init_docs.sh` | 创建标准 docs 结构 |
| 复制旧规范 | `bash tools/archive_spec.sh v1.6` | 复制上一版本文档 |
| 创建新模板 | `bash tools/make_next_spec.sh v1.6` | 生成空白规范模板 |
| 自动升级版本 | `python3 tools/bump_version.py v1.6` | 同步版本号到项目 |
| 查看当前版本 | `grep version neuroforge.py` | 快速确认版本 |

---

## 🧩 九、下一步建议（v1.6+）

> 🚀 在文档体系稳定后，v1.6 将主要聚焦于：
> - 增强 **Scene Context Chain（上下文链路）**
> - 引入 **Plugin Metadata Registry**
> - 建立 **Docs 自动发布机制（GitHub Actions）**