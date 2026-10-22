# R05 · Choosing a Colour

**Style:** every colour at once swirls like marbled ink, then a method takes over: the colours that don't fit
drain away, one colour pools out of the ink, and it separates into a few clean, labelled swatches.
**Made for:** the article "How to Choose Brand Colours That Actually Work for Your Business" (joaoqueiros.com).
**Length:** 26 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · HTML · WebGL2 (one fragment shader) · GSAP (one clock) · Python (score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 26-second 1920x1080 film in HyperFrames for my article "How to Choose Brand Colours That Actually Work
for Your Business". Story: full-frame marbled ink in every colour, and the line "Most brands start with “I like
blue.”" types over it. Then the article's five steps, each in a small card at the top left: 01 three adjectives
(clear, warm, precise) appear and every colour except teal and blue drains to warm grey; 02 twelve competitor
dots form a ring, most of them blue, with one empty slot labelled "the gap"; 03 the ink settles to dark and one
teal pool forms, with "#00A89D" typing beside it; 04 four swatches pour down from the top, 1 primary, 1
secondary, 2 neutrals (#00A89D, #0099D6, #1A1A18, #F5F5F0) with HEX and RGB; 05 the page turns light and the
palette appears on a business card, a web page, a social post, a dark and a light layout. End on "How to choose
brand colours that actually work." and joaoqueiros.com. All copy on screen paraphrases the article; no
statistics.
Technique: WebGL2, one full-screen fragment shader. No simulation: every pixel traces itself back through a
divergence-free flow field (the curl of moving noise) for 28 steps, then samples a dye of hue bands with pale
veins. Uniforms from one clock drive each step: drain, dim, pool, bands, fade. HTML carries the words.
Type: Manrope for labels and codes, Instrument Serif for the lines.
Score: compose it in code with numpy: wavering liquid pads and water drops, a note per competitor dot, a chime per
swatch climbing the chord, a D major resolve.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames.
Full-frame marbled ink in every colour while "{opening_line}" types.
Then {n} steps from {source}: {steps}, each one draining, dimming, pooling or separating the ink.
It ends as {k} swatches, {palette_with_codes}, tested on {applications}. Close on {final_line}.
WebGL2, one fragment shader, a time-only flow map, no simulation state. HTML for the words.
Fonts: {fonts}. Score composed in code: {score_idea}, from the same timing table.
```

Ideas: a paint brand's seasonal palette, a city's colours (river, stone, tiles) for a tourism page, a product
line's finishes, a data visualisation palette checked for colour blindness.

## How it's built

1. **A flow map, not a fluid sim.** Real fluid needs the previous frame, which breaks seeking. Here each pixel
   walks backwards through a moving flow field for 28 small steps and reads the dye where it lands, so any frame
   can be rendered on its own and the ink still swirls.
2. **The flow can't compress.** It's the curl of a noise field, so it is divergence-free: ink folds and stretches
   like marbling instead of bunching up.
3. **Dye with veins.** The dye is hue bands from noise, with a pale vein wherever the band index crosses a whole
   number, which reads as marbled paper.
4. **Steps as uniforms.** Draining keeps hues near teal and blue and moves the rest to warm greys; the pool is a
   circle with a noisy edge; the swatches fill down from the top with a wavy front. One clock sets them all.
5. **Slow the flow, don't stop it.** The step size shrinks as the method takes over, so the swirls relax instead
   of freezing.
6. **Sound from the same clock.** Drops thin out as the colours drain, the competitors share one note, and each
   swatch gets a chime as its label lands.

## Gotchas worth knowing

- Put shader source in a JavaScript string, not in a `<script type="x-shader">` tag: HyperFrames' lint reads every
  inline script as JavaScript.
- Create the WebGL context with `preserveDrawingBuffer: true` and draw inside the painter, so the frame the
  renderer captures is always the one painted for that time.
- White text on teal or bright blue fails contrast. Label those swatches in ink.
