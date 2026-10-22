# R07 · Gommage

**Style:** an image doesn't cut or fade. It comes apart from one edge into thousands of small leaves, each one
the colour of the spot it left; a wind gathers them into one swirling cloud, and they settle into the next image.
**Made for:** Imagined Worlds, the Stills collection on visions.joaoqueiros.com (Midjourney images by João Queirós).
**Length:** 26 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPURenderer, WebGL2 backend) · TSL · GSAP (one clock) · Python (score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 26-second 1920x1080 film in HyperFrames from two of my Midjourney stills: "Lantern Festival" and "Sea of
Blooms". Lantern Festival holds full frame with a slow push-in. Then a gold-edged dissolve front crosses it from
left to right and the picture comes apart into about 32,000 small leaves, one per 8 px cell, each carrying the
colour of the spot it left. A gust throws them up and to the right, then they gather into one slow swirling
cloud in the dark. The cloud opens and the leaves fall, bottom up, each into a random place in Sea of Blooms,
turning to that spot's colour as the picture resolves under them. A few keep drifting. End on "Stills ·
Midjourney", "Imagined Worlds" and visions.joaoqueiros.com/stills, bottom left over a soft shade.
Call the style Gommage, the name the effect goes by, but take nothing else from the game it comes from.
Technique: Three.js WebGPURenderer with the WebGL2 backend and TSL. Two image planes whose opacity comes from a
noise-shaped front in time; instanced sprite leaves whose birth and landing times use the same front functions,
so leaf and picture always agree. Every position comes from time and a per-leaf seed: no simulation. Bloom pass.
Score: compose it in code with numpy: an autumn waltz in 3/4, D minor to F, felt piano and string pads, wind, and
a leaf rustle that follows how many leaves are in the air.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames.
{image_a} holds, then comes apart from {edge} into {n} small {particle_shape}s in its own colours.
A wind {wind_path}, and they settle {direction} into {image_b}.
Close on {final_line} and {url}.
Three.js with TSL: image planes masked by a noise front in time, instanced sprites using the same front.
Score composed in code: {score_idea}, with a rustle that follows the particles in the air.
```

Ideas: a product shot breaking into its own ingredients, a before photo settling into the after, a season
changing on the same landscape, a logo dissolving into confetti on a launch day.

## How it's built

1. **Fronts, not a simulation.** Each spot of the frame has a time it leaves image A (left to right, shaped by
   noise) and a time it lands in image B (bottom up). Both are small functions of position, written once and used
   by the planes and by the leaves, so a leaf always appears exactly where the picture vanishes.
2. **One leaf per cell.** 32,400 instanced sprites, one per 8 px cell of A, each assigned a random cell of B. A
   leaf samples A at its start for its colour and B at its target, and blends between them as it lands.
3. **A path from time.** Between leaving and landing, a leaf's position is an eased line from start to target plus
   a gust, a spiral, a curl of noise wind and, mid-flight, a pull into a shared two-arm vortex. Nothing is stored
   between frames.
4. **A leaf in the fragment shader.** The sprite's alpha is two curved edges meeting at the tips, with a darker
   midrib, so no texture is needed.
5. **Gold at the edges.** The dissolve front adds gold for a fraction of a second where the picture is about to
   leave, and new leaves start warm; a bloom pass makes both glow.
6. **Sound from the same fronts.** The rustle's density is the share of leaves in the air at each moment, computed
   from the same leave and land times.

## Gotchas worth knowing

- Hide the WebGL extension KHR_parallel_shader_compile and render a few warm-up frames before the first capture,
  or the first frame of a render can come out blank.
- Thousands of small moving leaves are hard to compress: check the web encode up close and expect a bigger file
  than a flat film.
- An evenly spread cloud of particles reads as static. Pull them into a shape mid-flight and leave dark space.
