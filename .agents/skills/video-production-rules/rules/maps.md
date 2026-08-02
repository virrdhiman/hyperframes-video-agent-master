---
name: maps
description: Map animations in HyperFrames — registry map blocks and camera/line motion practices
---

# Maps

## Use a registry map block (preferred)

The catalog ships map blocks (`npx hyperframes catalog --tag data`): `us-map`, `us-map-bubble`, `us-map-hex`, `us-map-flow`, `world-map` (globe inset), `spain-map`, plus showcase blocks like `nyc-paris-flight` (map + animated plane) and `north-korea-locked-down` (map zoom). Install with `npx hyperframes add world-map` and feed your coordinates/markers. This is the simplest route for most map segments.

## Animating maps (general practices)

Whatever the underlying map, these editorial/determinism rules hold:

- **Drive all motion from the paused GSAP timeline** in seconds. Disable any motion the map library does itself (no library easing/fade) — those are non-deterministic and conflict with the render. If a map needs to finish loading before it animates, ensure it's ready synchronously before the timeline builds; never fetch tiles at render time non-deterministically.
- **Camera:** keep north up by default; don't jump between camera angles unless asked. For multi-step camera moves, set *every* relevant property (zoom, center, line progress) at *every* stage so nothing snaps from an unset value.
- **Drawing lines:** a line that should look straight on the map uses linear interpolation between endpoints; a line that follows the great-circle (flight path) uses geodesic interpolation — they look different on the projection, so pick deliberately. Don't add glow or extra points to a line unless asked.
- **Markers and labels:** size for downscaling. At 1920×1080, label text ≥40px; keep label offsets small so they sit close to their marker.
- Hide clutter from the base map (roads/labels/POIs) unless they're the point — a clean basemap reads better in motion.
