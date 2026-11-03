# R38 · Twice

**Style:** the same moment, twice. Time as the material, applied to a conversation: an app's own screens of a demo
call in one texture array in the order the call happens, and one WebGL2 fragment shader where every pixel picks its
own moment, for a brief written out of a slit, a question held in time, two windows on one beat, rows displaced by
each speaker, the whole call as one image and a tunnel of screens, under a 2D canvas and HTML type.
**Made for:** Klatea, every big conversation, rehearsed before it happens.
**Length:** 35.45 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · GLSL · GSAP · Python (shots, table, score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 35.45-second 1920x1080 film in HyperFrames for Klatea, my private preparation studio and live
meeting copilot, whose promise is that the hard moment of a call happens twice: first in rehearsal, then for real. Use
time as the material: bake the app's own screens of its demo call into slow shots, stack them in one texture array in the
order the call happens, and draw the film in one WebGL2 fragment shader where every pixel picks its own moment. Klatea's
brand: paper ground, ink and sage, coral only on the LIVE dot and the closing line, Fraunces with a sage italic accent
word, IBM Plex Mono labels and a rotated rail, no glow, gradients or shadows, and a score composed in code at 88 bpm.
Prepare: the prep form plays; a hairline slit sweeps across and the brief writes itself out of it as a time smear.
"Every big conversation,"
Rehearse: a scan brings in the role-play; the client's hard question is cut out of time, lifted and outlined in sage,
while the rest of the screen drifts back. "rehearsed out loud,"
Twice: the window splits into two, rehearsal and live, and the same objection lands in both on the same beat; then the
slit sweeps it all live, the LIVE dot comes on and the help from the prep lands. "before it happens."
Both sides: each side of the live transcript moves in time with its own speaker; talk time settles at the demo's own
numbers and a line is translated on the machine. "Audio stays on your computer."
Debrief: the whole call slit-scanned into one image, squeezed to a strip and unfolded into the debrief, its lines
outlined as they are read. "Then an honest debrief,"
The next one: a tunnel built from the call's screens comes out on a new prep. "and the prep for the next one."
Title: the name in letters that each show a different moment of the call, then the logo, placed flat, never redrawn or
recoloured, with "Every big conversation, rehearsed before it happens.", the URL and "Free Windows beta".
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product} with time as the material:
{your_screens} baked into slow shots, in one texture array in the order {the_session} happens, and one fragment shader
where every pixel picks its own moment. Write {the_first_output} out of a slit; cut {the_hard_moment} out of time and
hold it; split the frame into {before} and {after} so {the_same_moment} lands in both on one beat, then sweep it all to
{after}; move each side of {the_live_view} in time with {its_own_source}; press the whole session into one strip and
fold it into {the_result}; tunnel back to {the_start}; end on the name in letters cut out of the session and {your_mark}
with {line} and {url}. One baked table drives the beats, the type and a score composed in code.
```

Ideas:

- A driving-test app: the practice run and the real test side by side, the same roundabout arriving in both on one beat.
- A language tutor: the drill and the real conversation in two windows, the phrase you practised landing in both, then the café takes the whole frame.
- A rehearsal tool for speakers: the slide deck played as time, the hard question from the dry run held in the air until the real audience asks it.
- A flight simulator: the sim's engine failure and the checkride's, two cockpits on one beat, then the slit sweeps it all into the real aircraft.

## How it's built

1. **The brief out of a slit.** Ahead of the slit the prep form plays; behind it each column shows the brief a little further down the page the further it is from the slit, so the brief seems to write itself out of the line.
2. **Held in time.** The client's question is drawn from one fixed frame inside its own rectangle, lifted a little and outlined in sage, while the rest of the screen ripples on and drifts back towards paper.
3. **Twice.** Two window rectangles share the frame: the left one shows the rehearsal's frame, the right one the live call's frames as they play, so the same objection lands in both on the same beat.
4. **The sweep.** The live window grows back to the full frame and pushes the rehearsal out; just inside its leading edge the live call runs a moment behind, a time smear on the sweep.
5. **Both sides.** Two envelopes, one per speaker, displace the matching side of the transcript in time, so whoever is talking moves and the listener holds; talk time fills to the demo's own numbers.
6. **The call as one image.** A slit sweeps and leaves behind it one column per frame of the whole call; the window squeezes to a strip, labelled by section, and unfolds into the debrief.
7. **A tunnel of screens.** Two planes run to a horizon and each ring of depth is another screen of the call, until a new prep form fills the window.
8. **Type cut out of the call.** The name is drawn into an offscreen mask, a different moment for each letter, and the shader tints each screen into the brand's ink inside the letters.

## Gotchas worth knowing

- On a light ground the time effects need hard edges: a hairline slit in ink and a clean smear read as ink on paper, while any glow or blur turns the paper grey.
- Bake each screen into a short pan or push rather than a still: a time effect over identical frames does nothing, and a slow move gives every displacement something to show.
- Mix two neighbouring frames by the fraction on every lookup: with only a few dozen frames, stepping between them reads as flicker on a slow sweep.
- Crop recorded frames above any burned-in captions and pad the rest with the ground colour, so the footage sits on the page instead of in a box.
- Fill the letters with the screen darkened into the brand's ink: a pale interface inside pale letters on paper disappears.
- Keep the shader in a JavaScript template string, not a script tag with a custom type: the HyperFrames linter parses
  inline scripts and fails on GLSL.
- The overlays outline rectangles given in the 1600×900 frame: if you bring your own screens, move `bubbleR`,
  `feedbackY`, `liveBubbleR`, `helpR`, `arabicR` and `dbItems` in `bake/table.py` to where those things sit in yours.
