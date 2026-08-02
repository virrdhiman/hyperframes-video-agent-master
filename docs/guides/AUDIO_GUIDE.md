# AUDIO_GUIDE.md — the sound-design + master pass (every video)

Audio is the cheapest "feels 2× more pro" upgrade for AI short-form. A great cut with
flat audio reads as amateur; an average cut with a ducked music bed + tight SFX + a loud,
clean master reads as professional. **This pass is now mandatory** — PIPELINE step 6.5.

The whole pass is one deterministic tool over the finished render:
`tools/audio_finish.py --video out/<slug>/<slug>.mp4 --plan projects/<slug>/audio.json`
→ writes `out/<slug>/<slug>_final.mp4` (the deliverable) + `projects/<slug>/audio_finish.json`.

---

## 0) One-time: build the SFX + music library
**Primary — FETCH premade (real, royalty-free) from Freesound** (`FREESOUND_API_KEY` in `.env`;
free key at https://freesound.org/apiv2/apply). Defaults to **CC0** (no attribution needed):
```
python3 tools/stock_fetcher/freesound.py --pack all     # commonly-used SFX + 2026-popular + music beds
python3 tools/stock_fetcher/freesound.py -q "transition whoosh" --type sfx -n 5   # ad-hoc
python3 tools/stock_fetcher/freesound.py -q "lofi background" --type music -n 3
```
→ SFX into `assets/common/sfx/`, music into `assets/common/music/`; licenses logged to
`assets/common/CREDITS.md`. Reusable across every video. (NOTE: Pixabay's API does NOT expose
audio — only images/video — so don't use `pixabay.py` for sound.)

**Attribution:** CC0 files need none. **CC-BY** files (logged in `assets/common/CREDITS.md`) require
a credit — when a CC-BY asset is actually used in a video, append its `CREDITS.md` line to that
video's `post.md` (it goes in the YouTube description / IG caption). Prefer CC0 when equivalent.

**Fallback — GENERATE bespoke (ElevenLabs text-to-SFX)** when no premade clip fits a moment:
`python3 tools/audio_generator/sfx_gen.py --pack` (or `--prompt "deep cinematic boom" --out …`).
Generative, costs credits; the file is then reusable like any other. Catalogue picks in `COMMON_ASSETS.md`.

## 1) Music bed — mood-matched, ALWAYS ducked
- One bed per video, chosen by topic mood (energetic launch → upbeat-warm; serious/business →
  clean-corporate; big reveal → cinematic-swell). Light/optimistic by default (matches LIGHT).
- It sits **under** the VO: `audio_finish.py` ducks it automatically via `sidechaincompress`
  keyed off the VO (music drops ~8–12 dB whenever speech is present, swells back in the gaps).
  Set the resting level with `music_gain_db` (default **-18**; -16 in pure-graphic stretches
  with no VO, -20 under dense narration). VO stays dominant — never fight it.

## 2) SFX — moderate, motivated, one per beat (not every frame)
Map sound to the edit. The Director lists the cue *type* per beat in the BRIEF; Bella fills the
exact `t` (seconds, on the rendered timeline) into `projects/<slug>/audio.json`:
| Moment | SFX type | typical gain | max length (`dur`) |
|---|---|---|---|
| Hook / cold open (0.0s) | **riser** into the first cut | -5 | ≤2.5s, fade into the cut |
| Hard cut / scene change | **whoosh** | -7 | ≤0.7s |
| Element reveal / chip pop | **pop / click** | -8 | ≤0.4s |
| Stat slam / impact word | **impact / sub-boom** | -4 | ≤1.0s (`fade` 0.25) |
| Outro / CTA | **swell** | -6 | ≤2.0s, fade under the CTA line |
Rule: if a beat doesn't *need* a sound, leave it silent. Density kills impact.

### 2a) SFX LEVEL + LENGTH DISCIPLINE (the owner, 2026-06-11 — hard rules)
An SFX must **punctuate** the VO, never compete with it or shock the viewer. The "95% score"
slam read great; the "THE CATCH" hit was **too long and too loud** — that class of mistake is
now blocked mechanically:
- **Hard cap:** `audio_finish.py` clamps every cue to `sfx_cap_db` (default **-4 dB**; set in
  the plan or `--sfx-cap`). Don't raise the cap to "make a moment bigger" — make the *visual*
  bigger instead.
- **Trim every one-shot** with `"dur"` per the table above; the tool auto-fades the tail
  (default 0.15s, override with `"fade"`). A boom that rings past its beat smears the next line.
- **Never two heavy hits within 3s** — if two stat slams are adjacent, demote one to a pop.
- Listen check at QA: scrub each cue — the VO word it lands on must stay fully intelligible.

## 3) VO master — loud + clean
- The render already carries the VO; this pass mixes everything and **normalizes the final mix
  to -14 LUFS integrated, -1.5 dBTP** (the IG/TikTok/YT target) via `loudnorm`. That's what
  makes it hit as loud as pro content in the feed.
- If the source VO is noisy/boomy, pre-clean before HeyGen/TTS, or add a highpass+de-ess in the
  plan later — but loudnorm + ducking already covers 90% of the gap.

## 4) The plan file — `projects/<slug>/audio.json`
```json
{
  "music": "assets/common/music/upbeat_warm.mp3",
  "music_gain_db": -18,
  "sfx_cap_db": -4,
  "cues": [
    {"t": 0.0,  "file": "assets/common/sfx/riser.mp3",  "gain_db": -5},
    {"t": 1.4,  "file": "assets/common/sfx/whoosh.mp3", "gain_db": -7, "dur": 0.7},
    {"t": 6.3,  "file": "assets/common/sfx/pop.mp3",    "gain_db": -8, "dur": 0.4},
    {"t": 12.6, "file": "assets/common/sfx/impact.mp3", "gain_db": -4, "dur": 1.0, "fade": 0.25}
  ]
}
```
Times are **on the final rendered timeline** (already 1.10×-scaled — read them off the QA grid /
the composition's cut points). Missing SFX/music files are skipped with a warning, never fatal.

## 5) Gate
`pipeline_check.py` now requires `<slug>_final.mp4` to exist and `audio_finish.json` to report a
measured loudness within **-16…-12 LUFS**. The delivered file is the `_final.mp4`, not the raw render.
