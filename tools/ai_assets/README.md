# AI Assets — Replicate (Nano Banana 2 + Wan i2v)

`replicate_gen.py` generates bespoke image + motion assets via Replicate.
**This replaces `tools/image_generator/imagen.py` and `tools/video_generator/veo.py`** —
those use the suspended Google API key and are dead.

Auth: `REPLICATE_API_TOKEN` in the repo `.env` (already set, verified working).
Recipes + when-to-use rules: `docs/guides/HUMAN_EDIT_GUIDE.md` §5.
Budget: ≤4 images + ≤2 motion clips per video. All outputs go through the owner's
step-4b asset approval gate.

```bash
# image generate / edit (Nano Banana 2; --ref-image grounds identity/brand, repeatable)
python3 tools/ai_assets/replicate_gen.py image -p "<prompt>" [--ref-image x.png] \
    [-r 9:16] [--resolution 1K|2K|4K] [-o projects/<slug>/assets/ai]

# image → 5s/10s motion clip (Wan 2.5 i2v 1080p; --fast = Wan 2.2 720p, ~4x cheaper)
python3 tools/ai_assets/replicate_gen.py i2v -p "<motion prompt>" --image still.png \
    [--duration 5|10] [--fast] [-o projects/<slug>/assets/ai]
```

Timings (measured 2026-06-11): image ~20s · ref-edit ~16s · i2v --fast 5s clip ~2min.
Generated video must be dense-keyframe re-encoded before embedding (BROLL_GUIDE.md),
and color-matched warm like any external clip.

Likeness rule (hard): the owner's face only ever from a real captured frame
(`ffmpeg -ss 2 -i avatar.mp4 -frames:v 1 ref.jpg`) — never invented from text; no
mouth-flap motion; every likeness edit labeled in the approval shortlist.
