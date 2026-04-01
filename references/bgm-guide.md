# BGM Guide

BGM is not decoration — it is a structural tool. Every cue must serve a specific function in the script. Top podcasts (Serial, This American Life, S-Town, Gushi FM) use music with surgical precision: a 4-bar intro to set the emotional register, a 2-second sting to mark a scene cut, a low bed under a key monologue to hold tension. The music is almost never noticed consciously — but its absence would be felt immediately.

Read this file before executing Step 5. It covers: the five cue types, volume rules, mood-to-genre mapping, the cue sheet format template, and selection rules.

---

## 1. The Five Cue Types

Map these to the content map before searching for tracks.

| Cue type | Function | Typical duration | Volume level |
|----------|----------|-----------------|-------------|
| **Intro bed** | Plays under the cold open; sets the emotional register before the first word | 15–30 sec, then fade out | Full → duck to -15 dB under voice |
| **Transition sting** | Marks a scene cut or act break; gives the listener a moment to reset | 3–8 sec | Full, then hard out |
| **Tension bed** | Plays under a key monologue or the Act 2 peak; holds emotional pressure | 60–120 sec loop | -15 to -18 dB under voice |
| **Reflection bed** | Plays under the Moment of Reflection or closing; softer, more open | 30–60 sec | -18 dB under voice, fade out at end |
| **Outro** | Plays under the closing words and CTA; fades to silence | 20–30 sec | Full → fade out |

---

## 2. Volume Rules (Professional Standard)

- Music under voice: **-15 to -18 dB** relative to the voice track (the listener should feel it, not hear it)
- Music alone (intro/outro/sting): full level, then fade in/out over 2–3 seconds
- Never let music compete with speech — if the listener is thinking about the music, it's too loud
- Ducking: music fades down when voice starts, fades back up in silences

---

## 3. Mood-to-Genre Mapping

Match the episode's emotional arc to the right musical texture:

| Episode mood | Recommended genres / textures |
|-------------|-------------------------------|
| Intimate / confessional | Sparse piano, fingerpicked acoustic guitar, ambient with breath |
| Intellectual / analytical | Minimal electronic, light jazz, post-rock without drums |
| Tense / investigative | Low strings, drone, dark ambient, slow-build cinematic |
| Warm / nostalgic | Lo-fi, soft indie folk, vintage jazz, gentle orchestral |
| Energetic / cultural | Upbeat indie, light hip-hop beats, world music elements |
| Melancholic / reflective | Slow piano, ambient strings, minimal electronic with space |

---

## 4. BGM Cue Sheet Format Template

After selecting tracks, output a cue sheet that maps directly onto the content map. This is what the host/editor uses during production.

```
## BGM Cue Sheet — [Episode Title]

### Cue 1 — Intro Bed
Track: [Song name] — [Artist]
Netease ID: [id] | URL: [playable link if available]
Mood match: [why this track fits the cold open]
Start: Episode begins (0:00)
Fade in: 2 sec
Duration under voice: full cold open (~30 sec)
Duck to: -15 dB when first voice line starts
Fade out: 3 sec after cold open ends

### Cue 2 — Transition Sting (Act 1 → Act 2)
Track: [Song name] — [Artist]
Netease ID: [id]
Start: immediately after Act 1 closing line
Duration: 5 sec
Out: hard cut

### Cue 3 — Tension Bed (Act 2 peak)
Track: [Song name] — [Artist]
Netease ID: [id]
Mood match: [why this track fits the peak tension moment]
Start: [specific scripted anchor line that triggers the cue]
Duration: loops for ~90 sec
Volume: -18 dB under voice
Fade out: 3 sec before Act 2 ends

### Cue 4 — Reflection Bed (Moment of Reflection)
Track: [Song name] — [Artist]
Netease ID: [id]
Start: [the line that opens the reflection beat]
Duration: through the closing reflection and open-ended question
Volume: -18 dB under voice
Fade out: 4 sec, into silence before outro

### Cue 5 — Outro
Track: [Song name] — [Artist] (can reuse Intro Bed or use a variant)
Netease ID: [id]
Start: first word of outro
Duration: full outro (~25 sec)
Fade out: last 5 sec, to silence
```

---

## 5. Selection Rules

**Always use BGM for:**
- The cold open — this is the emotional handshake with the listener
- Act transitions — gives the listener permission to reset
- The Act 2 peak tension moment — when the hardest thing gets said
- The Moment of Reflection — the emotional landing
- The outro — the closing ritual

**Never use BGM for:**
- Under rapid back-and-forth dialogue — it competes with the rhythm of conversation
- Under moments of genuine laughter or levity — music makes it feel staged
- As wallpaper throughout the entire episode — listener fatigue; music loses meaning
- Any track with lyrics — lyrics compete directly with speech

**Track selection criteria:**
- Instrumental only (no lyrics)
- No strong melodic hook that draws attention to itself
- Loops cleanly or has a long enough runtime for the cue
- Tempo matches the emotional pace of the segment (slow for reflection, slightly faster for tension)
- Accessible on Netease Cloud Music (verify with `/song/url`)
