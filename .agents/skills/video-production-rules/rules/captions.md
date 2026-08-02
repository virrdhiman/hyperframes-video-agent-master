---
name: captions
description: Word-synced captions in HyperFrames — transcribe, transcript format, quality check, grouping, positioning, and the mandatory exit kill
---

# Captions (word-synced)

The HyperFrames caption pipeline turns a transcript into per-word-animated overlays on a paused GSAP timeline. See also [subtitles](./subtitles.md) and [display-captions](./display-captions.md).

## 1. Transcribe

```bash
npx hyperframes transcribe <audio|video> [--model <m>] [--language <code>]
```

Models: tiny / base / **small (default, 466MB)** / medium (noisy or music) / large-v3.

**`.en` RULE (non-negotiable):** `.en` models (`small.en`, `medium.en`) **translate** non-English audio to English, silently destroying the original. So:

- English audio → `--model small.en`.
- Known non-English → `--model small --language <code>`.
- Unknown → `--model small` (auto-detect). The default is `small`, **not** `small.en`.

`transcribe` also imports existing `.srt` / `.vtt` / `.json` (see [import-srt-captions](./import-srt-captions.md)).

## 2. Transcript format

A flat array; `id` is added on normalization:

```json
[{ "id": "w0", "text": "Hello", "start": 0.0, "end": 0.5 }, ...]
```

Word-level timestamps enable per-word animation. Auto-detected import formats: whisper.cpp JSON, OpenAI/Groq `verbose_json` (request `response_format=verbose_json` with `timestamp_granularities[]=word`), SRT/VTT (phrase-level only), and the normalized array.

## 3. Mandatory quality check

Read the transcript before building. Bad signals: `♪` / `�` tokens, garbled words, repeated filler (uh/huh), spans under 0.05s. If >20% junk, retry a larger model; if still bad, ask the user for a manual SRT/VTT or an external API result. Always clean: drop empty entries, music-note-only tokens, and short filler.

## 4. Word grouping

High energy: 2–3 words. Conversational: 3–5. Calm: 4–6. Break on sentence boundaries, 150ms+ pauses, or the max count.

## 5. Positioning

Landscape: bottom 80–120px, centered. Portrait: lower-middle, ~600–700px from the bottom. **Never cover the face.** Use a full-width `position:absolute` container — do not use `left:50%; transform:translateX(-50%)` (clips at edges). Set `overflow:visible` (not hidden, which clips scaled words and glow). Show one group at a time. Size dynamic text with `window.__hyperframes.fitTextFontSize(text, { maxWidth, fontFamily, fontWeight })` (maxWidth ~1600 landscape / ~900 portrait; if per-word scale > 1, divide maxWidth by the max scale).

## 6. Caption exit guarantee (mandatory)

Every group needs a hard deterministic kill at its end so it can never linger:

```js
tl.to(groupEl, { opacity: 0, scale: 0.95, duration: 0.12, ease: "power2.in" }, group.end - 0.12);
tl.set(groupEl, { opacity: 0, visibility: "hidden" }, group.end);
```

Self-lint before registering: seek to `group.end + 0.01`, warn if the group is still visible, then `tl.seek(0)`.

## Pre-built components

15 caption styles in the registry (`npx hyperframes catalog --tag caption-style`; e.g. `caption-highlight` = TikTok red sweep, the default social style). The component hardcodes its own WORDS array and grouping — to use *real* captions, port its animation into a host comp driven by your transcript (and adapt 1920×1080 components to portrait if needed).

## No recorded voiceover?

Generate one, then transcribe it for exact word boundaries:

```bash
npx hyperframes tts script.txt -o narration.wav
npx hyperframes transcribe narration.wav
```

See [voiceover](./voiceover.md).
