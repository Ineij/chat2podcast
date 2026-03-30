# chat2podcast

**Turn your WeChat group chats into professional podcast scripts — with a beautiful interactive website to show for it.**

**把微信群聊天记录，变成一期有深度的播客。**

---

## English

### What is this?

`chat2podcast` is a [CatDesk](https://catdesk.ai) AI skill that transforms WeChat group chat logs into professional podcast scripts, then generates a stunning single-file interactive HTML website to present the episode.

It's built on a simple belief: **the best conversations are already happening in your group chats — they just need a better stage.**

### What it does

Given a WeChat group chat (as screenshots, a folder of images, or pasted text), the skill will:

1. **Extract** all messages using vision OCR, clean noise, and organize by speaker
2. **Mine deeply** — reconstruct facts faithfully, cluster topics, and search the web for broader context
3. **Interact with you** before writing anything — confirm topics, style, length, structure, speaker names, and whether this is an ongoing show or a one-off
4. **Write a professional script** using the Ira Glass three-act narrative method (Cold Open → Confrontation → Moment of Reflection)
5. **Output** in your chosen format: interactive HTML website, Word document, or Markdown

### Key features

**Deep interaction before writing (Iron Rule)**
The skill never writes a single word of script until it has confirmed everything with you: which topics to focus on, what format and length you want, what to call each speaker, and whether this is a recurring show. No surprises.

**Ongoing show memory**
If you're building a regular podcast, the skill saves your show configuration (name, fixed hosts, tone, intro/outro templates) to persistent memory. Next time you use it, it loads automatically — no re-setup needed.

**Speaker name handling**
The skill asks for each speaker's real name. If you're not sure or prefer privacy, it assigns unique English names from a curated pool: Alex, Jamie, Morgan, Casey, Riley, Jordan, Taylor, Quinn, Avery, Blake, Drew, Sage, River, Skyler, Reese.

**Professional narrative structure**
Scripts follow the Ira Glass method — the gold standard for podcast storytelling. Every episode has a Cold Open hook, a three-act arc, and a Moment of Reflection that answers "why does this matter?"

**9 visual themes for the HTML output**
Dark Vinyl · Late Night Radio · Film Grain · Warm Paper · Minimal Terminal · Deep Space Blueprint · Glassmorphism · Handwritten Magazine · Newspaper Layout

**Auto-screenshot capture**
A bundled Python script automatically scrolls and screenshots your WeChat window, so you don't have to manually capture anything.

### How to use

This skill runs inside [CatDesk](https://catdesk.ai). Install it by placing the `SKILL.md` file in your CatDesk skills directory:

```
~/.catpaw/skills/chat2podcast/SKILL.md
```

Then trigger it by saying things like:
- "Turn this chat into a podcast"
- "chat2podcast"
- "Make a podcast from my group chat"
- "Generate a podcast script from these screenshots"

### Workflow overview

```
Step 0  →  Check memory for existing show config
Step 1  →  Collect chat log (auto-screenshot / folder / paste / upload)
Step 2  →  Deep mining: clean, reconstruct facts, cluster topics, web search
Step 3  →  Confirm everything with user (topics, format, length, names, show type)
Step 4  →  Load format template
Step 5  →  Write the script (Ira Glass three-act structure)
Step 6  →  Choose output format (HTML / Word / Markdown)
Step 7  →  Choose visual theme (HTML only)
Step 8  →  Generate the podcast website (HTML only)
Step 9  →  Generate Word document (Word only)
Step 10 →  Deliver files to desktop
```

### Output formats

| Format | Best for |
|--------|----------|
| Interactive HTML | Sharing, presenting, archiving — looks great in any browser |
| Word (.docx) | Editing, printing, sending for review |
| Markdown (.md) | Notion, Obsidian, or any plain-text workflow |

---

## 中文

### 这是什么？

`chat2podcast` 是一个运行在 [CatDesk](https://catdesk.ai) 上的 AI Skill，能把微信群聊天记录转化为专业播客脚本，并生成一个精美的单文件交互式 HTML 网站来展示这期节目。

它的核心信念是：**最好的对话已经在你的群聊里发生了——它们只是需要一个更好的舞台。**

### 它能做什么

给它一段微信群聊天记录（截图文件夹、图片、或直接粘贴文字），它会：

1. **提取**所有消息，用视觉模型 OCR 识别，清洗噪音，按发言人整理
2. **深度挖掘**——忠实还原事实，按话题聚类，联网搜索更大的背景
3. **先和你交互，再动笔**——确认话题、风格、时长、结构、发言人姓名、以及这是长期节目还是单次尝试
4. **用专业结构写脚本**——Ira Glass 三幕叙事法（Cold Open → 发展 → 反思时刻）
5. **输出**你选择的格式：交互式 HTML 网站、Word 文档、或 Markdown

### 核心特性

**铁律：先交互，再动笔**
在确认所有信息之前，Skill 不会写任何脚本内容。它会逐一确认：聚焦哪些话题、想要什么风格和时长、每位发言人叫什么名字、这是长期节目还是单次尝试。

**长期节目记忆**
如果你在做一档持续更新的播客，Skill 会把节目配置（名称、固定主持人、语气基调、开场白/片尾模板）写入持久化 Memory。下次使用时自动读取，无需重新设置。

**发言人姓名处理**
Skill 会主动询问每位发言人的真实姓名。如果你不确定或不方便透露，它会从精选名库中随机分配英文名：Alex、Jamie、Morgan、Casey、Riley、Jordan、Taylor、Quinn、Avery、Blake、Drew、Sage、River、Skyler、Reese。

**专业叙事结构**
脚本遵循 Ira Glass 方法论——播客叙事的黄金标准。每期节目都有 Cold Open 钩子、三幕结构、以及"为什么这件事重要"的反思时刻。

**9 种视觉主题（HTML 输出）**
暗黑唱片 · 深夜电台 · 胶片复古 · 温暖纸张 · 极简终端 · 深空蓝图 · 玻璃态 · 手写杂志 · 报纸排版

**自动滚动截图**
内置 Python 脚本，自动滚动并截取微信聊天窗口，无需手动操作。

### 如何使用

这个 Skill 运行在 [CatDesk](https://catdesk.ai) 中。将 `SKILL.md` 放入 CatDesk 的 skills 目录即可安装：

```
~/.catpaw/skills/chat2podcast/SKILL.md
```

然后通过以下方式触发：
- "把这个聊天记录做成播客"
- "chat2podcast"
- "帮我从群聊生成播客脚本"
- "把这些截图整理成一期播客"

### 工作流程

```
第零步  →  读取 Memory，检查是否有已有节目配置
第一步  →  获取聊天记录（自动截图 / 文件夹 / 粘贴 / 上传图片）
第二步  →  深度挖掘：清洗、事实还原、话题聚类、联网搜索
第三步  →  与用户确认所有信息（话题、格式、时长、姓名、节目类型）
第四步  →  加载 Format 模板
第五步  →  撰写脚本（Ira Glass 三幕结构）
第六步  →  选择输出格式（HTML / Word / Markdown）
第七步  →  选择视觉风格（仅 HTML）
第八步  →  生成播客网站（仅 HTML）
第九步  →  生成 Word 文档（仅 Word）
第十步  →  交付文件到桌面
```

### 输出格式

| 格式 | 适合场景 |
|------|---------|
| 交互式 HTML | 分享、展示、存档——在任何浏览器里都好看 |
| Word (.docx) | 编辑、打印、发给他人审阅 |
| Markdown (.md) | Notion、Obsidian 或任何纯文本工作流 |

---

## License

MIT
