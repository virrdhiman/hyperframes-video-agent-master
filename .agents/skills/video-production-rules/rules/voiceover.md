---
name: voiceover
description: Adding AI voiceover (TTS) to HyperFrames compositions
---

# Voiceover (TTS)

Generate narration locally with HyperFrames' built-in Kokoro TTS — no API key:

```bash
npx hyperframes tts "Welcome to the show." -o narration.wav
npx hyperframes tts script.txt --voice af_nova -o narration.wav
```

- `--list` shows the 54 voices; default is `af_heart`. Rough picks: product demo `af_heart`/`af_nova`, tutorial `am_adam`/`bf_emma`, marketing `af_sky`/`am_michael`, docs (British) `bf_emma`/`bm_george`, casual `af_sky`.
- The voice's first letter selects the language (a=US-Eng, b=Brit-Eng, e=Spanish, f=French, h=Hindi, i=Italian, j=Japanese, p=BR-Portuguese, z=Mandarin); override with `--lang`. Non-English needs `espeak-ng` installed.
- `--speed`: ~0.7–0.8 for tutorials, 1.0 default, 1.1–1.2 for punchy intros.

## Wiring it in

Add the generated file as a separate `<audio>` clip (voiceover sits on top of any music bed — keep music at ~0.12 under it, ~0.45 in pauses; see [audio](./audio.md)). One file per scene keeps timing manageable; place files in `assets/`.

## Pacing the composition to the voiceover

Let the narration drive scene durations: a scene should last as long as its line (plus a small head/tail). Lay each scene's clips to cover its VO clip's length, and overlap any scene transitions inside those bounds.

## Voiceover → captions

For exact word boundaries, transcribe the narration you just generated and feed it to the caption pipeline:

```bash
npx hyperframes transcribe narration.wav
```

See [captions](./captions.md).

## Script/narration craft

Write for the ear: short sentences, one idea per line, spell tricky numbers/units the way they're spoken, and open with a hook line. Read it aloud — if you stumble, rewrite it.
