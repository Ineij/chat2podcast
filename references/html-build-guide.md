# HTML Build Guide

This file defines the complete technical specification for generating the podcast HTML website in Step 8. It covers: page structure, required interactive features, the in-browser Edit Mode (with full code), HTML technical requirements, and design principles.

Read this file in full before writing a single line of HTML.

---

## 1. Page Structure

Every podcast website must follow this layout, top to bottom:

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

---

## 2. Required Interactive Features

**Navigation**: Fixed top or side nav; click a section name to smooth-scroll; current section highlights as you scroll.

**Reading experience**: Section headings trigger entrance animations when they enter the viewport (Intersection Observer); dialogue cards appear in a staggered reveal; speaker cards have micro-interactions on hover.

**Quote cards**: Core takeaways have a "copy" button; hover to expand for more context.

**Progress indicator**: A thin progress bar at the top fills as the user scrolls.

**Optional features** (if the content suits it):
- Speaker filter (roundtable format — click a person to see only their lines)
- Timeline mode (narrative documentary format)

---

## 3. In-Browser Edit Mode (required — every HTML output must include this)

Every generated HTML page must include a fully functional Edit Mode that lets the user modify content directly in the browser without touching any code.

### Toggle button

Place a floating button in the bottom-right corner of the page:

```html
<button id="edit-toggle" title="Toggle Edit Mode">✏️ Edit</button>
```

Style it as a pill-shaped floating action button, always visible, with a subtle shadow. When edit mode is active, change the label to "✅ Done editing" and add a visible highlight ring.

### What becomes editable

When edit mode is ON, add `contenteditable="true"` to:
- All dialogue bubble text (`.bubble` or equivalent)
- All quote card text (`.quote-text` or equivalent)
- All chapter/section titles (`.chapter-title` or equivalent)
- All reflection/context box text
- All takeaway items
- The hero title and subtitle
- The outro tagline

When edit mode is OFF, remove `contenteditable` from all elements (or set to `false`).

### Visual feedback when editable

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

### Save as new file button

When edit mode is active, show a second floating button: **"💾 Save changes"**

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
  toggleEditMode(true); // re-enable edit mode so the user can continue editing
}
```

### Edit toolbar (shown only when edit mode is active)

A slim bar at the top of the page (below the nav) with:
- A brief instruction: "Click any text to edit it directly"
- A "💾 Save changes" button (same as the floating one)
- An undo hint: "Cmd+Z to undo"

```html
<div id="edit-toolbar" style="display:none">
  <span>✏️ Edit mode on — click any text to edit it directly</span>
  <button onclick="saveEdits()">💾 Save changes</button>
  <span style="opacity:0.5">Cmd+Z to undo</span>
</div>
```

### JavaScript implementation

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
    toggleBtn.textContent = '✅ Done editing';
    toggleBtn.classList.add('active');
    if (saveBtn) saveBtn.style.display = 'block';
  } else {
    EDITABLE_SELECTORS.forEach(sel => {
      document.querySelectorAll(sel).forEach(el => {
        el.removeAttribute('contenteditable');
      });
    });
    toolbar.style.display = 'none';
    toggleBtn.textContent = '✏️ Edit';
    toggleBtn.classList.remove('active');
    if (saveBtn) saveBtn.style.display = 'none';
  }
}

document.getElementById('edit-toggle').addEventListener('click', () => toggleEditMode());
```

### UX rules for edit mode

- Edit mode is **OFF by default** — the page opens in clean reading mode
- Clicking the toggle button switches between view and edit mode
- In edit mode, the scroll-reveal animations are paused (so elements don't re-hide while editing)
- The progress bar and nav remain functional in both modes
- `Cmd+Z` / `Ctrl+Z` works natively for undo within any editable element
- The saved file opens in view mode (no edit toolbar visible) — the user must click the toggle to re-enter edit mode

---

## 4. HTML Technical Requirements

- **Zero dependencies**: Single file, all CSS/JS inline, no npm or build tools required
- **Fonts**: Load from Google Fonts or Fontshare — never use Arial or system fonts
- **CSS variables**: All colors, fonts, and spacing defined as `--var`
- **Responsive**: Mobile-friendly, breakpoints at 768px / 1024px
- **Motion**: Respect `prefers-reduced-motion`
- **Comments**: Clear `/* === SECTION === */` comments for every block

---

## 5. Design Principles (Avoiding the "AI Mediocrity" Look)

**Avoid:**
- Generic purple gradients
- Overly uniform card grids
- Too many small animations competing for attention
- Choosing Inter or Roboto as the primary typeface

**Aim for:**
- A cover with strong visual impact — the first screen should feel like a magazine cover, not a template
- Animations concentrated at key moments (section entries, quote reveals) — not sprinkled everywhere
- A typeface with personality — something that signals the show's tone before a word is read
- A dominant primary color that owns the palette — one strong color, not a rainbow
