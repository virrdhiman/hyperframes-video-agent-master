# Cutout world loops — abstract dynamic backgrounds (the owner-approved set)

Reusable **moving background loops** for the Cars24 cutout-explainer house style — the world
that sits BEHIND the chroma-keyed host. the owner locked 5 Mixkit looks + 4 minimal Pixabay looks on
2026-06-23 as standing world-modes. Use them when a topic suits an abstract/tech world instead
of (or alongside) the green/purple perspective grid floor we render in-engine.

**DEFAULT to the MINIMAL set** (the owner, 2026-06-23): pick low-distraction worlds first — the host +
the topic must own attention, never the background. The busier Mixkit looks are for beats that
genuinely want energy.

Reference sheets: `cutout-bg-picks.jpg` (Mixkit 5), `cutout-bg-picks-minimal.jpg` (Pixabay 4).

## Source + licence
The Mixkit 5 are **Mixkit free stock video** (720p, Mixkit's max free direct download). The minimal
4 are **Pixabay free stock video** (1080p large, API key). BOTH are free for commercial use,
**no attribution required**, and already **dense-keyframe re-encoded** (1 keyframe/sec @30fps,
faststart, audio stripped) → render-ready, no seek/decode crash. Files live in
`styles/assets/backgrounds/`.

## Minimal / low-distraction set — DEFAULT (Pixabay, the owner 2026-06-23)
Sparse, dark, low-motion, lots of negative space → host + topic stay the focus. Best host contrast.
| Look | When to use | File | Source | Notes |
|---|---|---|---|---|
| **Halftone matrix** | most minimal; dark mono dots — safe behind ANY outfit incl. blue polo | `assets/backgrounds/pix-halftone-matrix.mp4` | pixabay `356327` | best default; near-black |
| **Polygon lines** | calm purple low-poly drift; on-brand purple, non-blue (good contrast) | `assets/backgrounds/pix-polygon-lines.mp4` | pixabay `145026` | purple, sparse |
| **Plexus particles** | sparse dark plexus w/ subtle amber motes; "AI/connections" w/o clutter | `assets/backgrounds/pix-plexus-particles.mp4` | pixabay `27669` | dark + amber |
| **Hexagon data** | a few cyan hexagons drifting on near-black; lots of empty space | `assets/backgrounds/pix-hexagon-data.mp4` | pixabay `138087` | cyan-on-black; scrim if blue host |

Re-download (if lost): `https://cdn.pixabay.com/video/<path>_large.mp4` via the API by id (needs a
browser `User-Agent` header — the bare request 403s).

## The energy set (Mixkit) — use when a beat wants motion
| Look | When to use | File | Source | Dur |
|---|---|---|---|---|
| **Hex texture** | textured tech surface; premium/structured beats; subtle motion behind talk | `assets/backgrounds/hex-texture.mp4` | mixkit `26801` | 15s |
| **Node network** | AI / connections / "everything links" — plexus dots on a perspective grid floor | `assets/backgrounds/node-network.mp4` | mixkit `31771` | 15s |
| **Code matrix** | code / dev / data / "under the hood" beats | `assets/backgrounds/code-matrix.mp4` | mixkit `21053` | 5s |
| **Dust particles** | calm neutral world; B&W drifting motes — good when topic has no strong color | `assets/backgrounds/dust-particles.mp4` | mixkit `26773` | 15s |
| **Waveform bars** | audio / metrics / "the numbers moved" — pink/cyan equalizer | `assets/backgrounds/waveform-bars.mp4` | mixkit `18143` | 10s |

Re-download (if ever lost): `https://assets.mixkit.co/videos/<id>/<id>-720.mp4`.

## How to use (behind the cutout host)
1. Source clips are **16:9 (1280×720)** → in the comp put the `<video>` full-frame with
   `object-fit:cover` so it crops to 9:16 (1080×1920). Center the busiest area.
2. Layer ORDER: world loop (back) → optional grain/vignette → evidence cards → **`#host` cutout
   (top)**. Keep the world darker/lower-contrast than the host so the keyed edge reads clean.
3. Add subtle **parallax**: slow scale/drift on the world (see
   `../animations/parallax-world-motion.md`) and nudge it opposite the host's moves for depth.
   The clip already moves, so keep the added drift gentle.
4. Loop the clip across the scene length (it's a seamless-ish loop); the dense keyframes mean
   HyperFrames seeks it without the black-frame/`Target closed` crash.
5. Keep the Cars24 accent language constant on top (yellow up-arrows, red rubber-stamp, white
   label plates) so the brand reads the same whatever world you pick.
6. STYLE COOLDOWN: rotate which world you use day-to-day (these 5 + the in-engine green/purple/
   charcoal grid floor) so the look doesn't repeat inside the 3-day window.

## HOST CONTRAST — non-negotiable (the owner, 2026-06-23)
The keyed A-roll host must ALWAYS stay clearly visible and NEVER blend into the world. When you
pick + treat a background:
1. **Pick for contrast.** Choose a world whose dominant luminance/hue CONTRASTS the host — never
   put a predominantly **blue/teal** world flush behind his **blue polo**, or a skin-orange world
   behind his face (they merge). `node-network` is blue → it especially needs the steps below.
2. **Knock the world back** so it reads as background and the host reads as sharp foreground:
   `filter: brightness(.55) saturate(.85) blur(4px);` on the world `<video>`.
3. **Black scrim to lift the host** — a darkening layer ABOVE the world, BELOW the cards + host:
   - full-frame `background: rgba(0,0,0,.35–.55)`, OR (better, more cinematic)
   - a soft radial dark pool centred on him:
     `background: radial-gradient(closest-side at 50% 62%, rgba(0,0,0,.6), transparent 70%);`
4. Keep the host's **soft contact shadow + subtle rim** so the keyed edge separates from the world.
5. **QA GATE (BLOCKER):** at every host-over-world frame the host's outline must be clearly
   distinguishable from the world. If he blends in → darken the scrim or swap the world before
   APPROVED. Snapshot a host-on-world frame and eyeball the silhouette.

## Note
The classic green/purple **synthwave perspective grid floor** (our signature) is NOT stock — we
generate it in-engine (color-tunable per topic): see `../animations/parallax-world-motion.md` +
`../animations/green-grid-bg.md`. These 5 loops are the abstract *alternatives* to that floor.
