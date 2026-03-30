# 播客网站交互动画模式

## 核心原则

动画要服务于内容，而不是炫技。播客网站的动画目标是：
1. **引导注意力**：让读者知道该看哪里
2. **建立节奏感**：像播客的音乐节奏一样，有起伏
3. **增强沉浸感**：让读者感觉在"听"而不是在"读"

**黄金法则**：一个精心设计的入场动画 > 十个随机的微交互。

---

## 模式 1：页面加载入场（Hero Entrance）

用于封面区域，是第一印象，必须精心设计。

### 交错淡入（Staggered Fade）
```css
/* 适用：温暖纸张、玻璃态、报纸排版 */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

.hero-title    { animation: fadeUp 0.8s ease forwards; }
.hero-subtitle { animation: fadeUp 0.8s ease 0.2s forwards; opacity: 0; }
.hero-meta     { animation: fadeUp 0.8s ease 0.4s forwards; opacity: 0; }
```

### 打字机效果（Typewriter）
```js
/* 适用：极简终端、赛博霓虹 */
function typewriter(el, text, speed = 50) {
  let i = 0;
  el.textContent = '';
  const cursor = document.createElement('span');
  cursor.className = 'cursor';
  cursor.textContent = '█';
  el.appendChild(cursor);
  
  const timer = setInterval(() => {
    if (i < text.length) {
      el.insertBefore(document.createTextNode(text[i]), cursor);
      i++;
    } else {
      clearInterval(timer);
      // 光标继续闪烁
      cursor.style.animation = 'blink 1s step-end infinite';
    }
  }, speed);
}

/* CSS */
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
```

### 音波扩散（Wave Ripple）
```css
/* 适用：深夜电台 */
@keyframes ripple {
  0%   { transform: scale(0.8); opacity: 0.8; }
  100% { transform: scale(2.5); opacity: 0; }
}

.wave-ring {
  position: absolute;
  border-radius: 50%;
  border: 2px solid var(--accent);
  animation: ripple 2s ease-out infinite;
}
.wave-ring:nth-child(2) { animation-delay: 0.5s; }
.wave-ring:nth-child(3) { animation-delay: 1s; }
```

### 胶片闪烁（Film Flicker）
```css
/* 适用：胶片复古 */
@keyframes flicker {
  0%, 100% { opacity: 1; filter: brightness(1); }
  5%        { opacity: 0.8; filter: brightness(1.2); }
  10%       { opacity: 1; filter: brightness(0.9); }
  15%       { opacity: 0.9; filter: brightness(1.1); }
  20%       { opacity: 1; filter: brightness(1); }
}

.hero-bg { animation: flicker 0.5s ease 0.3s 3; }
```

---

## 模式 2：滚动触发入场（Scroll Reveal）

章节内容进入视口时触发，是正文区最重要的动画。

### 基础 Intersection Observer
```js
/* 通用框架，所有主题都用这个 */
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
      // 一次性动画，触发后不再重置
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

### 对话卡片交错出现
```css
/* 同一章节内的卡片依次出现 */
.dialogue-card {
  opacity: 0;
  transform: translateX(-20px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.dialogue-card.revealed { opacity: 1; transform: translateX(0); }

/* 用 JS 设置延迟 */
```
```js
document.querySelectorAll('.chapter').forEach(chapter => {
  chapter.querySelectorAll('.dialogue-card').forEach((card, i) => {
    card.style.transitionDelay = `${i * 0.08}s`;
  });
});
```

### 章节标题滑入
```css
.chapter-title {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.chapter-title.revealed { opacity: 1; transform: translateY(0); }
```

---

## 模式 3：导航交互（Navigation）

### 滚动进度条
```js
/* 顶部细线进度条 */
window.addEventListener('scroll', () => {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = (scrollTop / docHeight) * 100;
  document.getElementById('progress-bar').style.width = `${progress}%`;
});
```
```css
#progress-bar {
  position: fixed;
  top: 0; left: 0;
  height: 3px;
  background: var(--accent);
  transition: width 0.1s linear;
  z-index: 1000;
  /* 可以加发光效果 */
  box-shadow: 0 0 8px var(--accent);
}
```

### 当前章节高亮导航
```js
/* 滚动时自动高亮当前章节的导航项 */
const chapters = document.querySelectorAll('.chapter');
const navLinks = document.querySelectorAll('.nav-link');

const navObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.id;
      navLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.target === id);
      });
    }
  });
}, { threshold: 0.3 });

chapters.forEach(ch => navObserver.observe(ch));
```

### 平滑滚动
```js
/* 点击导航项平滑滚动 */
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const target = document.getElementById(link.dataset.target);
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});
```

---

## 模式 4：对话卡片微交互（Card Micro-interactions）

### 悬停上浮
```css
.dialogue-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.dialogue-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}
```

### 发言人高亮（圆桌讨论专用）
```js
/* 点击发言人名字，只显示该人的发言 */
let activeFilter = null;

document.querySelectorAll('.speaker-tag').forEach(tag => {
  tag.addEventListener('click', () => {
    const speaker = tag.dataset.speaker;
    
    if (activeFilter === speaker) {
      // 取消筛选
      activeFilter = null;
      document.querySelectorAll('.dialogue-card').forEach(card => {
        card.style.opacity = '1';
        card.style.transform = '';
      });
    } else {
      activeFilter = speaker;
      document.querySelectorAll('.dialogue-card').forEach(card => {
        const isSpeaker = card.dataset.speaker === speaker;
        card.style.opacity = isSpeaker ? '1' : '0.2';
        card.style.transform = isSpeaker ? 'scale(1.01)' : 'scale(0.98)';
      });
    }
  });
});
```

### 金句复制
```js
document.querySelectorAll('.quote-card').forEach(card => {
  const copyBtn = card.querySelector('.copy-btn');
  const text = card.querySelector('.quote-text').textContent;
  
  copyBtn.addEventListener('click', async () => {
    await navigator.clipboard.writeText(text);
    copyBtn.textContent = '已复制 ✓';
    copyBtn.classList.add('copied');
    setTimeout(() => {
      copyBtn.textContent = '复制';
      copyBtn.classList.remove('copied');
    }, 2000);
  });
});
```

---

## 模式 5：特殊效果（按主题选用）

### 噪点纹理（暗黑唱片、胶片复古）
```css
/* SVG 噪点滤镜 */
.noise-overlay {
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0.04;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  background-size: 200px 200px;
}
```

### 扫描线（赛博霓虹）
```css
@keyframes scanline {
  0%   { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}

.scanline {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(transparent, rgba(0,245,255,0.1), transparent);
  animation: scanline 4s linear infinite;
  pointer-events: none;
}
```

### 光斑漂移（玻璃态）
```css
@keyframes float-blob {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33%       { transform: translate(30px, -20px) scale(1.05); }
  66%       { transform: translate(-20px, 15px) scale(0.95); }
}

.blob {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float-blob 8s ease-in-out infinite;
  pointer-events: none;
}
```

### 音波可视化（深夜电台）
```js
/* 纯 CSS 动画模拟音波，不需要真实音频 */
```
```css
.audio-wave {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 30px;
}

.wave-bar {
  width: 3px;
  background: var(--accent);
  border-radius: 2px;
  animation: wave-dance 1.2s ease-in-out infinite;
}

@keyframes wave-dance {
  0%, 100% { height: 4px; }
  50%       { height: 24px; }
}

/* 每个 bar 不同延迟，形成波浪感 */
.wave-bar:nth-child(1) { animation-delay: 0s; }
.wave-bar:nth-child(2) { animation-delay: 0.1s; }
.wave-bar:nth-child(3) { animation-delay: 0.2s; }
/* ... 以此类推 */
```

---

## 模式 6：时间轴布局（叙事纪录片专用）

```css
/* 左侧时间轴，右侧内容 */
.timeline {
  position: relative;
  padding-left: 60px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 20px; top: 0; bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, var(--accent), transparent);
}

.timeline-item {
  position: relative;
  margin-bottom: 3rem;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -48px; top: 8px;
  width: 12px; height: 12px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 0 4px var(--bg), 0 0 0 6px var(--accent);
}

/* 滚动时时间轴节点发光 */
.timeline-item.revealed::before {
  animation: node-pulse 0.5s ease forwards;
}

@keyframes node-pulse {
  0%   { transform: scale(0); opacity: 0; }
  60%  { transform: scale(1.3); }
  100% { transform: scale(1); opacity: 1; }
}
```

---

## prefers-reduced-motion 支持

**必须**在所有动画相关 CSS 末尾加上：

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* 确保内容仍然可见（不依赖动画来显示） */
  .reveal, .dialogue-card, .chapter-title {
    opacity: 1 !important;
    transform: none !important;
  }
}
```
