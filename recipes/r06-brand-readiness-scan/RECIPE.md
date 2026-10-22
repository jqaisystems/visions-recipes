# R06 · Brand Readiness Scan

**Style:** an object is read by a scanner line. Behind the line it rises into a relief of glowing ridge lines,
and the scanner stops on one feature after another while a list ticks them off.
**Made for:** the free Brand Readiness Check (joaoqueiros.com/brand-readiness-check.html).
**Length:** 26 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · HTML · Canvas 2D · GSAP (one clock) · Python (score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 26-second 1920x1080 film in HyperFrames for my free Brand Readiness Check (8 questions, about 60 seconds,
a score out of 100). Story: my business card (JQ mark, João Queirós, Brand identity designer, joaoqueiros.com,
Porto, Portugal) lies in the dark as a flat outline. A teal scanner line sweeps across it and the card rises
behind the line into a relief of thin ridge lines. Then the scanner stops on eight features, one per question of
the check, about 1.5 seconds each: corner brackets frame the feature, it lights teal, a short label and the full
question appear under the card, and a list on the right ticks it off ("Brand Readiness Check · 3 / 8"). Small
proofs for some checks: the mark at 16 px, in one colour and on a van; a palette and two typefaces; margin
guides; vector anchor points on the mark; a dashed competitor card behind; the card lifting towards you. Then
the four bands as a scale (0 to 39 Starting point, 40 to 69 Growing pains, 70 to 89 Strong foundations, 90 to
100 Ready to scale), without claiming a score for my card. End on "Is your brand ready to grow?", "8 questions ·
about 60 seconds · a score out of 100" and joaoqueiros.com/brand-readiness-check.
Technique: Canvas 2D. Draw the card once into a height map (the mark from its SVG paths, the type, the edge),
blur it a little, then every frame redraw it as horizontal ridge lines lifted by height, back to front, each
filled below with the background so nearer lines hide farther ones. One painter computes every frame from time.
Look: #111110, teal #00A89D, bone #F5F5F0, grey lines. Manrope for labels, Instrument Serif for lines.
Score: compose it in code with numpy: a scanner drone and sweep, a two-note blip per check, a tick per tick,
four steps up for the bands, a C major resolve.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames.
{object} lies in the dark as a flat outline. A scanner line sweeps it and it rises into a relief of ridge lines.
The scanner stops on {n} features: {features}. Each lights up with its question: {questions},
and a list ticks it off. Then show {scale_or_result}. Close on {final_line} and {url}.
Canvas 2D: a height map drawn once, redrawn every frame as ridge lines lifted by height.
Palette: {palette}. Fonts: {fonts}. Score composed in code: a drone, a blip per check, from the same timing table.
```

Ideas: a product's packaging checked against a launch list, a website screenshot scanned for accessibility
issues, a floor plan scanned room by room, a contract scanned for its key clauses.

## How it's built

1. **A height map, drawn once.** The card is painted in greys on an offscreen canvas: the mark brightest (from
   its four SVG paths), the name and title a little lower, the card itself low. A small blur gives the relief
   slopes instead of cliffs.
2. **Ridge lines, back to front.** Every 5 px a horizontal line is drawn across the card, lifted by the height
   under each point. Each line's area below is filled with the background first, so nearer lines hide farther
   ones and the relief reads as solid.
3. **Revealed by the sweep.** Only the part left of the scanner is drawn as relief; the rest stays a flat
   outline. A soft teal gradient trails the line.
4. **Features as rectangles.** Each check is a rectangle on the card. The lines inside it are restroked in teal,
   corner brackets frame it, and a few checks add their own proof on top (guides, anchor points, a rival card).
5. **The scale, not a score.** The bands bar fills from 0 to 100 and lights each band's name, so the film shows
   how the check scores without claiming a result.
6. **Sound from the same clock.** Each check's blip lands as its feature lights up and each tick as it is ticked off.

## Gotchas worth knowing

- The height map contains type, so it depends on the web fonts. Build it once at load and again when the fonts
  are ready, then repaint.
- Draw the SVG mark with `Path2D` from its path data instead of loading the image, so the height map never
  waits on an image download.
- Once the sweep has passed, keep the relief: tie the reveal to the sweep, not to wherever the scanner is now, or
  the card disappears when the scanner moves back to a feature.
