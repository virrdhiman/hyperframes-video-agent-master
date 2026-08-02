# Stock Fetcher

Two tools for sourcing video b-roll: **Pexels** for generic stock and **YouTube** for real product demos.

**When to use which:**
- **YouTube** (`youtube.py`) — preferred for product demos, reviews, hands-on footage. Use `--shorts` for 9:16 vertical clips, `--topic` for smart transcript-based trimming. Real footage is always more authentic than AI-generated approximations.
- **Pexels** (`pexels.py`) — for generic contextual b-roll (people texting, city skylines, coding, etc.) where no specific product is featured.

---

## Pexels

Search and download free stock photos and videos from Pexels.

**Script:** `tools/stock_fetcher/pexels.py`
**Auth:** Reads `PEXELS_API_KEY` from `.env` at the project root (never hardcoded).
**Default output:**
- Photos → `assets/stock/images/`
- Videos → `assets/stock/videos/`

---

## Quick Start

```bash
cd tools/stock_fetcher

# Download 1 portrait photo (9:16)
python3 pexels.py --query "Bangalore skyline" --type photo --ratio 9:16

# Download 3 landscape videos (16:9)
python3 pexels.py --query "developer coding office" --type video --ratio 16:9 --count 3

# List search results without downloading
python3 pexels.py --query "AI technology futuristic" --type video --list

# Custom prefix and output dir for a specific scene
python3 pexels.py --query "Indian students hackathon" --type photo --prefix scene7 --out ../../projects/india_ai/assets/
```

---

## Arguments

| Argument | Short | Default | Description |
|---|---|---|---|
| `--query` | `-q` | required | Search terms (plain English, like Google) |
| `--type` | `-t` | required | `photo` or `video` |
| `--ratio` | `-r` | `16:9` | `9:16` (portrait), `16:9` (landscape), `1:1` (square) |
| `--count` | `-n` | `1` | Number of items to download (max 20) |
| `--out` | `-o` | see above | Output directory (created if needed) |
| `--prefix` | | `pexels` | Filename prefix |
| `--list` | `-l` | false | Print results without downloading |

---

## Output

Files are named:
```
<prefix>_<pexels_id>_<index>.<ext>
```

Example: `scene7_17066965_1.jpeg`, `sample_2278095_1.mp4`

The Pexels ID in the filename lets you trace back to the original source at:
`https://www.pexels.com/photo/<id>/` or `https://www.pexels.com/video/<id>/`

---

## Aspect Ratio → Pexels Orientation

| Ratio | Pexels Orientation | Best for |
|---|---|---|
| `9:16` | portrait | YouTube Shorts, Reels, TikTok |
| `16:9` | landscape | YouTube, wide b-roll |
| `1:1` | square | Instagram posts |

---

## Photo Quality

For portrait (9:16), the script downloads Pexels' `portrait` crop — a pre-cropped vertical version of the photo. For landscape, it downloads the `landscape` crop. This ensures the correct framing without manual cropping.

---

## Video Quality

The script automatically picks the best available quality in this order:
1. **HD** — highest available resolution (typically 1920x1080 or higher)
2. **SD** — fallback if HD is unavailable

---

## Agent Workflow Integration

When the agent reads an `editing_brief.json` and finds `"source_type": "stock_video"` or `"source_type": "stock_image"`, it should:

1. Extract the `search_query` from the scene's `visual` object
2. Determine the ratio from the project metadata
3. Run this script with `--prefix scene<N>` so files are clearly labeled
4. Update the `editing_brief.json` to mark `"downloaded": true` and fill in `"file"` path

```bash
# Example: fulfill all stock_image tasks from the India AI brief
python3 tools/stock_fetcher/pexels.py \
  --query "Bangalore or Hyderabad tech city aerial skyline" \
  --type photo --ratio 9:16 --count 2 --prefix scene2

python3 tools/stock_fetcher/pexels.py \
  --query "Indian software developers working in modern office" \
  --type video --ratio 9:16 --count 2 --prefix scene6

python3 tools/stock_fetcher/pexels.py \
  --query "Indian college students hackathon computer lab" \
  --type video --ratio 9:16 --count 2 --prefix scene7
```

---

## Search Query Tips

- Use **descriptive natural language**: "Indian software engineer modern office" beats "coding"
- Add **location context**: "India", "Bangalore", "Mumbai" for Indian content
- Add **style words**: "cinematic", "aerial", "close-up", "professional"
- For videos, add **motion cues**: "timelapse", "drone shot", "slow motion"
- Pexels has strong coverage of: tech/coding, cities, nature, business, education

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `PEXELS_API_KEY not found` | Missing `.env` | Check `.env` exists at project root with `PEXELS_API_KEY=...` |
| `No results found` | Query too specific | Try broader search terms |
| `Download failed 403` | Expired session | Re-run; the script includes the API key in download headers |
| Very small file size | SD quality only | Normal for some videos; HD not always available |
