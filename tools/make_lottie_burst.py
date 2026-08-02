#!/usr/bin/env python3
"""Generate a deterministic, seek-safe Bodymovin (lottie-web) JSON for a radial
"clay spark burst" logo sting: N rays shoot out from center, a ring pulses,
a center dot pops. fps 60, transparent bg. Hand-emitting the JSON keeps it valid
and self-contained (no AE export, no remote fetch). Tune via constants below."""
import json, math, sys

W = H = 500
CX = CY = 250
FPS = 60
OP = 48                      # total frames (0.8s)
CLAY = [0.800, 0.471, 0.361] # #CC785C
SAND = [0.831, 0.635, 0.498] # #D4A27F
N_RAYS = 12
RAY_W = 14
RAY_LEN = 150
RING_R = 86


def tr(p=(CX, CY), a=(0, 0), s=(100, 100), r=0, o=100):
    return {"p": {"a": 0, "k": list(p)}, "a": {"a": 0, "k": list(a)},
            "s": {"a": 0, "k": list(s)}, "r": {"a": 0, "k": r},
            "o": {"a": 0, "k": o}, "sk": {"a": 0, "k": 0}, "sa": {"a": 0, "k": 0}, "ty": "tr"}


def kf(frames):
    """frames = list of (t, value-list). Build an animated property."""
    out = []
    for i, (t, v) in enumerate(frames):
        node = {"t": t, "s": v}
        if i < len(frames) - 1:
            node["o"] = {"x": [0.33], "y": [0.0]}
            node["i"] = {"x": [0.67], "y": [1.0]}
        out.append(node)
    return {"a": 1, "k": out}


def fill(color):
    return {"ty": "fl", "c": {"a": 0, "k": color + [1]}, "o": {"a": 0, "k": 100}, "r": 1, "bm": 0}


def stroke(color, w):
    return {"ty": "st", "c": {"a": 0, "k": color + [1]}, "o": {"a": 0, "k": 100},
            "w": {"a": 0, "k": w}, "lc": 2, "lj": 1, "ml": 4, "bm": 0}


layers = []
idx = 1

# rays: each a group with a rounded rect pointing up, group rotated to its angle,
# group scale animates 0 -> 100 (shoots outward from center), staggered.
for i in range(N_RAYS):
    ang = (360.0 / N_RAYS) * i
    delay = (i % 4) * 1.5
    rect = {"ty": "rc", "d": 1, "s": {"a": 0, "k": [RAY_W, RAY_LEN]},
            "p": {"a": 0, "k": [0, -(RING_R + RAY_LEN / 2.0)]}, "r": {"a": 0, "k": RAY_W / 2.0}}
    grp_tr = tr(s=(100, 100), r=ang)
    grp_tr["s"] = kf([(0 + delay, [0, 0]), (10 + delay, [118, 118]), (16 + delay, [100, 100])])
    grp_tr["o"] = kf([(0 + delay, [0]), (6 + delay, [100]), (30, [100]), (OP, [0])])
    col = CLAY if i % 2 == 0 else SAND
    layers.append({
        "ddd": 0, "ind": idx, "ty": 4, "nm": f"ray{i}", "sr": 1,
        "ks": tr(), "ao": 0, "ip": 0, "op": OP, "st": 0, "bm": 0,
        "shapes": [{"ty": "gr", "nm": f"rayg{i}", "it": [rect, fill(col), grp_tr]}],
    })
    idx += 1

# pulsing ring (stroke ellipse)
ring_tr = tr()
ring_tr["s"] = kf([(2, [20, 20]), (16, [120, 120]), (OP, [150, 150])])
ring_tr["o"] = kf([(2, [0]), (10, [90]), (28, [60]), (OP, [0])])
layers.append({
    "ddd": 0, "ind": idx, "ty": 4, "nm": "ring", "sr": 1,
    "ks": tr(), "ao": 0, "ip": 0, "op": OP, "st": 0, "bm": 0,
    "shapes": [{"ty": "gr", "nm": "ringg", "it": [
        {"ty": "el", "d": 1, "s": {"a": 0, "k": [RING_R * 2, RING_R * 2]}, "p": {"a": 0, "k": [0, 0]}},
        stroke(CLAY, 10), ring_tr]}],
})
idx += 1

# center dot
dot_tr = tr()
dot_tr["s"] = kf([(0, [0, 0]), (9, [130, 130]), (15, [100, 100])])
layers.append({
    "ddd": 0, "ind": idx, "ty": 4, "nm": "dot", "sr": 1,
    "ks": tr(), "ao": 0, "ip": 0, "op": OP, "st": 0, "bm": 0,
    "shapes": [{"ty": "gr", "nm": "dotg", "it": [
        {"ty": "el", "d": 1, "s": {"a": 0, "k": [96, 96]}, "p": {"a": 0, "k": [0, 0]}},
        fill(CLAY), dot_tr]}],
})

doc = {"v": "5.7.4", "fr": FPS, "ip": 0, "op": OP, "w": W, "h": H,
       "nm": "claude-clay-burst", "ddd": 0, "assets": [], "layers": layers}

out = sys.argv[1] if len(sys.argv) > 1 else "assets/lottie/claude-burst.json"
with open(out, "w") as f:
    json.dump(doc, f, separators=(",", ":"))
print(f"wrote {out}  ({len(layers)} layers, op={OP}f @ {FPS}fps)")
