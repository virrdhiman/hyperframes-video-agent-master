# Physical Tech Explainer (Modern Cinematic Collage)

## Core Philosophy & Mindset

The "Physical Tech Explainer" is a highly dynamic, multi-layered editing style designed for vertical short-form content (9:16). It bridges the gap between a traditional "talking head" video and high-end motion graphics tech documentaries. 

The guiding mindset is the **"Human-Editable Physical Collage"**:
- Digital elements (UI mockups, text, B-roll) should not feel flat, sterile, or natively "computer-generated." 
- They should feel tangible—like physical stickers, printed photos, or tactile hardware components placed on a tangible canvas.
- The speaker is **not** detached from the graphics. Instead of the presenter blindly pointing at empty space, the video base layer (the talking head) physically reacts to the overlays by dodging, scaling down, or shifting away to "make room" for the data.
- **Attention Retention**: No two consecutive scenes should employ the exact same visual structure. You must constantly alternate between pure talking head, full-screen B-roll, bold single-word typography, split-screens, and custom data visualizations.

---

## 1. The 4-Layer Rendering Architecture

To execute this style efficiently, the composition should be structured using a strict 4-layer stack:

### Layer 1: The Transformable Base (Talking Head & Background)
- **Continuous Playback**: The talking head video plays continuously in the background. 
- **Continuous Ken Burns**: Never leave the talking head static. Apply continuous slow zooms (`1.02` to `1.08`), horizontal drifts, and pans depending on the pacing of the scene, tweened over the scene duration on the paused GSAP timeline (e.g., `tl.to(el, { scale: 1.08, duration: <seconds>, ease: "none" }, <start>)`).
- **Physics-Based Push Downs**: When a large geometric graphic or UI element needs to be introduced, translate the Y-axis of the talking head wrapper down (e.g., `y: 600`) and scale it down (`scale: 0.85`) with a smooth ease (`power2.out`/`power3.out`). The presenter gets "pushed" out of the way smoothly to allocate screen real estate. (Animate a non-timed wrapper `<div>` around the `<video muted playsinline>` — never the video element's own dimensions.)

### Layer 2: The Action Overlay (Cards, Mockups, B-Roll)
- This layer conditionally mounts different components mapped strictly to audio timestamps.
- **Split Screens**: Often, the screen splits horizontally, with cinematic, AI-generated B-roll or hardware mockups looping on the top half.
- **Full-Screen Takeovers**: Occasionally override the talking head completely with rich, abstract tech backgrounds or high-quality cinematic shots.

### Layer 3: Context-Aware "Pill" Captions
- Subtitles are not a static SRT block. They exist over top of everything, functioning as a synchronized, dynamic UI.
- **Context-Aware Styling**: Stay brightness-aware so captions always read against whatever is behind them. Default grounds are light/neutral (warm beige paper, off-white), so inactive words use a dark translucent fill/shadow. If a given overlay happens to be darker (e.g., a mid-tone photographic B-roll shot), flip inactive words to a translucent light fill so contrast holds. Captions are handled by HyperFrames via the caption pipeline.

### Layer 4: Spatial SFX
- Audio is the glue perfectly timed to visual frames.
- **Whooshes**: Fast mid-frequency sweeps on every split-screen reveal or base-layer translate/push-down.
- **Pops**: Used for staggering the entry of individual words or list items.
- **Clicks**: Sci-fi UI clicks used specifically for data matching or hardware button presses.
- **Impacts**: Deep cinematic booms for big reveals or concluding pipeline stages.

---

## 2. Animation Principles & Physics

Avoid flat linear interpolation for spatial movement. Map the old spring "feels" onto **GSAP eases** on the paused timeline:
- **Smooth** (`power2.out` / `power3.out`): Used for base layer shifts, camera pans, and large layout changes. It feels responsive but doesn't distract.
- **Snappy** (`power4.out` / `back.out(1.4)`): Used for rapid UI property reveals or fast slide-ins.
- **Bouncy** (`back.out(1.7)` / `elastic.out`): Used sparingly for physical element drops (like a sticker hitting the canvas).

### The "Alive" Micro-Motions (Wobble & Float)
To maintain the "physical collage" aesthetic, static text or images must never be perfectly still. Drive these from the timeline with a **finite** GSAP `repeat`/`yoyo` cycle (compute `repeat: Math.ceil(duration / cycle) - 1` — never `repeat: -1`).
- **Wobble**: A continuous rotation oscillation (e.g., `rotation: ±1.5deg`, `yoyo: true`, `ease: "sine.inOut"`).
- **Float**: A continuous vertical oscillation (e.g., `y: ±5`, `yoyo: true`, `ease: "sine.inOut"`).
When combined, cards, graphics, and text feel as though they are breathing or being held by a human hand.

### Staggered Reveal
Never show a complex diagram, a sentence of text, or multiple UI cards simultaneously. Cascade element entrances with small time offsets on the timeline (e.g., `+0s: Container`, `+0.15s: Image`, `+0.3s: First Label`, `+0.45s: Arrow`), or use GSAP `stagger` on a grouped `gsap.from()`.

---

## 3. Typography & The Dynamic Word Pill

Typography relies heavily on tightly-tracked, ultra-bold sans-serif fonts (`Inter Tight`, etc.) for loud statements, paired with sharp Monospace fonts (`JetBrains Mono`) for technical parameters.

### Caption Animation Behavior:
1. **The Active Word**: The current spoken word receives a saturated accent background (e.g., Cobalt Blue or Warm Amber — not neon).
2. **Physical Transformation**: The active word slightly scales up (`1.05x`) and rotates slightly off-axis (`-1deg` or `1deg`) to break the grid and look like a highlighter physically stamped onto it.
3. **Shadow Drop**: The active word gains a heavy solid shadow, separating it from the inactive words.
4. **Inactive Words**: Remaining words stay flat, translucent, and lack a background, creating an optical tunnel vision effect guiding the viewer's eye exactly to the current audio.

---

## 4. Styling, Colors & Depth Shadows

### The "Paper-Cutout" Shadow
Do not use soft, highly-blurred digital drop shadows (`box-shadow: 0 4px 12px rgba(0,0,0,0.2)`). 
Instead, rely on **Hard, Solid Shadows**:
- `box-shadow: 6px 8px 0px rgba(0,0,0,0.15)` against the light/neutral grounds.
This anchors elements in a physical pseudo-3D space.

### Borders
Wrap floating mockup cards, images, and important text boxes in thick, high-contrast borders (e.g., `3px solid #1A1A1A`) to distinguish them from the background video layer.

### Color Palettes
Build on a light, tactile foundation with tasteful saturated (but not neon) accents:
- **Base Grounds**: Warm, tactile beige and off-whites (`#F4F0EB`, `#FAF7F2`, soft `#EDE7DD`) instead of pure sterile white. These are the default canvas.
- **Ink / Text**: Dark charcoal (`#1A1A1A`) rather than harsh pure black, for an editorial feel.
- **Accents**: Confident, saturated-but-grounded identifier colors (e.g., Cobalt Blue `#2563EB`, Warm Amber `#D97706`, Forest Green `#16A34A`, Terracotta `#C2553D`). Alternate these accent colors per scene to keep the visual identity fresh but cohesive. Avoid neon/glow saturation.

---

## 5. Pacing & Timing
- Calculate the entire video based on a global speed modifier (e.g., `1.10x` or `1.15x`). This eliminates micro-pauses in the audio without forcing the presenter to talk artificially fast during recording.
- Jump cut ruthlessly during the talking head portions, masking the cuts with full-screen graphic takeovers or B-roll. You should almost never see the presenter take a breath.
