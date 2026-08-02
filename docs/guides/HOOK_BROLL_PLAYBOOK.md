# HOOK + B-ROLL PLAYBOOK

Reference learnings mined from high-performing AI-news reels. Apply to Retrofit hooks.
Check this BEFORE writing a hook/cold-open. Each new strong reference adds a row.

## STANDING RULE (the owner, 2026-06-19; HARDENED 2026-06-22) — full-screen purple-cow hook is MANDATORY
- EVERY Retrofit/short video OPENS with a ~4-5.5s FULL-SCREEN surreal "purple cow" AI hook starring
  the owner himself (metaphor = the headline). NON-SKIPPABLE — the daily cron shipped videos WITHOUT it
  (06-22) and the owner flagged it. Build it FULL-BLEED (full 1080×1920), never a small contained scene.
- Skip it ONLY when something genuinely more important must open (e.g. iconic official keynote footage)
  — and say so in idea.md.
- The hook VOICEOVER must be tightly RELEVANT to the on-screen B-roll — write the VO to match/describe
  the surreal visual metaphor (visual = the headline), never a generic line.
- **PROVEN RECIPE = the PREMIUM i2v path below (`tools/ai_assets/prem_i2v.py`), not just Kling v2.1.**
  Reference: retrofit-2026-06-21 hero (<example-link>), script `tools/_hero_proto2.sh`.

## Reference #1 — Vaibhav Sisinty "GLM 5.2 beats Claude" (IG reel DZsIUgxpsha, 2026-06-19)
Stats: 56s, 3.3K likes, **3.7K comments** (comments > likes = comment-gate working hard).
Source files: `topic_fetch/ig_analyze/` (reel.mp4, transcript reel_audio.json, frames_grid.jpg, hook_grid.jpg).

### The hook formula (first 5s) — STEAL THIS
The cold-open is NOT the talking head. It's two bespoke **AI image-to-video** clips
(Sora/Kling/Veo-class) that do 4 jobs before the presenter appears:
1. State the claim   2. Name the product   3. Signal the category   4. Land a JOKE.

- **0–3.2s Clip A "metaphor-literal":** AI lookalike reclining on a bamboo raft floating on a
  river of chili-oil broth + giant dumplings; a small Chinese flag planted (flag-plant = "China
  claimed this"). He pulls up a phone showing the product screen ("GLM 5.2") IN-WORLD.
- **3.2–5s Clip B "incumbent reacts":** a Western/"SF" stand-in eats dumplings from a blue-white
  porcelain bowl, fishes the product phone out of the soup, reacts with exaggerated shock.
- **~5s:** cut to real talking head to begin the explainer.

### Transferable principles
1. **Visual = the headline, not decoration.** "X beats Y" → show Y literally choking on X's thing.
   Build the metaphor; don't caption over stock.
2. **Pattern-interrupt + humor + payload in <5s.** Surreal/impossible image stops the scroll;
   a joke earns the watch-past-3s; the product reveal rides inside the entertainment.
3. **Place the product IN-WORLD** (phone/screen inside the surreal clip) so the brand never
   interrupts — it's part of the gag.
4. **Anchor on appetite/texture/culture cues** (food, color, a flag) — instantly readable, no text needed.
5. **Caption rhythm:** 2–3 word highlighted chunks, one per beat (magenta box + italic serif),
   synced to the visual beats.
6. **Rivalry / named-enemy framing** ("X just beat [BigName] at its own game") = built-in
   controversy → comments → reach. Reusable cold-open template.

### Structure of the whole reel (for reference)
HOOK (0-5 surreal) → REVEAL+SPECS (name it, 3 concrete specs) → PROOF (one concrete demo,
side-by-side vs rival) → HOW-TO (remove friction, "you could do this now") → CTA STACK
(comment-trigger + follow + community link).

### Growth mechanic
"Comment GLM → I'll DM the guide" (ManyChat-style trigger) manufactures comments (3.7K > likes)
that juice the algorithm AND build a DM list. Heavy (3 CTAs in 9s) — test before adopting wholesale.

### ⚠️ Truth guard
The "10x stronger / beats Claude" claims were creator marketing on a single cherry-picked test,
NO benchmarks cited. If building on such a topic: frame as "strong open-source contender," cite
real evals, never parrot unverified "10x / beats X" hype (the owner: truth over hallucination).

### How to produce this hook in our pipeline
- Generate 2 bespoke AI clips (image-to-video) for the metaphor — not stock. Tools: image_generate
  for stills → image-to-video model, or sourced gen clips. Dense-keyframe re-encode before render.
- Keep the surreal clips full-bleed; product screen composited in-world; talking head starts ~5s.
- Log the look in `projects/PRODUCED.md` STYLE LOG so the 3-day visual cooldown stays honest.

## Kling v2.1 i2v recipe (Replicate) — generate hooks starring the owner himself
Use the owner's own A-roll talking-head still as the START FRAME so the hook star is really him.
Generator template: `topic_fetch/ig_analyze/gen_hooks.py`.
- Model `kwaivgi/kling-v2.1`; inputs: prompt, start_image(file), duration(5|10 only), mode(standard|pro),
  negative_prompt. Auth header `Authorization: Token <key>` (token in hf-agent/.env). SDK in venv.
- Price: standard $0.05/s, pro(1080p) $0.09/s. 5s pro = $0.45. Min 5s → trim for 3s hooks. ~2min/clip.
- replicate.delivery URLs expire ~1h; if download times out the prediction still succeeded —
  GET /v1/predictions and re-fetch the output URL.
- Discord DM cap ~10MB: re-encode clips (libx264 crf23 native res ≈2.5-3MB) before attaching.

### Hard rules learned from the first test batch (DO every time)
1. **CLEAN start frame** — no burnt-in watermark/subtitle on the A-roll still (they stay baked on-screen
   the whole clip). Strip overlays first.
2. **Trim to 3-4s** — the last ~1s always degrades (body ghosting/double-exposure, face occlusion,
   eyewear drift). Hooks only need 3-4s.
3. **Keep surreal elements in lower-third / to the side** — never let them grow up over the face/chest
   ("nothing on the face" rule).
4. **Negative prompt** must include "changing glasses, morphing face, deforming eyeglasses, plastic skin"
   — Kling drifts eyewear/face over 5s.
5. **One hand system** — don't show a robotic hand AND his real hands acting at once.
6. Output is **silent** — add SFX/VO in the edit.

### Voiceover rule (the owner, 2026-06-19)
The hook VO must MATCH the surreal B-roll metaphor, not run generic. Write the visual first, then a VO
line that describes/pays off that exact image (e.g. city growing from desk → "It built the whole app
while you slept."). Visual = headline; VO = the punch that lands it.

## PREMIUM i2v recipe (the owner, 2026-06-22) — the proven full-screen hero path
Two-stage: photoreal START STILL → premium image-to-video. Proven on retrofit-2026-06-21
(<example-link>); reference script `tools/_hero_proto2.sh`.

1. **START STILL (full-screen 9:16, grounded on the owner's real face):**
   `python3 tools/ai_assets/replicate_gen.py image -p "<photoreal scene prompt>" --ref-image <clean
   front-facing the owner A-roll frame> --ratio 9:16 --resolution 2K -o <dir> --prefix herostart`
   (Nano Banana 2). GPT-image-2 is the alternate. Spec REAL props (a real monitor, NOT a floating
   hologram); photoreal lighting; no on-screen text. Grounding on his real frame = it's actually him.
   - **PRODUCT-GROUNDED HERO (the owner, 2026-06-23) — MANDATORY when the video is about a real product.**
     `--ref-image` is REPEATABLE: pass the real product photo as a SECOND reference alongside the owner's
     face frame (`--ref-image <face_frame> --ref-image <product_photo>`), and in the prompt say
     "the owner wearing/holding the EXACT product shown in the second reference image". This makes the hero
     show him with the GENUINE product (e.g. the actual Snap Specs) instead of a generic AI-imagined
     gadget. WHY: on the 06-23 Snap Specs hero the AI invented a generic pair of glasses because only
     his face was referenced — the real product photo (official press shot / our `assets/photos/*`) was
     never fed in. Always source the product reference FIRST (step 4b official-source-first) and feed it
     to the hero gen. If the metaphor needs the product worn/used, ground on BOTH refs every time.
2. **MOTION:** `python3 tools/ai_assets/prem_i2v.py --model <hailuo|seedance|kling> --resolution
   1080p --duration 6 --start <herostart.png> --prompt "<precise surreal action>" --out <hero.mp4>`.
   - Models (input keys handled by the tool): `hailuo`=minimax/hailuo-02 (strongest physics, PREFER
     for the hero), `seedance`=bytedance/seedance-1-pro, `kling`=kwaivgi/kling-v2.5-turbo-pro,
     `veo`=google/veo-3-fast. `--end` for a last-frame on hailuo/seedance/kling.
   - Describe the action concretely (e.g. "a robotic arm extends OUT from inside the monitor screen,
     reaches across the desk, and grabs the red apple") — physics models reward specific motion.
3. Dense-keyframe re-encode before embedding; place FULL-BLEED. Output is silent — add SFX/VO in edit.

### Cost cheat-sheet (Replicate, pulled live 2026-06-21)
- **Images:** nano-banana-2 — 1K $0.067 / 2K $0.101 / 4K $0.151.  gpt-image-2 — low $0.012 /
  medium $0.047 / high $0.128.
- **Video (i2v):** hailuo-02 (flat/clip) — 1080p 6s $0.48, 768p 6s $0.27, 512p 6s $0.10 (6s/10s only).
  seedance-1-pro (per s) — 480p $0.03 / 720p $0.06 / 1080p $0.15.  seedance-2.0 (per s, ~$0.18/s @1080p).
  kling-v2.5-turbo-pro $0.07/s ($0.35/5s).  veo-3-fast $0.10/s (no-audio) / $0.15/s (audio).
  wan-2.2-i2v-fast — flat $0.05–$0.145/clip (cheap in-between motion).
- **Example one hero clip** (GPT-image-2 high still + seedance 1080p): 5s ≈ $0.13+$0.75 ≈ $0.88;
  hailuo-02 1080p 6s + nano-banana 2K still ≈ $0.48+$0.10 ≈ $0.58.

### Likeness guard (every the owner shot)
- ALWAYS ground on a REAL clean front-facing A-roll frame (`--ref-image` / `--start`). NEVER invent
  his face. Negative-prompt face/eyewear drift ("morphing face, deforming glasses, plastic skin").
  Label "AI edit of your likeness" in the step-4b approval shortlist; he approves each.

## Reference #2 — Vaibhav Sisinty coffin / founder-reveal (IG reel DZt98OzJ3-t, 2026-06-23)
Hook: he walks to an open COFFIN with funeral flowers, lifts the lid, and Anthropic's FOUNDER
(Dario-style figure) climbs out alive → payoff "revive Fable 5 with this one free tool, use it
before it gets deleted." Caption CTA "Comment Fable". A textbook purple-cow cold-open: a literal,
shocking, impossible image that IS the headline ("the model everyone called dead is alive again").

### Why it works
- **Funeral = "it's dead" made literal.** The abstract claim ("a deprecated/killed model") is staged
  as a real-world ritual (coffin + flowers) the eye reads instantly with zero text.
- **The reveal is a TURN, not a frame.** Setup (walk up, somber) → action (open lid) → payoff (founder
  climbs out) → meaning ("you can bring it back"). The micro-story earns the watch-past-3s.
- **Recognizable face = the punchline.** It's not a random actor — it's the company's FOUNDER, so the
  brand and the stakes land in one beat without a caption.
- **Image = message on mute.** Mutes-scroll readable: dead thing → opened → alive. The VO only confirms.

## ⚡ PURPLE-COW PRINCIPLES (consolidated — apply to EVERY Retrofit hero hook)
Seth Godin's "purple cow" = be remarkable or be invisible. Our hook is the purple cow. Distilled from
Ref #1 (dumpling-raft) + Ref #2 (coffin/founder). Check these every time you spec the hero:
1. **PERSONIFY the abstract.** Put a HUMAN in the metaphor — the owner himself, or a recognizable FOUNDER /
   mascot / rival stand-in. People stop for faces + bodies doing impossible things, not for graphics.
2. **ONE bold metaphor that maps EXACTLY to the headline stakes.** "X is dead" → a coffin. "China beat
   the West" → the West choking on China's dumplings. Don't decorate — literalize the claim. One idea,
   not three.
3. **STAGE A MICRO-REVEAL, not a static frame.** The strongest hooks have a TURN: setup → action →
   reveal/payoff inside the first ~4-5s (lid opens, arm reaches out, founder climbs out). A still
   surreal image is weaker than a surreal image that *resolves*.
4. **Make it readable ON MUTE.** If the visual alone doesn't communicate the headline with sound off,
   it's not done. VO confirms/punches; it never carries the meaning alone.
5. **Place the product/brand IN-WORLD** — a phone showing the model in the scene, the founder as the
   reveal — so the brand rides inside the gag and never interrupts as an overlay.
6. **Commitment > budget.** A fully-committed silly/surreal idea (real coffin, real funeral flowers)
   beats a glossy generic one. Go all-in on the bit; half-commitment reads as cringe.
7. **Charged imagery, factual honesty.** The IMAGE can be wild; the CLAIM must stay true (truth guard).
   Don't let a dramatic metaphor imply a benchmark/fact we can't cite.
8. **RELATABILITY — use a metaphor the viewer ALREADY lives.** Remarkable only works if it's anchored to
   something the audience instinctively knows/feels. Pull the metaphor from EVERYDAY HUMAN experience
   (death/funeral, a job interview, getting fired, a doctor's diagnosis, a race, a courtroom, a wedding,
   a heist, sports, school exam) — NOT from inside-baseball tech imagery (no abstract "neural network /
   glowing brain / data streams"). The viewer should feel "I know that situation" in <1s, BEFORE they
   know the AI topic. Universal-emotion test: pick the metaphor by the FEELING the headline triggers
   (fear of being replaced → robot at your desk in your chair; the underdog wins → David vs Goliath;
   it's obsolete → museum / fossil), then cast the AI subject into that human scene.
9. **CLEAR MESSAGE — one sentence, said out loud before you build.** Before specing any hero, write the
   ONE takeaway in a single plain sentence ("Chinese open model just beat the US giants for free").
   The hook must deliver THAT and only that — not three sub-points. If you can't say it in one breath, or
   the metaphor needs a caption to be understood, it's not clear enough → simplify. The visual answers
   "what + so-what" instantly; the VO just confirms. Cut any prop/character that doesn't serve the one
   sentence.

### HOOK GENERATION FORMULA (use this to brainstorm — fill every slot)
Run this for every video to manufacture the hero on purpose instead of hoping for inspiration:
1. **MESSAGE** = the one-sentence takeaway (principle 9). Write it first, verbatim.
2. **STAKE EMOTION** = the single feeling it triggers (replaced / saved / robbed / freed / outclassed /
   resurrected / exposed). Pick ONE.
3. **HUMAN SCENE** = the everyday situation that universally carries that emotion (principle 8). List 3,
   pick the most visual + most universal.
4. **CAST** = drop the AI subject INTO that scene as a character — the owner, a recognizable FOUNDER, a
   rival stand-in, a mascot, or the product-as-object. The face/brand IS the punchline (principle 1+5).
5. **THE TURN** = the action that resolves setup→reveal inside ~4-5s (principle 3). Name the literal
   beat (lid opens → founder climbs out; robot sits in YOUR chair → spins around; old model wheeled
   into a museum case).
6. **MUTE CHECK + TRUTH CHECK** = does the silent visual alone say the MESSAGE (principle 4), and does
   the wild image still keep the claim factually honest (principle 7)? If either fails, redo 3-5.
Output of the formula = the hero prompt for the PREMIUM i2v path below.

### PASS / FAIL self-test (Director gate before approval)
A hero hook is APPROVED only if ALL are yes — else send back:
- [ ] I can state the MESSAGE in one plain sentence.
- [ ] The metaphor is an EVERYDAY human situation (not abstract tech imagery).
- [ ] A scroller with sound OFF gets the message in <2s.
- [ ] There is a TURN (action/reveal), not a static surreal frame.
- [ ] A human/face/brand is IN the scene as the point, not decoration.
- [ ] One idea only — nothing extra to explain.
- [ ] Wild image, but the underlying claim is true + citable.

### How to produce (our pipeline)
- Build it via the PREMIUM i2v path (`tools/ai_assets/prem_i2v.py`) grounded on the owner's real A-roll
  frame (and the product photo when relevant) — see the PREMIUM i2v recipe above. Full-bleed 1080×1920,
  ~4-5.5s, the reveal-turn inside it, silent → add SFX/VO in the edit. Log the look in `PRODUCED.md`.

## 🎬 B-ROLL GENERATION IDEOLOGY (the owner, 2026-06-23 — from 3 Vaibhav Sisinty reels: coffin/Dario, Ideogram fisheye, Kunal-Shah origin-story)
The purple-cow rules above govern the OPENING hero. This governs EVERY b-roll shot in the BODY. The
through-line across all three reels: **b-roll is the ARGUMENT made visible, not decoration.** Each shot
literalizes one line of the script so a muted viewer follows the whole story by pictures alone.
1. **ONE CLAIM = ONE SHOT (line-by-line literalization).** Write the script FIRST, then assign every
   sentence its own concrete visual that SHOWS that sentence. "Family went broke at 14" → a staged
   recreation of that moment; "sold pirated CDs" → CDs in hand; "$900M for 20%" → the money/handshake;
   "3B users but barely earns" → a packed crowd + an empty till. No sentence floats over generic stock.
2. **LITERAL > ABSTRACT.** Concrete real-world objects/people/scenes (coffin, phone-in-hand, CDs, a
   door, a CEO chair) beat abstract tech imagery (data streams, glowing brains, neural nets). The image
   must DECODE to the words on mute. If you need a caption to explain the b-roll, the b-roll is wrong.
3. **REAL, RECOGNIZABLE SUBJECTS = credibility.** Named products with their real logos (Nano Banana,
   Ideogram), the actual founders (Dario, Kunal Shah — grounded on real photos), real phone screens
   showing the genuine result. Specificity sells; generic avatars/props read as filler.
4. **STAGED ACTION + MOTION, never a static frame.** Every shot has a verb: walks toward camera, opens
   the coffin, lifts the phone, takes off one jacket and puts on another, hands over keys. Motion stops
   the scroll; a TURN (setup→reveal) inside the shot carries meaning. Prompt i2v with action verbs, not
   static descriptions.
5. **SHOW THE PAYOFF PHYSICALLY ("show, don't tell").** Put the result in-hand — the phone screen with
   the actual output, the product held up to camera — instead of narrating it.
6. **BIOGRAPHY/STORY = RECREATE THE SCENES.** For an origin-story or narrative beat, generate
   illustrative recreations of each life moment (kid in a struggling home, teen selling CDs), not a
   talking-head over text. Charged + emotional, but a factually honest recreation (editorial framing
   for real people; never imply a false action).
7. **OWN A SIGNATURE WRAPPER.** His fisheye walk-in + pink word-by-word captions + two-zone layout are
   the same every video = instant brand recognition. Ours = the Cars24 cutout house style + our caption
   system; keep it consistent so only the CONTENT changes.
8. **B-ROLL GETS ITS OWN ZONE — face never covered.** Top = graphic/b-roll card, bottom = host (or
   host steps aside per the cutout choreography). The b-roll is never slapped over his face.

### How to produce b-roll (our pipeline)
- **Storyboard from the script:** one image/i2v prompt PER LINE. For each, write the literal scene + an
  action verb. Generate the still (`tools/ai_assets/replicate_gen.py image`, Nano Banana 2 / GPT-image-2)
  → animate (`tools/ai_assets/prem_i2v.py`, hailuo/seedance/kling) → dense-keyframe re-encode → place in
  its zone. Real people → ground on a genuine photo (`--ref-image`); real products → pass the product
  photo. Prefer official footage/screenshots first (OFFICIAL-SOURCE-FIRST rule) for real product shots,
  AI-generate the staged/metaphor/biography scenes. Stock is the last-resort gap-filler.
