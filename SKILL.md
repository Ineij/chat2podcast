---
name: chat2podcast
description: "Transforms group chat logs into professional podcast scripts and generates a beautiful interactive HTML website. Accepts screenshot folders, pasted text, or uploaded images as input. Automatically extracts messages, clusters topics, selects a podcast format, enriches content with web research, and produces a single-file animated HTML podcast site. Trigger when the user says: 'turn this chat into a podcast', 'make a podcast from my group chat', 'chat2podcast', 'generate a podcast script from chat logs', or 'podcast from WeChat'. Also trigger if the user simply says 'make me a podcast' and provides chat screenshots or text."
---

# chat2podcast

A complete workflow for distilling group chat logs into a professional podcast.

**Core philosophy**: Chat logs are raw ore, not finished product. Your job is to: ① faithfully reconstruct what was actually discussed (facts first); ② search the web to give each topic broader context and depth; ③ restructure everything using professional podcast narrative techniques so it's worth listening to.

---

## Step 0: Read Memory (do this every time before anything else)

**Before taking any action, call `memory_read` to check for an existing show configuration.**

```
Call: memory_read()
Look for keywords: chat2podcast / show DNA / podcast_show
```

### Case A: Existing show config found

Show the user what was saved and ask how to proceed:

```
📻 I found your saved show configuration:

Show name: [name]
Regular hosts: [names]
Core positioning: [positioning]
Tone: [tone]
Intro template: [intro]
Outro template: [outro]

How would you like to proceed?
A. Keep this setup (recommended — maintains consistency)
B. Update specific fields (tell me what to change)
C. Start fresh (this is a new show or a one-off episode)
```

- User picks **A (keep)**: Skip the show-positioning questions in Step 3.5; use the saved config and display it in the final confirmation summary.
- User picks **B (update)**: Ask which fields to change, update them, then rewrite to memory.
- User picks **C (fresh start)**: Follow the full Step 3 flow as normal.

### Case B: No show config found

Proceed with the full workflow. Step 3 will ask about show positioning.

---

## ⚠️ Iron Rule: Talk First, Write Later

**No matter what — after reading and analyzing the chat log, you must engage in a deep interactive confirmation with the user before writing a single word of script. This step cannot be skipped.**

Forbidden behaviors:
- Starting to write the script immediately after analyzing the chat
- Outputting any script content before the user has confirmed style, length, and structure
- Substituting "I picked X style for you" for a genuine question

Required behaviors:
- Show the user your analysis results (topic list, key quotes, external context)
- Ask about podcast style preferences and target length
- Ask for each speaker's real name; if unclear, assign a random English name
- Ask whether this is an ongoing show or a one-off; ongoing shows need a name, regular hosts, and overall positioning
- Propose a specific narrative structure with reasoning, and wait for the user to confirm or revise
- Only proceed to script writing once all information is confirmed

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

### 2.3 Cluster by topic

Group messages by **topic** (not by time). Signals to look for:
- Keyword clustering (multiple people repeatedly mention the same word or concept)
- Conversational coherence (A asks, B answers, forming a thread)
- Topic-shift signals ("speaking of which", "changing the subject", "quick question")

Give each cluster a precise title, for example:
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

After presenting this, **immediately move into the Step 3 deep confirmation — do not start writing the script on your own.**

---

## Step 3: Deep User Confirmation (Iron Rule — cannot be skipped)

**This is a mandatory step.** After analyzing the chat, you must confirm all of the following with the user before writing anything. Every item. No exceptions.

### 3.1 Topic confirmation

Start by letting the user confirm the topic selection:

```
Above are the N core topics I identified from the chat.

Please tell me:
- Which topics do you want to focus on? (I'd suggest topics 1 and 2, because…)
- Is there anything important you feel I missed?
- Is there anything you'd rather not include in the podcast?
```

Wait for the user's reply. Adjust the topic list based on their feedback.

### 3.2 Podcast style and length

Once topics are confirmed, ask about style and length:

```
Great, topics confirmed! Now I need to understand the style you're going for:

🎙️ Podcast format (pick one):
A. Roundtable — multiple perspectives, great for topics with disagreement, like Radiolab
B. Deep interview — one host, one guest, great when someone has a lot to share, like Fresh Air
C. Narrative documentary — narration + fragments, great for complete story arcs, like This American Life
D. Solo / monologue — one person thinking deeply, like Hardcore History
E. Let me decide — I'll recommend the best format based on the content

⏱️ Target length:
- Short: 15–20 minutes (commute-friendly, good for focused topics)
- Standard: 25–35 minutes (most common, works for most topics)
- Deep dive: 40–50 minutes (for rich content with complex themes)

🎨 Overall vibe (optional — helps me calibrate tone):
- Casual and conversational / Serious and analytical / Warm and story-driven / Sharp and opinionated
```

Wait for the user's reply.

### 3.3 Propose a narrative structure (with reasoning)

Based on the user's chosen format and length, propose a specific three-act structure and explain why:

```
Based on your choices, here's the structure I'd recommend:

📐 Proposed structure: [structure name]

Act 1 (~X min): [specific content]
  → Why: [reason for this opening]

Act 2 (~X min): [specific content]
  → Why: [reason for this development]

Act 3 (~X min): [specific content]
  → Why: [reason for this ending]

Cold Open hook: I'm thinking of opening with "[specific opening line]"
  → Why: [reason for this hook]

Does this structure work for you? Anything you'd like to adjust?
```

Wait for confirmation or revisions. If the user wants changes, revise and confirm again.

### 3.4 Speaker name confirmation

Speaker names directly affect how real and listenable the podcast feels. **Always ask for each speaker's real name or preferred name.**

How to ask:

```
I identified the following speakers in the chat: [nickname1], [nickname2], [nickname3]…

In the podcast I'll refer to them by name — it sounds much more natural.
What name would each of them like to use? (Real name, English name, or a name you choose for them.)

If you're not sure or prefer not to share, I'll assign each of them a random English name — like Alex, Jamie, or Morgan.
```

**Handling rules:**

- User provides names → use exactly what they provide
- User says "not sure" / "whatever" / "you decide" → randomly assign from this pool, one unique name per person:
  `Alex, Jamie, Morgan, Casey, Riley, Jordan, Taylor, Quinn, Avery, Blake, Drew, Sage, River, Skyler, Reese`
- User says "keep the chat nicknames" → keep the original nicknames
- User says "anonymous" → use descriptive labels like "one guest" / "another guest"

**Host role**: If the format is roundtable or deep interview, also confirm who plays the host (can be someone from the chat, or a fictional host persona).

Also ask: Should I search the web for background material to enrich the content? (Default: yes.)

---

### 3.5 Show positioning: ongoing series vs. one-off

**This shapes the entire design of the podcast. It must be confirmed before writing begins.**

How to ask:

```
One more important question: is this podcast…

🎯 A. An ongoing show (you plan to keep making it, with a regular audience)
   → Needs a consistent show name, regular hosts, and a signature intro/outro style
   → Each episode should feel like part of the same series — listeners can recognize it

🎲 B. A one-off (just this episode, see how it goes)
   → More flexible — style can adapt to the content
   → No need to think about series consistency

If it's an ongoing show, I'll also need:
- What's the show name? (Or let me suggest a few options)
- Who are the regular hosts? (1–2 people recommended, for consistent voice)
- What's the show's core positioning? (Who is it for? What kinds of topics does it cover?)
```

**Additional rules for ongoing shows:**

If the user chooses ongoing, the script must include these fixed elements:

- **Fixed intro**: The same show introduction every episode (~15–20 seconds), building brand recognition
- **Regular hosts**: 1–2 fixed hosts throughout; guests can change but hosts don't
- **Consistent tone**: Determined by the show's positioning (casual / serious / warm / sharp) — maintained across all episodes
- **Fixed outro**: The same closing words and call to action every episode
- **Show DNA document**: At the final confirmation stage, output a "show style guide" (name, hosts, positioning, tone, intro template, outro template) for reference in future episodes

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

After writing, tell the user: "Show configuration saved. Next time you use chat2podcast, it'll load automatically — no need to set it up again."

If the user chooses one-off, skip the fixed elements and memory write. Optimize for this single episode.

---

### 3.6 All confirmed — ready to write

Once you have the user's replies to all of the above, do a final confirmation summary:

```
✅ Confirmed:

- Topics: [topic 1], [topic 2]
- Format: [format]
- Target length: [length]
- Vibe: [vibe]
- Structure: [structure name]
- Speakers: [nickname → name mappings]
- Host: [name]
- Show type: [Ongoing series / One-off]
  (Ongoing) Show name: [name] | Positioning: [positioning]
- Web research: [yes / no]

Everything's set. Starting the script now!
```

**Only proceed to Step 4 after the user explicitly confirms — "go ahead", "looks good", "yes", or equivalent.**

**For ongoing shows**: If the user chose "keep" or "update" in Step 0, call `memory_write(type="longterm")` after confirmation to update the "last updated" field to today's date.

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

## Step 5: Write the Podcast Script

Read `references/podcast-formats.md` for professional podcast structure methodology, then write according to the following principles.

### Core method: The Ira Glass approach

Ira Glass (creator of This American Life) developed the most authoritative framework for podcast storytelling:

**Two fundamental building blocks:**
1. **Anecdote**: A sequence of events unfolding in time, where each event raises a question that pulls the listener forward.
2. **Moment of Reflection**: After the story, explain why it matters — what larger truth it reveals.

**The golden rule**: Every story needs a "why does this matter" moment. Without it, the story is just a sequence of events.

### Three-act structure (applies to all formats)

```
Act 1: Setup
├── Cold Open / Hook: Open with the single most compelling line or scene
│   Not "Hi everyone, welcome to the show" — drop straight into the most gripping content
│   Example: "Last week, a musician told me his show had 20 people in the audience.
│             He said feeling invisible hurt more than losing money."
├── Context: Why are we talking about this now? Why does this topic matter?
└── Characters / perspectives: Who's speaking? What's their position?

Act 2: Confrontation
├── Core tension: What's the central conflict or question?
├── Multiple angles: Different viewpoints, experiences, data
├── Turning point: Is there a surprising discovery or unexpected perspective?
└── Deepening: Push the topic toward something broader and more profound

Act 3: Resolution
├── Moment of Reflection: What larger truth do these discussions reveal?
├── Open ending: You don't need an answer — but leave a question worth sitting with
└── Call to action: What can listeners do?
```

### Script writing conventions

**A script is a content map, not a word-for-word transcript.** For each section, write:
- What this section covers (core content)
- What material to use (which quote or story from the chat, or which data point from research)
- Approximate length (in minutes)
- Key lines or questions (1–3, not the full text)

**Format example:**

```markdown
## Act 1: Setup (~5 min)

### Cold Open (30 sec)
[Open directly with Ajie's story — no show intro]
Key line: "Last week, a friend told me his show had 20 people in the audience…"

### Context (2 min)
[Why is the independent music live scene so hard in 2024?]
Material: search data — China independent music live market size / ticket revenue
Lead-in question: "When someone loves music but music can't pay the bills — what do they do?"

### Character introductions (2 min)
[Introduce the three guests, one sentence each to establish their perspective]
- Ajie: the one who lived it — just came off a money-losing show
- Xiaoqing: the operator — focused on how community helps musicians
- Lao Wang: the thinker — looks at the structural picture

---

## Act 2: Confrontation (~20 min)

### Topic 1: The real cost of the live music struggle (8 min)
Core tension: it's not just the money — it's the psychological cost of feeling invisible
Material:
  - Ajie's 20-person show (direct quote: "feeling invisible hurts more than losing money")
  - Xiaoqing's similar experience
  - Search data: average attendance / ticket prices / costs for indie shows
Key question: "Do you think this is a marketing problem, or something deeper?"
Turning point: Lao Wang raises the structural argument — "effort can't fix this"

### Topic 2: Is community the cure? (12 min)
Core tension: community provides emotional support — but can it solve structural problems?
Material:
  - Xiaoqing: "this is a safe place" (psychological safety)
  - Ajie: concrete example of sharing recording studio resources
  - Lao Wang: "community isn't the answer, it just means we're not alone" (the disagreement)
  - Search: discussions from indie musicians about community on Reddit / forums
Deepening: push the disagreement toward a bigger question — "when the industry structure doesn't change, what can individuals do?"

---

## Act 3: Resolution (~5 min)

### Moment of Reflection (3 min)
[No answers — just a frame]
"On the surface, we talked about the live music market. But underneath, the question is:
 when you love something that can't pay your bills, how do you find balance between passion and reality?"
Close with Lao Wang's best line

### Open ending (2 min)
Question for listeners: "If you're doing something you love that doesn't pay — what's your answer?"
Call to action: share your story in the comments
```

### Format-specific requirements

**Roundtable**: The host should design "collision questions" — not questions that get everyone to agree, but questions that surface disagreement. Every topic needs at least one question where the guests genuinely diverge.

**Deep interview**: Use "funnel questioning" — broad to specific, facts to feelings, past to future. The best question is often "what were you feeling in that moment?"

**Narrative documentary**: Narration should be visual — describe a scene, don't summarize. Use present tense to create immediacy.

**Solo / monologue**: The opening must create resonance with a question or scene the listener can feel — don't lead with your thesis.

---

## Step 6: Choose Output Format

Once the script is complete, ask the user which format they want:

```
Script done! Choose your output format:

A. Interactive HTML website (recommended)
   - A beautiful podcast presentation page with animations and interactions
   - Choose from 9 visual themes (Dark Vinyl, Late Night Radio, etc.)
   - Single file — open directly in any browser

B. Word document (.docx)
   - Standard document format, easy to edit and print
   - Good for further revision or sharing for review

C. Markdown file (.md)
   - Plain text, lightweight, works with any note-taking app
   - Paste directly into Notion, Obsidian, etc.

D. All formats (HTML + Word + Markdown)
```

---

## Step 7 (HTML): Choose a Visual Theme

If the user chose HTML, enter the theme selection flow.

### How to choose

Ask the user: **"How would you like to choose the website's visual style?"**

- **A. Show me previews** (recommended) — generate 3 style previews; user picks from visuals
- **B. Pick directly** — show the theme list; user selects one

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
- Script by section (heading + content map + key lines)
- Standout quotes summary
- Outro

---

## Step 10: Deliver

**HTML output:**
1. Save the HTML file to the user's desktop: `[GroupName]_Podcast_Ep[X].html`
2. Open in Chrome: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome "file://[path]" &`
3. Clean up temp preview files: `rm -rf /tmp/podcast-preview/`
4. Tell the user: file path, theme name, and feature overview (navigation / quote copy / progress bar)

**Word output:**
1. Save to desktop: `[GroupName]_Podcast_Ep[X].docx`
2. Tell the user the file path

**Markdown output:**
1. Save to desktop: `[GroupName]_Podcast_Ep[X].md`
2. Tell the user the file path

---

## Notes

**Facts first**: The script must be faithful to what was actually discussed in the chat. Don't distort or exaggerate for the sake of a better story. If a topic was only briefly touched on, say so in the script — don't pad it into a deep discussion that never happened.

**Enrichment has limits**: Web research provides background and data — it cannot replace the real opinions from the chat. Clearly label enriched content as "from external sources" and keep it distinct from what was actually said.

**Privacy**: If the chat contains obviously private information (phone numbers, addresses, sensitive personal details), anonymize or omit it in the script.

**Speaker handling**: Nicknames can be kept, or replaced with "Guest A / B / C" — ask the user's preference.

**Length calibration**: A typical podcast episode runs 20–45 minutes. At roughly 150 words per minute: 20 min ≈ 3,000 words; 45 min ≈ 6,750 words.

**Quality checklist** — before delivering, verify:
- Is the script faithful to what was actually discussed in the chat?
- Is there a Cold Open hook?
- Is there a Moment of Reflection ("why does this matter")?
- Does the web research genuinely enrich the topic, rather than overshadow the original voices?
- Does the output format match what the user chose?

---

## Reference Files

| File | Purpose | When to read |
|------|---------|-------------|
| `references/podcast-formats.md` | Professional podcast structure methodology with detailed format templates | Step 4 — when writing the script |
| `references/html-themes.md` | Podcast website theme library with color palettes, fonts, and design characteristics | Step 6 — when selecting a visual theme |
| `references/animation-patterns.md` | Interactive animation code snippets and usage contexts | Step 7 — when generating the HTML |
| `scripts/auto_screenshot.py` | Auto-scroll screenshot capture script | Step 1 — when guiding the user to capture screenshots |
| `scripts/build_podcast_html.py` | Renders script JSON into an HTML website | Step 7 — when generating the HTML |
