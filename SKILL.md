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

**Mode 1 — Interactive (preferred)**: Use the `AskQuestion` tool to render interactive choice cards. The user clicks directly without typing.

**Mode 2 — Fallback (all other environments)**: If `AskQuestion` is unavailable or throws an error, immediately fall back to formatted text options. The user replies with a letter (A / B / C…) or a short answer.

### How to detect which mode to use

Try calling `AskQuestion` first. If it succeeds, use it for all subsequent STOP points in this session. If it fails or is not available, switch to fallback mode for the rest of the session. Do not retry `AskQuestion` after a failure.

### Fallback format template

When using fallback mode, always format choices like this — never ask open-ended questions without options:

```
[Brief context sentence]

Please choose (reply with a letter):
A. [Option A — short label] — [one-line description]
B. [Option B — short label] — [one-line description]
C. [Option C — short label] — [one-line description]

[If free text is also valid]: Or just tell me your thoughts directly.
```

### When free text is unavoidable

Some questions (e.g., "what's the show name?", "what are the speaker names?") can't be reduced to A/B/C. For these:
- In interactive mode: use `input_type: "mixed"` or `input_type: "text"` in `AskQuestion`
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

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "existing_config",
    "prompt": "📻 Found your saved show config:\nShow name: [name]\nHosts: [hosts]\nPositioning: [positioning]\n\nHow would you like to proceed?",
    "input_type": "choice",
    "options": [
      { "id": "keep",   "label": "A. Keep this setup (recommended)" },
      { "id": "update", "label": "B. Update specific fields" },
      { "id": "fresh",  "label": "C. Start fresh (new show or one-off)" }
    ]
  }]
}
```

**Fallback mode**:
```
📻 Found your saved show config:
Show name: [name] | Hosts: [hosts] | Positioning: [positioning]

Please choose (reply with a letter):
A. Keep this setup (recommended — maintains consistency)
B. Update specific fields (tell me what to change)
C. Start fresh (new show or one-off episode)
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
1. Grant permission first: System Settings → Privacy & Security → Screen Recording → enable the relevant app
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
python3 /path/to/chat2podcast/scripts/auto_screenshot.py --duration 120

# Custom duration and output folder
python3 /path/to/chat2podcast/scripts/auto_screenshot.py \
  --duration 60 \
  --output ~/Desktop/my_screenshots

# Manual scroll mode (no auto Page Up — you scroll yourself)
python3 /path/to/chat2podcast/scripts/auto_screenshot.py \
  --duration 120 --no-scroll
```

The script will print the output folder path when it finishes — the user just passes that path to you.

**If screenshots fail:** Guide the user to System Settings → Privacy & Security → Screen Recording → enable the relevant app.

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

### 2.4 Three-Source Enrichment Protocol (mandatory for every topic)

**Read `references/enrichment-protocol.md` now.** It defines the three required sources (social media resonance, academic research, sociology/psychology theory), search directions for each, quality standards, and the output format to use before moving to the content map.

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

**Read `references/positioning-guide.md` now.** It defines the three-step method (search the landscape, map unique assets, find the intersection), the exact output format for the positioning map, and what makes a positioning strong enough to use.

**Combined ask (topics + positioning)**

This is the single STOP point for both Step 2.6 and Step 2.7. Use the dual-mode pattern:

**Interactive mode** — call `AskQuestion` with two questions:
```json
{
  "questions": [
    {
      "id": "topics",
      "prompt": "① Topics: From the N topics above, which ones do you want to focus on? Anything to add or remove?",
      "input_type": "mixed",
      "allow_multiple": true,
      "options": [
        { "id": "t1", "label": "Topic 1: [title]" },
        { "id": "t2", "label": "Topic 2: [title]" },
        { "id": "t3", "label": "Topic 3: [title]" }
      ]
    },
    {
      "id": "positioning",
      "prompt": "② Positioning: Which direction resonates most with you?",
      "input_type": "choice",
      "options": [
        { "id": "A", "label": "A. [Positioning A — one sentence]" },
        { "id": "B", "label": "B. [Positioning B — one sentence]" },
        { "id": "C", "label": "C. [Positioning C — one sentence]" },
        { "id": "own", "label": "D. I have my own idea (tell me below)" }
      ]
    }
  ]
}
```

**Fallback mode**:
```
Two things to confirm before moving on:

① Topics: From the N topics above, which ones do you want to focus on?
(Reply with numbers, e.g. "1, 3", or tell me what to add/remove)

② Positioning: Which direction resonates most with you?
A. [Positioning A — one sentence]
B. [Positioning B — one sentence]
C. [Positioning C — one sentence]
D. I have my own idea (just tell me)
```

**STOP. Wait for the user's reply before continuing to Step 3.**

---

## Step 3: Deep User Confirmation (Iron Rule — cannot be skipped)

**This is a mandatory step.** After analyzing the chat and confirming positioning, you must confirm all of the following with the user before writing anything. Every item. No exceptions.

### 3.1 Ongoing series vs. one-off

**Ask this before format, structure, or speaker questions. The answer shapes everything that follows.**

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "show_type",
    "prompt": "Before we talk format — one thing to confirm: is this podcast…",
    "input_type": "choice",
    "options": [
      { "id": "ongoing", "label": "🎯 An ongoing series — planning to run long-term with a regular audience" },
      { "id": "oneoff",  "label": "🎲 A one-off episode — just trying it out, see how it goes" }
    ]
  }]
}
```

**Fallback mode**:
```
Before we talk format — one thing to confirm:

Please choose (reply with a letter):
A. 🎯 An ongoing series — planning to run long-term, needs a show name, regular hosts, and fixed intro/outro
B. 🎲 A one-off episode — just trying it out, style can be flexible
```

**STOP. Wait for the user's reply.**

### 3.2 Show DNA (ongoing series only)

**If ongoing**: Follow up with a second ask (interactive mode: new `AskQuestion` call; fallback: plain text questions):
```
A few more things I need to know:
- What's the show name? (Or I can suggest a few options)
- Who are the regular hosts? (1–2 recommended)
- What's the show's positioning? (Who is it for? What kinds of topics?)
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

After writing, tell the user: "Show config saved. Next time you use chat2podcast, it will load automatically — no need to set it up again."

If the user chooses one-off, skip the fixed elements and memory write.

### 3.3 Podcast style and length

**Interactive mode** — call `AskQuestion` with three questions:
```json
{
  "questions": [
    {
      "id": "format",
      "prompt": "🎙️ Which podcast format?",
      "input_type": "choice",
      "options": [
        { "id": "roundtable",  "label": "A. Roundtable — multiple perspectives clashing, great for topics with disagreement (à la Radiolab)" },
        { "id": "interview",   "label": "B. Deep interview — one host, one guest, great when someone has a lot to share (à la Fresh Air)" },
        { "id": "narrative",   "label": "C. Narrative documentary — narration + fragments, great for complete story arcs (à la This American Life)" },
        { "id": "monologue",   "label": "D. Solo / monologue — one person thinking deeply (à la Hardcore History)" },
        { "id": "auto",        "label": "E. Decide for me — recommend the best format based on the content" }
      ]
    },
    {
      "id": "length",
      "prompt": "⏱️ Target length?",
      "input_type": "choice",
      "options": [
        { "id": "short",  "label": "Short — 15–20 min (commute-friendly, focused topic)" },
        { "id": "medium", "label": "Standard — 25–35 min (most common, works for most topics)" },
        { "id": "long",   "label": "Deep dive — 40–50 min (rich content, complex themes)" }
      ]
    },
    {
      "id": "vibe",
      "prompt": "🎨 Overall vibe? (optional)",
      "input_type": "choice",
      "options": [
        { "id": "casual",     "label": "Casual chat — relaxed, conversational, like talking with friends" },
        { "id": "serious",    "label": "Serious analysis — rigorous, evidence-driven, intellectually demanding" },
        { "id": "warm",       "label": "Warm storytelling — empathetic, personal, emotionally resonant" },
        { "id": "sharp",      "label": "Sharp commentary — opinionated, punchy, doesn't pull punches" }
      ]
    }
  ]
}
```

**Fallback mode**:
```
🎙️ Podcast format (pick one):
A. Roundtable — multiple perspectives clashing, great for topics with disagreement (à la Radiolab)
B. Deep interview — one host, one guest, great when someone has a lot to share (à la Fresh Air)
C. Narrative documentary — narration + fragments, great for complete story arcs (à la This American Life)
D. Solo / monologue — one person thinking deeply (à la Hardcore History)
E. Decide for me — recommend the best format based on the content

⏱️ Target length:
- Short: 15–20 min (commute-friendly, focused topic)
- Standard: 25–35 min (most common, works for most topics)
- Deep dive: 40–50 min (rich content, complex themes)

🎨 Overall vibe (optional):
Casual chat / Serious analysis / Warm storytelling / Sharp commentary
```

**STOP. Wait for the user's reply.**

### 3.4 Propose a narrative structure (with reasoning)

Based on the user's chosen format and length, propose a specific three-act structure and explain why. Then ask for confirmation using the dual-mode pattern:

Present the structure in text first:
```
📐 Proposed structure: [structure name]

Act 1 (~X min): [specific content]
  → Why open this way: [reason]

Act 2 (~X min): [specific content]
  → Why develop this way: [reason]

Act 3 (~X min): [specific content]
  → Why close this way: [reason]

Cold Open hook: planning to open with "[specific opening line]"
  → Why: [reason]
```

Then ask:

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "structure",
    "prompt": "How does this structure feel to you?",
    "input_type": "mixed",
    "options": [
      { "id": "ok",     "label": "✅ Looks good, let's go" },
      { "id": "adjust", "label": "🔧 Needs adjustment (tell me below)" }
    ]
  }]
}
```

**Fallback mode**:
```
How does this structure feel to you?

A. ✅ Looks good, let's go
B. 🔧 Needs adjustment (tell me what to change)
```

**STOP. Wait for confirmation or revisions. If the user wants changes, revise and confirm again.**

### 3.5 Speaker name confirmation

Speaker names directly affect how real and listenable the podcast feels. **Always ask for each speaker's real name or preferred name.**

Note: if the show is ongoing (confirmed in 3.2), the fixed host(s) should already be known — just verify the names here.

For each speaker identified in the chat, ask their preferred name. This is a free-text question — use `input_type: "text"` in interactive mode, or plain text in fallback:

```
I identified the following speakers in the chat: [nickname1], [nickname2], [nickname3]…

Using real names makes the podcast feel more natural. What name should each person go by?
(Real name, English name, or I can assign one — your call)

If you're not sure, I'll randomly assign names from the pool, e.g. Alex, Jamie, Morgan.
```

**Handling rules:**

- User provides names → use exactly what they provide
- User says "not sure" / "whatever" / "you decide" → randomly assign from this pool, one unique name per person:
  `Alex, Jamie, Morgan, Casey, Riley, Jordan, Taylor, Quinn, Avery, Blake, Drew, Sage, River, Skyler, Reese`
- User says "keep the chat nicknames" → keep the original nicknames
- User says "anonymous" → use descriptive labels like "one guest" / "another guest"

**Host role**: If the format is roundtable or deep interview, confirm who plays the host (can be someone from the chat, or a fictional host persona). For ongoing shows, this should already be set from 3.2.

Also ask (interactive mode: include as a choice question; fallback: append to the same message):

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "web_research",
    "prompt": "Should I search the web to enrich the content with background context?",
    "input_type": "choice",
    "options": [
      { "id": "yes", "label": "✅ Yes, search for me (recommended)" },
      { "id": "no",  "label": "❌ No, stick to what's in the chat log" }
    ]
  }]
}
```

**Fallback mode**:
```
Should I search the web to enrich the content with background context?
A. ✅ Yes, search for me (recommended)
B. ❌ No, stick to what's in the chat log
```

**STOP. Wait for the user's reply.**

---

### 3.6 All confirmed — ready to write

Once you have the user's replies to all of the above, do a final confirmation summary, then ask for go-ahead using the dual-mode pattern:

Present the summary in text:
```
✅ Confirmed:

- Topics: [topic 1], [topic 2]
- Positioning: [chosen direction]
- Show type: [Ongoing series / One-off episode]
  (Ongoing) Show name: [name] | Positioning: [positioning]
- Format: [format]
- Target length: [length]
- Vibe: [vibe]
- Structure: [structure name]
- Speakers: [nickname → name mappings]
- Host: [name]
- Web research: [Yes / No]
```

Then ask:

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "confirm_start",
    "prompt": "Everything's set — ready to build the content map?",
    "input_type": "choice",
    "options": [
      { "id": "go",     "label": "🚀 Let's go!" },
      { "id": "adjust", "label": "✏️ I want to change something first" }
    ]
  }]
}
```

**Fallback mode**:
```
Everything's set — ready to build the content map?

A. 🚀 Let's go!
B. ✏️ I want to change something first (tell me what)
```

**STOP. Only proceed to Step 4 after the user picks "go ahead".**

**Memory write notes:**
- If this is a **new ongoing show** (set up in Step 3.2): memory was already written there — no need to write again here.
- If the user chose **"keep" or "update"** in Step 0: call `memory_write(type="longterm")` now to update the "last updated" field to today's date.
- If this is a **one-off**: no memory write needed.

---

## Step 4: Build the Content Map

**Before writing anything**: Read `references/podcast-formats.md` — it contains the format templates, benchmark show analysis, and cross-show principles that define the professional standard for this skill. Then draw the tension curve. Only then begin the content map.

### What a content map is (and is not)

**A content map is a high-density navigation guide — not a transcript, not a flow chart, not a list of topics.**

❌ Do NOT write:
- Full sentences for the hosts to say verbatim
- Filler dialogue ("that's a great point", "yeah totally", "so what you're saying is")
- Vague topic labels ("they'll discuss X")
- Anything that could be cut without losing information

✅ DO write:
- The **core dramatic tension** of each segment (one sentence, must contain a conflict or contradiction)
- **Scripted anchor lines** — the 2–3 sentences that MUST be said to land the key insight (not the whole conversation, just the load-bearing lines)
- **Guiding questions** that are designed to create collision, not consensus
- **Gold quotes** — see the Gold Quote System below
- **Information payloads** — the specific data, story, or finding from your deep-dig that gets dropped at a precise moment
- **Transition bridges** — the exact sentence that closes one segment and opens the next

### Information density standard

Professional podcasts run at 150–160 words per minute. Every minute of airtime must carry **at least one new piece of information, one emotional shift, or one perspective change**. If a minute passes without any of these, that content should be cut.

Apply this test to every segment in your content map: **"If a listener skipped this 2-minute block, what would they miss?"** If the answer is "not much," the segment needs to be compressed or cut.

**Signs of low information density (cut these):**
- Two speakers agreeing with each other at length
- Restating what was just said in different words
- Extended personal anecdotes that don't connect to the episode's core question
- Transitions that take more than 15 seconds
- Any exchange that could be summarized as "they talked about how hard X is"

**Read `references/content-map-guide.md` now.** It contains: the tension curve framework (with arc types and failure patterns), the Ira Glass anecdote + reflection method, the Gold Quote System (original vs. crafted, three-test filter, examples), the full content map format template, and format-specific writing rules for roundtable / interview / narrative / monologue.

### After completing the content map

Present the full content map — tension curve first, then the full map — then ask for feedback using the dual-mode pattern:

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "content_map_review",
    "prompt": "Content map is ready. I've included the tension curve at the top — does the arc feel right? Are the anchor lines landing? Any gold quotes to swap?",
    "input_type": "mixed",
    "options": [
      { "id": "good",   "label": "✅ Looks great, move on" },
      { "id": "adjust", "label": "✏️ A few things I'd like to adjust (tell me below)" }
    ]
  }]
}
```

**Fallback mode**:
```
Content map is ready — tension curve first, then the full map.

Key things to check:
- Does the arc feel right? (Act 1 baseline → Act 2 peak → Act 3 reframe)
- Are the scripted anchor lines the right load-bearing sentences?
- Do the gold quotes pass the test? Any to swap?
- Does the closing question land?

A. ✅ Looks great, move on
B. ✏️ A few things I'd like to adjust (tell me)
```

**STOP. Wait for the user's reply and incorporate any changes before proceeding.**

---

## Step 5: BGM Selection

Once the content map is confirmed, select background music for the episode. BGM is not decoration — it is a structural tool. Every cue must serve a specific function in the script.

**Read `references/bgm-guide.md` now.** It contains: the five cue types with duration and volume specs, professional volume rules, mood-to-genre mapping, the full cue sheet format template, and selection rules (when to use / never use BGM, track criteria).

### Search using the Netease Cloud Music API

Use the enhanced API at `https://github.com/neteasecloudmusicapienhanced/api-enhanced` to search for tracks. The API must be running locally (default port 3000) or via a deployed instance.

**Key endpoints:**

```bash
# Search for tracks by keyword + mood
GET /cloudsearch?keywords=[keyword]&type=1&limit=10
# type=1 = songs, type=1000 = playlists

# Get song detail (name, artist, album, duration)
GET /song/detail?ids=[song_id]

# Get playable URL (to verify the track is accessible)
GET /song/url?id=[song_id]

# Search a playlist by mood keyword
GET /cloudsearch?keywords=[mood keyword] 轻音乐 播客&type=1000&limit=5
```

**Search strategy — run these searches for each cue type needed:**

> Note: The keywords below are in Chinese because Netease Cloud Music's catalog and tagging system is primarily Chinese. These are search terms for the API, not content in the script.

```bash
# Intro bed — match the episode's opening emotional register
/cloudsearch?keywords=[episode mood] 轻音乐 纯音乐&type=1&limit=10

# Tension bed — for Act 2 peak
/cloudsearch?keywords=紧张 悬疑 ambient&type=1&limit=10

# Reflection bed — for closing / Moment of Reflection
/cloudsearch?keywords=治愈 温柔 钢琴&type=1&limit=10

# Transition sting — short, clean cut
/cloudsearch?keywords=过渡 转场 短片&type=1&limit=10

# Outro — warm, closing feeling
/cloudsearch?keywords=结尾 温暖 轻音乐&type=1&limit=10
```

For each cue, search → retrieve top results → check song detail → verify URL is accessible → select the best match.

**If the API is not available**, fall back to describing the track by mood/genre/texture and let the user find it manually. Do not skip the BGM plan — just note "manual search required" next to each cue.

### After completing the cue sheet

Present the full cue sheet to the user, then ask for confirmation using the dual-mode pattern:

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "bgm_review",
    "prompt": "BGM cue sheet ready — 5 tracks mapped to the episode structure. Does the mood match feel right? Any tracks to swap?",
    "input_type": "mixed",
    "options": [
      { "id": "good",   "label": "✅ Looks good, move on" },
      { "id": "adjust", "label": "🎵 Swap one or more tracks (tell me which)" },
      { "id": "skip",   "label": "⏭️ Skip BGM for this episode" }
    ]
  }]
}
```

**Fallback mode**:
```
BGM cue sheet ready — 5 tracks mapped to the episode structure.

A. ✅ Looks good, move on
B. 🎵 Swap one or more tracks (tell me which cue and what mood you want)
C. ⏭️ Skip BGM for this episode
```

**STOP. Wait for the user's reply before proceeding.**

---

## Step 6: Choose Output Format

Once the content map and BGM are confirmed, ask the user which format they want using the dual-mode pattern:

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "output_format",
    "prompt": "Content map confirmed! Choose your output format:",
    "input_type": "choice",
    "allow_multiple": false,
    "options": [
      { "id": "html", "label": "A. 🌐 Interactive HTML website (recommended) — animated, editable in-browser, single file" },
      { "id": "docx", "label": "B. 📄 Word document — easy to edit and print" },
      { "id": "md",   "label": "C. 📝 Markdown file — lightweight, paste into Notion / Obsidian" },
      { "id": "all",  "label": "D. 📦 All formats (HTML + Word + Markdown)" }
    ]
  }]
}
```

**Fallback mode**:
```
Content map confirmed! Choose your output format:

A. 🌐 Interactive HTML website (recommended)
   — Animated, editable directly in the browser, single file
B. 📄 Word document
   — Easy to edit and print, great for sharing for review
C. 📝 Markdown file
   — Lightweight, paste directly into Notion / Obsidian
D. 📦 All formats (HTML + Word + Markdown)
```

**STOP. Wait for the user's reply.**

---

## Step 7 (HTML): Choose a Visual Theme

If the user chose HTML, enter the theme selection flow.

Ask the user how they want to choose the visual style using the dual-mode pattern:

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "theme_method",
    "prompt": "How do you want to choose the visual style?",
    "input_type": "choice",
    "options": [
      { "id": "preview", "label": "A. 👀 Show me previews (recommended) — generate 3 style samples, I'll pick" },
      { "id": "direct",  "label": "B. 📋 Pick directly — show me the theme list, I'll choose myself" }
    ]
  }]
}
```

**Fallback mode**:
```
How do you want to choose the visual style?

A. 👀 Show me previews (recommended) — generate 3 style samples, I'll pick
B. 📋 Pick directly — show me the theme list, I'll choose myself
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

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "theme_pick",
    "prompt": "Three style previews generated — which one do you prefer?",
    "input_type": "choice",
    "options": [
      { "id": "A", "label": "A. Style A" },
      { "id": "B", "label": "B. Style B" },
      { "id": "C", "label": "C. Style C" }
    ]
  }]
}
```

**Fallback mode**:
```
Three style previews generated — which one do you prefer?
A. Style A
B. Style B
C. Style C
```

**STOP. Wait for the user to pick a theme before generating the full HTML.**

---

## Step 8 (HTML): Generate the Podcast Website

**Read `references/html-build-guide.md`, `references/html-themes.md`, and `references/animation-patterns.md` before writing any code.** The build guide defines the required page structure, interactive features, the full Edit Mode implementation (HTML/CSS/JS), technical requirements, and design principles.

### Generation checklist (verify before writing a single line)

- Theme selected (from Step 7) — apply its color palette, fonts, and design characteristics exactly
- Content map confirmed (from Step 4) — every section, gold quote, and anchor line must appear in the HTML
- BGM cue sheet confirmed (from Step 5) — include cue annotations as HTML comments at the relevant trigger points (e.g., `<!-- BGM CUE: Intro Bed starts here -->`)
- Edit Mode — must be fully implemented per `html-build-guide.md` Section 3 (toggle button, editable selectors, save-as-file function, edit toolbar)
- All animations from `animation-patterns.md` — use the patterns that match the chosen theme; do not invent new animation logic from scratch
- `prefers-reduced-motion` — required; include the media query block from `animation-patterns.md`
- Zero external dependencies — single file, all CSS/JS inline

### What to generate

Write the complete, self-contained HTML file. Structure it exactly as defined in `html-build-guide.md` Section 1 (Hero → Episode info bar → Topic nav → Main content → Key takeaways → Outro). Every section from the content map becomes a chapter in the HTML.

### After generating

Open the file in Chrome to verify it renders correctly:

```bash
open -a "Google Chrome" /path/to/output.html
```

Then present a brief summary to the user and ask for sign-off using the dual-mode pattern:

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "html_review",
    "prompt": "HTML generated and opened in Chrome. Does everything look right?",
    "input_type": "mixed",
    "options": [
      { "id": "good",   "label": "✅ Looks great, deliver it" },
      { "id": "adjust", "label": "🔧 Something needs fixing (tell me below)" }
    ]
  }]
}
```

**Fallback mode**:
```
HTML generated and opened in Chrome.

A. ✅ Looks great, deliver it
B. 🔧 Something needs fixing (tell me what)
```

**STOP. Wait for the user's reply before proceeding to Step 10.**

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

After generating, tell the user the file path and ask for sign-off using the dual-mode pattern:

**Interactive mode** — call `AskQuestion`:
```json
{
  "questions": [{
    "id": "docx_review",
    "prompt": "Word document generated. Does it look right?",
    "input_type": "mixed",
    "options": [
      { "id": "good",   "label": "✅ Looks good, deliver it" },
      { "id": "adjust", "label": "🔧 Something needs fixing (tell me below)" }
    ]
  }]
}
```

**Fallback mode**:
```
Word document generated — file path: [path]

A. ✅ Looks good, deliver it
B. 🔧 Something needs fixing (tell me what)
```

**STOP. Wait for the user's reply before proceeding to Step 10.**

---

## Step 10: Deliver

**HTML output:**
1. Save the HTML file to the user's desktop: `[ShowName]_Ep[X].html`
2. Open in browser to verify it renders correctly
3. Clean up temp preview files if any: `rm /tmp/podcast-preview/style-*.html` then `rmdir /tmp/podcast-preview`
4. Tell the user: file path, theme name, and feature overview (navigation / quote copy / progress bar / **edit mode**)
5. Specifically mention: "Click the ✏️ Edit button in the bottom-right corner to edit any text directly on the page. When done, click '💾 Save changes' to download the updated version."

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

**Length calibration**: A typical podcast episode runs 20–45 minutes. At roughly 150 words per minute: 20 min ≈ 3,000 words; 45 min ≈ 6,750 words. The content map should give enough material for the target length without over-scripting.

**Quality checklist** — before delivering, verify:
- Is the content map faithful to what was actually discussed in the chat?
- Is there a Cold Open hook?
- Is there a Moment of Reflection ("why does this matter") for each topic?
- Does the web research genuinely enrich the topic, rather than overshadow the original voices?
- Are the guiding questions open-ended and designed to let conversation flow naturally?
- Is there a BGM cue sheet with at least an intro bed, one transition sting, and an outro? (Unless the user skipped BGM)
- Does every BGM cue have a specific trigger point tied to the script?
- Does the HTML include a working Edit Mode toggle?
- Does the output format match what the user chose?

---

## Reference Files

| File | Purpose | When to read |
|------|---------|-------------|
| `references/enrichment-protocol.md` | Three-source enrichment protocol: social media, academic research, and theory — with search directions, quality standards, and output format | Step 2.4 — before enriching any topic |
| `references/positioning-guide.md` | Positioning analysis method: search the landscape, map unique assets, find the intersection — with output format template and quality criteria | Step 2.7 — before running the positioning analysis |
| `references/content-map-guide.md` | Tension curve framework, Ira Glass method, Gold Quote System, content map format template, and format-specific writing rules | Step 4 — before building the content map |
| `references/bgm-guide.md` | Five BGM cue types, volume rules, mood-to-genre mapping, cue sheet format template, and selection rules | Step 5 — before selecting tracks |
| `references/podcast-formats.md` | Format templates, benchmark show analysis, and cross-show principles | Step 4 — supplementary reference for format choice |
| `references/html-build-guide.md` | Page structure, required interactive features, Edit Mode full implementation (HTML/CSS/JS), technical requirements, and design principles | Step 8 — before generating the HTML |
| `references/html-themes.md` | Podcast website theme library with color palettes, fonts, and design characteristics | Step 7 — when selecting a visual theme |
| `references/animation-patterns.md` | Interactive animation code snippets and usage contexts | Step 8 — when generating the HTML |
| `scripts/auto_screenshot.py` | Auto-scroll screenshot capture script | Step 1 — when guiding the user to capture screenshots |
| `scripts/build_podcast_html.py` | Renders script JSON into an HTML website | Step 8 — when generating the HTML |

