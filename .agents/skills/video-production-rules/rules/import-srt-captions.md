---
name: import-srt-captions
description: Importing existing .srt/.vtt subtitle files into the HyperFrames caption pipeline
---

# Importing .srt / .vtt captions

If you already have a subtitle file, import it instead of re-transcribing:

```bash
npx hyperframes transcribe subtitles.srt
```

`transcribe` auto-detects and normalizes `.srt`, `.vtt`, and `.json` inputs into the standard transcript array (`[{ id, text, start, end }]`, times in seconds).

**Caveat — SRT/VTT are phrase-level only.** They give you the timing of whole subtitle cues, not individual words. That's fine for static subtitle display, but **per-word animation** (highlighting the spoken word, kinetic pop-per-word) needs word-level timestamps. If you need word-level and only have an SRT, either:

- re-transcribe the source audio with `npx hyperframes transcribe <audio>` (see [captions](./captions.md)), or
- produce an external word-level result (OpenAI/Groq `verbose_json` with `timestamp_granularities[]=word`) and import that JSON.

Once imported, the captions flow through the same display path as any transcript — see [display-captions](./display-captions.md).
