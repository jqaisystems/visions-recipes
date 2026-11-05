# R41 · Hatch

**Style:** one engraved field of lines, like a banknote. One stateless WebGL2 fragment shader: raymarched forms set tone
and depth, tone sets each line's width, and big words exist because the lines swell or bend. The small labels and the
mark are flat.
**Made for:** Codex Control Center, a local-first dashboard that keeps the metadata and not the words.
**Length:** 34.56 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 34.56-second 1920x1080 film in HyperFrames for Codex Control Center, a local-first dashboard that
keeps the metadata of a session and not its words. Make it dynamic motion design, a showreel piece. Almost the whole film
is one engraved field of lines, like a banknote, drawn by one stateless WebGL2 fragment shader: raymarched forms give
tone and depth, tone sets each line's width, cross-hatching comes in on the darkest tones, and the lines follow surfaces
in world space. Type reaches the shader through one canvas with mipmaps: red swells the lines, blue only bends them, green
is flat small type with a halo that clears the lines around it. 125 bpm, 72 beats. Palette: bone #EDE6D6, ink #0B0B0C, teal
#00A89D, amber #FFA024, red #E8341C, one pair at a time, changing on a radial front of solid ink. Archivo at 900, JetBrains
Mono for labels, a score composed in code in A minor. All shown data is fictional and labelled DEMO DATA.
The lines: still horizontal lines, then a sphere rises only by bending them and takes ink on the first hit.
The log: a demo log whose private words lose their ink. "SEES THE SHAPE". "NOT THE WORDS" swells, then loses all its ink and
stays readable only through the bends. "METADATA ONLY".
Observe: raymarched bars and a ring. "NO API KEY TO OBSERVE".
The gate: a closed gate in amber, "APPROVE?", the score drops out, the doors burst. A square tunnel, "READ-ONLY", "BY DEFAULT".
Full access: "FULL ACCESS" on red, a raymarched X slams onto it, "BLOCKED IN V1".
Publish check: "CHECKED BEFORE IT'S PUBLIC". CREDENTIALS, LOGS and PATHS fall through a sieve as bends alone, then SOURCE, DOCS and
DEMO stay. Every line collapses into one hairline.
Close: the logo placed flat, never put through the lines, redrawn or recoloured, with "Codex Control Center", the URL and
"OPEN SOURCE · MIT". Use "Codex" only in the system's name, take facts only from the case study, and claim no results.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, whose promise is {the_promise}, as one
engraved field of lines drawn by a single stateless WebGL2 fragment shader. Raymarch {your_forms} for tone and depth, let tone
set line width, and make the lines follow surfaces in world space. Bring type in through one canvas: one channel swells the
lines, one only bends them, one is flat small type with a halo. Change colours from {your_palette} on a radial front of solid
ink, at {bpm} bpm. Show {the_key_word} losing all its ink so it stays readable only through the bends, then {the_story_beats},
collapse every line into one hairline, and end on {your_mark}, placed flat, with {line} and {url}. A score composed in code, with
an impact on each word and one silence before the biggest move.
```

Ideas:

- A private notes app: a sentence loses its ink and only its outline stays, then the note locks.
- A banknote printer or an engraver: use the line field for what it was made for, with a portrait made of bends.
- An album release: tracks as raymarched forms and the title swelling out of the lines on each hit.
- A privacy policy you can actually read: what's collected keeps its ink, and what isn't falls through the sieve.

## How it's built

1. **A sphere with no outline.** Nothing is drawn but the lines. The sphere's depth displaces them, so a form appears before there's any ink on it. Tone arrives on the first hit.
2. **Words lose their ink.** NOT THE WORDS starts in the red channel, swelling the lines. Its red fades to nothing while the blue stays, so it remains readable from the bends alone.
3. **Lines that hold on.** The bars and the ring map the lines to world space, so as the form turns the lines turn with it, like an engraving on an object, and don't swim.
4. **The silence.** The gate holds at APPROVE? and the score drops out, so the doors bursting open on the next downbeat hit twice as hard.
5. **A tunnel made of lines.** The field switches to square rings driven by depth. The shutter narrows and the sub-frames rise to eight, because lines this fine would otherwise ghost.
6. **The X.** A raymarched X slams into FULL ACCESS, its depth bending the words' lines, on a red and ink pair.
7. **Falling as bends.** The private words fall through the sieve in the blue channel only, so they're felt in the lines and never printed.
8. **One hairline.** Every line converges into one, with eight sub-frames carrying it, and the frame clears for the logo, flat and outside the shader's lines.

## Gotchas worth knowing

- Map lines in world space on a form. In screen space the form appears to slide underneath a fixed grating.
- Don't put small type through the lines: it breaks up on every stripe. Give it a flat channel and a halo.
- A big word lost on thick bone stripes needs help: READ-ONLY only read once it moved to the flat channel.
- A wide shutter on fine lines at speed gives stacked ghosts. Slow the move and narrow the shutter together.
- Give falling bent words more time than printed ones. Bends are harder to read, and a fall that reads fine in ink is just a shiver.
