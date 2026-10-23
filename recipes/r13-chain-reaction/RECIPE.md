# R13 · Chain Reaction

**Style:** a marble run built from the parts of a workflow, filmed like a product commercial. Real physics, baked
once, so the film can bend time: slow motion through one station, bullet time at the climax, then the whole run
pulls back into one glowing line that becomes a word.
**Made for:** AI Automation Systems (ai.joaoqueiros.com/services/ai-automation).
**Length:** 34 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL bloom) · Matter.js · GSAP · Python (word, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 34-second 1920x1080 film in HyperFrames for my AI Automation service, as a cinematic 3D chain reaction that
runs a weekly report: collect, clean, sort, review, send. Dark studio, #0a0a09, teal #00BFB4 light.
Build the machine in 2D with Matter.js and bake it once in Node: every body's position per frame into a data file,
every impact into a list. Render it in Three.js as a real 3D machine: brushed-metal rails with a line of teal light,
a chrome ball, a glass tray, glass Galton board with light pegs, a brass bell on a rope, bloom and reflections.
Open on "$ run weekly-report" typed on a smoked glass terminal; on Enter a chrome ball condenses out of teal light.
Collect: envelopes arc in from the dark and land on a glass seesaw tray, the ball tips it. Clean: dominoes printed
with messy spreadsheet rows that turn clean as they fall, in 0.3x slow motion, sparks at each strike. Sort: the pegs
light and ripple when hit. Review: a person's cursor ticks "Approve" and the gate lifts. Send: bullet time at the
bell, physics frozen for 2 s, sparks and the shockwave hanging in the air, the camera orbiting the strike; then the
report card flies to camera. Pull back to the whole run as one glowing line; it breaks into beads that fly into the
word "automation". End on "AI Automation Systems", the tagline and the URL.
The film's clock drives the physics clock through a remap, so slow motion and the freeze are just a curve; show the
clock's speed in the HUD. Station titles wipe on bottom left.
Score: compose it in code from the impacts, placed at their film time through the same remap; pitch impacts down in
the slow motion, drop the pulse in the freeze, ring the bell out of the thaw. A quiet pad in D minor under it all,
resolving to F on the word.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}, as a cinematic 3D chain reaction that
runs {workflow}: {station_1}, {station_2}, {station_3}, {station_4}, {station_5}.
Build the machine in 2D with Matter.js and bake it once: positions per frame, impacts as a list. Render it in
Three.js with {materials} and {accent} light, bloom and reflections.
Open on "{command}". Give each station a physical gag: {gag_1}, {gag_2}, {gag_3}, {gag_4}, {gag_5}.
Slow motion through {slow_station}, bullet time at {climax}. Pull back to the whole run as one line that becomes
the word "{word}". End on {title}, {tagline} and {url}.
Score from the impacts, through the same time remap, over a quiet bed in {key}.
```

Ideas: an e-commerce order running from cart to doorstep; a hiring pipeline from application to offer; a release
going from commit to production; a podcast episode from recording to every platform.

## How it's built

1. **Bake the physics.** The machine is built in 2D with Matter.js and run once in Node at 120 steps a second. Every
   moving body's position is stored for every frame, and every impact (time, bodies, speed) goes into a list. The
   film never runs physics; it reads the table, so any frame renders the same on its own.
2. **A clock that bends.** The film's clock maps onto the physics clock through a remap built from a speed curve:
   0.3x through the dominoes, a slow approach to the bell, a 2 s freeze, then back to 1x. The HUD shows that speed.
3. **The machine in 3D.** Every static part of the 2D run is extruded into a 3D piece; dominoes, the tray, the gate
   and the bell read their positions from the bake. Sparks and the shockwave live in physics time, so they hang in
   the air during the freeze while the camera keeps moving in film time.
4. **One camera operator.** The camera follows the moving ball, smoothed once up front with a little look-ahead, and
   blends between keyframes of distance, angle and lens; the bullet time is a keyframe pair around a fixed point.
5. **Line to word.** The ball's whole path is one tube that grows as it runs. At the end it is sampled into 1,500
   beads that fly onto points sampled from the word's outlines, then the filled word fades in.

## Gotchas worth knowing

- In Matter.js, don't lock a ball's rotation with infinite inertia: friction then pins its speed near zero. Let it
  spin.
- A floor needs real friction or dominoes slide instead of tipping; ramps can stay slippery.
- A slow ball on a shallow ramp creeps for seconds. Make the ramp after any stop steeper than the rest.
- Bloom eats light surfaces: keep white cards and paper below the bloom threshold, and let only the emissive teal glow.
- Faded-out meshes still write depth and punch holes in what's behind them; hide them once their fade completes.
