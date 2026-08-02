# Element: Siri / Apple-Intelligence glow border

The instantly-recognizable Apple Intelligence "glow that runs around the border" when AI is
invoked. Animated conic-gradient ring + soft bloom. Pair with Liquid Glass for an instant Apple feel.
Original + SEEK-SAFE (drive the angle from GSAP `tl`, never CSS @keyframes).

## Reference implementation
Canonical source file: `projects/wwdc26-ios27-top3/assets/siri-glow.css` (+ `SIRI_GLOW.md` how-to).
Copy that CSS into any project's assets and link in <head>.

## Mechanism (measured)
- `@property --siri-angle {syntax:'<angle>'; initial-value:0deg; inherits:false}` so GSAP can
  interpolate it deterministically.
- `.siri-glow::before` = crisp ring, `.siri-glow::after` = blurred bloom (z-index -1 / -2).
- Ring made by `background: conic-gradient(from var(--siri-angle), …)` masked to border via
  dual mask + `mask-composite: exclude` (`-webkit-mask-composite: xor`) with
  `inset: -var(--siri-width)` and matching `padding`.
- Bloom: `filter: blur(var(--siri-bloom,26px)) saturate(1.6); opacity:.9`.

## Palette (Apple-Intelligence-ish)
blue #0A84FF · indigo #5E5CE6 · purple #BF5AF2 · pink #FF2D92 · coral #FF6B5E · yellow #FFD426 · teal #34D1C4 (loop to blue)

## Tunables (CSS vars)
`--siri-width` (ring px) · `--siri-radius` (match element corner) · `--siri-bloom` (blur px) ·
`--siri-bloom-opacity` · `--siri-pulse` (0..1 brightness, drive from tl for an "invoke" pulse).

## Seek-safe wiring
`tl.to(".siri-glow",{ "--siri-angle":"360deg", duration:6, ease:"none", repeat:-1 },0);`
For an "AI invoked" reveal: fade `.siri-edge` (full-frame) in with a `--siri-pulse` ramp on the beat.

## Use cases
Full-frame edge glow ("border comes around the screen"), ring a 3D device/card, ring number
badges / CTA pills. Feature it on AI beats; don't ring everything at once.

## Companion: Apple-feel fonts
SF Pro / SF Pro Display → free match = Inter (400–900) via `assets/fonts/fonts.css`
(`.apple-display` 900 / -0.035em tracking for keynote headlines). Swap in real SF Pro .otf if available.
