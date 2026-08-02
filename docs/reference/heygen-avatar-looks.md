# HeyGen avatar looks — mood → look → character_id

Stable `character_id`s for the 13 Retrofit AI HeyGen looks. Classify each script into a
dominant mood, pick the matching look. IDs are stable (they don't drift like grid indices),
so automation should match the tile whose `<img>` src contains the `character_id`
(`/[a-f0-9]{32}/`), with a fallback to the unique tile name.

> **[Remotion/server pipeline]** This drives HeyGen A-roll generation, which is human-assisted
> (needs the home-IP SOCKS tunnel + a logged-in session). In this local HyperFrames project you
> normally edit A-roll that's already in the project. Kept here as reference for the automation
> (`tools/heygen_playwright.py` `_select_avatar`).

| Mood signal | Look name | character_id |
|---|---|---|
| serious/landmark news, regulation | Authority (suit) | `b56ff77c19e64f7781f2ff7d978f5c98` |
| business/funding/markets/strategy | Pro (blazer) | `a12efdc233dd4f31bebc919e360cbd6b` |
| hardware/chips/dev-tools/tutorial | Desk (whiteboard) | `ba5264c5f4904949a3b80627314ca5b3` |
| exciting reveal / big tool launch | Hype (blue polo) | `02b6f12b86964938b557641987651103` |
| **standard news / explainer (DEFAULT)** | Explainer (beige) | `506b7b172c02483c928f38e1d4644b7b` |
| opinion / warning / hot take | RealTalk (dark crew) | `a4103a1de9a44c8e90f8bcb4ff3d63b0` |
| playful / quirky / light | Fun (orange tee) | `10c0a730f96548e28cde385250dc27a3` |
| quick "just happened" breaking | Update (car) | `c171fdb4653c4170a3015e248641c285` |
| consumer / everyday / lifestyle | Lifestyle (balcony) | `09199dcca4324ccaa465a48ba5bd77d2` |
| relaxed, mid-energy | Casual (navy tee) | `ba58cec5be6b4af99d06b120963b963e` |
| backup | Pro 2 | `1b0d9411c593488ca7b13a45893d6819` |
| backup | Update 2 | `0f99eaa3…` (partial) |
| backup | Lifestyle 2 | `0e62c009…` (partial) |

Selection: `--look Authority` → look up `character_id` → click the tile whose img-src contains
it. No index, no screenshot recon. (One-time code check: confirm the editor's look-picker panel
tiles also carry the id in img-src, not just the my-avatars grid.)

## Infra / sources (reference)
- **Replicate** ready (`REPLICATE_API_TOKEN` in `tools/.env`): `google/nano-banana` (image) →
  `wan-2.2` i2v (animate). Cost-check with `tools/scenes_dryrun.py` first.
- **Music/SFX:** reuse `public/common/sfx/` + `public/common/backgrounds/` first; new SFX via
  `tools/audio_generator/sfx_gen.py` (ElevenLabs); music beds via Pixabay/ElevenLabs; always
  re-encode (`libmp3lame`, never `-c copy`).
- **Topic feeds (recommended):** HN (Algolia API), Reddit JSON (r/artificial, r/LocalLLaMA,
  r/MachineLearning, r/technology), RSS (TechCrunch, The Verge, VentureBeat, Ars Technica),
  + SERPER for ad-hoc search. Engagement = HN points / Reddit score+ratio / RSS recency.
  Semantic dedupe: local `sentence-transformers/all-MiniLM-L6-v2` (free, on-server).
