---
name: chat2podcast
description: Transform WeChat group chat logs into professional podcast scripts and generate beautiful interactive HTML websites. Supports screenshot folder paths, pasted text logs, or uploaded screenshot images as input. Automatically extracts text, clusters topics, selects podcast format, enriches content, lets users choose a visual style, and outputs a single-file animated HTML podcast site. Trigger when users mention "turn chat into podcast", "chat2podcast", "generate podcast from group chat", "WeChat chat podcast", or "make a podcast from group messages". Also trigger when a user simply says "make me a podcast" and provides chat screenshots or text.
---

# chat2podcast

A complete workflow for distilling WeChat group chat logs into professional podcast scripts.

**Core Philosophy**: Chat logs are raw ore, not finished product. Your job is: ① faithfully reconstruct what was actually discussed (facts first); ② use web search to add broader context and depth; ③ reorganize everything with professional podcast narrative structure so it's worth being heard.

---

## Step 0: Read Memory (Required on Every Launch)

**Before doing anything else, call `memory_read` to check for an existing show configuration.**

```
Call: memory_read()
Search for: chat2podcast / show DNA / podcast_show
```

### Case A: Existing Show Config Found

Show the user their saved configuration and ask how to proceed:

```
📻 I found your previous show configuration:

Show Name: [name]
Fixed Host(s): [name(s)]
Core Positioning: [positioning]
Tone: [tone]
Fixed Intro: [intro template]
Fixed Outro: [outro template]

What would you like to do this time?
A. Keep this setup (recommended — maintains show consistency)
B. Update some settings (tell me what to change)
C. Start fresh (new show or one-off episode)
```

- User picks **A (Keep)**: Skip section 3.5 in Step 3, use existing config, just display it in the final summary
- User picks **B (Update)**: Ask which fields to change, update them, then re-save to memory
- User picks **C (Fresh start)**: Walk through all sub-steps of Step 3 normally

### Case B: No Show Config Found

Proceed with the full workflow. Step 3 will ask about show positioning.

---

## ⚠️ Iron Rule: Always Interact Before Writing

**No matter what, after reading and analyzing the chat log, you MUST have a deep interactive conversation with the user and get explicit confirmation before writing any podcast script. This step cannot be skipped.**

Forbidden behaviors:
- Starting to write the script immediately after analyzing the chat log
- Outputting any script content before the user has confirmed style / length / structure
- Replacing genuine questions with "I chose X style for you"

Required behaviors:
- Show the user your analysis results (topic list, key quotes, external context)
- Ask about podcast style preference and target length
- Ask for each speaker's real name; if unclear, assign random English names
- Ask whether this is an ongoing show or a one-off; for ongoing shows, confirm show name, fixed host(s), and overall positioning
- Recommend a script structure with reasoning, and wait for the user to confirm or revise
- Only begin writing after all information is confirmed

---

## Step 1: Collect the Chat Log

Users may provide chat logs in the following ways. **If the user hasn't specified a method, proactively guide them to the best option.**

---

### Method A: Auto-Scroll Screenshot (Recommended — Easiest)

This is the most recommended approach. The user just opens the WeChat chat window; the script automatically takes screenshots and scrolls. No manual work needed.

**Script to guide the user:**

```
The easiest way is auto-screenshot:
1. Grant permission: System Settings → Privacy & Security → Screen Recording → enable CatPaw Desk
2. Open WeChat, go to the group chat you want to capture, scroll to the latest message
3. Tell me how long a chat history you want to capture (see the duration table below)
4. I'll run the screenshot script — you just need to keep WeChat in the foreground after the countdown
```

**Duration reference table (each screenshot captures ~8–14 messages):**

| Duration | ~Screenshots | ~Messages Covered | Best For |
|----------|-------------|-------------------|----------|
| 30 sec   | ~15         | 120–210           | Last 1–2 days |
| 60 sec   | ~30         | 240–420           | Last 3–5 days |
| 120 sec  | ~60         | 480–840           | Last 1–2 weeks |
| 300 sec  | ~150        | 1,200–2,100       | Last month |

**Run the screenshot script:**

```bash
# Basic usage (120 seconds, recommended)
python3 ~/.catpaw/skills/chat2podcast/scripts/auto_screenshot.py --duration 120

# Custom duration and save location
python3 ~/.catpaw/skills/chat2podcast/scripts/auto_screenshot.py \
  --duration 60 \
  --output ~/Desktop/my_screenshots

# Manual scroll mode (no auto Page Up — you scroll yourself)
python3 ~/.catpaw/skills/chat2podcast/scripts/auto_screenshot.py \
  --duration 120 --no-scroll
```

The script outputs the screenshot folder path — just share that path with me.

**Permission issues:** If screenshots fail, guide the user to: System Settings → Privacy & Security → Screen Recording → find CatPaw Desk → enable it.

---

### Method B: Manual Screenshot Folder

The user already has screenshots and provides a folder path (e.g. `~/Desktop/wechat_screenshots/`).

Use the vision model to read each image in order, extracting chat content. Sort by filename to ensure correct chronological order.

```python
import os, glob
images = sorted(
    glob.glob(os.path.join(folder_path, "*.png")) +
    glob.glob(os.path.join(folder_path, "*.jpg"))
)
# For each image: extract speaker nickname, message content, timestamp (if visible)
```

---

### Method C: Paste Text Chat Log

The user pastes an exported text log directly. Skip the screenshot step and go straight to Step 2.

---

### Method D: Upload Screenshot Images in Chat

The user sends images directly. Run vision recognition on each image to extract content.

---

### After Extraction

Organize all content into a unified format:
```
[time] Speaker: content
[time] Speaker: content
...
```

Tell the user: "Extracted XX valid messages spanning [date range]. Starting content analysis."

---

## Step 2: Deep Mining of the Chat Log

This is the most critical step in the entire workflow. **Facts first. Search broadly. Understand deeply.**

### 2.1 Clean

Remove: system messages ("xxx joined the group"), retracted messages, pure emoji reactions, voice message placeholders ("[Voice]"), and content-free filler like "haha" / "ok" / "got it".

Keep: messages with opinions, personal stories, debates, or substantive information.

### 2.2 Fact Reconstruction (Most Important)

**Read through the chat log line by line and faithfully record what actually happened.** No guessing, no embellishing, no skipping details.

For each topic, extract:
- **Core facts**: What exactly was said? Who said it? Any specific numbers, cases, or personal experiences?
- **Real opinions**: What is each person's position? Are there disagreements?
- **Emotional temperature**: Was the discussion light or heated? Were there moments of resonance or controversy?
- **Unfinished threads**: Were any topics cut off, left without a conclusion, or left hanging?

**Wrong extraction:**
> The group discussed the struggles of the live music market.

**Right extraction:**
> Alex shared that only 20 people showed up to his show last week, saying "feeling invisible hurts more than losing money." Jamie added that converting online traffic is hard. Morgan argued it's a structural problem that effort alone can't fix. The three disagreed on whether community can solve this — Jamie felt community provides psychological safety, while Morgan said "community isn't the answer, it just means we're not alone."

### 2.3 Topic Clustering

Group messages by **topic** (not by time). Identify clusters by:
- Keyword density (multiple people repeatedly mentioning the same word/concept)
- Conversational continuity (A asks, B answers, forming a thread)
- Topic-shift signals ("speaking of which", "changing the subject", "by the way")

Give each cluster a precise title, e.g.:
- "Live Shows: The Real Cost and Psychological Toll of a 20-Person Crowd" (not "Live Music Struggles")
- "Community Value: Psychological Safety vs. Structural Problems" (not "Community Discussion")

### 2.4 Broad Search (Web Enrichment)

**For every valuable topic, proactively search for relevant background information.** Don't wait for the user to ask — this is default behavior.

Search strategy:
- Use `web_search` to find industry data, social phenomena, and others' experiences related to the topic
- Search Reddit, Twitter/X, Substack, and relevant forums for broader resonance
- Search for related news, research reports, and expert opinions

**Search examples:**
```
web_search("independent music live shows 2024 market data attendance")
web_search("indie musician losing money on shows personal experience reddit")
web_search("music community mutual support independent artists")
```

Use search results to:
- Back up opinions from the chat with data ("This phenomenon affects XX% of independent musicians")
- Surface important context that wasn't mentioned in the chat
- Find the larger social context so the topic isn't just "what this group talked about"

### 2.5 Filter for Podcast Value

Not every topic is worth podcasting. Prioritize:
- Topics with real stories and specific details (not vague generalities)
- Topics with clashing viewpoints or disagreements (not unanimous agreement)
- Topics with emotional resonance (listeners will say "I feel that too")
- Topics with meaning beyond the group chat itself

Exclude: purely logistical announcements, content-free small talk, private information.

### 2.6 Show Analysis Results to User

Before moving on, show the user your analysis:

```
📊 Chat Log Analysis Complete

Extracted XX valid messages. Identified N core topics:

1. "[Precise Topic Title]"
   Core content: [2–3 sentences faithfully describing what was actually discussed]
   Key quote: [1–2 most representative original lines]
   External context: [relevant data/phenomenon found via search]
   Podcast potential: ⭐⭐⭐⭐⭐

2. "[Precise Topic Title]"
   ...
```

After displaying, **immediately move to Step 3's deep interactive confirmation — do not start writing the script on your own.**

---

## Step 3: User Confirmation (Iron Rule — Cannot Be Skipped)

**This is a mandatory step.** After analyzing the chat log, you must confirm all of the following with the user before writing any script.

### 3.1 Topic Confirmation

First, let the user confirm the topic selection:

```
Above are the N core topics I identified from the chat log.

Please tell me:
- Which topics do you want to focus on? (I suggest topics 1 and 2, because…)
- Is there anything important I missed?
- Are there any topics you don't want in the podcast?
```

Wait for the user's reply and adjust the topic list based on their feedback.

### 3.2 Podcast Style and Length

After topics are confirmed, ask about style and length:

```
Great, topics confirmed! Now I need to understand the style you're going for:

🎙️ Podcast Format (pick one):
A. Roundtable — multiple perspectives, great for topics with disagreement (like Radiolab)
B. Deep Interview — one host, one guest, great when someone has a lot to share (like Fresh Air)
C. Narrative Documentary — narration + clips, great for a complete story arc (like This American Life)
D. Solo / Personal Podcast — one person thinking deeply (like Hardcore History)
E. Let me decide — I'll recommend the best format based on the content

⏱️ Target Length:
- Short: 15–20 min (commute-friendly, bite-sized)
- Standard: 25–35 min (most common, works for most topics)
- Deep dive: 40–50 min (for rich content with complex topics)

🎨 Overall Vibe (optional — helps me calibrate tone):
- Casual & conversational / Serious & analytical / Warm & storytelling / Sharp & opinionated
```

Wait for the user's reply.

### 3.3 Recommended Structure (Must Include Reasoning)

Based on the user's chosen format and length, recommend a specific three-act structure with reasoning:

```
Based on your choices, here's the structure I recommend:

📐 Proposed Structure: [Structure Name]

Act 1 (~X min): [specific content]
  → Why: [reason for this opening]

Act 2 (~X min): [specific content]
  → Why: [reason for this development]

Act 3 (~X min): [specific content]
  → Why: [reason for this ending]

Cold Open hook: I'm thinking of opening with "[specific opening line]"
  → Why: [reason for choosing this hook]

What do you think of this structure? Anything you'd like to adjust?
```

Wait for the user to confirm or revise. If they have changes, update the structure and confirm again.

### 3.4 Speaker Name Confirmation

Speaker names directly affect how natural and authentic the podcast feels. **You must proactively ask for each speaker's real name or preferred name.**

Script:

```
I identified the following speakers in the chat log: [nickname1], [nickname2], [nickname3]…

In the podcast, I'll refer to them by name — it sounds much more natural.
What name would you like to use for each of them? (Can be their real name, English name, or any name you choose.)

If you're not sure or prefer not to share, I'll randomly assign each of them a unique English name — like Alex, Jamie, or Morgan.
```

**Handling rules:**

- User provides names → use exactly what they provide
- User says "not sure" / "up to you" / "random" → randomly assign from this name pool, one unique name per person:
  `Alex, Jamie, Morgan, Casey, Riley, Jordan, Taylor, Quinn, Avery, Blake, Drew, Sage, River, Skyler, Reese`
- User says "keep nicknames" → keep original chat nicknames
- User says "anonymous" → use descriptive labels like "one guest" / "another guest"

**Host role**: If the format is roundtable or interview, also confirm who plays the host (can be someone from the chat, or a fictional host persona).

Also ask: Should I search the web for background material to enrich the content? (Default: yes)

---

### 3.5 Show Positioning: Ongoing Show vs. One-Off

**This is a critical question that shapes the entire podcast design. It must be confirmed before writing begins.**

Script:

```
One more important question — is this podcast…

🎯 A. An ongoing show (you plan to keep making it, with a regular audience)
   → Needs a consistent show name, fixed host(s), and a consistent intro/outro style
   → Each episode should feel like part of the same show — listeners recognize it

🎲 B. A one-off (just this episode, trying it out)
   → More flexible — style can adapt to the content
   → No need to think about series consistency

If it's an ongoing show, I also need to know:
- What's the show name? (Or let me suggest a few options)
- Who are the fixed host(s)? (1–2 recommended for vocal consistency)
- What's the core positioning? (Who is the audience? What kinds of topics does it cover?)
```

**Extra rules for ongoing shows:**

If the user chooses an ongoing show, the script must include these fixed elements:

- **Fixed intro**: Same show introduction every episode (~15–20 seconds), builds brand recognition
- **Fixed host(s)**: 1–2 fixed hosts throughout; guests can change but hosts stay consistent
- **Unified tone**: Tone is set based on show positioning (casual / serious / warm / sharp) and stays consistent across all episodes
- **Fixed outro**: Same closing words and call-to-action every episode
- **Show DNA doc**: At the final confirmation step, output a "Show Style Guide" (show name, host(s), positioning, tone, intro template, outro template) for reference in future episodes

**After collecting all ongoing show information, immediately write to longterm memory:**

```
Call: memory_write(type="longterm")

Content format:
## chat2podcast Show Config

- Show Name: [name]
- Fixed Host(s): [name1], [name2 (if applicable)]
- Core Positioning: [target audience] + [topic type]
- Tone: [casual / serious / warm / sharp]
- Fixed Intro: [full intro text]
- Fixed Outro: [full outro text]
- Created: [current date]
- Last Updated: [current date]
```

After saving, tell the user: "Show config saved. Next time you use chat2podcast, it'll load automatically — no need to set it up again."

If the user chooses a one-off, skip the fixed elements and memory write. Treat it as a standalone episode.

---

### 3.6 Final Confirmation — Ready to Write

After receiving the user's replies to all of the above, do a summary confirmation:

```
✅ Confirmed Settings:

- Focus topics: [topic 1], [topic 2]
- Format: [format]
- Target length: [length]
- Overall vibe: [vibe]
- Structure: [structure name]
- Speaker names: [nickname → name mapping]
- Host: [name]
- Show type: [Ongoing show / One-off]
  (Ongoing) Show name: [name] | Positioning: [positioning]
- Web search: [yes / no]

Everything's set — I'm starting the script now!
```

**Only proceed to Step 4 after the user explicitly confirms with something like "go ahead" / "looks good" / "start".**

**Ongoing show extra action**: If this is an ongoing show and the user chose "Keep" or "Update" in Step 0, call `memory_write(type="longterm")` after confirmation to update the "Last Used" field to today's date.

---

## Step 4: Select Podcast Format (Internal Reference — Already Confirmed in Step 3)

The format was confirmed with the user in Step 3. This step is for internal reference — use it to load the corresponding format template.

```
Format mapping:
A. Roundtable → roundtable format
B. Deep Interview → interview format
C. Narrative Documentary → narrative format
D. Solo → monologue format
E. Auto-select → determine based on number of topics and content characteristics
```

---

## Step 5: Write the Podcast Script

Read `references/podcast-formats.md` for professional podcast structure methodology, then write according to the following principles.

### Core Principle: The Ira Glass Method

Ira Glass (founder of This American Life) developed the most authoritative podcast narrative framework:

**Two fundamental building blocks:**
1. **Anecdote**: A sequence of events in chronological order, where each event raises a question that pulls the listener forward.
2. **Moment of Reflection**: After the story, explain why it matters and what larger truth it reveals.

**Golden rule:** Every story needs a "why this matters" moment. Without it, the story is just a sequence of events.

### Three-Act Structure (Universal Across All Formats)

```
Act 1: Setup
├── Cold Open / Hook: Open with the most striking line or scene
│   Not "Hi everyone, welcome to the show" — drop straight into the most compelling content
│   Example: "Last week, a friend told me his show had 20 people in the audience.
│             He said feeling invisible hurt more than losing money."
├── Context: Why are we talking about this now? Why does this topic matter?
└── Character / Perspective Intro: Who's speaking? What are their positions?

Act 2: Confrontation
├── Core tension: What is the central conflict or question?
├── Multiple angles: Different perspectives, experiences, data
├── Turning point: Is there a surprising discovery or unexpected viewpoint?
└── Deepening: Push the topic toward a deeper, broader dimension

Act 3: Resolution
├── Moment of reflection: What larger truth do these discussions reveal?
├── Open ending: Doesn't need an answer, but needs a question worth sitting with
└── Call to action: What can listeners do?
```

### Script Writing Standards

**A script is a content map, not a word-for-word transcript.** For each section, write:
- What to cover (core content)
- What material to use (which opinion/story from the chat, or which data from search)
- Approximate length (in minutes)
- Key lines or questions (1–3 sentences, not the full text)

**Format example:**

```markdown
## Act 1: Setup (~5 min)

### Cold Open (30 sec)
[Open directly with Alex's story — no show intro]
Key line: "Last week, a friend told me his show had 20 people in the audience…"

### Context (2 min)
[Why is the indie live music market especially hard in 2024?]
Material: Search data — indie music market size / box office figures
Core question: "When someone loves music but music can't pay the bills — what do they do?"

### Character Intro (2 min)
[Introduce today's three voices, one sentence each]
- Alex: firsthand experience, just came off a money-losing show
- Jamie: operations perspective, focused on how community helps musicians
- Morgan: structural thinker, sees the problem from a systemic angle

---

## Act 2: Confrontation (~20 min)

### Topic 1: The Real Struggle of Live Shows (8 min)
Core tension: It's not just losing money — it's the psychological cost of feeling invisible
Material:
  - Alex's 20-person show (direct quote: "feeling invisible hurts more than losing money")
  - Jamie's similar experience
  - Search data: average attendance / ticket prices / costs for indie shows
Key question: "Do you think this is a marketing problem, or something deeper?"
Turning point: Morgan raises the structural argument — "This isn't something effort can fix"

### Topic 2: Is Community the Answer? (12 min)
Core tension: Community provides emotional support — but can it fix structural problems?
Material:
  - Jamie: "This is a safe place" (psychological safety)
  - Alex: concrete example of sharing studio resources
  - Morgan: "Community isn't the answer, it just means we're not alone" (the disagreement)
  - Search: Reddit/forum discussions on indie musicians and community
Deepening: Push the disagreement toward a bigger question — "When the industry structure doesn't change, what can individuals do?"

---

## Act 3: Resolution (~5 min)

### Moment of Reflection (3 min)
[No answers — just a framework]
"On the surface, we talked about live shows. But underneath, the question is:
 When the thing you love can't pay your bills, how do you find balance between passion and reality?"
Close with Morgan's key line

### Open Ending (2 min)
Question for listeners: "If you're doing something you love that doesn't pay — what's your answer?"
Call to action: Share your story in the comments
```

### Format-Specific Requirements

**Roundtable**: The host should design "collision questions" — not questions that get everyone to agree, but questions that surface disagreement. Every topic needs at least one question where guests take different positions.

**Deep Interview**: Use "funnel questioning" — broad to specific, facts to feelings, past to future. The best question is always "How did that feel?"

**Narrative Documentary**: Narration should be visual — describe a scene, don't summarize. Use present tense for immediacy.

**Solo**: The opening must have a question or scene the listener can relate to. Don't lead with your thesis.

---

## Step 6: Choose Output Format

After the script is complete, ask the user which output format they want:

```
Script complete! Choose your output format:

A. Interactive HTML Website (recommended)
   - Beautiful podcast showcase page with animations and interactions
   - Choose from 9 visual themes (Dark Vinyl, Late Night Radio, etc.)
   - Single file — open directly in any browser

B. Word Document (.docx)
   - Standard document format, easy to edit and print
   - Great for further editing or sharing for review

C. Markdown File (.md)
   - Plain text, lightweight, works in any note-taking app
   - Paste directly into Notion, Obsidian, etc.

D. All formats (HTML + Word + Markdown)
```

---

## Step 7 (HTML): Choose Visual Style

If the user chooses HTML, enter the style selection flow.

### Style Selection Method

Ask the user: **"How would you like to choose the website style?"**

- **A. Show me previews** (recommended) — generate 3 style previews, user picks from visuals
- **B. Pick directly** — show the style list, user selects one

### If A: Generate 3 Style Previews

Based on the podcast content's vibe, generate 3 different single-page HTML previews (each ~80–120 lines, showing cover + one quote card).

Save to `/tmp/podcast-preview/` (style-a.html, style-b.html, style-c.html), then open each in Chrome:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome "file:///tmp/podcast-preview/style-a.html" &
```

**Style selection guide** (see `references/html-themes.md` for full details):

| Content Vibe | Recommended Styles |
|-------------|-------------------|
| Music / Art / Culture | Dark Vinyl, Film Grain, Handwritten Magazine |
| Tech / Startup / Product | Minimal Terminal, Deep Space Blueprint, Glassmorphism |
| Life / Emotion / Story | Warm Paper, Late Night Radio, Film Grain |
| Society / News / Analysis | Newspaper Layout, Minimal Terminal, Late Night Radio |

Each preview must demonstrate: distinctive typography, color palette, one entrance animation, and hover effects on quote cards.

---

## Step 8 (HTML): Generate the Podcast Website

Read `references/html-themes.md` and `references/animation-patterns.md`, then generate a complete single-file HTML podcast website.

### Website Structure

```
┌─────────────────────────────────────┐
│  Hero / Cover                        │
│  Show name + episode topic + animation│
├─────────────────────────────────────┤
│  Show Info Bar                       │
│  Host / Guests / Length / Source     │
├─────────────────────────────────────┤
│  Topic Navigation (sticky sidebar    │
│  or top tabs) — click to jump        │
├─────────────────────────────────────┤
│  Main Content (scroll to read)       │
│  Each exchange as a card             │
│  Speaker avatar/label + quote bubble │
│  Section titles animate on entry     │
├─────────────────────────────────────┤
│  Key Takeaways                       │
│  3–5 highlight quotes, card layout   │
├─────────────────────────────────────┤
│  Outro                               │
│  Next episode teaser + follow CTA    │
└─────────────────────────────────────┘
```

### Required Interactive Features

**Navigation**: Fixed top or side nav; click section names for smooth scroll; current section highlights as you scroll.

**Reading experience**: Section titles trigger entrance animations via Intersection Observer; dialogue cards appear with staggered reveal; speaker cards have micro-interactions on hover.

**Quote cards**: Core takeaways have a "Copy" button; hover to expand for more context.

**Progress indicator**: Thin progress bar at the top fills as you scroll.

**Optional features** (if content fits): Speaker filter (roundtable format — click a person to see only their lines); timeline mode (narrative documentary format).

### HTML Technical Standards

- **Zero dependencies**: Single file, all CSS/JS inline, no npm or build tools required
- **Fonts**: Load from Google Fonts or Fontshare — never use Arial or system fonts
- **CSS variables**: All colors, fonts, and spacing defined with `--var`
- **Responsive**: Mobile-friendly, breakpoints at 768px / 1024px
- **Animation**: Respects `prefers-reduced-motion`
- **Code comments**: Each section has a clear `/* === SECTION === */` comment

### Design Principles (Avoiding "AI Mediocrity")

Avoid: generic purple gradients, overly uniform card grids, too many fragmented animations, choosing Inter/Roboto.

Aim for: a cover with strong visual impact; animations concentrated at key moments; distinctive typography choices; a dominant primary color.

---

## Step 9 (Word): Generate Word Document

If the user chooses Word output, use the `docx` skill to generate a properly formatted Word document.

Document structure:
- Cover page: show name, episode number, topic, date
- Table of contents
- Show info (host, guests, length, source material)
- Script sections (title + content map + key lines)
- Highlight quotes summary
- Outro

---

## Step 10: Delivery

**HTML output:**
1. Save the HTML file to the user's desktop: `[GroupName]_Podcast_Ep[X].html`
2. Open in Chrome: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome "file://[path]" &`
3. Clean up temp preview files: `rm -rf /tmp/podcast-preview/`
4. Tell the user: file path, theme name, feature overview (navigation / quote copy / progress bar)

**Word output:**
1. Save to desktop: `[GroupName]_Podcast_Ep[X].docx`
2. Tell the user the file path

**Markdown output:**
1. Save to desktop: `[GroupName]_Podcast_Ep[X].md`
2. Tell the user the file path

---

## Notes

**Facts first**: Script content must faithfully reflect what was actually discussed in the chat log. Don't distort or exaggerate for the sake of sounding good. If a topic was only briefly touched on, say so in the script — don't pad it into a deep discussion.

**Enrichment has limits**: Web search content is for providing background and data — it cannot replace the real opinions from the chat. Clearly label enriched content as "from external sources" and keep it distinct from original chat content.

**Privacy**: If the chat log contains obvious private information (phone numbers, addresses, sensitive personal situations), anonymize or skip it in the script.

**Speaker handling**: Can keep chat nicknames, or replace with "Guest A/B/C" — ask the user's preference.

**Length control**: A typical podcast episode runs 20–45 minutes. At ~150 words per minute: 20 min ≈ 3,000 words; 45 min ≈ 6,750 words.

**Quality checklist**: After finishing, verify —
- Does the script faithfully reflect the actual discussions in the chat log?
- Is there a Cold Open hook?
- Is there a "Moment of Reflection" (why this matters)?
- Does the external search content genuinely enrich the topic rather than overshadow it?
- Does the output format match what the user chose?

---

## Reference Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `references/podcast-formats.md` | Professional podcast structure methodology with detailed format templates | Step 5 — writing the script |
| `references/html-themes.md` | Podcast website theme library with color palettes, fonts, and design characteristics | Step 7 — style selection |
| `references/animation-patterns.md` | Interactive animation code snippets and usage scenarios | Step 8 — generating HTML |
| `scripts/auto_screenshot.py` | Auto-scroll screenshot script | Step 1 — guiding user to capture screenshots |
| `scripts/build_podcast_html.py` | Renders script JSON into an HTML website | Step 8 — generating HTML |
