---
name: chat2podcast
description: "Transforms group chat logs into professional podcast scripts and generates a beautiful interactive HTML website. Accepts screenshot folders, pasted text, or uploaded images as input. Automatically extracts messages, clusters topics, selects a podcast format, enriches content with web research, and produces a single-file animated HTML podcast site. Trigger when the user says: 'turn this chat into a podcast', 'make a podcast from my group chat', 'chat2podcast', 'generate a podcast script from chat logs', or 'podcast from WeChat'. Also trigger if the user simply says 'make me a podcast' and provides chat screenshots or text."
---

# chat2podcast

A complete workflow for distilling group chat logs into a professional podcast.

**Core philosophy**: Chat logs are raw ore, not finished product. Your job is to: ① faithfully reconstruct what was actually discussed (facts first); ② search the web to give each topic broader context and depth; ③ restructure everything using professional podcast narrative techniques so it's worth listening to.

---

## ⚠️ Iron Rule: Ask First, Act Never

**Every single step in this workflow requires explicit user confirmation before proceeding to the next step. No exceptions.**

Forbidden behaviors:
- Moving to the next step without waiting for the user's reply
- Saying "I'll proceed with X" and then immediately doing X
- Substituting "I picked X for you" for a genuine question
- Generating any script content before the user has confirmed topics, style, and structure
- Generating the HTML before the user has confirmed the script

Required behaviors at every step:
- Present your findings or proposal
- Use the **dual-mode interaction pattern** (see below) to ask
- **STOP. Wait for the user's explicit reply before continuing.**

---

## 🎛️ Dual-Mode Interaction Pattern (use at every STOP point)

At every decision point, you must offer clickable choices — not just ask the user to type a free-form answer.

### How it works

**Mode 1 — CatDesk (preferred)**: Use the `AskQuestion` tool to render interactive choice cards. The user clicks directly without typing.

**Mode 2 — Fallback (all other environments)**: If `AskQuestion` is unavailable or throws an error, immediately fall back to formatted text options. The user replies with a letter (A / B / C…) or a short answer.

### How to detect which mode to use

Try calling `AskQuestion` first. If it succeeds, you're in CatDesk — use it for all subsequent STOP points in this session. If it fails or is not available, switch to fallback mode for the rest of the session. Do not retry `AskQuestion` after a failure.

### Fallback format template

When using fallback mode, always format choices like this — never ask open-ended questions without options:

```
[Brief context sentence]

请选择（直接回复字母即可）：
A. [Option A — short label] — [one-line description]
B. [Option B — short label] — [one-line description]
C. [Option C — short label] — [one-line description]

[If free text is also valid]: 或者直接告诉我你的想法。
```

### When free text is unavoidable

Some questions (e.g., "what's the show name?", "what are the speaker names?") can't be reduced to A/B/C. For these:
- In CatDesk: use `input_type: "mixed"` or `input_type: "text"` in `AskQuestion`
- In fallback: ask the question clearly and concisely, one question at a time

---

## Step 0: Read Memory (do this every time before anything else)

**Before taking any action, call `memory_read` to check for an existing show configuration.**

```
Call: memory_read()
Look for keywords: chat2podcast / show DNA / podcast_show
```

### Case A: Existing show config found

Show the user what was saved, then ask how to proceed using the dual-mode pattern:

**CatDesk mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "existing_config",
    "prompt": "📻 找到了你的节目配置：\n节目名：[name]\n主播：[hosts]\n定位：[positioning]\n\n如何继续？",
    "input_type": "choice",
    "options": [
      { "id": "keep",   "label": "A. 保持现有配置（推荐）" },
      { "id": "update", "label": "B. 修改某些字段" },
      { "id": "fresh",  "label": "C. 重新开始（新节目或一次性）" }
    ]
  }]
}
```

**Fallback mode**:
```
📻 找到了你的节目配置：
节目名：[name] | 主播：[hosts] | 定位：[positioning]

请选择（直接回复字母即可）：
A. 保持现有配置（推荐 — 保持节目一致性）
B. 修改某些字段（告诉我改哪里）
C. 重新开始（新节目或一次性单集）
```

**STOP. Wait for the user's reply before continuing.**

- User picks **A (keep)**: Skip Step 3.2 ongoing/one-off questions; use the saved config and display it in the final confirmation summary.
- User picks **B (update)**: Ask which fields to change, update them, then rewrite to memory.
- User picks **C (fresh start)**: Follow the full Step 3 flow as normal.

### Case B: No show config found

Proceed with the full workflow. Step 3 will ask about show positioning.

---

## Step 1: Collect the Chat Log

Users may provide chat logs in several ways. **If the user hasn't specified, guide them toward the best option.**

---

### Method A: Auto-scroll screenshot capture (recommended — least effort)

This is the preferred method. The user just opens their WeChat chat window; the script handles all the scrolling and screenshotting automatically.

**How to guide the user:**

```
The easiest way is auto-screenshot:
1. Grant permission first: System Settings → Privacy & Security → Screen Recording → enable CatPaw Desk
2. Open WeChat, go to the group chat you want to capture, scroll to the latest message
3. Tell me how far back you want to capture (see the table below)
4. I'll run the screenshot script — just keep WeChat in the foreground once the countdown ends
```

**Duration reference (each screenshot captures roughly 8–14 messages):**

| Duration | ~Screenshots | ~Messages covered | Best for |
|----------|-------------|-------------------|----------|
| 30 sec   | ~15         | 120–210           | Last 1–2 days |
| 60 sec   | ~30         | 240–420           | Last 3–5 days |
| 120 sec  | ~60         | 480–840           | Last 1–2 weeks |
| 300 sec  | ~150        | 1,200–2,100       | Last month |

**Run the screenshot script:**

```bash
# Basic usage (120 seconds, recommended)
python3 ~/.catpaw/skills/chat2podcast/scripts/auto_screenshot.py --duration 120

# Custom duration and output folder
python3 ~/.catpaw/skills/chat2podcast/scripts/auto_screenshot.py \
  --duration 60 \
  --output ~/Desktop/my_screenshots

# Manual scroll mode (no auto Page Up — you scroll yourself)
python3 ~/.catpaw/skills/chat2podcast/scripts/auto_screenshot.py \
  --duration 120 --no-scroll
```

The script will print the output folder path when it finishes — the user just passes that path to you.

**If screenshots fail:** Guide the user to System Settings → Privacy & Security → Screen Recording → find CatPaw Desk → enable it.

---

### Method B: Existing screenshot folder

The user already has screenshots and provides a folder path (e.g. `~/Desktop/wechat_screenshots/`).

Use a vision model to read each image in order, extracting chat content. Sort by filename to preserve chronological order.

```python
import os, glob
images = sorted(
    glob.glob(os.path.join(folder_path, "*.png")) +
    glob.glob(os.path.join(folder_path, "*.jpg"))
)
# For each image: extract speaker nickname, message content, timestamp (if visible)
```

---

### Method C: Paste text directly

The user pastes an exported text log. Skip the screenshot step and go straight to Step 2.

---

### Method D: Upload screenshots in the conversation

The user sends images directly. Run vision recognition on each one to extract content.

---

### After extraction

Organize everything into a unified format:
```
[time] Speaker: message
[time] Speaker: message
...
```

Tell the user: "Extracted XX valid messages spanning [date range]. Starting analysis."

---

## Step 2: Deep Mining

This is the most critical step in the entire workflow. **Facts first. Search broadly. Understand deeply.**

### 2.1 Clean the data

Remove: system messages ("X joined the group"), retracted messages, pure emoji reactions, voice message placeholders ("[Voice]"), and content-free filler like "haha" / "ok" / "noted".

Keep: messages with opinions, personal stories, disagreements, or substantive information.

### 2.2 Reconstruct the facts (most important)

**Read through the chat log carefully and faithfully record what was actually discussed.** No guessing, no embellishing, no skipping details.

For each topic, extract:
- **Core facts**: What specifically was said? Who said it? Were there concrete numbers, examples, or personal experiences?
- **Real opinions**: What was each person's position? Were there disagreements?
- **Emotional temperature**: Was the discussion light or heated? Were there moments of resonance or friction?
- **Unfinished threads**: Were any topics cut short, left without a conclusion, or left hanging?

**Wrong way to summarize:**
> The group discussed challenges in the live music market.

**Right way:**
> Ajie shared that only 20 people showed up to his gig last week, saying "feeling invisible hurts more than losing money." Xiaoqing added that converting online followers to ticket buyers is nearly impossible. Lao Wang argued this is a structural problem, not one that effort can solve. The three disagreed on whether community could fix it — Xiaoqing felt community provides psychological safety, while Lao Wang said "community isn't the answer, it just means we're not alone."

### 2.3 Cluster by topic (cross-time perspective)

Group messages by **topic** (not by time). **Do not follow the chronological order of the chat log.** Your job is to find the underlying themes that connect messages across different time points.

Signals to look for:
- Keyword clustering (multiple people repeatedly mention the same word or concept)
- Conversational coherence (A asks, B answers, forming a thread)
- Emotional resonance (different messages that share the same underlying feeling)
- Topic-shift signals ("speaking of which", "changing the subject", "quick question")

Give each cluster a precise title that captures the **core tension**, for example:
- "Live Shows: The Real Cost and Psychological Toll of a 20-Person Gig" (not "live music struggles")
- "Community Value: Psychological Safety vs. Structural Problems — A Genuine Disagreement" (not "community discussion")

### 2.4 Broad search (web enrichment)

**For every topic worth exploring, proactively search for relevant background.** Don't wait for the user to ask — this is default behavior.

Search strategy:
- Use `web_search` to find industry data, social phenomena, and others' experiences related to each topic
- Search for discussions on Reddit, Twitter/X, or relevant forums to understand how widely the topic resonates
- Look for news articles, research reports, and expert perspectives

**Example searches:**
```
web_search("independent music live shows 2024 market data")
web_search("indie musician losing money on shows personal experience")
web_search("music community mutual support independent artists")
```

Use search results to:
- Back up points made in the chat with data ("this phenomenon the group described affects XX% of independent musicians")
- Surface important context that wasn't mentioned in the chat
- Find the larger social frame so the topic isn't just "something this group talked about"

### 2.5 Filter for podcast value

Not every topic deserves airtime. Prioritize:
- Topics with real stories and specific details (not vague generalities)
- Topics with clashing viewpoints or genuine disagreement (not unanimous agreement)
- Topics with emotional resonance (listeners will say "I've felt that too")
- Topics with meaning beyond the group chat itself

Exclude: purely logistical announcements, content-free small talk, private information.

### 2.6 Show the user your analysis

Before moving on, present your findings:

```
📊 Analysis complete

Extracted XX valid messages. Identified N core topics:

1. "[Precise topic title]"
   What was actually discussed: [2–3 sentences, faithful to the chat]
   Key quote: ["most representative line from the chat"]
   External context: [relevant data or phenomenon found via search]
   Podcast potential: ⭐⭐⭐⭐⭐

2. "[Precise topic title]"
   ...
```

After presenting the topic analysis, **immediately continue to Step 2.7 without waiting** — the user will review both together and reply once.

---

## Step 2.7: Podcast Positioning Analysis (Red Ocean Warning)

**Run this immediately after Step 2.6, without waiting for the user's reply. Present both the topic analysis and the positioning analysis together, then use the dual-mode pattern to STOP once for the user's combined feedback.**

**This step must happen before any discussion of format or structure. Its purpose: help the user find a differentiated position in the market, and avoid entering a saturated space.**

### Why this matters

Most podcasts fail not because the content is bad, but because they're doing exactly what 500 other shows are already doing. A chat-to-podcast workflow is especially prone to this — the content is personal and specific, but the framing can easily default to generic categories (e.g., "a show about life and work", "a show about tech and culture").

### How to do it

**Step 1: Search the current podcast landscape**

Based on the topics identified in Step 2, search for existing podcasts in the same space:

```
web_search("[topic area] podcast 2024 popular shows")
web_search("[topic area] podcast Chinese 小宇宙 2024")
web_search("best podcasts about [core theme] recommendations")
```

Look for: what shows already exist, what angles they take, what audiences they serve, what's oversaturated.

**Step 2: Map the user's unique assets**

From the chat log analysis, identify what's genuinely distinctive about this group:
- Specific life stage or identity (e.g., "people in their late 20s navigating the gap between ambition and stability")
- Specific perspective or expertise (e.g., "people who've worked in both big tech and government")
- Specific emotional texture (e.g., "the kind of conversations you have at 11pm after a few drinks")
- Specific format advantage (e.g., "real unfiltered group chat, not a produced interview")

**Step 3: Find the intersection**

Present a positioning map:

```
🗺️ Podcast Positioning Analysis

🔴 Red Ocean (avoid — already crowded):
- [Category 1]: [why it's saturated, examples of existing shows]
- [Category 2]: [why it's saturated, examples of existing shows]

🟡 Adjacent (possible but competitive):
- [Category]: [what exists, what gap might remain]

🟢 White Space (your opportunity):
- [Positioning A]: "[one-sentence description]"
  Why it's open: [reason]
  Your unique asset that fits: [from the chat analysis]

- [Positioning B]: "[one-sentence description]"
  Why it's open: [reason]
  Your unique asset that fits: [from the chat analysis]

- [Positioning C]: "[one-sentence description]"
  Why it's open: [reason]
  Your unique asset that fits: [from the chat analysis]

💡 My recommendation: [Positioning X], because [specific reason tied to the chat content].
   One-line pitch: "[what this show is, for whom, and why it's different]"
```

**Step 4: Combined ask (topics + positioning)**

This is the single STOP point for both Step 2.6 and Step 2.7. Use the dual-mode pattern:

**CatDesk mode** — call `AskQuestion` with two questions:
```json
{
  "questions": [
    {
      "id": "topics",
      "prompt": "① 话题确认：以上 N 个话题，你想聚焦哪几个？有没有想加或去掉的？",
      "input_type": "mixed",
      "allow_multiple": true,
      "options": [
        { "id": "t1", "label": "话题 1：[title]" },
        { "id": "t2", "label": "话题 2：[title]" },
        { "id": "t3", "label": "话题 3：[title]" }
      ]
    },
    {
      "id": "positioning",
      "prompt": "② 定位方向：哪个方向最打动你？",
      "input_type": "choice",
      "options": [
        { "id": "A", "label": "A. [Positioning A 一句话]" },
        { "id": "B", "label": "B. [Positioning B 一句话]" },
        { "id": "C", "label": "C. [Positioning C 一句话]" },
        { "id": "own", "label": "D. 我有自己的想法（下面说）" }
      ]
    }
  ]
}
```

**Fallback mode**:
```
两件事确认一下，再往下走：

① 话题：以上 N 个话题，你想聚焦哪几个？（直接说编号，如"1、3"，或告诉我增减）

② 定位：哪个方向最打动你？
A. [Positioning A 一句话]
B. [Positioning B 一句话]
C. [Positioning C 一句话]
D. 我有自己的想法（直接说）
```

**STOP. Wait for the user's reply before continuing to Step 3.**

---

## Step 3: Deep User Confirmation (Iron Rule — cannot be skipped)

**This is a mandatory step.** After analyzing the chat and confirming positioning, you must confirm all of the following with the user before writing anything. Every item. No exceptions.

### 3.1 Topic confirmation

Topics were already confirmed in Step 2.7. If the user's reply there was clear, carry those choices forward and skip re-asking. Only ask again here if the user's Step 2.7 reply was ambiguous.

### 3.2 Ongoing series vs. one-off

**Ask this before format, structure, or speaker questions. The answer shapes everything that follows.**

**CatDesk mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "show_type",
    "prompt": "在聊格式之前，先确认一件事：这个播客是……",
    "input_type": "choice",
    "options": [
      { "id": "ongoing", "label": "🎯 持续节目 — 打算长期做，有固定受众" },
      { "id": "oneoff",  "label": "🎲 单集尝试 — 先做这一期，看看效果" }
    ]
  }]
}
```

**Fallback mode**:
```
在聊格式之前，先确认一件事：

请选择（直接回复字母即可）：
A. 🎯 持续节目 — 打算长期做，有固定受众，需要节目名、固定主播和片头片尾
B. 🎲 单集尝试 — 先做这一期，看看效果，风格可以灵活
```

**STOP. Wait for the user's reply.**

**If ongoing**: Follow up with a second ask (CatDesk: new `AskQuestion` call; fallback: plain text questions):
```
需要再了解几件事：
- 节目名叫什么？（或者让我来提几个选项）
- 固定主播是谁？（建议 1–2 人）
- 节目定位是什么？（面向谁？聊什么类型的话题？）
```

**Additional rules for ongoing shows:**

If the user chooses ongoing, the script must include these fixed elements:

- **Fixed intro**: The same show introduction every episode (~15–20 seconds), building brand recognition
- **Regular hosts**: 1–2 fixed hosts throughout; guests can change but hosts don't
- **Consistent tone**: Determined by the show's positioning — maintained across all episodes
- **Fixed outro**: The same closing words and call to action every episode
- **Show DNA document**: At the final confirmation stage, output a "show style guide" for reference in future episodes

**Once the ongoing show details are collected, immediately write to longterm memory:**

```
Call: memory_write(type="longterm")

Format to write:
## chat2podcast Show Configuration

- Show name: [name]
- Regular hosts: [name1], [name2 (if applicable)]
- Core positioning: [target audience] + [topic type]
- Tone: [casual / serious / warm / sharp]
- Fixed intro: [full intro text]
- Fixed outro: [full outro text]
- Created: [current date]
- Last updated: [current date]
```

After writing, tell the user: "节目配置已保存，下次使用 chat2podcast 会自动加载，不用重新设置。"

If the user chooses one-off, skip the fixed elements and memory write.

### 3.3 Podcast style and length

**CatDesk mode** — call `AskQuestion` with two questions:
```json
{
  "questions": [
    {
      "id": "format",
      "prompt": "🎙️ 播客形式选哪种？",
      "input_type": "choice",
      "options": [
        { "id": "roundtable",  "label": "A. 圆桌讨论 — 多视角碰撞，适合有分歧的话题（参考 Radiolab）" },
        { "id": "interview",   "label": "B. 深度访谈 — 一主一客，适合有大量内容要分享（参考 Fresh Air）" },
        { "id": "narrative",   "label": "C. 叙事纪录 — 旁白+片段，适合完整故事弧（参考 This American Life）" },
        { "id": "monologue",   "label": "D. 独白/单人 — 一人深度思考（参考 Hardcore History）" },
        { "id": "auto",        "label": "E. 帮我决定 — 根据内容推荐最合适的形式" }
      ]
    },
    {
      "id": "length",
      "prompt": "⏱️ 目标时长？",
      "input_type": "choice",
      "options": [
        { "id": "short",  "label": "短 15–20 分钟 — 通勤友好，适合聚焦话题" },
        { "id": "medium", "label": "标准 25–35 分钟 — 最常见，适合大多数话题" },
        { "id": "long",   "label": "深度 40–50 分钟 — 内容丰富、主题复杂时用" }
      ]
    }
  ]
}
```

**Fallback mode**:
```
🎙️ 播客形式（选一个）：
A. 圆桌讨论 — 多视角碰撞，适合有分歧的话题（参考 Radiolab）
B. 深度访谈 — 一主一客，适合有大量内容要分享（参考 Fresh Air）
C. 叙事纪录 — 旁白+片段，适合完整故事弧（参考 This American Life）
D. 独白/单人 — 一人深度思考（参考 Hardcore History）
E. 帮我决定 — 根据内容推荐最合适的形式

⏱️ 目标时长：
- 短：15–20 分钟（通勤友好，适合聚焦话题）
- 标准：25–35 分钟（最常见，适合大多数话题）
- 深度：40–50 分钟（内容丰富、主题复杂时用）

🎨 整体氛围（可选）：
随意聊天 / 严肃分析 / 温暖故事 / 犀利观点
```

**STOP. Wait for the user's reply.**

### 3.4 Propose a narrative structure (with reasoning)

Based on the user's chosen format and length, propose a specific three-act structure and explain why. Then ask for confirmation using the dual-mode pattern:

Present the structure in text first:
```
📐 推荐结构：[structure name]

第一幕（约 X 分钟）：[specific content]
  → 为什么这样开场：[reason]

第二幕（约 X 分钟）：[specific content]
  → 为什么这样展开：[reason]

第三幕（约 X 分钟）：[specific content]
  → 为什么这样收尾：[reason]

Cold Open 钩子：打算用「[specific opening line]」开场
  → 为什么：[reason]
```

Then ask:

**CatDesk mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "structure",
    "prompt": "这个结构你觉得怎么样？",
    "input_type": "mixed",
    "options": [
      { "id": "ok",     "label": "✅ 可以，就这样" },
      { "id": "adjust", "label": "🔧 需要调整（下面说说）" }
    ]
  }]
}
```

**Fallback mode**:
```
这个结构你觉得怎么样？

A. ✅ 可以，就这样
B. 🔧 需要调整（告诉我改哪里）
```

**STOP. Wait for confirmation or revisions. If the user wants changes, revise and confirm again.**

### 3.5 Speaker name confirmation

Speaker names directly affect how real and listenable the podcast feels. **Always ask for each speaker's real name or preferred name.**

Note: if the show is ongoing (confirmed in 3.2), the fixed host(s) should already be known — just verify the names here.

For each speaker identified in the chat, ask their preferred name. This is a free-text question — use `input_type: "text"` in CatDesk, or plain text in fallback:

```
我在聊天记录里识别到以下发言人：[nickname1]、[nickname2]、[nickname3]…

播客里用名字称呼会更自然。每个人想用什么名字？（真名、英文名、或你帮他们取一个都行）

如果不确定，我会随机分配英文名，比如 Alex、Jamie、Morgan。
```

**Handling rules:**

- User provides names → use exactly what they provide
- User says "not sure" / "whatever" / "you decide" → randomly assign from this pool, one unique name per person:
  `Alex, Jamie, Morgan, Casey, Riley, Jordan, Taylor, Quinn, Avery, Blake, Drew, Sage, River, Skyler, Reese`
- User says "keep the chat nicknames" → keep the original nicknames
- User says "anonymous" → use descriptive labels like "one guest" / "another guest"

**Host role**: If the format is roundtable or deep interview, confirm who plays the host (can be someone from the chat, or a fictional host persona). For ongoing shows, this should already be set from 3.2.

Also ask (CatDesk: include as a choice question; fallback: append to the same message):

**CatDesk mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "web_research",
    "prompt": "需要我搜索网络资料来丰富内容背景吗？",
    "input_type": "choice",
    "options": [
      { "id": "yes", "label": "✅ 是，帮我搜（推荐）" },
      { "id": "no",  "label": "❌ 不用，只用聊天记录里的内容" }
    ]
  }]
}
```

**Fallback mode**:
```
需要我搜索网络资料来丰富内容背景吗？
A. ✅ 是，帮我搜（推荐）
B. ❌ 不用，只用聊天记录里的内容
```

**STOP. Wait for the user's reply.**

---

### 3.6 All confirmed — ready to write

Once you have the user's replies to all of the above, do a final confirmation summary, then ask for go-ahead using the dual-mode pattern:

Present the summary in text:
```
✅ 已确认：

- 话题：[topic 1]、[topic 2]
- 定位：[chosen direction]
- 节目类型：[持续节目 / 单集尝试]
  （持续）节目名：[name] | 定位：[positioning]
- 形式：[format]
- 目标时长：[length]
- 氛围：[vibe]
- 结构：[structure name]
- 发言人：[nickname → name mappings]
- 主播：[name]
- 网络搜索：[是 / 否]
```

Then ask:

**CatDesk mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "confirm_start",
    "prompt": "一切就绪，开始写内容地图？",
    "input_type": "choice",
    "options": [
      { "id": "go",     "label": "🚀 开始！" },
      { "id": "adjust", "label": "✏️ 还有些地方想改" }
    ]
  }]
}
```

**Fallback mode**:
```
一切就绪，开始写内容地图？

A. 🚀 开始！
B. ✏️ 还有些地方想改（告诉我）
```

**STOP. Only proceed to Step 4 after the user picks "go ahead".**

**Memory write notes:**
- If this is a **new ongoing show** (set up in Step 3.2): memory was already written there — no need to write again here.
- If the user chose **"keep" or "update"** in Step 0: call `memory_write(type="longterm")` now to update the "last updated" field to today's date.
- If this is a **one-off**: no memory write needed.

---

## Step 4: Select Podcast Format (confirmed in Step 3 — internal reference only)

The format was confirmed with the user in Step 3. This step is internal reference: load the corresponding format template based on the user's choice.

```
Format mapping:
A. Roundtable → roundtable format
B. Deep interview → interview format
C. Narrative documentary → narrative format
D. Solo / monologue → monologue format
E. Auto-select → determine based on topic count and content characteristics
```

---

## Step 5: Build the Content Map (NOT a word-for-word script)

Read `references/podcast-formats.md` for professional podcast structure methodology, then build the content map according to the following principles.

### What a content map is (and is not)

**A content map is a navigation guide for the hosts — not a script to be read aloud.**

❌ Do NOT write:
- Full sentences for the hosts to say
- Narration paragraphs
- Dialogue transcripts
- Anything that sounds like a finished script

✅ DO write:
- The **core tension** of each topic (what makes it interesting to dig into)
- **3–5 guiding questions** per topic (open-ended, designed to let conversation flow naturally)
- **2–3 gold quote candidates** per topic (pulled directly from the chat log — real words, not AI-generated)
- **External context hooks** (a data point or social phenomenon that gives the topic a larger frame)
- **Transition cues** (how to move from one topic to the next)
- **Approximate time allocation** per section

### Cross-time clustering (critical)

**Do not follow the chronological order of the chat log.** The chat log is raw material — your job is to find the underlying architecture.

Ask yourself: what is this conversation *really* about? What's the deeper theme connecting messages from different times? Cluster by emotional and intellectual resonance, not by when things were said.

Example: A message from Monday about "feeling invisible at work" and a message from Thursday about "not knowing if this path is right" might belong to the same topic cluster — even though they're days apart and seem unrelated on the surface.

### Go deeper than the surface (critical)

The chat log shows what people said. Your job is to find what they *meant* — and what it connects to in the wider world.

For each topic:
1. What's the surface-level conversation? (what they literally discussed)
2. What's the underlying tension? (the real question beneath the words)
3. What does this connect to in the broader social/cultural/psychological landscape? (use web research)
4. What's the "why does this matter" moment? (the Ira Glass reflection — what larger truth does this reveal?)

### The Ira Glass approach

Ira Glass (creator of This American Life) developed the most authoritative framework for podcast storytelling:

**Two fundamental building blocks:**
1. **Anecdote**: A sequence of events unfolding in time, where each event raises a question that pulls the listener forward.
2. **Moment of Reflection**: After the story, explain why it matters — what larger truth it reveals.

**The golden rule**: Every story needs a "why does this matter" moment. Without it, the story is just a sequence of events.

### Content map format

```markdown
## Cold Open (30–60 sec)

Hook line: [the single most compelling line or moment from the entire chat — drop straight in, no intro]
Why this works: [reason]

---

## Act 1: [Title] (~X min)

### Core tension
[One sentence: what's the real question or conflict here? Not "they discussed X" but "the tension between X and Y"]

### Background context
[1–2 sentences of external context from web research that gives this topic a larger frame]
Source: [search result or data point]

### Guiding questions (for the hosts)
1. [Open question that invites personal story, not yes/no]
2. [Question that surfaces the tension or disagreement]
3. [Question that pushes toward the deeper "why does this matter"]
4. [Optional: question that connects to the external context]
5. [Optional: question that opens toward the next topic]

### Gold quotes from the chat
- "[exact quote from chat log]" — [speaker]
- "[exact quote from chat log]" — [speaker]
- "[exact quote from chat log]" — [speaker]

### Moment of reflection
[What larger truth does this topic reveal? 1–2 sentences. This is what the hosts should land on before moving on.]

### Transition to next topic
[One sentence: how does this topic naturally lead into the next one?]

---

## Act 2: [Title] (~X min)

[Same structure as above]

---

## Act 3: [Title] (~X min)

[Same structure as above]

### Closing reflection
[The final "why does this whole episode matter" — not a summary, but a frame]

### Open-ended closing question
[A question for listeners to sit with — not answered in the episode]

---

## Outro (~30 sec)

[Fixed outro text if ongoing show / flexible closing if one-off]
```

### Format-specific requirements

**Roundtable**: Design "collision questions" — not questions that get everyone to agree, but questions that surface disagreement. Every topic needs at least one question where the guests genuinely diverge.

**Deep interview**: Use "funnel questioning" — broad to specific, facts to feelings, past to future. The best question is often "what were you feeling in that moment?"

**Narrative documentary**: Narration should be visual — describe a scene, don't summarize. Use present tense to create immediacy.

**Solo / monologue**: The opening must create resonance with a question or scene the listener can feel — don't lead with your thesis.

### After completing the content map

Present the full content map, then ask for feedback using the dual-mode pattern:

**CatDesk mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "content_map_review",
    "prompt": "内容地图写好了，检查一下：话题顺序对吗？引导问题有没有要改的？金句选得准吗？",
    "input_type": "mixed",
    "options": [
      { "id": "good",   "label": "✅ 很好，进入下一步" },
      { "id": "adjust", "label": "✏️ 有些地方想调整（下面说）" }
    ]
  }]
}
```

**Fallback mode**:
```
内容地图写好了，检查一下：
- 话题顺序对吗？（我按主题重组了，不是时间顺序）
- 引导问题有没有要删或加的？
- 金句选得准吗？有没有想换的？
- 收尾反思落地了吗？

A. ✅ 很好，进入下一步
B. ✏️ 有些地方想调整（告诉我）
```

**STOP. Wait for the user's reply and incorporate any changes before proceeding.**

---

## Step 6: Choose Output Format

Once the content map is confirmed, ask the user which format they want using the dual-mode pattern:

**CatDesk mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "output_format",
    "prompt": "内容地图确认！选择输出格式：",
    "input_type": "choice",
    "allow_multiple": false,
    "options": [
      { "id": "html", "label": "A. 🌐 交互式 HTML 网站（推荐）— 动画、可编辑、单文件直接打开" },
      { "id": "docx", "label": "B. 📄 Word 文档 — 方便编辑和打印" },
      { "id": "md",   "label": "C. 📝 Markdown 文件 — 轻量，可粘贴到 Notion / Obsidian" },
      { "id": "all",  "label": "D. 📦 全部格式（HTML + Word + Markdown）" }
    ]
  }]
}
```

**Fallback mode**:
```
内容地图确认！选择输出格式：

A. 🌐 交互式 HTML 网站（推荐）
   — 动画效果、可在浏览器直接编辑文字、单文件打开
B. 📄 Word 文档
   — 方便编辑和打印，适合进一步修改或分享审阅
C. 📝 Markdown 文件
   — 轻量，可直接粘贴到 Notion / Obsidian
D. 📦 全部格式（HTML + Word + Markdown）
```

**STOP. Wait for the user's reply.**

---

## Step 7 (HTML): Choose a Visual Theme

If the user chose HTML, enter the theme selection flow.

Ask the user how they want to choose the visual style using the dual-mode pattern:

**CatDesk mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "theme_method",
    "prompt": "怎么选网站视觉风格？",
    "input_type": "choice",
    "options": [
      { "id": "preview", "label": "A. 👀 给我看预览（推荐）— 生成 3 个风格小样，我来挑" },
      { "id": "direct",  "label": "B. 📋 直接选 — 给我看主题列表，我自己选" }
    ]
  }]
}
```

**Fallback mode**:
```
怎么选网站视觉风格？

A. 👀 给我看预览（推荐）— 生成 3 个风格小样，我来挑
B. 📋 直接选 — 给我看主题列表，我自己选
```

**STOP. Wait for the user's reply.**

### If they choose A: Generate 3 style previews

Based on the podcast's overall vibe, generate 3 different single-page HTML previews (each ~80–120 lines, showing the cover + one quote card). Save to `/tmp/podcast-preview/` as style-a.html, style-b.html, style-c.html, then open each in Chrome:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome "file:///tmp/podcast-preview/style-a.html" &
```

**Theme selection guide** (see `references/html-themes.md` for full details):

| Content vibe | Recommended themes |
|-------------|-------------------|
| Music / art / culture | Dark Vinyl, Film Grain, Handwritten Magazine |
| Tech / startup / product | Minimal Terminal, Deep Space Blueprint, Glassmorphism |
| Life / emotion / stories | Warm Paper, Late Night Radio, Film Grain |
| Society / journalism / depth | Newspaper Layout, Minimal Terminal, Late Night Radio |

Each preview must demonstrate: a distinctive typeface, a color palette, one entrance animation, and a hover effect on quote cards.

After showing the previews, ask the user to pick using the dual-mode pattern:

**CatDesk mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "theme_pick",
    "prompt": "三个风格小样已生成，你更喜欢哪个？",
    "input_type": "choice",
    "options": [
      { "id": "A", "label": "A. 风格 A" },
      { "id": "B", "label": "B. 风格 B" },
      { "id": "C", "label": "C. 风格 C" }
    ]
  }]
}
```

**Fallback mode**:
```
三个风格小样已生成，你更喜欢哪个？
A. 风格 A
B. 风格 B
C. 风格 C
```

**STOP. Wait for the user to pick a theme before generating the full HTML.**

---

## Step 8 (HTML): Generate the Podcast Website

Read `references/html-themes.md` and `references/animation-patterns.md`, then generate a complete single-file HTML podcast website.

### Page structure

```
┌─────────────────────────────────────┐
│  Hero / Cover                        │
│  Show name + episode title + entrance animation │
├─────────────────────────────────────┤
│  Episode info bar                    │
│  Hosts / Guests / Length / Source   │
├─────────────────────────────────────┤
│  Topic navigation (sticky sidebar or top tabs) │
│  Click to jump to any section        │
├─────────────────────────────────────┤
│  Main content (scroll to read)       │
│  Each exchange displayed as a card  │
│  Speaker avatar/label + speech bubble │
│  Section headings animate on entry  │
├─────────────────────────────────────┤
│  Key takeaways section              │
│  3–5 standout quotes, card layout   │
├─────────────────────────────────────┤
│  Outro                              │
│  Next episode teaser + follow CTA   │
└─────────────────────────────────────┘
```

### Required interactive features

**Navigation**: Fixed top or side nav; click a section name to smooth-scroll; current section highlights as you scroll.

**Reading experience**: Section headings trigger entrance animations when they enter the viewport (Intersection Observer); dialogue cards appear in a staggered reveal; speaker cards have micro-interactions on hover.

**Quote cards**: Core takeaways have a "copy" button; hover to expand for more context.

**Progress indicator**: A thin progress bar at the top fills as the user scrolls.

**Optional features** (if the content suits it): Speaker filter (roundtable format — click a person to see only their lines); timeline mode (narrative documentary format).

---

### ✏️ In-Browser Edit Mode (required — every HTML output must include this)

Every generated HTML page must include a fully functional **Edit Mode** that lets the user modify content directly in the browser without touching any code.

#### Edit Mode toggle button

Place a floating button in the bottom-right corner of the page:

```html
<button id="edit-toggle" title="Toggle Edit Mode">✏️ 编辑</button>
```

Style it as a pill-shaped floating action button, always visible, with a subtle shadow. When edit mode is active, change the label to "✅ 完成编辑" and add a visible highlight ring.

#### What becomes editable

When edit mode is ON, add `contenteditable="true"` to:
- All dialogue bubble text (`.bubble` or equivalent)
- All quote card text (`.quote-text` or equivalent)
- All chapter/section titles (`.chapter-title` or equivalent)
- All reflection/context box text
- All takeaway items
- The hero title and subtitle
- The outro tagline

When edit mode is OFF, remove `contenteditable` from all elements (or set to `false`).

**Visual feedback when editable:**
```css
[contenteditable="true"] {
  outline: 2px dashed var(--accent);
  outline-offset: 3px;
  border-radius: 4px;
  cursor: text;
  background: rgba(255, 255, 255, 0.03);
}
[contenteditable="true"]:focus {
  outline-color: var(--accent-2);
  background: rgba(255, 255, 255, 0.06);
}
```

#### Save as new file button

When edit mode is active, show a second floating button: **"💾 保存修改"**

Clicking it triggers a JavaScript download of the current page's full HTML (including all edits) as a new file:

```javascript
function saveEdits() {
  // Disable contenteditable before saving so the saved file opens in view mode
  document.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
  // Also hide the edit toolbar in the saved file
  document.getElementById('edit-toolbar').style.display = 'none';

  const html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
  const blob = new Blob([html], { type: 'text/html' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = document.title.replace(/\s+/g, '_') + '_edited.html';
  a.click();

  // Re-enable edit mode UI after saving
  document.getElementById('edit-toolbar').style.display = '';
  toggleEditMode(true); // restore edit state
}
```

#### Edit toolbar (shown only when edit mode is active)

A slim bar at the top of the page (below the nav) with:
- A brief instruction: "点击任意文字即可直接编辑"
- A "💾 保存修改" button (same as the floating one)
- A "↩️ 撤销" hint: "Cmd+Z 撤销"

```html
<div id="edit-toolbar" style="display:none">
  <span>✏️ 编辑模式已开启 — 点击任意文字即可直接编辑</span>
  <button onclick="saveEdits()">💾 保存修改</button>
  <span style="opacity:0.5">Cmd+Z 撤销</span>
</div>
```

#### JavaScript implementation

```javascript
let editModeActive = false;

const EDITABLE_SELECTORS = [
  '.bubble', '.quote-text', '.chapter-title', '.chapter-desc',
  '.reflection-text', '.context-box p', '.takeaway-item',
  '.hero-title', '.hero-subtitle', '.outro-tagline',
  '.speaker-name' // optional — allow renaming speakers inline
];

function toggleEditMode(forceState) {
  editModeActive = (forceState !== undefined) ? forceState : !editModeActive;

  const toolbar = document.getElementById('edit-toolbar');
  const toggleBtn = document.getElementById('edit-toggle');
  const saveBtn = document.getElementById('save-btn');

  if (editModeActive) {
    EDITABLE_SELECTORS.forEach(sel => {
      document.querySelectorAll(sel).forEach(el => {
        el.setAttribute('contenteditable', 'true');
        el.setAttribute('spellcheck', 'false');
      });
    });
    toolbar.style.display = 'flex';
    toggleBtn.textContent = '✅ 完成编辑';
    toggleBtn.classList.add('active');
    if (saveBtn) saveBtn.style.display = 'block';
  } else {
    EDITABLE_SELECTORS.forEach(sel => {
      document.querySelectorAll(sel).forEach(el => {
        el.removeAttribute('contenteditable');
      });
    });
    toolbar.style.display = 'none';
    toggleBtn.textContent = '✏️ 编辑';
    toggleBtn.classList.remove('active');
    if (saveBtn) saveBtn.style.display = 'none';
  }
}

document.getElementById('edit-toggle').addEventListener('click', () => toggleEditMode());
```

#### UX rules for edit mode

- Edit mode is **OFF by default** — the page opens in clean reading mode
- Clicking the toggle button switches between view and edit mode
- In edit mode, the scroll-reveal animations are paused (so elements don't re-hide while editing)
- The progress bar and nav remain functional in both modes
- `Cmd+Z` / `Ctrl+Z` works natively for undo within any editable element
- The saved file opens in view mode (no edit toolbar visible) — the user must click the toggle to re-enter edit mode

---

### HTML technical requirements

- **Zero dependencies**: Single file, all CSS/JS inline, no npm or build tools required
- **Fonts**: Load from Google Fonts or Fontshare — never use Arial or system fonts
- **CSS variables**: All colors, fonts, and spacing defined as `--var`
- **Responsive**: Mobile-friendly, breakpoints at 768px / 1024px
- **Motion**: Respect `prefers-reduced-motion`
- **Comments**: Clear `/* === SECTION === */` comments for every block

### Design principles (avoiding the "AI mediocrity" look)

Avoid: generic purple gradients, overly uniform card grids, too many small animations, choosing Inter or Roboto.

Aim for: a cover with strong visual impact; animations concentrated at key moments; a typeface with personality; a dominant primary color that owns the palette.

---

## Step 9 (Word): Generate the Word Document

If the user chose Word output, use the `docx` skill to generate a properly formatted Word document.

Document structure:
- Cover page: show name, episode number, topic, date
- Table of contents
- Episode info (hosts, guests, length, source material)
- Content map by section (heading + core tension + guiding questions + gold quotes)
- Standout quotes summary
- Outro

---

## Step 10: Deliver

**HTML output:**
1. Save the HTML file to the user's desktop: `[ShowName]_Ep[X].html`
2. Open in browser to verify it renders correctly
3. Clean up temp preview files if any: `rm /tmp/podcast-preview/style-*.html` then `rmdir /tmp/podcast-preview`
4. Tell the user: file path, theme name, and feature overview (navigation / quote copy / progress bar / **edit mode**)
5. Specifically mention: "点击右下角 ✏️ 编辑 按钮可以直接在页面上修改任何文字，改完后点「💾 保存修改」下载新版本。"

**Word output:**
1. Save to desktop: `[ShowName]_Ep[X].docx`
2. Tell the user the file path

**Markdown output:**
1. Save to desktop: `[ShowName]_Ep[X].md`
2. Tell the user the file path

---

## Notes

**Facts first**: The content map must be faithful to what was actually discussed in the chat. Don't distort or exaggerate for the sake of a better story. If a topic was only briefly touched on, say so — don't pad it into a deep discussion that never happened.

**Enrichment has limits**: Web research provides background and data — it cannot replace the real opinions from the chat. Clearly label enriched content as "from external sources" and keep it distinct from what was actually said.

**Privacy**: If the chat contains obviously private information (phone numbers, addresses, sensitive personal details), anonymize or omit it.

**Speaker handling**: Nicknames can be kept, or replaced with "Guest A / B / C" — ask the user's preference.

**Length calibration**: A typical podcast episode runs 20–45 minutes. At roughly 150 words per minute: 20 min ≈ 3,000 words; 45 min ≈ 6,750 words. The content map should give enough material for the target length without over-scripting.

**Quality checklist** — before delivering, verify:
- Is the content map faithful to what was actually discussed in the chat?
- Is there a Cold Open hook?
- Is there a Moment of Reflection ("why does this matter") for each topic?
- Does the web research genuinely enrich the topic, rather than overshadow the original voices?
- Are the guiding questions open-ended and designed to let conversation flow naturally?
- Does the HTML include a working Edit Mode toggle?
- Does the output format match what the user chose?

---

## Reference Files

| File | Purpose | When to read |
|------|---------|-------------|
| `references/podcast-formats.md` | Professional podcast structure methodology with detailed format templates | Step 4 — when building the content map |
| `references/html-themes.md` | Podcast website theme library with color palettes, fonts, and design characteristics | Step 7 — when selecting a visual theme |
| `references/animation-patterns.md` | Interactive animation code snippets and usage contexts | Step 8 — when generating the HTML |
| `scripts/auto_screenshot.py` | Auto-scroll screenshot capture script | Step 1 — when guiding the user to capture screenshots |
| `scripts/build_podcast_html.py` | Renders script JSON into an HTML website | Step 8 — when generating the HTML |
