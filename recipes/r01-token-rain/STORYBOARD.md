---
message: "Same model. Your voice."
mode: collaborative
duration: 26
---

# Token Rain · storyboard

One continuous take: a single Three.js stage (`#tr-gl`) under DOM type layers. The camera never cuts; DOM
"world" content rides the same camera function as the particles, so the seams are camera moves and
particle moves, never fades. Timings are constants in `index.html` (`T`).

## Frame 1 · Prompt (0 to 4.6 s)
status: outline
src: index.html
motion: `prompt-type-submit-generate` (blueprint); rules `discrete-text-sequence`, `context-sensitive-cursor`
beat: a HUD rule draws; a mono prompt types "write a launch post for our new product"; enter; a stock AI
paragraph streams back word by word.

## Frame 2 · Anti-pattern scan (4.6 to 9.4 s)
status: outline
src: index.html
motion: rules `css-marker-patterns` (highlight), `particle-burst` (glyph dissolve, GPU form)
beat: a teal scan line sweeps the paragraph; seven clichés light up with mono tags (cliché opener, hype
verb, buzzword, em dash...). They burn into teal token particles left to right; then the rest of the draft
dissolves into grey tokens.

## Frame 3 · The chain (9.4 to 15.8 s)
status: outline
src: index.html
motion: rules `3d-camera-flight` (GL camera form), `ambient-glow-bloom`
beat: the camera dives with the rain; tokens helix through three glowing rings: 01 DRAFT, 02 CRITIQUE,
03 REWRITE, changing colour at each pass.

## Frame 4 · Recompile (15.8 to 21 s)
status: outline
src: index.html
motion: rules `depth-scatter-assemble` (GPU form), `sine-wave-loop` (one drift)
beat: the rain lands as "Same model. Your voice." in Instrument Serif; sharp type takes over; a halo of
spare tokens breathes around it. Held about 4 s.

## Frame 5 · Lockup (21 to 26 s)
status: outline
src: index.html
motion: blueprint `titlecard-reveal`; rules `svg-path-draw` (rule form), `waterfall-entry`
beat: the halo tokens collapse into a teal rule; JQ AI SYSTEMS logo wipes in; "Prompt Engineering" and the
URL arrive; hold to the end.
