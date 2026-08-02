---
name: display-captions
description: Displaying word-synced captions in HyperFrames — pages, active-word highlight, exit guarantee
---

# Displaying captions

Once you have a transcript (`[{ id, text, start, end }]` in seconds — see [captions](./captions.md)), display it as grouped pages with optional active-word highlighting, all on the paused GSAP timeline.

## Grouping into pages

Group consecutive words into short pages. How many words per page is the rhythm dial: high energy 2–3 words, conversational 3–5, calm 4–6. Break on sentence boundaries, 150ms+ pauses, or the max count. (This is the editorial equivalent of "combine tokens within N ms" — pick the grouping by the energy of the segment, not a fixed number.)

## Showing one page at a time

Build one container element per group. Reveal it with a `gsap.from()` entrance at the group's `start`, and kill it at the group's `end`. Only one group is visible at any time — don't let pages overlap.

## Active-word highlighting

To highlight the currently spoken word, give each word its own span and schedule the highlight on the timeline at the word's boundaries:

```js
// for each word in the group:
tl.set(wordEl, { color: HIGHLIGHT_COLOR }, word.start);
tl.set(wordEl, { color: BASE_COLOR }, word.end);
```

Because times are deterministic seconds, this is fully seekable. Keep whitespace intact between words (`white-space: pre` and include leading spaces in the text) so spacing renders correctly.

## Exit guarantee (mandatory)

Every group must hard-kill at its end so nothing lingers:

```js
tl.to(groupEl, { opacity: 0, scale: 0.95, duration: 0.12, ease: "power2.in" }, group.end - 0.12);
tl.set(groupEl, { opacity: 0, visibility: "hidden" }, group.end);
```

## Captions over video

Layer the caption container above the `<video muted playsinline>` clip (use CSS `z-index`). If the footage is bright, add a subtle dark scrim div beneath the text for legibility. Keep captions in their own track so their timing is independent of the video. For each distinct video, keep its own transcript so timing stays in sync.

## Reuse the registry

Rather than hand-build, install a caption style component (`npx hyperframes add caption-highlight`, etc.) and drive it from your real transcript by porting its per-word animation into a host comp.
