# Audio Generator — ElevenLabs

Search, explore, and generate voice audio using the **ElevenLabs API**.

**Script:** `tools/audio_generator/elevenlabs.py`  
**Auth:** Uses `ELEVENLABS_API_KEY` or `XI_API_KEY` from `.env`  
**Default output:** `assets/audio/`

---

## What This Tool Does

The script supports four workflows:

1. `models` — list available ElevenLabs models
2. `voices` — search voices in the current ElevenLabs account/workspace
3. `shared-voices` — explore public/shared voices from the ElevenLabs library
4. `tts` — generate speech audio from text

It is designed as a lightweight CLI for both human use and agent use.

---

## Auth

The script reads the API key from the project root `.env` file.

Supported variable names:

- `ELEVENLABS_API_KEY`
- `XI_API_KEY`

Optional:

- `ELEVENLABS_API_BASE` to override the default API host

Default API base:

```bash
https://api.elevenlabs.io
```

---

## Quick Start

```bash
cd tools/audio_generator

# List models that support text-to-speech
python3 elevenlabs.py models --tts-only

# Search voices in your own account/workspace
python3 elevenlabs.py voices --query "narrator" --limit 20

# Explore public/shared voices
python3 elevenlabs.py shared-voices --query "calm female" --language en

# Generate one speech file
python3 elevenlabs.py tts \
  --voice-id JBFqnCBsd6RMkjVDRZzb \
  --text "The first move is what sets everything in motion."
```

---

## Commands

### 1. `models`

Lists models from:

```bash
GET /v1/models
```

Useful for checking which models support TTS before generating.

Example:

```bash
python3 elevenlabs.py models --tts-only
```

Arguments:

| Argument | Default | Description |
|---|---|---|
| `--tts-only` | off | Show only models with `can_do_text_to_speech=true` |
| `--json` | off | Print raw JSON |

---

### 2. `voices`

Searches voices in the current account/workspace using:

```bash
GET /v2/voices
```

Example:

```bash
python3 elevenlabs.py voices --query "female narrator" --voice-type saved --limit 25
```

Arguments:

| Argument | Short | Default | Description |
|---|---|---|---|
| `--query` | `-q` | none | Search term |
| `--limit` | `-n` | `10` | Max results to fetch |
| `--sort` | | none | `created_at_unix` or `name` |
| `--sort-direction` | | none | `asc` or `desc` |
| `--voice-type` | | none | `personal`, `community`, `default`, `workspace`, `non-default`, `saved` |
| `--category` | | none | `premade`, `cloned`, `generated`, `professional` |
| `--json` | | off | Print raw JSON |

---

### 3. `shared-voices`

Explores public/shared voices using:

```bash
GET /v1/shared-voices
```

Example:

```bash
python3 elevenlabs.py shared-voices --query "documentary" --category professional --language en
```

Arguments:

| Argument | Short | Default | Description |
|---|---|---|---|
| `--query` | `-q` | none | Search term |
| `--limit` | `-n` | `10` | Max results to fetch |
| `--category` | | none | `professional`, `famous`, `high_quality` |
| `--gender` | | none | Gender filter |
| `--age` | | none | Age filter |
| `--language` | | none | Language filter |
| `--accent` | | none | Accent filter |
| `--json` | | off | Print raw JSON |

---

### 4. `tts`

Generates speech audio using:

```bash
POST /v1/text-to-speech/{voice_id}
```

Example:

```bash
python3 elevenlabs.py tts \
  --voice-id JBFqnCBsd6RMkjVDRZzb \
  --text "AI tools are powerful, but the workflow matters." \
  --model eleven_multilingual_v2 \
  --output-format mp3_44100_128
```

You must provide exactly one of:

- `--text`
- `--text-file`

Arguments:

| Argument | Short | Default | Description |
|---|---|---|---|
| `--voice-id` | | required | ElevenLabs voice ID |
| `--text` | | none | Inline text to synthesize |
| `--text-file` | | none | UTF-8 text file to synthesize |
| `--model` | | `eleven_multilingual_v2` | Model ID |
| `--output-format` | | `mp3_44100_128` | Output codec/quality |
| `--language-code` | | none | Optional ISO 639-1 language |
| `--stability` | | none | Voice stability override |
| `--similarity-boost` | | none | Voice similarity override |
| `--style` | | none | Style exaggeration override |
| `--speed` | | none | Voice speed override |
| `--speaker-boost` | | off | Enable speaker boost |
| `--seed` | | none | Optional deterministic seed |
| `--output` | `-o` | auto | Output file path |
| `--prefix` | | `elevenlabs` | Filename prefix when output path is auto-generated |
| `--timeout` | | `60` | HTTP timeout seconds |

---

## Output

If `--output` is omitted, files are written to:

```bash
assets/audio/
```

Auto-generated naming pattern:

```bash
<prefix>_<timestamp>.<ext>
```

Examples:

```bash
elevenlabs_20260310_231455.mp3
voiceover_intro_20260310_231501.wav
```

---

## Agent Workflow Notes

When using this tool from an agent:

1. Run `models --tts-only` if the model choice is unclear.
2. Run `voices --query ...` to search the workspace/account voices first.
3. Run `shared-voices --query ...` only when you want to explore public voices.
4. For generation, prefer `--text-file` for long scripts so prompts stay clean and reusable.
5. Save generated speech to `assets/audio/` or a project-specific audio folder.
6. Do not print or log API keys.

Good flow for a new voiceover:

```bash
python3 tools/audio_generator/elevenlabs.py voices --query "tech narrator"
python3 tools/audio_generator/elevenlabs.py tts \
  --voice-id <picked_voice_id> \
  --text-file projects/my_project/script.txt \
  --prefix my_project_voiceover
```

---

## Security Notes

- The script only reads API credentials from local environment variables.
- It does not echo secrets back to stdout.
- It only writes audio files to disk and does not execute returned content.
- If you use `--text-file`, make sure the source text does not contain secrets that should not be spoken or exported.

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `API key not found` | Missing ElevenLabs key in `.env` | Add `ELEVENLABS_API_KEY` or `XI_API_KEY` |
| `404` or `422` from TTS | Wrong `voice_id`, bad params, or unsupported format | Verify the voice and retry with a standard format like `mp3_44100_128` |
| No good voice matches | Search too narrow | Retry with broader terms like `narrator`, `calm`, `male`, `female`, `documentary` |
| Output sounds off | Voice settings too aggressive | Lower `--style`, reduce `--similarity-boost`, or omit overrides |
| Network error | Connectivity or provider issue | Retry after a short wait |

---

## Recommended Defaults

For most voiceover use cases in this repo:

- Model: `eleven_multilingual_v2`
- Format: `mp3_44100_128`
- Start with no voice overrides
- Only add `stability`, `style`, or `speed` after hearing a baseline result
