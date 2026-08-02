# Full style — "Vaibhav style" (numbered countdown listicle)

Long-form (~90s) vertical **numbered countdown explainer** (#01→#N) on tech/AI news, warm talking-head
PiP + rotating Apple-clean content beats, single LIME accent. Decoded via the grid method from the
reference reel (facebook.com/reel/3878133782327059 · 1080×1920 · 30fps · ~89.6s · topic: Apple Siri
now runs on Google Gemini). Reproduce the SPEC — never clone frame-for-frame. Reference assets:
`~/workspace/workspace/topic_fetch/style_reel_2/` (grid_2s.png contact sheet, fr/f_*.png, STYLE_NOTES.md).

## When to use
"Top N things…" / countdown listicles that pack MANY points (8–12) into one longer reel: a news
recap, a feature roundup, "everything Apple announced," a tips list. Warm-but-premium, Apple-keynote-
adjacent. Picks up where webveda's single-number motif stops — this is the *multi-item* spine. Great
when you have a lot to say and want a persistent "where am I in the list" tracker.

## Palette → lime-on-shifting-gradient  (see elements/palettes/vaibhav-lime.md)
- **Accent (numbers ONLY):** lime/chartreuse `#C4FB00`. Nowhere else — that's what makes it pop.
- **"#" glyph:** silver-gray `#A5A5A5` (sits left of the lime number).
- **Caption:** near-white `#F9F6FA`, bold.
- **Background = soft vertical GRADIENT, re-tinted per section:** near-white top `#F2F1F4` →
  section tone at bottom (e.g. brick-red `#8D2B24`, or neutral black `#1A1A1A`). Each item can swap
  the bottom tone for variety while the top stays light.
- PiP warm interior (wood/skin) `~#563718`.

## Typography
- **Numbers:** ultra-bold grotesque display (Druk/Clash-Display/Helvetica-Black vibe), tight.
- **UI / list / labels:** Apple **SF Pro** system font (matches real iOS screenshots).
- **Hook headline (cold open):** elegant SERIF with ITALIC emphasis on the key phrase.

## Composition (1080×1920)
- **SIGNATURE lower-third module (constant on item beats):** PiP avatar BOTTOM-LEFT (rounded-rect
  ~r30, thin white/gray ~2px border, ~330px wide, warm-tinted) + giant `#NN` to its right (silver #
  + lime number) + white bold caption (2–4 lines) under the number. See
  elements/subtitles/numbered-pip-lowerthird.md.
- **UPPER ~⅔ = content zone**, rotates per item (diagram / scroll-list / phone mock / stat / white card).
- Cold open & a few accent beats go **full-bleed** (concept image, big stat). PiP avatar NEVER over
  the content's key text; content's key text stays clear of the avatar.

## Scene-by-scene skeleton (new item every ~6–8s; ~2s sub-cuts inside an item)
| # | Beat | What's on screen | Technique / element |
|---|---|---|---|
| 1 | COLD OPEN (0–7s) | AI-composited concept hero TOP (Tim→Sundar orb handoff) + serif-italic hook ("So *Apple handed it to Google*") + presenter BELOW | serif-italic-hook over concept image |
| 2 | Item #01… | lower module appears; upper = relevant beat | numbered-pip-lowerthird |
| — | VS / compare | two node-graph icons (Apple red vs Google blue) + labels | comparison-nodegraph-vs |
| — | scroll list | a long list scrolls, the ACTIVE line bold-black, rest dimmed | scrolling-highlight-list |
| — | phone mock | full-bleed rounded iPhone frame showing the actual feature UI | (ken-burns-broll / static mock) |
| — | stat | big % number(s) full-screen (30% / 70% / 80%) | percent-stat-card |
| — | white card | clean white Apple explainer card (logo, iCloud, privacy copy) | (white slide) |
| — | scan | circular scan/loading ring around the avatar | (siri-intelligence-glow ring) |
| last | CTA (~84–90s) | tilted 3D phone-STACK mockup of a WhatsApp community ("AI Updates Community") + "Want to stay…" headline → join | phone-stack-cta |

## Signature techniques (what makes this look)
1. **Persistent numbered lower module** — PiP-left + silver `#` + LIME number + emphasized white
   caption. The spine; identical every item, only the number + copy change.
2. **`#NN` count tracker** — the giant lime number both *labels* the item and shows progress through
   the list. Number pops/scales in as each item begins.
3. **Single lime accent discipline** — `#C4FB00` ONLY on numbers; everything else neutral. Premium pop.
4. **Per-section gradient re-tint** — background bottom tone changes per item (red, black, …) to keep
   a long video from feeling samey, while the light top keeps it clean.
5. **Rotating Apple-clean content** — node-graph compares, scrolling highlight lists, full-bleed iOS
   mockups, big-% stat cards, white explainer cards, scan rings. Never two identical content beats.
6. **Serif-italic hook over an AI concept image** — the cold-open formula (claim + fabricated visual).
7. **Inline stat emphasis in captions** — key numbers/words bolded inside the white caption sentence.
8. **WhatsApp/community phone-stack CTA** — tilted 3D stacked-phone mockup of a community page to join.

## Overlap rules
MAY: lower module over the bottom gradient · content fills upper ⅔ · full-bleed on cold-open/stat/mock.
MUST NOT: content key-text colliding with the PiP avatar · lime used on anything but numbers · more
than one giant number on screen · text bleeding past ~80–105px safe margins.

## Reproduce-it checklist
1. 9:16 1080×1920, true 60fps. Warm talking-head PiP, bg = light-top→section-tone gradient.
2. Build the lower module ONCE (PiP bottom-left + silver `#` + lime `#C4FB00` number + white caption),
   reuse every item; animate the number pop + caption slide.
3. Lime ONLY on numbers. Re-tint the bottom gradient per item for variety.
4. Rotate ≥4 different content beats (compare diagram / scroll-list / phone mock / % stat / white card).
5. Cold open = AI concept image + serif-italic hook + presenter below.
6. At least one scrolling-highlight list and one big-% stat card (cheap, high-impact beats).
7. Close on a tilted phone-stack community CTA ("Want to stay…").
8. New item every ~6–8s, ~2s sub-cuts; keep every beat visually UNIQUE — house mindset, not a clone.
