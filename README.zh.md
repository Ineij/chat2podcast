# chat2podcast

**把群聊天记录，变成一期有深度的播客。**

> 🇺🇸 [View English Documentation →](README.md)

---

## 这是什么？

`chat2podcast` 是一个 **AI Agent Skill**，能把群聊天记录（微信或任何聊天工具）转化为专业播客脚本，并生成一个精美的单文件交互式 HTML 网站来展示这期节目。

**你可以在任何支持自定义 Skill 的 AI Agent 上使用它** —— 无论是 CatDesk、Claude，还是任何能读取 `SKILL.md` 指令文件的 Agent 框架。

---

## 如何在你的 Agent 上调用

### 方式一 — 放入 Skills 文件夹

如果你的 Agent 支持 skills 目录（如 `~/.catpaw/skills/` 或类似路径），把整个文件夹放进去：

```
your-agent-skills/
└── chat2podcast/
    ├── SKILL.md
    ├── references/
    ├── scripts/
    └── evals/
```

然后直接对 Agent 说：

> *"把这个聊天记录做成播客"*
> *"帮我从群聊生成播客脚本"*
> *"chat2podcast"*

### 方式二 — 把 SKILL.md 粘贴为系统提示词

复制 `SKILL.md` 的全部内容，粘贴到你的 Agent 的系统提示词（System Prompt）或自定义指令里。Agent 会自动按照工作流执行。

### 方式三 — 在 Agent 配置中引用

在你的 Agent 配置文件中，将 `SKILL.md` 作为指令文件路径引用。大多数 Agent 框架都支持从外部文件加载指令。

---

## 它能做什么

给它一段群聊天记录（截图文件夹、图片、或直接粘贴文字），它会：

1. **提取**所有消息，用视觉模型 OCR 识别，清洗噪音，按发言人整理
2. **深度挖掘**——忠实还原事实，按话题聚类，联网搜索更大的背景
3. **先和你交互，再动笔**——确认话题、风格、时长、结构、发言人姓名、以及这是长期节目还是单次尝试，然后才开始写
4. **用专业结构写脚本**——Ira Glass 三幕叙事法（Cold Open → 发展 → 反思时刻）
5. **输出**你选择的格式：交互式 HTML 网站、Word 文档、或 Markdown

---

## 核心特性

### 🔒 铁律：先交互，再动笔
在确认所有信息之前，Skill 不会写任何脚本内容。不会自作主张，不会跳过确认。

### 🧠 长期节目记忆
在做一档持续更新的播客？Skill 会把节目配置（名称、固定主持人、语气基调、开场白/片尾模板）写入 Agent 的持久化 Memory。下次使用时自动读取，无需重新设置。

### 👤 智能发言人命名
主动询问每位发言人的真实姓名。如果你不确定或不方便透露，它会从精选名库中随机分配英文名：
`Alex, Jamie, Morgan, Casey, Riley, Jordan, Taylor, Quinn, Avery, Blake, Drew, Sage, River, Skyler, Reese`

### 🎙️ 专业叙事结构
脚本遵循 **Ira Glass 方法论**——播客叙事的黄金标准，被 This American Life、Serial、NPR 广泛采用。每期节目都有 Cold Open 钩子、三幕结构、以及"为什么这件事重要"的反思时刻。

### 🎨 9 种视觉主题（HTML 输出）
`暗黑唱片` · `深夜电台` · `胶片复古` · `温暖纸张` · `极简终端` · `深空蓝图` · `玻璃态` · `手写杂志` · `报纸排版`

### 📸 自动滚动截图
内置 Python 脚本，自动滚动并截取微信聊天窗口，无需手动操作。

---

## 工作流程

```
第零步   读取 Memory，检查是否有已有节目配置
第一步   获取聊天记录（自动截图 / 文件夹 / 粘贴 / 上传图片）
第二步   深度挖掘：清洗、事实还原、话题聚类、联网搜索
第三步   与用户确认所有信息（话题、格式、时长、姓名、节目类型）
第四步   加载 Format 模板
第五步   撰写脚本（Ira Glass 三幕结构）
第六步   选择输出格式（HTML / Word / Markdown）
第七步   选择视觉风格（仅 HTML）
第八步   生成播客网站（仅 HTML）
第九步   生成 Word 文档（仅 Word）
第十步   交付文件到桌面
```

---

## 输出格式

| 格式 | 适合场景 |
|------|---------|
| 交互式 HTML | 分享、展示、存档——在任何浏览器里都好看 |
| Word (.docx) | 编辑、打印、发给他人审阅 |
| Markdown (.md) | Notion、Obsidian 或任何纯文本工作流 |

---

## 支持的播客形式

| 形式 | 参考节目 | 适合场景 |
|------|---------|---------|
| 圆桌讨论 | Radiolab | 有分歧、多视角的话题 |
| 深度访谈 | Fresh Air | 某人有大量干货分享 |
| 叙事纪录片 | This American Life | 有完整故事线的话题 |
| 独白/个人播客 | Hardcore History | 单人深度思考 |

---

## 文件结构

```
chat2podcast/
├── SKILL.md                      # 主 Skill 文件——完整工作流
├── references/
│   ├── podcast-formats.md        # Ira Glass 方法论 + 各 format 详细模板
│   ├── html-themes.md            # 9 种视觉主题定义
│   └── animation-patterns.md    # 交互动画代码片段
├── scripts/
│   ├── auto_screenshot.py        # 自动滚动截图脚本
│   └── build_podcast_html.py    # 将脚本 JSON 渲染为 HTML 网站
└── evals/
    └── evals.json                # Skill 评估测试用例
```

---

## 环境要求

- 任何支持读取 `SKILL.md` 指令文件的 AI Agent
- macOS（自动截图功能需要）
- Python 3（截图脚本和 HTML 生成脚本需要）
- Google Chrome（打开 HTML 输出文件需要）

---

## License

MIT
