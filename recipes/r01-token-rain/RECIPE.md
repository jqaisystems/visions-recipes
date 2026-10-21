# R01 · Token Rain

**Style:** text dissolves into particles, the particles flow through a sequence of gates, then recompile into new text.
**Made for:** Prompt Engineering, JQ AI SYSTEMS (ai.joaoqueiros.com/services/prompt-engineering).
**Length:** 26 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPURenderer on its WebGL2 backend) · TSL shaders · GSAP · Canvas 2D · numpy for the score.
**Cost:** €0. Everything here is free and open source.

## The prompt

This is the brief I gave Claude Code (with the HyperFrames skills installed) to start the film.

```
Make a 26-second 1920x1080 film in HyperFrames for my Prompt Engineering service.
Story: a prompt types "write a launch post for our new product" and a stock AI paragraph streams back,
full of clichés. A teal scan line sweeps the paragraph and flags seven anti-patterns with small mono tags
(cliché opener, hype, buzzword, empty verb, cliché, em dash, "not x, it's y"). The flagged phrases burn
into glowing token particles, then the rest of the draft dissolves too. The camera dives with the rain
of tokens through three glowing rings labelled 01 DRAFT, 02 CRITIQUE, 03 REWRITE; the tokens change
colour at each ring. They land and recompile as one line in Instrument Serif: "Same model. Your voice."
Spare tokens collapse into a glowing rule under it, then my logo, "Prompt Engineering" and the URL.
Technique: Three.js WebGPURenderer (WebGL2 backend) with TSL. Sample the real glyph pixels of the DOM text
so the particles start exactly where the letters were. Every particle position must be a pure function
of time (seeded start, fall, helix through the rings, landing), no simulation state, so the render is
deterministic. Brand: #111110 background, #F5F5F0 text, #00A89D teal, Geist and Geist Mono.
Score: compose it in code with numpy, synced to the same timing table as the picture.
No beat punches on held text. Hold the final line about 4 seconds.
```

## Remix it

Swap the bracketed parts and paste it in:

```
Make a {duration}-second {width}x{height} film in HyperFrames.
A {source_text} appears. A scan line flags {what_is_wrong} with small labels. The flagged parts burn
into particles sampled from the real glyph pixels, then the rest dissolves. The particles fall through
{n} glowing rings labelled {gate_labels}, changing colour at each ring, and recompile as {final_line}.
Close on {lockup}. Palette: {palette}. Fonts: {fonts}. Three.js WebGPURenderer (WebGL2 backend) + TSL,
every particle a pure function of time. Score composed in code, synced to the picture.
```

Ideas: bad code turning into clean code, a messy inbox becoming one reply, raw data rows becoming a chart
label, a long contract becoming one sentence.

## How it's built

1. **Glyph-exact dissolve.** At setup the page measures every word, draws it on an offscreen canvas at the same
   pixel position and samples its pixels: 29,872 particles start inside the real letters. Each particle is released
   by a left-to-right burn sweep, and a CSS clip wipe hides the word at the same moment, so text turns into
   particles with no visible seam.
2. **One equation per particle.** A TSL shader computes each particle's position from time alone: float, fall
   (smoothstep), a helix that tightens through each ring (a gaussian funnel), noise turbulence, then landing on a
   pixel of the final line. 88,872 sprites in total, including rain from above and depth dust.
3. **A camera that rides the rain.** The camera follows the same smoothstep as the particles' mean fall, sitting
   above the stream and looking down into it. The DOM layer rides the same camera function, so type and particles
   never drift apart.
4. **Light.** Additive blending plus a bloom pass; colour changes as the particles cross each ring.
5. **Sound.** The score is generated in Python from the same timing table and the per-word times from the page:
   key ticks, a blip per streamed word, a ping per flag, a granular crackle for the burn, a pulse through the dive,
   three chimes at the rings, an F major landing and a Bbmaj9 close. Mixed to -17 LUFS.

## Gotchas worth knowing

- Render with one worker (`--workers 1`). With parallel workers, the first frame of each chunk drew the GL scene
  with a stale time and lost its particles. One worker renders all 780 frames clean in about a minute.
- Words set to `display: inline-block` report the full line height, not the glyph height. Centre the glyph in the
  box before sampling, or the particles start a few pixels off.
- Build the timeline inside the async setup and register it last, after fonts load and the layout is measured.
