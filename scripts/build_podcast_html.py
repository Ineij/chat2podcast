#!/usr/bin/env python3
"""
chat2podcast HTML Builder
=========================
将播客脚本数据渲染为完整的单文件 HTML 播客网站。

用法：
    python build_podcast_html.py <script.json> --theme dark-vinyl --output podcast.html

脚本数据格式（script.json）：
{
  "show_name": "节目名称",
  "episode": 1,
  "title": "本期主题",
  "source": "C9群 2024-03-16 至 2024-03-20",
  "hosts": ["主持人A"],
  "guests": ["嘉宾B", "嘉宾C"],
  "duration_min": 30,
  "chapters": [
    {
      "id": "chapter-1",
      "title": "第一章标题",
      "dialogues": [
        {"speaker": "主持人A", "text": "台词内容..."},
        {"speaker": "嘉宾B", "text": "回应内容..."}
      ]
    }
  ],
  "key_quotes": [
    {"speaker": "嘉宾B", "text": "这是一条金句", "context": "来自第一章讨论"}
  ],
  "outro": "片尾总结文字",
  "next_episode": "下期预告（可选）"
}

主题选项：
  dark-vinyl      暗黑唱片（音乐/艺术）
  cyber-neon      赛博霓虹（科技/游戏）
  warm-paper      温暖纸张（生活/情感）
  minimal-terminal 极简终端（技术/开发）
  film-grain      胶片复古（纪录片/历史）
  late-night-radio 深夜电台（深度访谈）
  broadsheet      报纸排版（新闻/社会）
  glassmorphism   玻璃态（科技产品）
  handmade-zine   手写杂志（独立文化）
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

# ─── 主题配置 ────────────────────────────────────────────────────────────────

THEMES = {
    "dark-vinyl": {
        "name": "暗黑唱片",
        "css_vars": """
    --bg: #0a0a0a;
    --surface: #141414;
    --accent: #e8c547;
    --accent-2: #c0392b;
    --text: #f0ece0;
    --text-muted: #6b6b6b;
    --border: #2a2a2a;
    --card-bg: #1a1a1a;
    --nav-bg: rgba(10,10,10,0.95);
""",
        "fonts": '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Mono:wght@400;500&family=Cormorant+Garamond:ital@1&display=swap" rel="stylesheet">',
        "font_heading": "'Playfair Display', serif",
        "font_body": "'DM Mono', monospace",
        "font_quote": "'Cormorant Garamond', serif",
        "hero_animation": "fadeUp",
        "extra_css": """
    .chapter-num { color: var(--accent); font-size: clamp(3rem, 8vw, 6rem); font-weight: 900; opacity: 0.15; }
    .speaker-name { text-transform: uppercase; letter-spacing: 0.15em; font-size: 0.75rem; color: var(--accent); }
    .dialogue-card { border-left: 3px solid var(--accent); }
    .quote-card { border-left: 5px solid var(--accent-2); }
    .noise-overlay { position: fixed; inset: 0; pointer-events: none; opacity: 0.03;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
      background-size: 200px; z-index: 9999; }
""",
        "extra_html_before_nav": '<div class="noise-overlay"></div>',
    },
    "cyber-neon": {
        "name": "赛博霓虹",
        "css_vars": """
    --bg: #050510;
    --surface: #0d0d1a;
    --accent: #00f5ff;
    --accent-2: #ff006e;
    --accent-3: #7b2fff;
    --text: #e0e0ff;
    --text-muted: #4a4a7a;
    --border: #1a1a3a;
    --card-bg: #0d0d20;
    --nav-bg: rgba(5,5,16,0.95);
    --glow: 0 0 20px rgba(0,245,255,0.3);
""",
        "fonts": '<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;600&family=JetBrains+Mono&display=swap" rel="stylesheet">',
        "font_heading": "'Orbitron', monospace",
        "font_body": "'Space Grotesk', sans-serif",
        "font_quote": "'JetBrains Mono', monospace",
        "hero_animation": "glitch",
        "extra_css": """
    .speaker-name::before { content: '> '; color: var(--accent); }
    .dialogue-card { border: 1px solid var(--border); box-shadow: var(--glow); }
    .dialogue-card:hover { border-color: var(--accent); box-shadow: 0 0 30px rgba(0,245,255,0.2); }
    .quote-card { border: 1px solid var(--accent-2); box-shadow: 0 0 20px rgba(255,0,110,0.2); }
    .scanline { position: fixed; top: 0; left: 0; right: 0; height: 2px;
      background: linear-gradient(transparent, rgba(0,245,255,0.08), transparent);
      animation: scanline 4s linear infinite; pointer-events: none; z-index: 9998; }
    @keyframes scanline { 0% { transform: translateY(-100%); } 100% { transform: translateY(100vh); } }
    @keyframes glitch {
      0%,100% { clip-path: inset(0 0 100% 0); transform: translateX(0); }
      10% { clip-path: inset(10% 0 80% 0); transform: translateX(-5px); }
      20% { clip-path: inset(30% 0 50% 0); transform: translateX(5px); }
      30% { clip-path: inset(50% 0 30% 0); transform: translateX(-3px); }
      40% { clip-path: inset(70% 0 10% 0); transform: translateX(3px); }
      50% { clip-path: inset(0 0 0 0); transform: translateX(0); }
    }
""",
        "extra_html_before_nav": '<div class="scanline"></div>',
    },
    "warm-paper": {
        "name": "温暖纸张",
        "css_vars": """
    --bg: #faf6f0;
    --surface: #f5ede0;
    --accent: #c0392b;
    --accent-2: #e67e22;
    --text: #2c1810;
    --text-muted: #8b6f5e;
    --border: #d4b896;
    --card-bg: #ffffff;
    --nav-bg: rgba(250,246,240,0.95);
    --shadow: rgba(44,24,16,0.08);
""",
        "fonts": '<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:wght@300;400;600&family=Caveat:wght@400;600&display=swap" rel="stylesheet">',
        "font_heading": "'Lora', serif",
        "font_body": "'Source Serif 4', serif",
        "font_quote": "'Caveat', cursive",
        "hero_animation": "fadeUp",
        "extra_css": """
    .dialogue-card { box-shadow: 0 2px 12px var(--shadow); border-radius: 4px; }
    .speaker-name { font-family: 'Caveat', cursive; font-size: 1rem; color: var(--accent); }
    .quote-card { font-family: 'Caveat', cursive; font-size: 1.3rem; background: var(--surface); }
    .chapter-divider { border: none; border-top: 2px solid var(--border); margin: 3rem 0; }
""",
        "extra_html_before_nav": "",
    },
    "minimal-terminal": {
        "name": "极简终端",
        "css_vars": """
    --bg: #1e1e1e;
    --surface: #252526;
    --accent: #4ec9b0;
    --accent-2: #dcdcaa;
    --accent-3: #569cd6;
    --text: #d4d4d4;
    --text-muted: #6a9955;
    --border: #3e3e42;
    --card-bg: #2d2d2d;
    --nav-bg: rgba(30,30,30,0.97);
""",
        "fonts": '<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&display=swap" rel="stylesheet">',
        "font_heading": "'JetBrains Mono', monospace",
        "font_body": "'JetBrains Mono', monospace",
        "font_quote": "'JetBrains Mono', monospace",
        "hero_animation": "typewriter",
        "extra_css": """
    .chapter-title::before { content: '// '; color: var(--text-muted); }
    .speaker-name::after { content: '()'; color: var(--text-muted); font-size: 0.8em; }
    .dialogue-card { border-left: 3px solid var(--accent-3); font-size: 0.9rem; }
    .quote-card { background: var(--surface); border: 1px solid var(--accent); }
    .quote-card .quote-text::before { content: '"'; color: var(--accent-2); }
    .quote-card .quote-text::after  { content: '"'; color: var(--accent-2); }
    .timestamp { color: var(--text-muted); font-size: 0.75rem; }
    .timestamp::before { content: '// '; }
""",
        "extra_html_before_nav": "",
    },
    "late-night-radio": {
        "name": "深夜电台",
        "css_vars": """
    --bg: #0f0f1a;
    --surface: #16162a;
    --accent: #ff9f43;
    --accent-2: #a29bfe;
    --text: #dfe6e9;
    --text-muted: #636e72;
    --border: #2d3436;
    --card-bg: #1a1a2e;
    --nav-bg: rgba(15,15,26,0.95);
    --warm-glow: radial-gradient(ellipse at 50% 0%, rgba(255,159,67,0.12) 0%, transparent 60%);
""",
        "fonts": '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Nunito:wght@300;400;600;700&family=Libre+Baskerville:ital@1&display=swap" rel="stylesheet">',
        "font_heading": "'Bebas Neue', sans-serif",
        "font_body": "'Nunito', sans-serif",
        "font_quote": "'Libre Baskerville', serif",
        "hero_animation": "waveRipple",
        "extra_css": """
    body::before { content: ''; position: fixed; inset: 0; background: var(--warm-glow); pointer-events: none; z-index: 0; }
    .dialogue-card { border-left: 3px solid var(--accent); }
    .speaker-name { color: var(--accent); font-weight: 700; }
    .quote-card { background: var(--accent); color: #1a1a1a; }
    .quote-card .speaker-attr { color: rgba(26,26,26,0.7); }
    .audio-wave { display: flex; align-items: center; gap: 3px; height: 24px; }
    .wave-bar { width: 3px; background: var(--accent); border-radius: 2px; animation: wave-dance 1.2s ease-in-out infinite; }
    @keyframes wave-dance { 0%,100% { height: 4px; } 50% { height: 20px; } }
""",
        "extra_html_before_nav": "",
    },
    "glassmorphism": {
        "name": "玻璃态",
        "css_vars": """
    --bg-gradient: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    --bg: #1a1a2e;
    --surface: rgba(255,255,255,0.07);
    --surface-border: rgba(255,255,255,0.15);
    --accent: #e94560;
    --accent-2: #f5a623;
    --text: #ffffff;
    --text-muted: rgba(255,255,255,0.5);
    --border: rgba(255,255,255,0.1);
    --card-bg: rgba(255,255,255,0.07);
    --nav-bg: rgba(26,26,46,0.8);
    --blur: blur(20px);
    --glass-shadow: 0 8px 32px rgba(31,38,135,0.37);
""",
        "fonts": '<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">',
        "font_heading": "'Syne', sans-serif",
        "font_body": "'DM Sans', sans-serif",
        "font_quote": "'Syne', sans-serif",
        "hero_animation": "blobFloat",
        "extra_css": """
    body { background: var(--bg-gradient); min-height: 100vh; }
    .dialogue-card { backdrop-filter: var(--blur); -webkit-backdrop-filter: var(--blur);
      border: 1px solid var(--surface-border); box-shadow: var(--glass-shadow); }
    .dialogue-card:hover { transform: translateY(-4px); box-shadow: 0 16px 48px rgba(31,38,135,0.5); }
    .quote-card { backdrop-filter: var(--blur); border: 1px solid var(--accent); }
    .blob { position: fixed; border-radius: 50%; filter: blur(80px); opacity: 0.3; pointer-events: none;
      animation: float-blob 8s ease-in-out infinite; }
    .blob-1 { width: 400px; height: 400px; background: #e94560; top: -100px; right: -100px; }
    .blob-2 { width: 300px; height: 300px; background: #0f3460; bottom: 100px; left: -50px; animation-delay: -3s; }
    @keyframes float-blob { 0%,100% { transform: translate(0,0) scale(1); } 33% { transform: translate(20px,-15px) scale(1.05); } 66% { transform: translate(-15px,10px) scale(0.95); } }
""",
        "extra_html_before_nav": '<div class="blob blob-1"></div><div class="blob blob-2"></div>',
    },
}

# 默认主题（如果指定的主题不存在）
DEFAULT_THEME = "dark-vinyl"

# ─── HTML 模板 ────────────────────────────────────────────────────────────────

def build_html(data: dict, theme_key: str) -> str:
    theme = THEMES.get(theme_key, THEMES[DEFAULT_THEME])
    
    show_name = data.get("show_name", "播客节目")
    episode = data.get("episode", 1)
    title = data.get("title", "本期主题")
    source = data.get("source", "")
    hosts = data.get("hosts", [])
    guests = data.get("guests", [])
    duration_min = data.get("duration_min", 30)
    chapters = data.get("chapters", [])
    key_quotes = data.get("key_quotes", [])
    outro = data.get("outro", "")
    next_episode = data.get("next_episode", "")
    
    all_speakers = list(set(
        [d["speaker"] for ch in chapters for d in ch.get("dialogues", [])]
    ))
    
    # 为每个发言人分配颜色
    speaker_colors = [
        "#e8c547", "#00f5ff", "#ff9f43", "#a29bfe",
        "#2ed573", "#ff4757", "#1e90ff", "#ffa502",
        "#eccc68", "#ff6b81", "#70a1ff", "#7bed9f"
    ]
    speaker_color_map = {
        sp: speaker_colors[i % len(speaker_colors)]
        for i, sp in enumerate(all_speakers)
    }
    
    # 生成导航 HTML
    nav_items = "\n".join([
        f'<a class="nav-link" data-target="chapter-{ch["id"]}" href="#chapter-{ch["id"]}">'
        f'{i+1}. {ch["title"]}</a>'
        for i, ch in enumerate(chapters)
    ])
    
    # 生成章节 HTML
    chapters_html = ""
    for i, chapter in enumerate(chapters):
        dialogues_html = ""
        for j, dlg in enumerate(chapter.get("dialogues", [])):
            speaker = dlg["speaker"]
            color = speaker_color_map.get(speaker, "#ffffff")
            dialogues_html += f"""
        <div class="dialogue-card reveal" data-speaker="{speaker}" style="--speaker-color:{color}">
          <div class="speaker-name" style="color:{color}">{speaker}</div>
          <div class="dialogue-text">{dlg['text']}</div>
        </div>"""
        
        chapters_html += f"""
    <section class="chapter" id="chapter-{chapter['id']}">
      <div class="chapter-header reveal">
        <span class="chapter-num">{str(i+1).zfill(2)}</span>
        <h2 class="chapter-title">{chapter['title']}</h2>
      </div>
      <div class="dialogues">
        {dialogues_html}
      </div>
    </section>"""
    
    # 生成金句 HTML
    quotes_html = ""
    for q in key_quotes:
        color = speaker_color_map.get(q.get("speaker", ""), "#ffffff")
        quotes_html += f"""
      <div class="quote-card reveal">
        <div class="quote-text">"{q['text']}"</div>
        <div class="quote-footer">
          <span class="speaker-attr" style="color:{color}">— {q.get('speaker', '')}</span>
          <button class="copy-btn" data-text="{q['text']}">复制</button>
        </div>
        {f'<div class="quote-context">{q["context"]}</div>' if q.get("context") else ""}
      </div>"""
    
    # 生成发言人筛选按钮
    filter_btns = ""
    for sp in all_speakers:
        color = speaker_color_map.get(sp, "#ffffff")
        filter_btns += f'<button class="filter-btn" data-speaker="{sp}" style="--c:{color}">{sp}</button>'
    
    # 生成音波装饰（深夜电台主题）
    wave_bars = "".join([
        f'<div class="wave-bar" style="animation-delay:{i*0.1:.1f}s"></div>'
        for i in range(12)
    ])
    
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{show_name} · 第{episode}期 · {title}</title>
  {theme['fonts']}
  <style>
    /* === CSS VARIABLES === */
    :root {{
      {theme['css_vars']}
      --font-heading: {theme['font_heading']};
      --font-body: {theme['font_body']};
      --font-quote: {theme['font_quote']};
      --radius: 8px;
      --max-width: 860px;
      --nav-width: 240px;
    }}

    /* === RESET === */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      line-height: 1.7;
      overflow-x: hidden;
    }}

    /* === PROGRESS BAR === */
    #progress-bar {{
      position: fixed; top: 0; left: 0;
      height: 3px; width: 0%;
      background: var(--accent);
      box-shadow: 0 0 8px var(--accent);
      transition: width 0.1s linear;
      z-index: 2000;
    }}

    /* === NAVIGATION === */
    .nav {{
      position: fixed; top: 0; left: 0; bottom: 0;
      width: var(--nav-width);
      background: var(--nav-bg);
      backdrop-filter: blur(12px);
      border-right: 1px solid var(--border);
      padding: 2rem 1.5rem;
      overflow-y: auto;
      z-index: 100;
      display: flex; flex-direction: column; gap: 0.5rem;
    }}
    .nav-show {{ font-family: var(--font-heading); font-size: 0.85rem; color: var(--accent); margin-bottom: 1rem; }}
    .nav-link {{
      display: block; padding: 0.5rem 0.75rem;
      color: var(--text-muted); text-decoration: none;
      font-size: 0.82rem; border-radius: var(--radius);
      transition: all 0.2s ease;
      border-left: 2px solid transparent;
    }}
    .nav-link:hover {{ color: var(--text); background: rgba(255,255,255,0.05); }}
    .nav-link.active {{ color: var(--accent); border-left-color: var(--accent); background: rgba(255,255,255,0.05); }}

    /* === MAIN CONTENT === */
    .main {{
      margin-left: var(--nav-width);
      max-width: calc(var(--max-width) + 4rem);
      padding: 0 2rem 6rem;
    }}

    /* === HERO === */
    .hero {{
      min-height: 80vh;
      display: flex; flex-direction: column; justify-content: center;
      padding: 6rem 0 4rem;
      border-bottom: 1px solid var(--border);
      margin-bottom: 4rem;
    }}
    .hero-episode {{ font-size: 0.8rem; color: var(--accent); letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 1rem; opacity: 0; animation: fadeUp 0.6s ease 0.1s forwards; }}
    .hero-title {{ font-family: var(--font-heading); font-size: clamp(2.5rem, 6vw, 5rem); line-height: 1.1; margin-bottom: 1.5rem; opacity: 0; animation: fadeUp 0.6s ease 0.3s forwards; }}
    .hero-meta {{ display: flex; flex-wrap: wrap; gap: 1.5rem; color: var(--text-muted); font-size: 0.85rem; opacity: 0; animation: fadeUp 0.6s ease 0.5s forwards; }}
    .hero-meta span {{ display: flex; align-items: center; gap: 0.4rem; }}
    .audio-wave {{ display: flex; align-items: center; gap: 3px; height: 20px; margin-top: 2rem; opacity: 0; animation: fadeUp 0.6s ease 0.7s forwards; }}
    .wave-bar {{ width: 3px; background: var(--accent); border-radius: 2px; animation: wave-dance 1.2s ease-in-out infinite; }}
    @keyframes wave-dance {{ 0%,100% {{ height: 4px; }} 50% {{ height: 18px; }} }}

    /* === SPEAKER FILTERS === */
    .speaker-filters {{
      display: flex; flex-wrap: wrap; gap: 0.5rem;
      margin-bottom: 2rem; padding: 1.5rem;
      background: var(--card-bg); border-radius: var(--radius);
      border: 1px solid var(--border);
    }}
    .filter-label {{ width: 100%; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem; }}
    .filter-btn {{
      padding: 0.3rem 0.8rem; border-radius: 20px;
      border: 1px solid var(--c, var(--accent));
      background: transparent; color: var(--c, var(--accent));
      cursor: pointer; font-size: 0.8rem; font-family: var(--font-body);
      transition: all 0.2s ease;
    }}
    .filter-btn:hover, .filter-btn.active {{ background: var(--c, var(--accent)); color: var(--bg); }}

    /* === CHAPTERS === */
    .chapter {{ margin-bottom: 5rem; }}
    .chapter-header {{ display: flex; align-items: baseline; gap: 1rem; margin-bottom: 2rem; }}
    .chapter-num {{ font-family: var(--font-heading); font-size: clamp(2rem, 5vw, 4rem); color: var(--accent); opacity: 0.2; line-height: 1; }}
    .chapter-title {{ font-family: var(--font-heading); font-size: clamp(1.3rem, 3vw, 2rem); }}
    .dialogues {{ display: flex; flex-direction: column; gap: 1.25rem; }}

    /* === DIALOGUE CARDS === */
    .dialogue-card {{
      background: var(--card-bg);
      border-radius: var(--radius);
      padding: 1.25rem 1.5rem;
      border: 1px solid var(--border);
      transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.3s ease;
    }}
    .dialogue-card:hover {{ transform: translateY(-2px); }}
    .speaker-name {{ font-size: 0.78rem; font-weight: 600; margin-bottom: 0.5rem; letter-spacing: 0.05em; }}
    .dialogue-text {{ font-size: 0.95rem; line-height: 1.8; }}

    /* === KEY QUOTES === */
    .quotes-section {{ margin: 5rem 0; }}
    .quotes-section h2 {{ font-family: var(--font-heading); font-size: clamp(1.5rem, 3vw, 2.2rem); margin-bottom: 2rem; color: var(--accent); }}
    .quotes-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }}
    .quote-card {{
      background: var(--card-bg); border-radius: var(--radius);
      padding: 1.5rem; border: 1px solid var(--border);
      transition: transform 0.2s ease;
    }}
    .quote-card:hover {{ transform: translateY(-3px); }}
    .quote-text {{ font-family: var(--font-quote); font-size: 1.05rem; line-height: 1.7; margin-bottom: 1rem; }}
    .quote-footer {{ display: flex; justify-content: space-between; align-items: center; }}
    .speaker-attr {{ font-size: 0.8rem; }}
    .quote-context {{ font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem; }}
    .copy-btn {{
      padding: 0.25rem 0.6rem; border-radius: 4px;
      border: 1px solid var(--border); background: transparent;
      color: var(--text-muted); cursor: pointer; font-size: 0.75rem;
      font-family: var(--font-body); transition: all 0.2s ease;
    }}
    .copy-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
    .copy-btn.copied {{ border-color: #2ed573; color: #2ed573; }}

    /* === OUTRO === */
    .outro-section {{
      margin: 5rem 0;
      padding: 2.5rem;
      background: var(--card-bg);
      border-radius: var(--radius);
      border: 1px solid var(--border);
    }}
    .outro-section h2 {{ font-family: var(--font-heading); font-size: 1.3rem; color: var(--accent); margin-bottom: 1rem; }}
    .next-episode {{ margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border); color: var(--text-muted); font-size: 0.9rem; }}
    .next-episode strong {{ color: var(--accent-2); }}

    /* === SCROLL REVEAL === */
    .reveal {{
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 0.5s ease, transform 0.5s ease;
    }}
    .reveal.revealed {{ opacity: 1; transform: translateY(0); }}

    /* === RESPONSIVE === */
    @media (max-width: 768px) {{
      .nav {{ display: none; }}
      .main {{ margin-left: 0; padding: 0 1rem 4rem; }}
      .hero {{ min-height: 60vh; padding: 4rem 0 3rem; }}
      .quotes-grid {{ grid-template-columns: 1fr; }}
    }}

    /* === REDUCED MOTION === */
    @media (prefers-reduced-motion: reduce) {{
      *, *::before, *::after {{ animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }}
      .reveal, .hero-episode, .hero-title, .hero-meta, .audio-wave {{ opacity: 1 !important; transform: none !important; }}
    }}

    /* === THEME-SPECIFIC === */
    {theme.get('extra_css', '')}

    /* === ANIMATIONS === */
    @keyframes fadeUp {{
      from {{ opacity: 0; transform: translateY(24px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
</head>
<body>
  {theme.get('extra_html_before_nav', '')}

  <!-- Progress Bar -->
  <div id="progress-bar"></div>

  <!-- Navigation -->
  <nav class="nav">
    <div class="nav-show">{show_name}</div>
    {nav_items}
  </nav>

  <!-- Main Content -->
  <main class="main">

    <!-- Hero -->
    <header class="hero">
      <div class="hero-episode">第 {episode} 期</div>
      <h1 class="hero-title">{title}</h1>
      <div class="hero-meta">
        {''.join([f'<span>🎙 {h}</span>' for h in hosts])}
        {''.join([f'<span>👤 {g}</span>' for g in guests])}
        <span>⏱ 约 {duration_min} 分钟</span>
        {f'<span>📅 {source}</span>' if source else ''}
      </div>
      <div class="audio-wave">{wave_bars}</div>
    </header>

    <!-- Speaker Filters (only if multiple speakers) -->
    {f'''<div class="speaker-filters">
      <div class="filter-label">按发言人筛选</div>
      {filter_btns}
    </div>''' if len(all_speakers) > 1 else ''}

    <!-- Chapters -->
    {chapters_html}

    <!-- Key Quotes -->
    {f'''<section class="quotes-section">
      <h2>本期金句</h2>
      <div class="quotes-grid">{quotes_html}</div>
    </section>''' if key_quotes else ''}

    <!-- Outro -->
    <section class="outro-section reveal">
      <h2>本期小结</h2>
      <p>{outro}</p>
      {f'<div class="next-episode"><strong>下期预告：</strong>{next_episode}</div>' if next_episode else ''}
    </section>

  </main>

  <script>
    // === PROGRESS BAR ===
    const progressBar = document.getElementById('progress-bar');
    window.addEventListener('scroll', () => {{
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      progressBar.style.width = `${{(scrollTop / docHeight * 100).toFixed(1)}}%`;
    }});

    // === SCROLL REVEAL ===
    const revealObserver = new IntersectionObserver((entries) => {{
      entries.forEach(entry => {{
        if (entry.isIntersecting) {{
          entry.target.classList.add('revealed');
          revealObserver.unobserve(entry.target);
        }}
      }});
    }}, {{ threshold: 0.1, rootMargin: '0px 0px -40px 0px' }});

    document.querySelectorAll('.reveal').forEach((el, i) => {{
      // 同一父容器内的卡片交错出现
      const siblings = el.parentElement.querySelectorAll('.reveal');
      const idx = Array.from(siblings).indexOf(el);
      el.style.transitionDelay = `${{idx * 0.06}}s`;
      revealObserver.observe(el);
    }});

    // === ACTIVE NAV ===
    const chapters = document.querySelectorAll('.chapter');
    const navLinks = document.querySelectorAll('.nav-link');
    const navObserver = new IntersectionObserver((entries) => {{
      entries.forEach(entry => {{
        if (entry.isIntersecting) {{
          const id = entry.target.id;
          navLinks.forEach(link => {{
            link.classList.toggle('active', link.dataset.target === id);
          }});
        }}
      }});
    }}, {{ threshold: 0.3 }});
    chapters.forEach(ch => navObserver.observe(ch));

    // === SMOOTH SCROLL ===
    navLinks.forEach(link => {{
      link.addEventListener('click', e => {{
        e.preventDefault();
        const target = document.getElementById(link.dataset.target);
        if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }});
    }});

    // === SPEAKER FILTER ===
    let activeFilter = null;
    document.querySelectorAll('.filter-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const speaker = btn.dataset.speaker;
        if (activeFilter === speaker) {{
          activeFilter = null;
          document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
          document.querySelectorAll('.dialogue-card').forEach(card => {{
            card.style.opacity = '1';
            card.style.transform = '';
          }});
        }} else {{
          activeFilter = speaker;
          document.querySelectorAll('.filter-btn').forEach(b => b.classList.toggle('active', b.dataset.speaker === speaker));
          document.querySelectorAll('.dialogue-card').forEach(card => {{
            const match = card.dataset.speaker === speaker;
            card.style.opacity = match ? '1' : '0.15';
            card.style.transform = match ? 'scale(1.01)' : 'scale(0.98)';
          }});
        }}
      }});
    }});

    // === COPY QUOTES ===
    document.querySelectorAll('.copy-btn').forEach(btn => {{
      btn.addEventListener('click', async () => {{
        const text = btn.dataset.text;
        try {{
          await navigator.clipboard.writeText(text);
          btn.textContent = '已复制 ✓';
          btn.classList.add('copied');
          setTimeout(() => {{ btn.textContent = '复制'; btn.classList.remove('copied'); }}, 2000);
        }} catch(e) {{
          btn.textContent = '复制失败';
        }}
      }});
    }});
  </script>
</body>
</html>"""


# ─── CLI 入口 ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="将播客脚本 JSON 渲染为 HTML 网站")
    parser.add_argument("input", help="脚本 JSON 文件路径")
    parser.add_argument("--theme", default="dark-vinyl", choices=list(THEMES.keys()), help="视觉主题")
    parser.add_argument("--output", help="输出 HTML 文件路径（默认：同目录下同名 .html）")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误：找不到文件 {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    html = build_html(data, args.theme)

    output_path = Path(args.output) if args.output else input_path.with_suffix(".html")
    output_path.write_text(html, encoding="utf-8")
    print(f"✅ 已生成：{output_path}")
    print(f"   主题：{THEMES[args.theme]['name']}")
    print(f"   大小：{len(html) // 1024} KB")


if __name__ == "__main__":
    main()
