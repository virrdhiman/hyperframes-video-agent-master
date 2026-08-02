---
name: light-leaks
description: Light-leak overlay effects over scene cuts in HyperFrames
---

# Light leaks

A light leak is a warm overlay that blooms over a cut — it reveals during the first half of its time and retracts during the second half, so its midpoint lands on the cut between two scenes. It reads as a film-camera light flare and suits **warm / nostalgic / organic** moods.

In HyperFrames:

- The registry ships a **`light-leak` shader transition** (`npx hyperframes catalog --tag shader`) — the simplest way to drop a light-leak between two scenes as a one-shot effect.
- For a leak that plays **over** a cut without shortening the timeline, layer a separate overlay element above both scenes (high CSS `z-index`) and animate its reveal/retract on the timeline so the peak sits on the cut. This is the overlay pattern: it decorates the cut rather than being the cut.
- A light leak can also be a **decorative ambient overlay** inside a single scene — a slow bloom that drifts across the frame.

Knobs worth varying: the bloom **shape/seed** (so repeated leaks don't look identical — drive any randomness with a seeded PRNG, never `Math.random()`), the **hue** (default warm yellow-orange; shift toward green or blue for a colder palette), and the **duration** (longer = gentler).

Keep leaks subtle — they're seasoning over a cut, not the main event. Don't strobe.
