#!/usr/bin/env python3
"""
audio_finish.py — the audio sound-design + master pass for a finished render.

Takes a rendered HyperFrames mp4 (which already carries the VO) and layers a
ducked music bed + timed SFX, then masters the whole mix to a social loudness
target (-14 LUFS integrated). 100% ffmpeg + deterministic — no network, no rng.

  python3 tools/audio_finish.py --video out/<slug>/<slug>.mp4 \
      [--plan projects/<slug>/audio.json] \
      [--music assets/common/music/<bed>.mp3] [--music-gain -18] \
      [--lufs -14] [--out out/<slug>/<slug>_final.mp4]

audio.json (the Director specs it in the BRIEF; Bella fills the cue times):
  {
    "music": "assets/common/music/upbeat_warm.mp3",   # optional bed
    "music_gain_db": -18,                              # under the VO
    "sfx_cap_db": -4,                                  # optional, default -4: louder cue gains are CLAMPED
    "cues": [                                          # SFX one-shots
      {"t": 0.0,  "file": "assets/common/sfx/riser.mp3",  "gain_db": -5},
      {"t": 1.4,  "file": "assets/common/sfx/whoosh.mp3", "gain_db": -7, "dur": 0.7},
      {"t": 12.6, "file": "assets/common/sfx/impact.mp3", "gain_db": -5, "dur": 1.0, "fade": 0.25}
    ]
  }

Per-cue: "dur" trims the SFX to that many seconds (with an automatic fade-out so the
tail never lingers — "fade" overrides the fade length, default 0.15s). "sfx_cap_db"
(plan key or --sfx-cap) is a hard ceiling: any cue gain above it is clamped with a
warning, so a single mis-specced one-shot can never jump-scare the viewer.

On success it writes a sidecar `<projdir>/audio_finish.json` (measured output
LUFS + what was layered) so the pipeline gate can verify the master cheaply.
"""
import argparse, json, os, subprocess, sys, pathlib, re

def die(msg): sys.exit("audio_finish: " + msg)

def ffprobe_dur(path):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","json", path], capture_output=True, text=True)
    try: return float(json.loads(r.stdout)["format"]["duration"])
    except Exception: die("could not probe duration of " + path)

def has_audio(path):
    r = subprocess.run(["ffprobe","-v","error","-select_streams","a","-show_entries",
                        "stream=index","-of","json", path], capture_output=True, text=True)
    try: return len(json.loads(r.stdout).get("streams", [])) > 0
    except Exception: return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--plan", help="audio.json with music + sfx cues")
    ap.add_argument("--music"); ap.add_argument("--music-gain", type=float, default=-18.0)
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--tp", type=float, default=-1.5)      # true-peak ceiling
    ap.add_argument("--sfx-cap", type=float, default=None,
                    help="hard ceiling for per-cue SFX gain_db (default -4; plan sfx_cap_db overrides)")
    ap.add_argument("--out")
    a = ap.parse_args()

    video = a.video
    if not os.path.exists(video): die("video not found: " + video)
    if not has_audio(video): die("render has no audio track (VO missing) — nothing to master")
    vdur = ffprobe_dur(video)

    plan = {}
    if a.plan and os.path.exists(a.plan):
        plan = json.loads(pathlib.Path(a.plan).read_text())
    music = a.music or plan.get("music")
    music_gain = plan.get("music_gain_db", a.music_gain)
    cues = plan.get("cues", [])
    cues = [c for c in cues if os.path.exists(c.get("file",""))]   # skip missing sfx
    sfx_cap = a.sfx_cap if a.sfx_cap is not None else float(plan.get("sfx_cap_db", -4.0))
    if music and not os.path.exists(music):
        print("audio_finish: WARN music not found, skipping:", music); music = None

    out = a.out or re.sub(r"\.mp4$", "_final.mp4", video)

    # ---- build inputs + filtergraph (input 0 = VO from the render) ----
    inputs = ["-i", video]; idx = 1; fc = []
    if music:
        # split VO: one copy into the mix, one as the sidechain key for ducking
        fc.append("[0:a]asplit=2[vo][vokey]")
        mix_labels = ["[vo]"]
        inputs += ["-stream_loop","-1","-i", music]
        fc.append(f"[{idx}:a]volume={music_gain}dB,aformat=channel_layouts=stereo[mus]")
        fc.append("[mus][vokey]sidechaincompress=threshold=0.04:ratio=8:attack=5:release=260[ducked]")
        mix_labels.append("[ducked]")
        idx += 1
    else:
        mix_labels = ["[0:a]"]            # no ducking key needed
    applied = []
    for n, c in enumerate(cues):
        inputs += ["-i", c["file"]]
        ms = max(0, int(round(float(c.get("t",0))*1000)))
        g  = float(c.get("gain_db", -6))
        if g > sfx_cap:
            print(f"audio_finish: WARN cue t={c.get('t')} {os.path.basename(c['file'])} "
                  f"gain {g}dB exceeds cap — clamped to {sfx_cap}dB")
            g = sfx_cap
        chain = f"[{idx}:a]"
        cue_dur = c.get("dur")
        if cue_dur is not None:
            cue_dur = max(0.1, float(cue_dur))
            fade = max(0.05, float(c.get("fade", 0.15)))
            fade = min(fade, cue_dur)
            chain += f"atrim=0:{cue_dur:.3f},afade=t=out:st={max(0.0, cue_dur-fade):.3f}:d={fade:.3f},"
        chain += f"adelay={ms}:all=1,volume={g}dB[s{n}]"
        fc.append(chain)
        mix_labels.append(f"[s{n}]")
        applied.append({"t": c.get("t"), "file": c["file"], "gain_db": g,
                        **({"dur": cue_dur} if cue_dur is not None else {})})
        idx += 1
    n_in = len(mix_labels)
    fc.append("".join(mix_labels) + f"amix=inputs={n_in}:normalize=0:duration=first[premix]")
    fc.append(f"[premix]loudnorm=I={a.lufs}:TP={a.tp}:LRA=11[outa]")
    filtergraph = ";".join(fc)

    cmd = ["ffmpeg","-y", *inputs,
           "-filter_complex", filtergraph,
           "-map","0:v","-map","[outa]",
           "-c:v","copy","-c:a","aac","-b:a","256k",
           "-t", f"{vdur:.3f}","-movflags","+faststart", out]
    print("audio_finish: layering", ("music + " if music else ""), f"{len(cues)} SFX → mastering to {a.lufs} LUFS")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-2000:]); die("ffmpeg failed")

    # measure the master loudness (single-pass analysis) for the gate
    meas = subprocess.run(["ffmpeg","-i",out,"-af","loudnorm=print_format=json","-f","null","-"],
                          capture_output=True, text=True)
    li = None
    m = re.search(r'"input_i"\s*:\s*"(-?[\d.]+)"', meas.stderr)
    if m: li = float(m.group(1))
    projdir = pathlib.Path(video).resolve().parents[1]
    side = None
    # out/<slug>/<slug>.mp4 -> projects/<slug>/audio_finish.json if that projects dir exists
    slug = pathlib.Path(out).stem.replace("_final","")
    cand = pathlib.Path(__file__).resolve().parents[1] / "projects" / slug
    if cand.exists():
        side = cand / "audio_finish.json"
        side.write_text(json.dumps({
            "out": str(out), "measured_lufs": li, "target_lufs": a.lufs,
            "music": music, "music_gain_db": music_gain, "sfx_count": len(cues),
            "sfx_cap_db": sfx_cap, "cues_applied": applied
        }, indent=2))
    print(f"audio_finish: DONE → {out}" + (f"  (measured {li} LUFS)" if li is not None else ""))
    if side: print("audio_finish: wrote", side)

if __name__ == "__main__":
    main()
