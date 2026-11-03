# R39 · Echo

**Style:** a page that remembers. Ink feedback: one WebGL2 feedback buffer that flows the last frame, fades it
towards paper and lays the new marks over it, so a voice becomes ridgelines, words leave trails and two ripples make
a moiré, under a crisp 2D canvas and HTML type.
**Made for:** Klatea, every big conversation, rehearsed before it happens.
**Length:** 33.75 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · GLSL · GSAP · Python (table, score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 33.75-second 1920x1080 film in HyperFrames for Klatea, my private preparation studio and live
meeting copilot, whose promise is that the hard moment of a call happens twice: first in rehearsal, then for real. No
screens: the film is one page that remembers. Use one WebGL2 feedback buffer, two float framebuffers in ping-pong, where
each frame the last page is flowed through a field, faded towards paper and the new marks from a 2D canvas are laid
over it, so everything that moves leaves its own history behind, as ink and never as glow. Restart the page from paper
at three anchors so any frame can be rebuilt by stepping from its anchor. Klatea's brand: paper ground, ink and sage,
coral only on the LIVE dot and the closing line, Fraunces with a sage italic accent word, IBM Plex Mono labels and a
rotated rail, no glow, gradients or shadows, and a score composed in code at 112 bpm.
A voice: a pen draws a waveform and the page recedes towards a vanishing point, so the voice becomes ridgelines.
"Every big conversation,"
The brief: eight words from the demo's brief slam in on the beat with speed lines, hold, and fly into a numbered list.
"researched before the call,"
Rehearse: the client's question lands word by word; on the impact a sage ripple fills the page and stays.
"rehearsed out loud,"
Twice: the client's objection lands live, word by word, with the LIVE dot; its ripple in ink spreads from another centre
over the rehearsed one and the two make a moiré, then the page settles. "so the hard moment happens twice."
Both sides: two pens, one per speaker, each as heavy as its own voice, wind into spirals inside a talk-time ring that
settles at the demo's own numbers; a line is translated on the machine. "Both sides, transcribed on your computer."
Debrief: the page is pulled into one column, the score lands as ink and the debrief's lines are wiped in.
"Then an honest debrief,"
The next one: the ridgelines again. "and the prep for the next one."
Close: the logo, placed flat, never redrawn or recoloured, with "Every big conversation, rehearsed before it happens.",
the URL and "Free Windows beta".
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product} as one page that remembers:
a WebGL2 feedback buffer that flows the last frame, fades it towards {ground} and lays new marks over it, restarted
from {ground} at a few anchors so any frame can be rebuilt. Draw {the_input} as ridgelines receding into the page;
slam {the_key_words} in on the beat and fly them into a list; land {the_first_moment} with a ripple in {colour_one}
that stays, then {the_second_moment} with a ripple in {colour_two} from another centre, so the two make a moiré; wind
{two_sources} into two spirals inside {a_ring_meter}; pull the page into one column and land {the_result} as ink;
come back to the ridgelines; end on {your_mark} with {line} and {url}. One baked table drives the marks, the type
and a score composed in code.
```

Ideas:

- A music practice app: the scale you drilled and the one you played on stage, two ripples from two centres, and the moiré where they meet.
- A pitch coach: the investor's question from the mock pitch leaves a sage field, the real one lands in ink over it.
- A language tutor: the phrase you practised and the one you said in the café, two echoes on one page.
- A sports analytics tool: the drilled play and the match play drawn as two pens, winding into one spiral.

## How it's built

1. **A voice as ridgelines.** Every third frame a pen draws the voice's waveform with paper under it, and the page recedes towards a vanishing point, so each earlier line sits further back and the newest one hides what is behind it.
2. **Words that leave trails.** Each word of the brief slams in at the centre with speed lines, holds for a moment and flies to its place in the list; while it flies, a faint copy is laid on the page, so its path stays as a smear.
3. **The rehearsed ripple.** On the question's impact a ring is drawn every frame as it spreads from one centre, and the page keeps every ring, so a sage field fills the frame and stays.
4. **Twice, as a moiré.** The live objection's rings spread in ink from another centre over the sage field; the two sets of rings cross and beat against each other, then the fade is raised and the page settles.
5. **Two pens.** Two pens trace two spirals, one winding in and one winding out, each line as heavy as its speaker's envelope at that moment, while a swirl in the flow winds the trails; talk time fills a ring to the demo's own numbers.
6. **The score as ink.** The flow pulls the page into one column, the fade clears it, and the 8 is laid on the page for a few frames, so it lands crisp on the top layer and feathers out underneath.
7. **The next one.** The recession comes back on and the ridgelines draw again, with the debrief's last trace drifting back into them.
8. **The logo, flat.** The page clears to paper and the logo is placed as it is, never drawn into the ink.

## Gotchas worth knowing

- On a paper ground, lay the marks over the page instead of adding light: ink mixed onto paper stays ink, while additive trails turn the page grey and read as glow.
- A feedback buffer cannot be seeked by itself: restart it from paper at a few anchors and step it to the frame, and keep every mark a function of time with no randomness.
- Use float framebuffers for the page: an 8-bit page fading towards paper by a small amount each frame gets stuck a few levels short of paper and leaves stains.
- Draw the type crisp on a layer above the ink and lay only a faint copy into the page: words that live only in the buffer smear before anyone can read them.
- Give each impact its own centre: two ripples from the same point only stack, while two centres a few hundred pixels apart make the moiré.
- Keep the shaders in JavaScript template strings, not script tags with a custom type: the HyperFrames linter parses
  inline scripts and fails on GLSL.
- Float framebuffers need `EXT_color_buffer_float`; render with hardware acceleration on, or the page will not draw.
