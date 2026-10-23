# R12 · Denoise

**Style:** a prompt types out and an image resolves out of noise like a generation preview, in forty visible
steps. The camera dives through it into a page that renders card by card, then pulls back into a wall of every
image.
**Made for:** the Stills page on Imagined Worlds (visions.joaoqueiros.com/stills). It's the page's intro film.
**Length:** 10 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · Canvas 2D · HTML · GSAP (one clock and its eases) · Python (score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 10-second 1920x1080 intro film in HyperFrames for the Stills page of my site, on #0b0a09.
The page's own prompt "/imagine stills --curated --upscaled" types out in IBM Plex Mono with an ember #ff6d3b
caret. On Enter, my still "Pure Form", a close-up of an eye, resolves out of noise like a generation preview:
mosaic, blur, grain and grey fall away in forty visible steps while the HUD counts "step 00 / 40".
The camera pushes in and dives through the pupil into the Stills page, which renders card by card in its real
one, two and three column rhythm, each card denoising on the beat. The last card turns out to be one tile of a
wall of all my stills: the camera pulls back as the other tiles resolve outwards from it, empty cells and a
"/imagine" caret in the corner, and the wall dims under the title "Stills" in Fraunces with
"Hand-picked from thousands of generations." below.
No counts anywhere: the collection grows.
Technique: one painter draws every frame from time; one denoise function draws any image at any step on a
canvas (downscale for the mosaic, a blur filter, desaturation and seeded grain); camera keyframes with zoom in
log space.
Score: compose it in code with numpy, D major: a tick per typed letter, a click on each of the forty steps, a
bell when the eye is clean, a whoosh into the dive, a rising note per card and one hit for the title.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}, on {background}.
The prompt "{prompt}" types out, then {hero_image} resolves out of noise in forty visible steps
(mosaic, blur, grain and grey fall away) while the HUD counts them.
The camera dives through {focus_point} into {page}, which renders card by card, each card denoising on the beat.
The last card becomes one tile of a wall of {collection}; pull back as the tiles resolve outwards, then dim the
wall under the title "{title}".
One painter draws every frame from time; one denoise function draws any image at any step.
Score composed in code: a click per step, a rising note per card, one hit for the title.
```

Ideas: a product range resolving into a shop's grid; a photographer's portfolio from one portrait; a
lookbook where the dive goes through a button; a team page from one face to every face.

## How it's built

1. **One denoise function.** `denoise(ctx, img, p)` draws an image at progress p, rounded to one of forty steps.
   Early steps draw it tiny and scale it up without smoothing (the mosaic), with a blur and low saturation; seeded
   grain sits on top and fades as the steps run out.
2. **Seeded grain.** Six noise tiles are made once from a seeded random function, so every render is the same.
3. **The dive.** At the last step the canvas hands over to the clean image, which zooms 26 times about the pupil
   with an expo ease, in log space, so the push feels even.
4. **The page renders.** The page's cards are canvases in their real layout. Each one starts on the beat and
   denoises in 0.85 s while the camera moves down the column.
5. **Card to wall.** The last card and tile 18 of the wall share the same screen size at the swap, so the cut is
   invisible; the other tiles resolve outwards by their distance from it.

## Gotchas worth knowing

- Quantise the progress into steps. A smooth denoise reads as a blur; forty hard steps read as a generation.
- Hand over from the canvas to a plain image before the big zoom: a canvas the size of the frame goes soft when
  it's scaled up 26 times.
- Match the last card and its wall tile in screen size at the swap, or the cut shows.
- Load the images before building the timeline: the denoise draws them onto canvases, and a canvas drawn
  before its image has loaded stays empty.
