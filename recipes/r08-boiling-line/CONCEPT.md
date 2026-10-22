# R08 · Boiling Line · concept card (approved by João 2026-10-22: the Music page, score composed in code in the style of his tracks, sepia ink with one sunset wash)

**Style (reusable):** Boiling Line. Everything looks drawn by hand: ink lines that never sit still, redrawn with
a slightly different wobble on every second frame (12 drawings a second, "on twos", like hand-drawn animation),
over warm paper, with one watercolour wash. Anyone can swap the drawings and the colour.

**Why now:** handmade-looking motion is a popular direction in motion design, often set against glossy AI and 3D
work. The twist here is that nothing is drawn by hand: the wobble, the strokes and the wash are all computed,
from time.

**Subject:** the Music page on visions, your eight calm tracks made with Suno (piano, ocean waves, chillout:
"Sunset Reflections", "Waves of Tranquility", "Calm Shores" and five more). The film draws the world those tracks
describe: a sea, a sunset and a piano on the shore. No track count on screen, as with the page intros.

**Story in one line:** a pen draws a shaky horizon, a sun and the first waves; the waves start rolling, boiling on
twos; a small piano is sketched on the shore and its keys press in time with the score; the sun sinks and a warm
watercolour wash spreads across the sea; the title boils in: "Music", "piano, ocean, made with Suno" and
visions.joaoqueiros.com/music.

**Sound:** the score is composed in code in the spirit of your tracks (soft piano over an ocean wash), not taken
from them, so the source stays MIT. The piano keys in the drawing press on the score's own notes.

**Spec:** about 26 s, 16:9 1920×1080; drawn at 12 fps on twos inside a 30 fps file. Same MIT source routine.

**Look:** warm paper #F4EEE2 with grain, sepia ink #2B2420, one wash in sunset orange #E8894A fading to sea teal
#3E8C8A. Lines are 2 to 3 overlapping passes, like a fineliner. Type: Instrument Serif, boiled by the same
displacement as the lines. Technique: SVG. Each drawing is a set of paths; on every second frame their points
are offset by seeded noise (a new seed per drawing step), strokes draw on with dash offsets, the wash is an SVG
turbulence filter, also on twos. Not like any earlier recipe: no WebGL, no canvas, no particles.

## Beats
| Time | Beat | Technique |
|---|---|---|
| 0 to 4 s | Paper. A pen draws a shaky horizon line and a sun | stroke draw-on, boiling on twos |
| 4 to 10 s | Waves are sketched and start to roll toward the shore; birds tick across | looping wave paths, frame-stepped |
| 10 to 16 s | A small upright piano is drawn on the sand; its keys press with the score's notes | per-key paths, note table |
| 16 to 21 s | The sun sinks; an orange wash spreads over the sky and sea | turbulence-filtered fill, on twos |
| 21 to 26 s | Title: "Music" · "piano, ocean, made with Suno" · visions.joaoqueiros.com/music | boiling type |

## Open choices for João
- Subject: the Music page (recommended).
- Sound: a score composed in code in the style of your tracks (recommended, keeps the source MIT), or one of your
  own Suno tracks under the film (then the audio can't go in the public source).
- Palette: sepia ink with one sunset wash (recommended), or black ink with teal.
