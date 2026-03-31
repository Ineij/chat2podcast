# chat2podcast

**Turn your group chats into professional podcast content maps — with a beautiful, editable interactive website to show for it.**

> 🇨🇳 [查看中文文档 →](README.zh.md)

---

## What is this?

`chat2podcast` is an **AI agent skill** that transforms group chat logs (WeChat or any messaging app) into professional podcast content maps, then generates a stunning single-file interactive HTML website to present the episode.

**You can use this skill in any AI agent that supports custom skills** — including CatDesk, Claude, or any agent framework that reads `SKILL.md` instruction files.

---

## How to Use in Your Agent

### Option 1 — Drop into your skills folder

If your agent supports a skills directory (e.g. `~/.catpaw/skills/` or similar), place the entire folder there:

```
your-agent-skills/
└── chat2podcast/
    ├── SKILL.md
    ├── references/
    ├── scripts/
    └── evals/
```

Then just tell your agent:

> *"Turn this chat into a podcast"*
> *"Make a podcast from my group chat"*
> *"chat2podcast"*

### Option 2 — Paste SKILL.md as a system prompt

Copy the contents of `SKILL.md` and paste it into your agent's system prompt or custom instructions. The agent will follow the workflow automatically.

### Option 3 — Reference in your agent config

Point your agent config to `SKILL.md` as an instruction file. Most agent frameworks support loading external instruction files by path.

---

## What it does

Given a group chat log (as screenshots, a folder of images, or pasted text), the skill:

1. **Extracts** all messages via vision OCR, cleans noise, organizes by speaker
2. **Mines deeply** — reconstructs facts faithfully, clusters topics, searches the web for broader context
3. **Analyzes the podcast landscape** — maps red-ocean categories to avoid and surfaces white-space positioning opportunities
4. **Talks to you first** — confirms topics, positioning, style, length, structure, and speaker names before writing a single word
5. **Builds a content map** using the Ira Glass three-act narrative method — guiding questions, gold quotes, and reflection moments (not a word-for-word script)
6. **Outputs** in your chosen format: interactive HTML website, Word document, or Markdown

---

## Key Features

### 🔒 Iron Rule: Ask First, Act Never

The skill never writes a word of content until it has confirmed everything with you — topics, positioning, format, structure, speaker names. No surprises, no assumptions.

### 🗺️ Podcast Positioning Analysis (Red Ocean Warning)

Before any scripting, the skill searches the current podcast landscape and maps out:
- **Red Ocean** — oversaturated categories to avoid
- **Adjacent** — competitive but possible
- **White Space** — open positioning that fits your unique content

It then recommends a specific one-line pitch for your show and asks you to confirm before proceeding.

### 🎛️ Dual-Mode Interaction

Every decision point offers clickable choices — not just open-ended questions:
- **CatDesk mode**: Uses the `AskQuestion` tool to render interactive choice cards. You click directly without typing.
- **Fallback mode**: If running in another agent environment, automatically falls back to formatted A/B/C text options. You reply with a letter.

The skill auto-detects which mode to use and stays consistent throughout the session.

### 📋 Content Map (Not a Word-for-Word Script)

The skill produces a **navigation guide for hosts**, not a script to be read aloud:
- Core tension of each topic (what makes it worth discussing)
- 3–5 guiding questions per topic (open-ended, designed for natural conversation)
- 2–3 gold quote candidates per topic (real words from the chat, not AI-generated)
- External context hooks (data or social phenomena that give the topic a larger frame)
- Transition cues and time allocation

This approach respects the hosts' voice and keeps the conversation authentic.

### ✏️ In-Browser Edit Mode

Every generated HTML page includes a fully functional **Edit Mode**:
- Click the **✏️ 编辑** floating button (bottom-right) to enter edit mode
- Click any text on the page to edit it directly — no code required
- Click **💾 保存修改** to download the edited page as a new HTML file
- The saved file opens in clean reading mode; click the button again to re-enter edit mode

### 🧠 Persistent Show Memory

Building a regular podcast? The skill saves your show config (name, fixed hosts, tone, intro/outro templates) to persistent memory. Next session, it loads automatically — no re-setup needed.

### 👤 Smart Speaker Naming

Asks for each speaker's real name. If you're unsure or prefer privacy, it assigns unique English names from a curated pool:
`Alex, Jamie, Morgan, Casey, Riley, Jordan, Taylor, Quinn, Avery, Blake, Drew, Sage, River, Skyler, Reese`

### 🎙️ Professional Narrative Structure

Content maps follow the **Ira Glass method** — the gold standard for podcast storytelling, used by This American Life, Serial, and NPR. Every episode has a Cold Open hook, a three-act arc, and a Moment of Reflection.

### 🎨 9 Visual Themes for HTML Output

`Dark Vinyl` · `Late Night Radio` · `Film Grain` · `Warm Paper` · `Minimal Terminal` · `Deep Space Blueprint` · `Glassmorphism` · `Handwritten Magazine` · `Newspaper Layout`

### 📸 Auto-Screenshot Capture

A bundled Python script automatically scrolls and screenshots your WeChat window — no manual capture needed.

---

## Workflow

```
Step 0   Check memory for existing show config
Step 1   Collect chat log (auto-screenshot / folder / paste / upload)
Step 2   Deep mining: clean, reconstruct facts, cluster topics, web search
Step 2.7 Podcast positioning analysis (Red Ocean Warning)
Step 3   Confirm everything with user (topics, positioning, format, length, names, show type)
Step 4   Load format template
Step 5   Build the content map (guiding questions + gold quotes + reflection moments)
Step 6   Choose output format (HTML / Word / Markdown)
Step 7   Choose visual theme (HTML only)
Step 8   Generate the podcast website (HTML only) — includes Edit Mode
Step 9   Generate Word document (Word only)
Step 10  Deliver files to desktop
```

---

## Output Formats

| Format | Best for |
|--------|----------|
| Interactive HTML | Sharing, presenting, archiving — looks great in any browser, fully editable in-browser |
| Word (.docx) | Editing, printing, sending for review |
| Markdown (.md) | Notion, Obsidian, or any plain-text workflow |

---

## Podcast Formats Supported

| Format | Like | Best for |
|--------|------|----------|
| Roundtable | Radiolab | Topics with disagreement, multiple voices |
| Deep Interview | Fresh Air | One guest with a lot to share |
| Narrative Documentary | This American Life | Complete story arcs |
| Solo / Monologue | Hardcore History | One person thinking deeply |

---

## File Structure

```
chat2podcast/
├── SKILL.md                    # Main skill — the full workflow
├── references/
│   ├── podcast-formats.md      # Ira Glass methodology + format templates
│   ├── html-themes.md          # 9 visual theme definitions
│   └── animation-patterns.md  # Interactive animation code snippets
├── scripts/
│   ├── auto_screenshot.py      # Auto-scroll screenshot capture
│   └── build_podcast_html.py  # Renders script JSON → HTML website
└── evals/
    └── evals.json              # Skill evaluation test cases
```

---

## Requirements

- Any AI agent that can read `SKILL.md` instruction files
- macOS (for auto-screenshot feature)
- Python 3 (for screenshot and HTML generation scripts)
- Google Chrome (for opening HTML output)

---

## License

MIT
