# R36 · Tideline

**Style:** slit-scan on real footage. Time as the material: the frames of a real clip in one texture array, and one
WebGL2 fragment shader where every pixel picks its own moment, for slit-scan, time smears, echoes, a datamosh, ripples
of time and a tunnel whose depth is time, under a 2D canvas and HTML type.
**Made for:** the Tidesstunes Social Pipeline, one video in, three platforms out.
**Length:** 33.4 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · GLSL · GSAP · Python (energy, frames, table) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 33.4-second 1920x1080 film in HyperFrames for the Tidesstunes Social Pipeline, my system that
turns a music video into vertical clips of its strongest minute with a caption for each platform, using time as the
material: slit-scan and time displacement on real footage, in one WebGL2 fragment shader. Extract 144 consecutive
frames at 12 fps from inside the track's strongest minute into one texture array, plus one slit-scan photograph of
the whole video (the centre column of 1920 moments), and let every pixel pick its own moment. Deep sea-ink ground, one
off-white line weight, teal for the window, Libre Baskerville, Inter and JetBrains Mono. Measure the track's loudness
a second at a time in Python and take the strongest 60 seconds; cut the soundtrack from the same moment.
One video in: the video plays and a bright slit crosses the frame; behind it the whole video becomes one strip of
time, a clock along its edge. "One video in,"
The strongest minute: the loudness draws on as a line; a teal window sits on the first minute, is struck out, and
slides to the strongest one; it opens to the frame and the strip unfolds back into the moving picture. "the strongest
minute,"
Cut to vertical: the slits outside the 9:16 centre crop drift back in time, then fall with echo trails, and the crop
stands alone. "cut to vertical,"
One link: the frame holds while a smooth flow keeps dragging blocks of it along, a datamosh, then collapses into one
bright line with the clip's ID. "one link,"
Three captions: the line opens into three phones showing the same wave at three moments, a ripple of time through
them, each typing its own caption: short with hashtags, a hook with a link in bio, keyword-rich for a board. "three
captions,"
Queued: the phones line up on a rail, spaced out, then fly into a slit-scan tunnel whose depth is time. "spaced out,
queued."
Title: the name in letters that each show a different second of the footage, then the mark, placed flat, never
redrawn or recoloured, with "One video in, three platforms out." and the URL.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject} with time as the material:
{n_frames} frames of {your_footage} in one texture array, and one fragment shader where every pixel picks its own
moment. Lay {the_whole_input} out as one slit-scan strip; find {the_part_that_matters} by {a_real_measure} and lock a
window onto it; cut it to {the_new_shape} as the slits outside drift back in time and fall; hold it in a datamosh
until it collapses into {one_thing}; open it into {n_outputs}, each showing the same moment at a different time, with
{what_each_gets}; then dive through a slit-scan tunnel to the name in type cut out of time and {your_mark} with {line}
and {url}. One baked table drives the beats, the type and the sound.
```

Ideas:

- A podcast clipper: a two-hour episode laid out as a strip of time, the loudest laugh found by its own waveform, cut to vertical and sent out as three clips with their own captions.
- A sports highlights tool: a whole match as one slit-scan strip, the minute with the most crowd noise locked by a window, the goal held in a datamosh and sent out three ways.
- A wedding film editor: the day as a strip of time, the vows found by the quiet before them, and three phones showing the same kiss at three moments.
- A timelapse product: a day of a city in one strip, the golden hour found by brightness, and type cut out of time where each letter shows a different hour.

## How it's built

1. **The slit.** Left of the slit the strip shows; just behind it the picture is sampled further back in time the further it is from the slit, so the wake smears into the strip instead of cutting to it.
2. **The real minute.** The line is the track's own loudness, one value a second. The window starts on the first minute, is struck out, and slides to the 60 seconds with the most energy, the pipeline's own rule.
3. **Unfold.** The window's part of the strip stretches to the frame, and a second slit turns it back into moving picture, so the strip and the footage are the same thing.
4. **Falling through time.** Each 32 px slit outside the crop is sampled further back in time the further it is from the crop, then falls under gravity, drawing five echoes from earlier moments behind it.
5. **A datamosh.** The frame freezes, and one smooth flow field reaches the 16 px blocks from the bottom up: those blocks stop refreshing and drag the held picture along the flow, sampled over a run of later moments.
6. **One wave, three moments.** Each phone shows the same centre crop at its own offset in time, and a ring of time ripples out from each phone's centre as the captions type on.
7. **A tunnel of time.** Two planes run to a horizon; a pixel's distance from it sets its depth, and the depth sets both where it samples the picture and how far back in time.
8. **Type cut out of time.** The title is drawn once into a mask with each letter's number in its green channel, so every letter shows the footage at its own second over a dimmed hold.

## Gotchas worth knowing

- Keep the frames in one texture array and blend between two layers: sampling a single layer per pixel steps visibly at 12 fps when time is displaced across the frame.
- Run the frame time back and forth rather than clamping it, so a displacement that reaches past either end of the slab still lands on a real frame instead of a frozen edge.
- Give the datamosh one smooth flow field rather than a random vector per block, or it reads as a pixel mosaic instead of motion bleeding through a held frame.
- Mind the texture memory: 144 frames at 1024×688 is about 400 MB on the GPU, so size the slab to the frame rather than the source.
- For the portrait cut, add the centre of the source at its own resolution as a second array: the 9:16 crop uses less than half the slab's width, and stretched to full frame it goes soft.
- Keep the shader in a JavaScript template string, not a script tag with a custom type: the HyperFrames linter parses
  inline scripts and fails on GLSL.
